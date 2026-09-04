
import os
import uuid
 
import boto3
from botocore.exceptions import BotoCoreError, ClientError
 
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.dependencies import get_db, require_role
from app.models import Service_Report, User, UserRole, Work_Order
from app.schemas.service_report import ServiceReportRead
 
router = APIRouter(prefix="/reports", tags=["reports"])
 
# Same env-var-with-local-default pattern used in database.py.
# The script hardcoded this bucket; keep the default identical so nothing breaks,
# but allow override in deployment.
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "medflow-reports-binx")
 
# Allowed content per 4D: images or .txt / .pdf logs.
ALLOWED_CONTENT_TYPES = {
    "text/plain",
    "application/pdf",
    "image/png",
    "image/jpeg",
}
 
 
@router.post("", response_model=ServiceReportRead, status_code=status.HTTP_201_CREATED)
async def upload_service_report(
    work_order_id: int = Form(...),
    file: UploadFile = File(...),
    notes: str | None = Form(default=None),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN, UserRole.FIELD_TECHNICIAN)),
) -> Service_Report:
    # 1. Validate the target work order exists before we touch S3,
    #    so we never orphan a file against a missing FK.
    work_order = await db.get(Work_Order, work_order_id)
    if work_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order {work_order_id} not found",
        )
 
    # 2. Basic content-type guard.
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type {file.content_type!r}. "
                f"Allowed: {', '.join(sorted(ALLOWED_CONTENT_TYPES))}"
            ),
        )
 
    # 3. Build a collision-proof key. uuid prefix keeps two 'report.pdf'
    #    uploads from overwriting each other.
    safe_name = file.filename or "upload"
    s3_key = f"reports/{work_order_id}/{uuid.uuid4().hex}-{safe_name}"
 
    # 4. Upload to S3. upload_fileobj streams rather than loading whole file.
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": file.content_type},
        )
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"S3 upload failed: {exc}",
        ) from exc
 
    file_url = f"s3://{BUCKET_NAME}/{s3_key}"
 
    # 5. Persist the DB row (same shape the boto3 demo script created).
    report = Service_Report(
        work_order_id=work_order_id,
        file_url=file_url,
        notes=notes,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report

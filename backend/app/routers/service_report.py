
import os
from select import select
import uuid
 
import boto3
from botocore.exceptions import BotoCoreError, ClientError
 
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.dependencies import get_db, require_role, get_current_user
from app.models import Service_Report, User, UserRole, Work_Order
from app.schemas.service_report import ServiceReportRead
 
router = APIRouter(prefix="/reports", tags=["reports"])
 
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "medflow-reports-binx")
 
# Allowed content per 4D: images or .txt / .pdf logs.
ALLOWED_CONTENT_TYPES = {
    "text/plain",
    "application/pdf",
    "image/png",
    "image/jpeg",
}

#Get all service reports
@router.get("", response_model=list[ServiceReportRead])
async def list_service_reports(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    statement = select(Service_Report)
    result = await db.execute(statement)
    return list(result.scalars().all())

#Get specific service report by id
@router.get("/{report_id}", response_model=ServiceReportRead)
async def get_service_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    report = await db.get(Service_Report, report_id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service report with ID {report_id} not found",
        )
    return report
 
#Create/upload
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

#Update
@router.put("/{report_id}", response_model=ServiceReportRead)
async def update_service_report(
    report_id: int,
    payload: ServiceReportRead,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    report = await db.get(Service_Report, report_id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service report with ID {report_id} not found",
        )
 
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(report, field, value)
 
    await db.commit()
    await db.refresh(report)
    return report




#Delete
@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    report = await db.get(Service_Report, report_id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service report with ID {report_id} not found",
        )
 
    # Delete the file from S3 first, then delete the DB row.
    s3_client = boto3.client("s3")
    s3_key = report.file_url.replace(f"s3://{BUCKET_NAME}/", "")
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"S3 delete failed: {exc}",
        ) from exc
 
    await db.delete(report)
    await db.commit()
    return None
"""
Uploads a service_report to S3 using Boto3 SDK
then creates a matching record in the database with a real s3 url
"""


import asyncio 
import boto3

from app.database import AsyncSessionLocal
from app.models import Service_Report

BUCKET_NAME = "medflow-reports-binx"
LOCAL_FILE_PATH = "scripts/sample_report.txt"

#S3 key is just a path within the s3 bucket where the file will be stored
S3_KEY = "reports/PR-1002-002.txt"

#A function to upload the file to the s3 bucket and return the s3 url
def upload_to_s3() -> str:
    #pass the name of the service you want to connect to, for this its s3
    s3_client =  boto3.client("s3")
    s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_KEY)
    return f"s3://{BUCKET_NAME}/{S3_KEY}"

#async function to record service report into database :3
async def record_service_report(file_url: str) -> None:
    async with AsyncSessionLocal() as session:
        log = Service_Report(
            work_order_id = 1,
            file_url = file_url,
            notes = "Uploaded via boto3 demo script.",
        )

        session.add(log)
        await session.commit()
        await session.refresh(log)
        print(f"Created Service_Report id = {log.id}, file_url = {log.file_url}")

#async main function to run the upload and record the log
async def main() -> None:
    file_url = upload_to_s3()
    print(f"Uploaded to {file_url}")
    await record_service_report(file_url)

if __name__ == "__main__":
    asyncio.run(main())
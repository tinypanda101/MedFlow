"""
Reconciliation script to detect desync issues between database and s3 bucket
"""
import asyncio

import boto3

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Service_Report

BUCKET_NAME = "medflow-reports-binx"
PREFIX = "reports/"

def extract_s3_key(file_url: str) -> str:
   """
   s3://bucket-name/diagnostics/rx1001-002.txt -> diagnostics/rx1001-002.txt

   Strips the scheme and bucket name, keeping only the actual object key aka the part that has a match what list_object_v2 returns
   """

   without_scheme = file_url.removeprefix("s3://")
   #The _ is the bucket name, the second _ is the slash after the bucket name, and the key is the rest
   _, _, key = without_scheme.partition("/")
   return key

def list_s3_keys(bucket_name: str, prefix: str) -> set[str]:
    s3_client = boto3.client("s3")

    #Uses a paginator rather than a single list_objects_v2() call
    #because list_objects_v2 caps out at 1,000 keys per response so a paginator automatically follows the continuation token for anything more than 1,000
    paginator = s3_client.get_paginator("list_objects_v2")

    #Accumulat all the keys in a set so we can do operations later
    keys: set[str] = set()
    for page in paginator.paginate(Bucket = bucket_name, Prefix = prefix):
        for obj in page.get("Contents", []):
            keys.add(obj["Key"])
    return keys

#async function to fetch all service reports from the database
async def fetch_service_reports() -> list[Service_Report]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Service_Report))
        return list(result.scalars().all())

#async function to compare the s3 keys against the database rows and print the results
async def main() -> None:
    s3_keys = list_s3_keys(BUCKET_NAME, PREFIX)
    logs = await fetch_service_reports()

    healthy: list[Service_Report] = []
    broken: list[Service_Report] = []
    referenced_keys: set[str] = set()

    for log in logs:
        key = extract_s3_key(log.file_url)
        referenced_keys.add(key)
        if key in s3_keys:
            healthy.append(log)
        else:
            broken.append(log)

    orphaned_keys = s3_keys - referenced_keys

    print("== Healthy (database row + matching s3 file) ==")
    if not healthy:
        print(" None Found ")
    for log in healthy:
        print(f"Service_Report {log.id}: {log.file_url}")

    print("== Broken (database row, no matching file) ==")
    if not broken:
        print(" None Found ")
    for log in broken:
        print(f"Service_Report {log.id}: {log.file_url}")

    #Bonus section per research prompt but not required
    print("== Orphaned (file in s3, but no matching database row) ==")
    if not orphaned_keys:
        print(" None Found ")
    for key in orphaned_keys:
        print(f"s3://{BUCKET_NAME}/{key}")

if __name__ == "__main__":
    asyncio.run(main())
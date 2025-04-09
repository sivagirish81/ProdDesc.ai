import os
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
import uuid
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        self.is_production = os.getenv("ENVIRONMENT") == "production"
        if self.is_production:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
            self.bucket_name = os.getenv("AWS_S3_BUCKET")
        else:
            self.upload_dir = "uploads/images"
            os.makedirs(self.upload_dir, exist_ok=True)

    async def upload_image(self, file: UploadFile, user_id: str) -> Optional[str]:
        try:
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"

            if self.is_production:
                # Upload to S3
                s3_key = f"users/{user_id}/products/{unique_filename}"
                self.s3_client.upload_fileobj(
                    file.file,
                    self.bucket_name,
                    s3_key,
                    ExtraArgs={
                        "ContentType": file.content_type,
                        "ACL": "public-read"
                    }
                )
                # Generate public URL
                url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            else:
                # Save locally
                file_path = os.path.join(self.upload_dir, unique_filename)
                with open(file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                # Generate local URL
                url = f"/uploads/images/{unique_filename}"

            return url

        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return None

    def delete_image(self, image_url: str) -> bool:
        try:
            if self.is_production:
                # Extract key from S3 URL
                key = image_url.split(f"https://{self.bucket_name}.s3.amazonaws.com/")[1]
                self.s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=key
                )
            else:
                # Delete local file
                filename = image_url.split("/uploads/images/")[1]
                file_path = os.path.join(self.upload_dir, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            return True
        except Exception as e:
            logger.error(f"Error deleting image: {str(e)}")
            return False 
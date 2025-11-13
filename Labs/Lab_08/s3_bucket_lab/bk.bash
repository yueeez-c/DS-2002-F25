#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <local-file> <bucket-name> <expiration-seconds>"
    exit 1
fi

LOCAL_FILE="$1"
BUCKET_NAME="$2"
EXPIRATION="$3"

FILE_NAME=$(basename "$LOCAL_FILE")

echo "Uploading $LOCAL_FILE to s3://$BUCKET_NAME/$FILE_NAME ..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET_NAME/$FILE_NAME"

if [ $? -ne 0 ]; then
    echo "Upload failed!"
    exit 1
fi

echo "Generating presigned URL (expires in $EXPIRATION seconds)..."
URL=$(aws s3 presign "s3://$BUCKET_NAME/$FILE_NAME" --expires-in "$EXPIRATION")

echo ""
echo "✔ Upload complete!"
echo "✔ Presigned URL:"
echo "$URL"
echo ""


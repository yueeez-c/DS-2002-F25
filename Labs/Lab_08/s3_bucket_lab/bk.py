import argparse

import boto3
import requests
import os
def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")


# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("filename", help="name of the file")
    parser.add_argument("bucket", help="Bucket name")
    parser.add_argument("link", help="Link to the file you wanna download:")
    parser.add_argument("time", help="Expiring time:")

    args = parser.parse_args()
    bucket = args.bucket
    file = args.filename
    image_url = args.link
    path = os.path.join(os.getcwd(), file)  # Saves to current directory
    print("Downloading files")
    download_file(image_url, path)
    s3 = boto3.client('s3', region_name="us-east-1")
    local_file = path
    object_name = os.path.basename(path)
    expires_in = args.time  #

    # 1. Open the file in binary read mode ('rb')
    with open(local_file, 'rb') as data:
        resp = s3.put_object(
            Body=data,        # PASS THE OPEN FILE OBJECT HERE
            Bucket=bucket,
            Key=object_name    # This is the destination key/path in S3
    )
    response = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': object_name},
        ExpiresIn=expires_in
    )
    print("Link(expiring %s): " %expires_in)
    print(response)
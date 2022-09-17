import boto3


class S3Bucket:
    def __init__(self, bucket):
        """Utility class to abstract AWS S3 functions"""
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.Bucket(bucket)

    def upload_file(self, filename=None, key=None, fileobj=None) -> bool:
        """Upload a file to an S3 bucket

        Params:
            filename(str): File to upload
            key(str): S3 object name. If not specified then Filename
                      is used
            fileobj(byte): A file-like object to upload. At a minimum,
                       it must implement the read method, and must
                       return bytes.

        Returns:
            True if file was uploaded, else False
        """
        if fileobj is not None:
            return self.bucket.upload_fileobj(Fileobj=fileobj, Key=key)
        elif filename is not None:
            return self.bucket.upload_file(Filename=filename, Key=key)
        else:
            raise Exception("No file or Fileobject provided")

    def download_file(self, filename=None, key=None, fileobj=None) -> bool:
        """Download a file from an S3 bucket

        Params
            filename(str): Filename to save locally.
            key(str): S3 object name.
            fileobj(byte): A file-like object to download into. At a minimum,
                          it must implement the write method and must accept
                          bytes.
        Returns:
            None
        """
        if fileobj is not None:
            return self.bucket.download_fileobj(Fileobj=fileobj, Key=key)
        elif filename is not None:
            return self.bucket.download_file(Filename=filename, Key=key)
        else:
            raise Exception("No file or Object provided")

    def search(self, prefix: str):
        """Searches for the file in the bucket

        Params:
            prefix(str): file to search for (provide full directory path)

        Returns:
            collection of objects matching the prefix
        """
        return self.bucket.objects.filter(Prefix=prefix)

    def delete(self, keys: list):
        """Deletes the file(s) in the bucket

        Params:
            keys(list[str]): S3 keys to delete (provide full directory path)

        Returns:
            None
        """
        self.bucket.delete_objects(Delete={"Objects": keys})

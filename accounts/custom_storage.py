from storages.backends.s3boto3 import S3Boto3Storage
from teambuilder import settings


class MediaStorage(S3Boto3Storage):
    if settings.ENVIRONMENT == 'production':
        bucket_name = 'teambuilder-media'
    else:
        bucket_name = 'teambuilder-media-dev'
    file_overwrite = False

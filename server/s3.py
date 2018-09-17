import boto3

ACCESS_KEY = ''
SECRET_KEY = ''


def get_directory_data(s3_key, s3_bucket_name='bashlist-78'):
    s3 = boto3.resource('s3',
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY,
                        config=boto3.session.Config(signature_version='s3v4'))

    try:
        object_summary = s3.ObjectSummary(s3_bucket_name, s3_key)
        return object_summary.size / 1000  # convert to KB
    except Exception as e:
        return None


def generate_s3_push_url(s3_object_key, size_limit, s3_bucket_name='bashlist-78'):
    s3 = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      config=boto3.session.Config(signature_version='s3v4'))

    fields = {"acl": "private"}
    conditions = [
        {"acl": "private"},
        ["content-length-range", 0, size_limit]
    ]
    post = s3.generate_presigned_post(
        Bucket=s3_bucket_name,
        Key=s3_object_key,
        Fields=fields,
        Conditions=conditions,
        ExpiresIn=600
    )
    return post


def generate_get_url(s3_object_key, s3_bucket_name='bashlist-78'):
    s3 = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      config=boto3.session.Config(signature_version='s3v4'))

    url = s3.generate_presigned_url('get_object',
                                    Params={'Bucket': s3_bucket_name, 'Key': s3_object_key},
                                    ExpiresIn=600)
    return url


def delete_object(s3_object_key, s3_bucket_name='bashlist-78'):
    s3 = boto3.resource('s3',
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY,
                        config=boto3.session.Config(signature_version='s3v4'))
    try:
        s3.Object(s3_bucket_name, s3_object_key).delete()
        return 1
    except:
        return 0

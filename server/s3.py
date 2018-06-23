from boto3.session import Session

ACCESS_KEY='AKIAJ6Z4VJKTOTZSFOYA'
SECRET_KEY='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'

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)
s3 = session.resource('s3')

def generate_s3_pull_url(s3_bucket_key,s3_bucket_name='bashlist-7'):
	url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': s3_bucket_name,
        'Key': s3_bucket_key
    	},
    ExpiresIn=600,
	)
	return url

def generate_s3_push_url(s3_bucket_key,size_limit,s3_bucket_name='bashlist-7'):
	fields = {"acl": "private"}
	conditions = [
    	{"acl": "private"},
    	["content-length-range", 0, size_limit]
	]
	post = s3.generate_presigned_post(
    	Bucket='bucket-name',
    	Key='key-name',
    	Fields=fields,
    	Conditions=conditions,
    	ExpiresIn=600
	)
	return post

def get_directory_data(s3_bucket_name,s3_directory_key):
	return "https://www.google.com"



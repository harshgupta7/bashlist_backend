# import boto3
# ACCESS_KEY='AKIAJ6Z4VJKTOTZSFOYA'
# SECRET_KEY='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'
# s3 = boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)



# def generate_s3_pull_url(s3_bucket_key,s3_bucket_name='bashlist-7'):
# 	url = s3.generate_presigned_url(
#     ClientMethod='get_object',
#     Params={
#         'Bucket': s3_bucket_name,
#         'Key': s3_bucket_key
#     	},
#     ExpiresIn=600,
# 	)
# 	return url

# def generate_s3_push_url(s3_bucket_key,size_limit,s3_bucket_name='bashlist-7'):
# 	fields = {"acl": "private"}
# 	conditions = [
#     	{"acl": "private"},
#     	["content-length-range", 0, size_limit]
# 	]
# 	post = s3.generate_presigned_post(
#     	Bucket=s3_bucket_name,
#     	Key=s3_bucket_key,
#     	Fields=fields,
#     	Conditions=conditions,
#     	ExpiresIn=600
# 	)
# 	# print(post)
# 	return post


# def generate_s3_put_url(s3_bucket_key,size_limit,s3_bucket_name='bashlist-7'):
# 	url = s3.generate_presigned_url(
# 		ClientMethod='put_object',
# 		Params={
# 			'Bucket':s3_bucket_name,
# 			'Key':s3_bucket_key,
# 			# 'ContentLength':size_limit,
# 			# 'ACL':'private',
# 		},
# 		ExpiresIn=600
# 	)
# 	return url	

# def get_directory_data(s3_key,s3_bucket_name='bashlist-7'):
# 	try:
# 		object_summary = s3.ObjectSummary(s3_bucket_name,s3_key)
# 		return object_summary.size
# 	except:
# 		return None

# # print(generate_s3_put_url('hahahahah',size_limit=3232))
import boto3
import requests
import boto3
ACCESS_KEY='AKIAICDC2ZVHRX25EYNQ'
SECRET_KEY='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'
s3 = boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,config=boto3.session.Config(signature_version='s3v4'))

def get_directory_data(s3_key,s3_bucket_name='bashlist-7'):
	try:
		object_summary = s3.ObjectSummary(s3_bucket_name,s3_key)
		return object_summary.size
	except:
		return None


def generate_s3_push_url(s3_bucket_key,size_limit,s3_bucket_name='bashlist-78'):
	fields = {"acl": "private"}
	conditions = [
    	{"acl": "private"},
    	["content-length-range", 0, size_limit]
	]
	post = s3.generate_presigned_post(
    	Bucket=s3_bucket_name,
    	Key=s3_bucket_key,
    	Fields=fields,
    	Conditions=conditions,
    	ExpiresIn=600
	)
	# print(post)
	return post
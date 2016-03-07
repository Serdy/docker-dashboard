#!/usr/bin/python

from boto.s3.connection import S3Connection


def s3_list_folder(*args):
	aws_access_key = ''
	aws_secret_key = ''
	bucket_name = "bekey-test"


	conn = S3Connection(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
	folder_list = []
	file_list = []
	
	bucket = conn.get_bucket(bucket_name)
	
	if args != (None,):
		for x in args:
			args = x
			folders = bucket.list(args, "/")
	else:
		folders = bucket.list("", "/")	
	for folder in folders:
		if  folder.name.endswith("/") and folder.name != args:
			folder_list.append(folder.name)
		elif folder.name != args:
			file_list.append(folder.name)
	s3_list = {'folder': folder_list, 'files': file_list}
	return s3_list


	   



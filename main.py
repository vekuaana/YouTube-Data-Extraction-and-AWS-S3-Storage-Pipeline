import youtube_api_requests as ytapi
import boto3
from botocore.exceptions import NoCredentialsError
import json

channel_ids = ['UCtYLUTtgS3k1Fg4y5tAhLbw', # Statquest
               'UCCezIgC97PvUuR4_gbFUs5g', # Corey Schafer
               'UCfzlCWGWYyIQ0aLC5w48gBQ', # Sentdex
               'UCNU_lfiiWBdtULKOw6X0Dig', # Krish Naik
               'UCzL_0nIe8B4-7ShhVPfJkgw', # DatascienceDoJo
               'UC7cs8q-gJRlGwj4A8OmCmXg', # Alex the analyst
               'UC2UXDak6o7rBm23k3Vv5dww', # Tina Huang
              ]

# Get channels_infos
channel_infos = ytapi.get_channel_info(channel_ids)
# Get videos_info
videos_info = ytapi.get_videos_info(channel_infos)
# Get comments
videos_comments = ytapi.get_video_comments(videos_info)

# Initialize the S3 resource
s3 = boto3.client('s3')

# List all buckets (for verification)
s3_resource = boto3.resource('s3')
for bucket in s3_resource.buckets.all():
    print(bucket.name)

# Set the bucket name and object name
bucket_name = 'ana-airflow-youtube-api'

# Convert the channel info to a JSON string
channel_info_json = json.dumps(channel_infos, indent=4)  # Use json.dumps to get a JSON string
videos_info_json = json.dumps(videos_info, indent=4) 
videos_comments_json = json.dumps(videos_comments, indent=4) 

object_name_channel_info = 'channel_info.json'
object_name_videos_info = 'videos_info.json'
object_name_videos_comments = 'videos_comments.json'

with open(object_name_channel_info, 'w') as json_file:
    json.dump(channel_info_json, json_file, indent=4) 

with open(object_name_videos_info, 'w') as json_file:
    json.dump(videos_info_json, json_file, indent=4) 

with open(object_name_videos_comments, 'w') as json_file:
    json.dump(videos_comments_json, json_file, indent=4) 

try:
    # Upload the JSON string to S3
    s3.put_object(Bucket=bucket_name, Key=object_name_channel_info, Body=channel_info_json, ContentType='application/json')
    print(f"JSON data uploaded to '{bucket_name}' as '{object_name_channel_info}'.")
except NoCredentialsError:
    print("Credentials not available.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

try:
    # Upload the JSON string to S3
    s3.put_object(Bucket=bucket_name, Key=object_name_videos_info, Body=videos_info_json, ContentType='application/json')
    print(f"JSON data uploaded to '{bucket_name}' as '{object_name_videos_info}'.")
except NoCredentialsError:
    print("Credentials not available.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

try:
    # Upload the JSON string to S3
    s3.put_object(Bucket=bucket_name, Key=object_name_videos_comments, Body=videos_comments_json, ContentType='application/json')
    print(f"JSON data uploaded to '{bucket_name}' as '{object_name_videos_comments}'.")
except NoCredentialsError:
    print("Credentials not available.")
except Exception as e:
    print(f"An error occurred: {str(e)}")


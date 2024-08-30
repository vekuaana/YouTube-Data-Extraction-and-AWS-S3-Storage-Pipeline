# YouTube Data Extraction and AWS S3 Integration

This project retrieves information from YouTube channels including channel's details, videos's details and video's comment using the Youtube Data API. The data extracted is then uploaded to an AWS S3 bucket for storage.

## Table of Contents
- Prerequisites
- Setup
- Usage
    1. Extract youtube channel infotmation
    2. Extract youtube videos information 
    3. Extract comments from youtube video
- Functions
- S3 Integration
- Example Execution
- Logging
- Error Handling

## Prerequisites 
Before running this project, ensure you have the following:

- Python 3.6 or higher installed.
- An AWS account with an S3 bucket created.
- AWS credentials configured for accessing S3.
- YouTube Data API v3 enabled and an API key generated.

## Setup
1. Clone the repository
git clone [Link text](https://github.com/vekuaana/youtube-api.git)
cd YouTube-Data-Extraction-and-AWS-S3-Storage-Pipeline

2. Create a virtual environment 
```
python3 -m venv myenv
source myenv/bin/activate
```
3. Install the required dependencies
```
pip install -r requirements.txt
```
4. Set up environment variables:
add your YouTube Data API key to the .env.example file
```
API_KEY_YOUTUBE_API=your_api_key_here
```

## Usage
The script `main.py` contains all the functions to extract youtube data from the Youtube Data API. To run the script and start extracting data:
1. Extract Channel Information
This function retrieves basic details about a YouTube channel base in the youtube channel id, including the channel name, description, view count, subscriber count, video count, and the ID of the uploads playlist.
```
channel_id = ["UCJQJAI7IjbLcpsjWdSzYz0Q"]  # Example channel ID
channel_info = get_channel_info(channel_id)

```
2. Extract Video Information
This function fetches details about all videos uploaded by the channel, using the uploads playlist ID, contained in the channel details, obtained from the previous step. 
```
videos_info = get_videos_info(channel_info)
```
3. Extract Video Comments
This function retrieves top-level comments and their replies for each video.
```
video_comments = get_video_comments(videos_info)
```

## S3 Integration
Use the `main.py` script to integrate with AWS S3 the extracted data. Remember that you need to create the S3 bucket beforehand for this use case:

- Bucket Name: 'your bucket name'
- Files Uploaded:
        - channel_info.json
        - videos_info.json
        - videos_comments.json

Ensure your AWS credentials are correctly configured and that the specified S3 bucket exists.

## Logging 
The script uses Python's built-in logging module to provide real-time feedback during execution. Logs are generated for:
- Successful retrieval of channel, video, and comment data.
- Errors encountered during API requests or data processing.
- Successful uploads to S3.
## Error Handling 
The script includes robust error handling to manage issues such as:
- API Errors: Handles HTTP errors returned by the YouTube API, including quota exceeded errors.
- AWS S3 Errors: Catches issues related to AWS credentials or other S3-specific errors.
- General Exceptions: Catches and logs unexpected errors during script execution.


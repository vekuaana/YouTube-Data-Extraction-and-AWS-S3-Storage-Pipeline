# YouTube Data Extraction and AWS S3 Integration

## Introduction
This project retrieves information from YouTube channels including channel's details, videos's details and video's comment using the Youtube Data API. The data extracted is then uploaded to an AWS S3 bucket for storage.

 ### Key Features
- Extract detailed information from YouTube channels and videos.
- Collect top-level comments and replies from videos.
- Store extracted data in JSON format and upload it to AWS S3.
- Robust error handling and logging for seamless operation.
  
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
- Results

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
  ## Results
Snippets of the results are displayed below
- channel_info.json
    ```{    "channel_name": "StatQuest with Josh Starmer",
        "description": "Statistics, Machine Learning and Data Science can sometimes seem like very scary topics, but since each technique is really just a combination of small and simple steps, they are actually quite simple. My goal with StatQuest is to break down the major methodologies into easy to understand pieces. That said, I don't dumb down the material. Instead, I build up your understanding so that you are smarter.\n\nContact, Video Index, Etc: https://statquest.org",
        "viewcount": "68188122",
        "subscribers": "1230000",
        "videocount": "281",
        "uploads_playlist_id": "UUtYLUTtgS3k1Fg4y5tAhLbw"
    }```
- videos_info.json
  ```{
        "channel_name": "StatQuest with Josh Starmer",
        "video_id": "wIGOnM6Cf_E",
        "title": "Human Stories in AI: Abbas Merchant@Matics Analytics",
        "description": "In this episode we have special guest Abbas Merchant, Founder and CEO of Matics Analytics, which uses a combination of AI and analytics to transform enterprise data into intelligent actions.\n\nIf you'd like to support StatQuest, please consider...\nPatreon: https://www.patreon.com/statquest\n...or...\nYouTube Membership: https://www.youtube.com/channel/UCtYLUTtgS3k1Fg4y5tAhLbw/join\n\n...buying my book, a study guide, a t-shirt or hoodie, or a song from the StatQuest store...\nhttps://statquest.org/statquest-store/\n\n...or just donating to StatQuest!\npaypal: https://www.paypal.me/statquest\nvenmo: @JoshStarmer\n\nLastly, if you want to keep up with me as I research and create new StatQuests, follow me on twitter:\nhttps://twitter.com/joshuastarmer\n\n#StatQuest",
        "viewcount": "4997",
        "likecount": "105",
        "commentcount": "23"
    }```
- videos_comments.json
```{
  "video_id": "dQw4w9WgXcQ",
  "comments": [
    {
      "comment_id": "UgxH0HSRJyJzT6k5z014AaABAg",
      "author": "John Doe",
      "text": "Great explanation! Really helped me understand p-values.",
      "like_count": 23,
      "published_at": "2022-01-16T14:25:00Z",
      "replies": []
    },
    {
      "comment_id": "UgyO2QfYoeYt_1W-YkF4AaABAg",
      "author": "Jane Smith",
      "text": "Can you do a video on confidence intervals?",
      "like_count": 15,
      "published_at": "2022-01-16T15:30:00Z",
      "replies": [
        {
          "comment_id": "UgyGzXfWGRvY3_4Bz015AaABAg",
          "author": "StatQuest with Josh Starmer",
          "text": "Sure! That's on my list for the next video.",
          "like_count": 5,
          "published_at": "2022-01-16T16:45:00Z"
        }
      ]
    }
  ]
}```

  

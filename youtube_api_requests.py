import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pprint
import json
import pandas as pd
import logging
import time
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# Constantes
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
API_KEY = os.getenv('API_KEY_YOUTUBE_API')

# Get credentials and create an API client
youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

def get_channel_info(youtube_channels_id):
    """
    Get YouTube channel information: title, description, total views count, subscribers count, videos count, the ID of the uploads playlist.

    Params:
    youtube_channels_id: list of channel IDs

    Returns:
    List of dictionaries containing the channel information for all requested channels: title, description, total views count, subscribers count, videos count, the ID of the uploads playlist.
    """
    youtube_channels_info = []

    for youtube_channel_id in youtube_channels_id:
        try:
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=youtube_channel_id
            )
            response = request.execute()

            # Check if no channels were found
            if response.get('pageInfo', {}).get('totalResults', 0) == 0:
                logger.error(f"No channel found with ID: {youtube_channel_id}")
                continue  # Skip to the next ID

            # Process the response if a channel is found
            items = response.get('items', [])
            if items:
                item = items[0]
                snippet = item.get('snippet', {})
                channel_info = {
                    'channel_name': snippet.get('title', 'Unknown'),
                    'description': snippet.get('description', 'No description available'),
                    'viewcount': item.get('statistics', {}).get('viewCount', '0'),
                    'subscribers': item.get('statistics', {}).get('subscriberCount', '0'),
                    'videocount': item.get('statistics', {}).get('videoCount', '0'),
                    'uploads_playlist_id': item.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads', 'Unknown')
                }
                youtube_channels_info.append(channel_info)
                logger.info(f"Channel found: {channel_info['channel_name']}")

        except HttpError as e:
            try:
                error_details = json.loads(e.content.decode('utf-8'))
                error_message = error_details.get('error', {}).get('message', 'An unknown error occurred')
                logger.error(f"HTTP error {e.resp.status} occurred for channel ID {youtube_channel_id}: {error_message}")
            except json.JSONDecodeError as parse_error:
                logger.error(f"Failed to parse error response for channel ID {youtube_channel_id}: {parse_error}")
                logger.error(f"Raw error content: {e.content}")

        except Exception as e:
            logger.error(f"An unexpected error occurred with channel ID {youtube_channel_id}: {e}")

    return youtube_channels_info


def get_videos_id(uploads_playlist_id):
    """
    Get the id and publication date of a youtube videos uploaded by a specified youtube channel based on the youtube playlist id. 

    Params:  
    The id of the uploads playlist of a youtube channel. 
    
    Returns:
    A list of dictionaries containing the id and the publication date of a youtube channel uploaded videos. 
    """
    videos_id_date = []
    
    try: 

        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=uploads_playlist_id,
        )
        response = request.execute()
        items = response.get('items', [{}])

        for item in items: 
            videos_id_date.append(item.get('contentDetails', {}))

        next_page_token = response.get('nextPageToken')
        more_pages = True

        while more_pages:
            if next_page_token is None:
                more_pages = False
            else:
                request = youtube.playlistItems().list(
                            part='contentDetails',
                            playlistId = uploads_playlist_id,
                            maxResults = 50,
                            pageToken = next_page_token)
                response = request.execute()
                items = response.get('items', [{}])

                for item in items: 
                    videos_id_date.append(item.get('contentDetails', {}))

                next_page_token = response.get('nextPageToken')

    except HttpError as e:
        try:
            error_details = json.loads(e.content.decode('utf-8'))
            error_message = error_details.get('error', {}).get('message', 'An unknown error occurred')
            logger.error(f"HTTP error {e.resp.status} occurred for channel ID {uploads_playlist_id}: {error_message}")
        except json.JSONDecodeError as parse_error:
            logger.error(f"Failed to parse error response for channel ID {uploads_playlist_id}: {parse_error}")
            logger.error(f"Raw error content: {e.content}")

    except Exception as e:
        logger.error(f"An unexpected error occurred with playlist ID {uploads_playlist_id}: {e}")


    return videos_id_date

def get_videos_info(youtube_channels_info):
    """
    Fetches information about YouTube videos from a list of channels.

    Params:
        youtube_channels_info (list): A list of dictionaries, each containing channel information including the uploads playlist ID. 
                                    The channel information should be retrieved through the function "get_channel_info".

    Returns:
        list: A list of dictionaries, each containing details for a video. Each dictionary includes:
            - 'channel_name': The name of the YouTube channel.
            - 'video_id': The unique identifier for the video.
            - 'title': The title of the video.
            - 'description': The description of the video.
            - 'viewcount': The number of views the video has received.
            - 'likecount': The number of likes the video has received.
            - 'commentcount': The number of comments the video has received.
    """

    videos_info = []

    for channel_info in youtube_channels_info:
        uploads_playlist_id = channel_info.get('uploads_playlist_id', '')  # Get uploads playlist ID for each YouTube channel
        videos_id = get_videos_id(uploads_playlist_id)  # Get videos IDs

        for video in videos_id:
            video_id = video.get('videoId', '')
            try:
                request = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=video_id
                )
                response = request.execute()

                items = response.get('items', [])
                if not items:
                    logger.warning(f"No items found for video ID {video_id}")
                    continue

                item = items[0]
                snippet = item.get('snippet', {})
                statistics = item.get('statistics', {})

                video_info = {
                    'channel_name': channel_info.get('channel_name', ''),
                    'video_id': item.get('id', ''),
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'viewcount': statistics.get('viewCount', '0'),
                    'likecount': statistics.get('likeCount', '0'),
                    'commentcount': statistics.get('commentCount', '0')
                }
                videos_info.append(video_info)

            except HttpError as e:
                try:
                    error_details = json.loads(e.content.decode('utf-8'))
                    error_message = error_details.get('error', {}).get('message', 'An unknown error occurred')
                    logger.error(f"HTTP error {e.resp.status} occurred for video ID {video_id}: {error_message}")
                except json.JSONDecodeError as parse_error:
                    logger.error(f"Failed to parse error response for video ID {video_id}: {parse_error}")
                    logger.error(f"Raw error content: {e.content}")
                # Continue to the next video ID after logging the error
                continue

            except Exception as e:
                logger.error(f"An unexpected error occurred with video ID {video_id}: {e}")
                # Continue to the next video ID after logging the error
                continue

    return videos_info


def get_video_comments(videos_info):
    """
    Fetches comments for a list of YouTube videos based on their IDs.

    Params:
        videos_info (list): A list of dictionaries, each containing a 'video_id' key with the YouTube video ID.

    Returns:
        list: A list of dictionaries, each containing details about a comment. Each dictionary includes:
            - 'video_id': The unique identifier for the video.
            - 'text_original': The original text of the comment.
            - 'published_at': The publication date of the comment.
            - 'like_count': The number of likes the comment has received.
            - 'kind': Indicates whether the comment is a 'top level' comment or a 'reply'.
            - 'parentId' (optional): The ID of the parent comment if the comment is a reply.
    """
    comments = []
    for video in videos_info:
        video_id = video.get('video_id', '')

        try:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=100,
                order='time'
            )
            response = request.execute()
        except HttpError as e:
            try:
                error_details = json.loads(e.content.decode('utf-8'))
                error_message = error_details.get('error', {}).get('message', 'An unknown error occurred')
                logger.error(f"HTTP error {e.resp.status} occurred for video ID {video_id}: {error_message}")
                if e.resp.status == 403:
                    logger.error(f"Quota exceeded for the day. Stopping requests until the quota resets.")
                    # Sleep for 24 hours or until the quota reset time
                    time.sleep(86400)
                    continue  # continue the loop after sleeping
            except json.JSONDecodeError as parse_error:
                logger.error(f"Failed to parse error response for video ID {video_id}: {parse_error}")
                logger.error(f"Raw error content: {e.content}")
            # Skip to the next video ID after logging the error
            continue
        except Exception as e:
            logger.error(f"An unexpected error occurred with video ID {video_id}: {e}")
            # Skip to the next video ID after logging the error
            continue
    
        items = response.get('items', [{}])
        for item in items:
            try:
                top_level_dic = {}  # Create a new dictionary for each top-level comment

                snippet = item.get('snippet', {})
                top_level_comment = snippet.get('topLevelComment', {}).get('snippet', {})
                reply_comment = snippet.get('replies', {}).get('snippet', {})

                # Extract the required details
                top_level_dic['video_id'] = video_id
                top_level_dic['text_original'] = top_level_comment.get('textOriginal')
                top_level_dic['published_at'] = top_level_comment.get('publishedAt')
                top_level_dic['like_count'] = top_level_comment.get('likeCount', 0)
                top_level_dic['kind'] = 'top level'
                comments.append(top_level_dic)

                if top_level_comment.get('totalReplyCount', 0) != 0:
                    reply_dict = {}
                    replies = snippet.get('replies', {}).get('comments', {})
                    for reply in replies:
                        reply_dict['video_id'] = video_id
                        reply_dict['id'] = reply.get('id', {})
                        reply_dict['text_original'] = reply.get('snippet', {}).get('textOriginal', {})
                        reply_dict['published_at'] = reply.get('snippet', {}).get('publishedAt', {})
                        reply_dict['like_count'] = reply.get('snippet', {}).get('likeCount', {})
                        reply_dict['kind'] = 'reply'
                        reply_dict['parentId'] = reply.get('snippet', {}).get('parentId', {})
                    comments.append(reply_dict)
            except Exception as e:
                logger.error(f"An error occurred while processing a comment for video ID {video_id}: {e}")
                continue

        # Handle pagination
        more_pages = True
        next_page_token = response.get('nextPageToken')

        while more_pages:
            if next_page_token is None:
                more_pages = False
            else:
                try:
                    request = youtube.commentThreads().list(
                        part="snippet,replies",
                        videoId=video_id,
                        maxResults=100,
                        order='time',
                        pageToken=next_page_token
                    )
                    response = request.execute()

                except HttpError as e:

                    try:
                        error_details = json.loads(e.content.decode('utf-8'))
                        error_message = error_details.get('error', {}).get('message', 'An unknown error occurred')
                        logger.error(f"HTTP error {e.resp.status} occurred for video ID {video_id}: {error_message}")
                        
                        if e.resp.status == 403:
                            logger.error(f"Quota exceeded for the day. Stopping requests until the quota resets.")
                            # Sleep for 24 hours or until the quota reset time
                            time.sleep(86400)
                        continue  # continue the loop after sleeping

                    except json.JSONDecodeError as parse_error:
                        logger.error(f"Failed to parse error response for video ID {video_id}: {parse_error}")
                        logger.error(f"Raw error content: {e.content}")
                    continue
                except Exception as e:
                    logger.error(f"An unexpected error occurred with video ID {video_id}: {e}")
                    # Skip to the next video ID after logging the error
                    continue

                items = response.get('items', [{}])
                next_page_token = response.get('nextPageToken')

                for item in items:
                    try:
                        top_level_dic = {}  # Create a new dictionary for each top-level comment

                        snippet = item.get('snippet', {})
                        top_level_comment = snippet.get('topLevelComment', {}).get('snippet', {})
                        reply_comment = snippet.get('replies', {}).get('snippet', {})

                        # Extract the required details
                        top_level_dic['video_id'] = video_id
                        top_level_dic['text_original'] = top_level_comment.get('textOriginal')
                        top_level_dic['published_at'] = top_level_comment.get('publishedAt')
                        top_level_dic['like_count'] = top_level_comment.get('likeCount', 0)
                        top_level_dic['kind'] = 'top level'
                        comments.append(top_level_dic)

                        if top_level_comment.get('totalReplyCount', 0) != 0:
                            reply_dict = {}
                            replies = snippet.get('replies', {}).get('comments', {})
                            for reply in replies:
                                reply_dict['video_id'] = video_id
                                reply_dict['id'] = reply.get('id', {})
                                reply_dict['text_original'] = reply.get('snippet', {}).get('textOriginal', {})
                                reply_dict['published_at'] = reply.get('snippet', {}).get('publishedAt', {})
                                reply_dict['like_count'] = reply.get('snippet', {}).get('likeCount', {})
                                reply_dict['kind'] = 'reply'
                                reply_dict['parentId'] = reply.get('snippet', {}).get('parentId', {})
                            comments.append(reply_dict)
                    except Exception as e:
                        logger.error(f"An error occurred while processing a comment for video ID {video_id} on pagination: {e}")
                        continue

    return comments



if __name__ == "__main__":

    channel_id =  ["UCJQJAI7IjbLcpsjWdSzYz0Q"] # Channel id of Thu Vu 
    channel_info = get_channel_info(channel_id)
    filename_channel = 'ThuVu_channel_info.json'

    # Open the file in write mode and use json.dump to write the data
    with open(filename_channel, 'w') as json_file:
        json.dump(channel_info, json_file, indent=4)  # indent=4 makes the JSON pretty-printed

    videos_info = get_videos_info(channel_info)
    # Specify the filename
    filename_video = 'ThuVu_videos_info.json'
    # Open the file in write mode and use json.dump to write the data
    with open(filename_video, 'w') as json_file:
        json.dump(videos_info, json_file, indent=4)  # indent=4 makes the JSON pretty-printed

    video_comments = get_video_comments(videos_info)
    # Specify the filename
    filename_comments = 'ThuVu_videos_comments.json'

    # Open the file in write mode and use json.dump to write the data
    with open(filename_comments, 'w') as json_file:
        json.dump(video_comments, json_file, indent=4)  # indent=4 makes the JSON pretty-printed


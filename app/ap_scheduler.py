from datetime import datetime, date
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler

from apiclient.discovery import build

from .models import Item


def periodic_execution():# 任意の関数名
    # ここに定期実行したい処理を記述する
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    rows = Item.objects.values('channel_id')
    joined_channel_ids = ','.join((row['channel_id'] for row in rows))

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=settings.YOUTUBE_API_KEY
    )

    channels_response = youtube.channels().list(part='snippet,contentDetails,statistics', id=joined_channel_ids).execute()

    for item in channels_response['items']:
        item_record = {}
        channel_id = item['id']
        snippet = item.get('snippet')
        content_details = item.get('contentDetails')
        statistics = item.get('statistics')
        channel_title = snippet['title']
        item_record['channel_title'] = channel_title
        video_count = statistics.get('videoCount')
        item_record['video_count'] = video_count

        upload_playlist_id = content_details.get('relatedPlaylists').get('uploads')
        item_record['uploads_playlist_id'] = upload_playlist_id
        playlist_items_response = youtube.playlistItems().list(part='id,snippet', playlistId=upload_playlist_id).execute()
        recent_video_item = playlist_items_response['items'][0]
        recently_video_snippet = recent_video_item.get('snippet')
        recently_video_id = recently_video_snippet.get('resourceId').get("videoId")
        if recently_video_id:
            item_record['recently_upload_video_id'] = recently_video_id
            item_record['recently_upload_video_title'] = recently_video_snippet.get('title')

            item_record['recently_upload_video_published_at'] = datetime.fromisoformat(recently_video_snippet.get('publishedAt').replace('Z', '+00:00'))

            medium_thumbnail = recently_video_snippet.get('thumbnails').get('medium')
            if medium_thumbnail:
                item_record['recently_upload_video_tumbnail_url'] = medium_thumbnail.get('url')
                item_record['recently_upload_video_tumbnail_width'] = medium_thumbnail.get('width')
                item_record['recently_upload_video_tumbnail_height'] = medium_thumbnail.get('height')
        
        Item.objects.filter(channel_id=channel_id).update(**item_record)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'cron', minute='*/30')
    #scheduler.add_job(periodic_execution, 'interval', seconds=5)
    scheduler.start()

# pythonanywhereで定期実行を行うため
if __name__ == '__main__':
    periodic_execution()
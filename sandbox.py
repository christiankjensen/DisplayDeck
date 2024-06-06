from pyyoutube import Api
api = Api(api_key='')

CHANNEL_ID = 'UCOSD5Dvu_-cCOpGQ7PnBINQ'

response = api.get_channel_info(channel_id=CHANNEL_ID)
channel_info = response.items[0]
channel_snippet = channel_info.snippet
channel_statistics = channel_info.statistics
print(channel_snippet.title)
print(f'{channel_statistics.viewCount} views')
print(f'{channel_statistics.subscriberCount} subscribers')

uploads_playlist_id = channel_info.contentDetails.relatedPlaylists.uploads
# Get the 5 most recent videos from the uploads playlist
playlist_items = api.get_playlist_items(playlist_id=uploads_playlist_id, count=5)

print('\nRecent Videos:')
for item in playlist_items.items:
    video_id = item.contentDetails.videoId
    video_response = api.get_video_by_id(video_id=video_id)
    video = video_response.items[0]
    title = video.snippet.title
    view_count = video.statistics.viewCount
    print(f'\t{title} ({view_count} views)')

# Get playlists by channel id
playlists = api.get_playlists(channel_id=CHANNEL_ID, count=None)

print('\nChannel Playlists:')
for playlist in playlists.items:
    print(f'\t{playlist.snippet.title}')

print('---------------------------------------------------------------------------------------------------------------')
print()
# Get items from the uploads playlist
playlist_items = api.get_playlist_items(playlist_id=uploads_playlist_id, count=50)

shorts = []

for item in playlist_items.items:
    video_id = item.contentDetails.videoId
    video_response = api.get_video_by_id(video_id=video_id)
    video = video_response.items[0]
    if video.contentDetails.duration:
        duration = video.contentDetails.duration
        # Parse duration to seconds
        if 'S' in duration:
            # ISO 8601 duration format PT#M#S or PT#S
            minutes = 0
            seconds = 0
            if 'M' in duration:
                minutes = int(duration.split('M')[0].replace('PT', ''))
                seconds = int(duration.split('M')[1].replace('S', ''))
            else:
                seconds = int(duration.replace('PT', '').replace('S', ''))

            total_seconds = minutes * 60 + seconds

            if total_seconds < 60:
                shorts.append(video)
                if len(shorts) == 5:
                    break

for short in shorts:
    title = short.snippet.title
    view_count = short.statistics.viewCount
    print(f'{title} ({view_count} views)')

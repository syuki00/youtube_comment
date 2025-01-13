import requests
import json

URL = 'https://www.googleapis.com/youtube/v3/'

API_KEY = 'AIzaSyAXDopzPeJnzW7_IHB8JkxiQz--_w6xkf8'

def print_video_comment(video_id, next_page_token):
  params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': video_id,
    'order': 'relevance',
    'textFormat': 'plaintext',
    'maxResults': 100,
  }
  if next_page_token is not None:
    params['pageToken'] = next_page_token
  response = requests.get(URL + 'commentThreads', params=params)
  resource = response.json()

  for comment_info in resource['items']:
    # コメント
    text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
    # グッド数
    like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
    # 返信数
    reply_cnt = comment_info['snippet']['totalReplyCount']

    print('{}\t{}\t{}'.format(text.replace('\n', ' '), like_cnt, reply_cnt))
  
  if 'nextPageToken' in resource:
    print_video_comment(video_id, resource["nextPageToken"])

# ここにVideo IDを入力
video_id = 'TlcfucoVb9g'
print_video_comment(video_id, None)

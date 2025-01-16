from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from googleapiclient.discovery import build
import os
import youtube_comment.settings as settings

# FastAPI アプリケーションの作成
app = FastAPI()

# YouTube Data API の設定
API_KEY = settings.AK
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# コメント取得用のリクエストモデル
class VideoRequest(BaseModel):
    video_id: str

# 動画コメントを取得する関数
def get_youtube_comments(video_id: str):
    try:
        # YouTube Data API クライアントの作成
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
        
        # コメントスレッドのリクエスト
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=20  # 必要に応じて変更
        ).execute()

        # コメントをパース
        comments = []
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            comments.append({"author": author, "comment": comment})

        return comments

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching comments: {str(e)}")

# エンドポイント定義
@app.post("/get_comments")
async def fetch_comments(request: VideoRequest):
    comments = get_youtube_comments(request.video_id)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found")
    return {"video_id": request.video_id, "comments": comments}

from fastapi import APIRouter, Body
import re
import requests
from pydantic import BaseModel


router = APIRouter(tags=["douyin"])


class VideoParams(BaseModal):
    share_content: str = Body(..., description="抖音分享内容")


# 提取 URL 链接
def extract_urls(content: str):
    # 使用正则表达式匹配 URL
    # urls = re.findall(r"https?://\S+", text)
    # return urls
    # if len(re.findall("[a-z]+://[\S]+", content, re.I | re.M)) > 0:
    #     return re.findall("[a-z]+://[\S]+", content, re.I | re.M)[0]
    if len(re.findall(r"https?://\S+", content, re.I | re.M)) > 0:
        return re.findall(r"https?://\S+", content, re.I | re.M)[0]


# 获取重定向后的 URL
def get_redirect_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/92.0.4515.107 Safari/537.36"
    }
    response = requests.get(url, headers)
    return response.url


@router.post("/douyin")
def get_no_watermark_video_url(videoParams: DouyinVideoParams):
    # 使用正则表达式匹配 URL
    # urls = re.findall(r"https?://\S+", share_url)

    print("提取到的 URL 链接:")
    for url in urls:
        print(url)

    return urls

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
import re
import requests
from pydantic import BaseModel


router = APIRouter(tags=["douyin"])


"""
 2.82 wsr:/ Happy birthday to Kobe.%篮球 %曼巴精神 %科比生日  https://v.douyin.com/d8LpxMQ/ 复制佌鏈接，da鐦Dou音搜索，直接观看視频！
"""


class DouyinVideoParams(BaseModel):
    share_content: str = None


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
# def get_no_watermark_video_url(form_data: DouyinVideoParams = None):
def get_no_watermark_video_url(form_data: DouyinVideoParams = None):
    # 使用正则表达式匹配 URL
    # urls = re.findall(r"https?://\S+", share_url)
    if not form_data or not form_data.share_content:
        return JSONResponse(
            content={
                "code": 400,
                "message": "缺少参数",
                "data": None,
            }
        )

    urls = extract_urls(form_data.share_content)

    print("提取到的 URL 链接:")
    for url in urls:
        print(url)

    return JSONResponse(content={"code": 200, "message": "success", "data": urls})

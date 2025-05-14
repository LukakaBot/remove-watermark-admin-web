import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import re
import requests
from pydantic import BaseModel
import httpx

router = APIRouter(tags=["douyin"])


"""
 8.18 https://v.douyin.com/JyCk5gy/ 复制佌鏈接，da鐦Dou音搜索，直接观看視频！
"""


class DouyinVideoParams(BaseModel):
    share_content: str = None


headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Referer": "https://www.douyin.com/",
}

url_regex = r"https?://\S+"
video_id_regex = r"/video/(\d+)"
json_regex = r"window\._ROUTER_DATA\s*=\s*({.*})</script>"


# 提取 URL 链接
def extract_url(share_content: str):
    # 使用正则表达式匹配 URL 链接
    return re.compile(url_regex).search(share_content).group()


# 获取重定向后的 URL
def get_redirect_url(url):
    response = requests.get(url, headers)
    return response.url


# 从 URL 中提取视频 ID
def get_video_id(url: str):
    return re.search(video_id_regex, url).group(1)


# 根据视频 ID 获取请求 URL
def get_request_url_by_video_id(video_id) -> str:
    return f"https://www.iesdouyin.com/share/video/{video_id}/"


def is_web_share_url(share_url: str) -> bool:
    return share_url.startswith("https://www.douyin.com/video/")


async def get_video_info(share_url: str):

    if is_web_share_url(share_url):
        # 网页分享链接
        video_id = share_url.strip("/").split("/")[-1]
    else:
        # app分享链接
        redirect_url = get_redirect_url(share_url)
        video_id = get_video_id(redirect_url)

    request_url = get_request_url_by_video_id(video_id)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(
            request_url,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

    match = re.search(json_regex, response.text, flags=re.DOTALL)

    if not match or not match.group(1):
        print(f"原始响应内容片段:\n{response.text[:500]}...")
        raise ValueError("无法提取有效JSON数据")

    try:
        json_data = json.loads(match.group(1).strip())
        return json_data.get("loaderData")
    except json.JSONDecodeError:
        print(f"JSON解析失败: {str(e)}")
        print(f"原始内容: {match.group(1).strip()[:200]}...")
        raise ValueError("无效的JSON数据")


@router.post("/douyin")
async def get_no_watermark_video_url(form_data: DouyinVideoParams = None):
    if not form_data or not form_data.share_content:
        return JSONResponse(
            content={
                "code": 400,
                "message": "缺少参数",
                "data": None,
            }
        )

    url = extract_url(form_data.share_content)

    if not url:
        return JSONResponse(
            content={
                "code": 400,
                "message": "参数错误",
                "data": None,
            }
        )

    try:
        video_info = await get_video_info(url)
    except Exception as error:
        return JSONResponse(
            content={
                "code": 500,
                "message": str(error),
                "data": None,
            }
        )

    return JSONResponse(
        content={
            "code": 200,
            "message": "success",
            "data": video_info,
        }
    )

import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import re
import requests
from pydantic import BaseModel
import httpx

router = APIRouter(tags=["douyin"])


"""
 2.82 wsr:/ Happy birthday to Kobe.%篮球 %曼巴精神 %科比生日  https://v.douyin.com/d8LpxMQ/ 复制佌鏈接，da鐦Dou音搜索，直接观看視频！
 https://v.douyin.com/JyCk5gy/
"""


class DouyinVideoParams(BaseModel):
    share_content: str = None


# 提取 URL 链接
def extract_url(content: str):
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


def get_video_id(url: str):
    return re.search(r"/video/(\d+)", url).group(1)


def get_request_url_by_video_id(video_id) -> str:
    return f"https://www.iesdouyin.com/share/video/{video_id}/"


async def parse_share_url(share_url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.douyin.com/",
    }

    if share_url.startswith("https://www.douyin.com/video/"):
        # 支持电脑网页版链接 https://www.douyin.com/video/xxxxxx
        video_id = share_url.strip("/").split("/")[-1]
        share_url = get_request_url_by_video_id(video_id)
    else:
        # 支持app分享链接 https://v.douyin.com/xxxxxx
        async with httpx.AsyncClient(follow_redirects=False) as client:
            # share_response = await client.get(share_url, headers=headers)
            # video_id = (
            #     share_response.headers.get("location")
            #     .split("?")[0]
            #     .strip("/")
            #     .split("/")[-1]
            # )
            # share_url = get_request_url_by_video_id(video_id)
            redirect_url = get_redirect_url(share_url)
            video_id = get_video_id(redirect_url)
            print(video_id)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(
            share_url,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

    pattern = r"window\._ROUTER_DATA\s*=\s*({.*})</script>"
    match = re.search(pattern, response.text, flags=re.DOTALL)

    if not match or not match.group(1):
        print(f"原始响应内容片段:\n{response.text[:500]}...")
        raise ValueError("无法提取有效JSON数据")

    try:
        json_data = json.loads(match.group(1).strip())
        return json_data
    except json.JSONDecodeError:
        print(f"JSON解析失败: {str(e)}")
        print(f"原始内容: {match.group(1).strip()[:200]}...")
        raise ValueError("无效的JSON数据")


async def get_video_info(video_id: str):
    # url = f"https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200f230000btcaac52m1gham4830p0&ratio=720p&line=0"
    url = (
        f"https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}&ratio=720p&line=0"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "video/*",
    }
    # response = await requests.get(url, headers=headers)
    # print(response.url)
    # return response

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return {
                "video_url": str(response.url),
                "content_type": response.headers.get("Content-Type"),
                "status_code": response.status_code,
            }
        except httpx.HTTPStatusError as e:
            return {"error": f"API请求错误: {str(e)}"}
        except Exception as e:
            return {"error": f"请求异常: {str(e)}"}

    # async with httpx.AsyncClient() as client:  # 创建异步客户端
    #     try:
    #         response = await client.get(url, headers)  # 发送 GET 请求
    #         response.raise_for_status()  # 检查状态码（非 2xx 抛出异常）
    #         return {
    #             "video_url": str(response.url),
    #             "content_type": response.headers.get("Content-Type"),
    #             "status_code": response.status_code,
    #         }
    #     except httpx.HTTPStatusError as e:
    #         raise HTTPException(
    #             status_code=e.response.status_code, detail="第三方接口返回错误"
    #         )
    #     except httpx.RequestError:
    #         raise HTTPException(status_code=503, detail="无法连接第三方接口")


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
    # redirect_url = get_redirect_url(url)
    # video_id = get_video_id(redirect_url)
    # video_info = await get_video_info(video_id)
    video_info = await parse_share_url(url)
    # print(video_info)

    return JSONResponse(content={"code": 200, "message": "success", "data": video_info})

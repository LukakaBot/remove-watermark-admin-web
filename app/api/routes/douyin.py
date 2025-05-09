from fastapi import APIRouter


router = APIRouter()


@router.get("/douyin")
def get_no_watermark_video_url():
    return "video url"

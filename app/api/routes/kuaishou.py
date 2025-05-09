from fastapi import APIRouter


router = APIRouter(tags=["kuaishou"])


@router.get("/kuaishou")
def get_no_watermark_video_url():
    return "video url"

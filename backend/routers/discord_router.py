"""
Discord Notification Endpoint Router.
Endpoint: POST /discord
"""

from fastapi import APIRouter, Depends, status
from backend.schemas.common import APIResponse
from backend.schemas.discord import DiscordNotificationRequest, DiscordNotificationResponse
from backend.services.discord_service import DiscordService, get_discord_service

router = APIRouter(tags=["Discord"])


@router.post(
    "/discord",
    response_model=APIResponse[DiscordNotificationResponse],
    status_code=status.HTTP_200_OK,
    summary="Dispatch Discord Webhook Notification",
    description="Posts research summary notification to configured Discord channel webhook.",
)
async def dispatch_discord_notification(
    request: DiscordNotificationRequest,
    service: DiscordService = Depends(get_discord_service),
) -> APIResponse[DiscordNotificationResponse]:
    """POST /discord async endpoint utilizing dependency injection."""
    result = await service.send_notification(request)
    return APIResponse(
        success=True,
        message=f"Discord notification for '{request.company_name}' dispatched successfully.",
        data=result,
    )

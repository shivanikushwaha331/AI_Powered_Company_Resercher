"""
Discord Webhook & Bot Notification Schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class DiscordNotificationRequest(BaseModel):
    """POST /discord Request Schema."""

    applicant_name: Optional[str] = Field(default="John Doe", description="Applicant Full Name")
    applicant_email: Optional[str] = Field(default="applicant@example.com", description="Applicant Email Address")
    company_name: str = Field(..., min_length=1, description="Company name")
    company_website: Optional[str] = Field(default="", description="Official company website URL")
    summary: Optional[str] = Field(default="", description="Executive research summary snippet")
    title: Optional[str] = Field(default="Company Research Report", description="Notification title")
    pdf_url: Optional[str] = Field(default="", description="Generated PDF report download URL")
    webhook_url: Optional[str] = Field(default=None, description="Optional Discord webhook URL")
    bot_token: Optional[str] = Field(default=None, description="Optional Discord Bot Token")
    channel_id: Optional[str] = Field(default=None, description="Optional Discord Channel ID")


class DiscordNotificationResponse(BaseModel):
    """POST /discord Response Schema."""

    dispatch_id: str = Field(..., description="Unique dispatch ID")
    status: str = Field(..., description="Status string (sent / failed)")
    message_id: str = Field(..., description="Discord message ID or mock ID")
    channel_name: str = Field(default="research-reports", description="Target Discord channel")
    dispatched_at: str = Field(..., description="ISO 8601 UTC timestamp")

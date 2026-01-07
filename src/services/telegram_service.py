"""Telegram bot service for sending notifications."""

import requests
from typing import Optional


class TelegramService:
    """Service for sending Telegram notifications."""

    def __init__(self, token: str, chat_id: str):
        """
        Initialize the Telegram service.

        Args:
            token: Telegram bot API token
            chat_id: Telegram chat ID to send messages to
        """
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send_message(self, message: str) -> bool:
        """
        Send a message via Telegram.

        Args:
            message: Message text to send

        Returns:
            True if successful, False otherwise
        """
        try:
            params = {"chat_id": self.chat_id, "text": message}
            response = requests.get(f"{self.base_url}/sendMessage", params=params)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Telegram message: {e}")
            return False

    def is_available(self) -> bool:
        """Check if Telegram API is available."""
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

"""Error handling and recovery management module."""

from datetime import datetime
from typing import Optional, Callable


class ErrorHandler:
    """Manages error states and recovery with interval-based notifications."""

    def __init__(
        self,
        notification_callback: Callable[[str], None],
        notification_interval: int = 1200,
    ):
        """
        Initialize the error handler.

        Args:
            notification_callback: Function to call for sending notifications
            notification_interval: Seconds between notifications while in error state (default: 1200 = 20 min)
        """
        self.notification_callback = notification_callback
        self.notification_interval = notification_interval
        self._reset_error_state()

    def _reset_error_state(self) -> None:
        """Reset error tracking state."""
        self.in_error = False
        self.error_message: Optional[str] = None
        self.first_error_time: Optional[datetime] = None
        self.last_notification_time: Optional[datetime] = None

    def handle_error(self, error_message: str) -> None:
        """
        Handle an error with graceful notifications.

        Args:
            error_message: Description of the error
        """
        now = datetime.now()

        if not self.in_error:
            # First time hitting this error
            self._first_error_occurrence(now, error_message)
        else:
            # Already in error state, check if we should notify again
            self._check_and_notify_persistent_error(now, error_message)

    def _first_error_occurrence(self, now: datetime, error_message: str) -> None:
        """Handle the first occurrence of an error."""
        self.in_error = True
        self.error_message = error_message
        self.first_error_time = now
        self.last_notification_time = now

        notification = (
            f"❌ ERROR DETECTED:\n{error_message}\n\n"
            f"Will notify you every {self.notification_interval // 60} minutes if issue persists."
        )
        self.notification_callback(notification)
        print(f"[ERROR] {error_message}")

    def _check_and_notify_persistent_error(
        self, now: datetime, error_message: str
    ) -> None:
        """Check if we should send another notification for persistent error."""
        if self.last_notification_time is None:
            return

        time_since_last_notification = (
            now - self.last_notification_time
        ).total_seconds()

        if time_since_last_notification >= self.notification_interval:
            time_in_error = (now - self.first_error_time).total_seconds() / 60
            notification = (
                f"⏱️ Still having issues (for {int(time_in_error)} minutes):\n{error_message}"
            )
            self.notification_callback(notification)
            self.last_notification_time = now
            print(f"[ERROR - {int(time_in_error)} min] {error_message}")

    def handle_recovery(self) -> None:
        """Handle recovery from error state."""
        if not self.in_error or self.first_error_time is None:
            return

        time_in_error = (datetime.now() - self.first_error_time).total_seconds() / 60
        notification = (
            f"✅ SERVICE RECOVERED!\n"
            f"System is back to normal after {int(time_in_error)} minutes of errors."
        )
        self.notification_callback(notification)
        print(f"[RECOVERED] Service back to normal after {int(time_in_error)} minutes")
        self._reset_error_state()

    def is_in_error_state(self) -> bool:
        """Check if system is currently in error state."""
        return self.in_error

import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from pdf_slack_bot.utils import configs


class SlackMessageSender:
    def __init__(self):
        """
        Initialize the SlackMessageSender.
        """
        self._logger = configs.logger
        self._bot_token = os.getenv('SLACK_BOT_TOKEN')
        self._channel_id = os.getenv('SLACK_CHANNEL_ID')

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(requests.RequestException),
        reraise=True
    )
    def _send_request(self, slack_data: dict) -> requests.Response:
        """
        Send a POST request to Slack.

        Args:
            slack_data (dict): The data to be sent to Slack.

        Returns:
            requests.Response: The response from the Slack API.

        Raises:
            requests.RequestException: If all retry attempts fail.
        """
        headers = {
            'Authorization': f'Bearer {self._bot_token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            'https://slack.com/api/chat.postMessage',
            json=slack_data,
            headers=headers
        )
        response.raise_for_status()
        return response

    def send_message(self, message: str) -> bool:
        """
        Send a message to Slack.

        Args:
            message (str): The message to be sent.

        Returns:
            bool: True if the message was sent successfully, False otherwise.

        Raises:
            ValueError: If the Slack bot token or channel ID is not set.
        """
        if not self._bot_token or not self._channel_id:
            raise ValueError("Slack bot token or channel ID is not set.")

        slack_data = {
            'channel': self._channel_id,
            'text': message
        }

        try:
            response = self._send_request(slack_data)
            if response.json().get('ok'):
                self._logger.info("Successfully sent message to Slack!")
                return True
            else:
                self._logger.error(f"Failed to send message to Slack: {response.json().get('error')}")
                return False
        except requests.RequestException as e:
            self._logger.error(f"Failed to send message to Slack after retries: {str(e)}")
            return False


if __name__ == "__main__":
    slack_sender = SlackMessageSender()
    slack_sender.send_message(message="This is a test message from a python class")

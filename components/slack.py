import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from utils import configs


class SlackMessageSender:
    def __init__(self):
        """
        Initialize the SlackMessageSender.
        """
        self._logger = configs.logger
        self._webhook_url = os.getenv('SLACK_WEBHOOK_URL')

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
        response = requests.post(
            self._webhook_url,
            json=slack_data,
            headers={'Content-Type': 'application/json'}
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
            ValueError: If the Slack webhook URL is not set.
        """
        if not self._webhook_url:
            raise ValueError("Slack webhook URL is not set.")

        slack_data = {'text': message}

        try:
            self._send_request(slack_data)
            self._logger.info("Successfully sent message to Slack!")
            return True
        except requests.RequestException as e:
            self._logger.error(f"Failed to send message to Slack after retries: {str(e)}")
            return False


if __name__ == "__main__":
    slack_sender = SlackMessageSender()
    slack_sender.send_message(message="This is a test message from a python class")

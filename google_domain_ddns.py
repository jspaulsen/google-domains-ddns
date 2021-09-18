import os
import logging
import time
from typing import List

import pendulum
import requests


REQUIRED_ENV_VAR = [
    'DOMAIN',
    'USERNAME',
    'PASSWORD',
]


logging.basicConfig(format='[%(asctime)s] %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))


class DomainClient:
    def __init__(self, username: str, password: str) -> None:
        self.url = "https://domains.google.com/nic/update"
        self.user_agent = "google-domain-ddns-updater fatiguely@gmail.com"

        self.username = username
        self.password = password

    def update_ddns(self, hostname: str) -> str:
        response = requests.post(
            url=self.url,
            params={'hostname': hostname},
            headers={'user-agent': self.user_agent},
            auth=(self.username, self.password),
        )

        print(response.text)
        response.raise_for_status()
        return response.text



def missing_req_envar() -> List[str]:
    return [v for v in REQUIRED_ENV_VAR if not os.getenv(v)]


def main():
    interval = os.getenv('INTERVAL', 'PT30M')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    domain = os.getenv('DOMAIN')

    if missing := missing_req_envar():
        raise Exception(f"Missing required environment variable(s) {missing}")

    # Parse and validate provided interval
    try:
        interval = pendulum.parse(interval)
    except ValueError as err:
        raise ValueError(f"INTERVAL must be an ISO8601 Duration") from err

    if not isinstance(interval, pendulum.Duration):
        raise ValueError(f"INTERVAL must be a valid ISO8601 Duration")

    if interval.seconds < 300:
        raise ValueError(f"INTERVAL cannot be less than 5 minutes")

    client = DomainClient(username, password)
    error_retry_interval = pendulum.duration(minutes=5)

    while True:
        next_sleep = interval

        try:
            result = client.update_ddns(domain)
        except requests.exceptions.RequestException as err:
            logger.exception(f"An exception occurred attempting to update DDNS: ")
            next_sleep = error_retry_interval

        if '911' in result:
            logger.warning(f"An error occurred on the backend; waiting 5 minutes...")
            next_sleep = error_retry_interval

        if not ('good' in result or 'nochg' in result):
            logger.error(
                "An error occurred attempting to update DDNS entry; these are not considered retryable and "
                f"manual intervention is likely required:  Response: {result}"
            )
            break

        logger.debug(f"Result of update request: {result}; sleeping for {next_sleep.seconds}")
        time.sleep(next_sleep.seconds)


if __name__ == '__main__':
    main()

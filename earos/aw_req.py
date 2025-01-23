import json
import logging
import requests
from colorama import init, Fore, Style

init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ColoredConsoleHandler(logging.StreamHandler):
    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT
    }

    def emit(self, record):
        try:
            message = self.format(record)
            color = self.LEVEL_COLORS.get(record.levelno, '')
            print(f"{color}{message}")
        except Exception:
            self.handleError(record)


handler = ColoredConsoleHandler()
logger.addHandler(handler)

EAROS_WEBSITE = "https://earos.io/index.html"
EAROS_BASE_URL = "https://app.earos.io/api"
PING_CHECK_URL = "https://app.earos.io/api"
HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json; charset=utf-8",
    "Version": "1.0.0",
    "Accept-Language": "en"
}
PING_PULSE = 15 * 60


def ping_aw_server(disconnect_signal, aw_license, node_id):
    HEADERS['Authorization'] = 'Bearer {}'.format(aw_license)
    HEADERS['X-Device-Id'] = node_id
    url = f"{PING_CHECK_URL}/clients/ping"
    while not disconnect_signal.is_set():
        logger.info("*************PULSE***************")
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            response_data = response.json()
            logger.info("The network is performing normally and is continuously monitored.")
            if response_data['code'] != 200:
                msg = response_data['message']
                code = response_data['code']
                logger.warning(f"Sync Failed\ncode: {code}\nmessage: {msg}")
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to report status: {e}") from e
        if disconnect_signal.wait(PING_PULSE):
            break


def aw_verification(node_data: dict):
    aw_license = node_data['aw_license']
    HEADERS['Authorization'] = 'Bearer {}'.format(node_data['aw_license'])
    HEADERS['X-Device-Id'] = node_data['node_id']
    payload = {
        "ip": node_data['ip'],
        "node_data": node_data
    }
    url = f"{EAROS_BASE_URL}/clients/check"
    try:
        response = requests.get(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        response_data = response.json()
        if response_data['code'] == 200:
            return True
        else:
            msg = response_data['message']
            code = response_data['code']
            logger.warning(f"Qualification failed with license {aw_license} \ncode: {code}\nmessage: {msg}")
            return False

    except requests.RequestException as e:
        raise RuntimeError(f"Failed to contribute model result: {e}, "
                           f"Please contact us {EAROS_WEBSITE}") from e


def model_task_req(node_data: dict) -> dict:
    HEADERS['Authorization'] = 'Bearer {}'.format(node_data['aw_license'])
    HEADERS['X-Device-Id'] = node_data['node_id']
    url = f"{EAROS_BASE_URL}/clients/tasks/take"
    try:
        response = requests.post(url, headers=HEADERS, json=node_data)
        response.raise_for_status()
        response_data = response.json()
        code = response_data['code']
        msg = response_data["message"]
        task_id = response_data["data"]["id"]
        task_name = response_data["data"]["name"]
        model_type = response_data["data"]["model"]
        params = response_data["data"]["training_data"]
        if response_data["code"] == 200:
            return {
                "task_id": task_id,
                "task_name": task_name,
                "model_type": model_type,
                "params": params,
                "msg": msg
            }
        else:
            logger.warning(f"!!!!WARNING!!!Bad request: \ncode: {code}\nmessage: {msg}")
    except requests.exceptions.HTTPError as http_err:
        raise RuntimeError(f"HTTP error occurred: {http_err}") from http_err
    except requests.RequestException as req_err:
        raise RuntimeError(f"Request error occurred: {req_err}") from req_err
    except (json.JSONDecodeError, KeyError) as parse_err:
        logger.error(f"!!!!WARNING!!!Bad request: {msg}")
        raise ValueError(f"Failed to parse response: {parse_err}") from parse_err


def model_res_contribute(node_data, model_res, task_id) -> bool:
    HEADERS['Authorization'] = 'Bearer {}'.format(node_data['aw_license'])
    HEADERS['X-Device-Id'] = node_data['node_id']

    payload = {
        "node_data": node_data,
        "model_res": model_res
    }
    url = f"{EAROS_BASE_URL}/clients/tasks/{task_id}/complete"
    try:
        response = requests.put(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        response_data = response.json()
        code = response_data['code']
        msg = response_data["message"]
        if response_data["code"] == 200:
            return True
        else:
            logger.warning(f"!!!!WARNING!!!Bad request: \ncode: {code}\nmessage: {msg}")
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to contribute model result: {e}") from e

import functools
import hashlib
import platform
import psutil
import requests
import uuid


def generate_machine_id():
    hostname = uuid.getnode()

    unique_str = f"{hostname}"
    md5_hash = hashlib.md5()
    md5_hash.update(unique_str.encode('utf-8'))
    return md5_hash.hexdigest()


def get_node_loc(timeout=8):
    urls = [
        'https://api.ipify.org?format=json',
        'http://httpbin.org/ip',
        'https://ipinfo.io/json'
    ]
    for url in urls:
        try:
            # SSL verification enabled by default
            response = requests.get(url, timeout=timeout, verify=True)
            # Raise an error for bad HTTP status codes
            response.raise_for_status()
            ip_key = next((key for key in ['ip', 'origin', 'loc'] if key in response.json()), None)
            if ip_key:
                return response.json().get(ip_key)
        except requests.exceptions.SSLError as ssl_error:
            print(f"SSL Error with {url}: {ssl_error}")
        except requests.exceptions.Timeout:
            print(f"Request timed out for {url}.")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")

    return None


def safe_call(default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error calling {func.__name__}: {e}")
                return default

        return wrapper

    return decorator


@safe_call()
def get_cpu_model():
    return platform.processor()


@safe_call(default=None)
def get_memory_info():
    return psutil.virtual_memory()._asdict()


@safe_call(default=0)
def get_cpu_count(logical=False):
    return psutil.cpu_count(logical=logical)

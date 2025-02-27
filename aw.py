import logging
import os
import threading
import time
from colorlog import ColoredFormatter
from contextlib import contextmanager
from functools import wraps

# Configure logging for detailed tracking
log_format = "%(log_color)s%(asctime)s - %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()

# Import necessary modules from earos package
from earos.sys import get_node_loc, get_cpu_model, get_memory_info, get_cpu_count, generate_machine_id
from earos.aw_req import aw_verification, model_task_req, model_res_contribute, ping_aw_server
from earos.aw_model import model_processor, unit_model_processor
from earos.interact import aw_license as fetch_aw_license, aw_welcome


# Decorator for logging function calls
def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__} completed.")
        return result

    return wrapper


# Decorator for exception handling
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise

    return wrapper


# Context manager for managing background threads
@contextmanager
def managed_thread(target, aw_license, node_id, *args, **kwargs):
    disconnect_signal = threading.Event()
    thread = threading.Thread(
        target=target,
        args=(disconnect_signal, aw_license, node_id) + args,
        kwargs=kwargs,
        daemon=True
    )
    thread.start()
    try:
        yield thread
    finally:
        disconnect_signal.set()
        thread.join()


# Generator to continuously fetch model tasks
def continuous_model_tasks(node_data):
    while True:
        logger.info(
            "The AI is initializing its neural cores, ready to assimilate the incoming mission parameters. Task acquisition protocol engaged")
        task = model_task_req(node_data)
        yield task


# Main program logic
@handle_exceptions
@log_function
def main():
    # Welcome message and initialization
    aw_welcome()

    # Fetch user license
    logger.info("User license retrieved.")

    # Collect node data
    aw_license = fetch_aw_license()
    aw_license = aw_license.strip()
    node_data = {
        "node_id": generate_machine_id(),
        "ip": get_node_loc(),
        "cpu_model": get_cpu_model(),
        "cpu_count": get_cpu_count(),
        "memory_info": get_memory_info(),
        "aw_license": aw_license
    }
    logger.info("Node data collected.")
    # User verification
    aw_qualify = aw_verification(node_data)
    logger.info("User verification completed.")

    if not aw_qualify:
        logger.warning("Program aborting...")
        time.sleep(2)
        return

    # Start network monitoring thread
    with managed_thread(ping_aw_server, node_data["aw_license"], node_data["node_id"]) as reporter_thread:
        logger.info("Network start working.")

        # Continuously fetch and process model tasks
        for model_task in continuous_model_tasks(node_data):
            params = model_task["params"]
            logger.info(f"Mission parameters received\nModel mission initiating execution.")

            # Process the model task
            aw_dir = os.getcwd()
            model_type = os.path.join(aw_dir, "earos", "models", model_task["model_type"])
            model_res = model_processor(
                unit_model_processor,
                task_args=(model_task["task_name"],
                           model_type,
                           model_task["params"])
            )
            logger.info(f"Start to commit aw node contribution...{model_res}")
            # Contribute node results
            if model_res_contribute(node_data=node_data, model_res=model_res, task_id=model_task["task_id"]):
                logger.info("Contribution has increased!")
                logger.info("Earos is growing...")
            else:
                logger.info("Contribution needs improvement, try again later...")


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            support = "https://earos.io/index.html"
            logger.critical(f"Unexpected error: {e}\nPlease contact us: {support}")
            time.sleep(2)

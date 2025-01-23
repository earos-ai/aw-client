import logging
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
from rich.console import Console

console = Console()
from rich.panel import Panel
from functools import wraps
import pyfiglet


def aw_ascii_art(text: str, font: str = 'smslant') -> str:
    figlet = pyfiglet.Figlet(font=font)
    return figlet.renderText(text)


def aw_welcome():
    ascii_art0 = aw_ascii_art("Earos", font="banner3-D")
    ascii_art1 = aw_ascii_art("AW GEN", font="banner3-D")

    panel0 = Panel(ascii_art0, title="Earos")
    panel1 = Panel(ascii_art1, title="AW GEN")
    console.print(panel0)
    console.print(panel1)


def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Initialize AW ENV for user input........")
        result = func(*args, **kwargs)
        logger.info(f"Confirm user input or restart the program: {result}")
        return result

    return wrapper


@log_function_call
def aw_license():
    user_input = input(f"Please input your AW license: ")
    return user_input.lower()

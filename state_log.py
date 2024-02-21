import logging
from baseline_constants import system_logs_path

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

handler = logging.FileHandler(system_logs_path, "a")
handler.setFormatter(formatter)

logger = logging.getLogger('main_baseline_logger')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)03d %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG,
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

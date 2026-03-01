import logging

from picomc.colors import ColorFormatter

logger = logging.getLogger("picomc.cli")
debug = False


def initialize(debug_):
    global debug
    debug = debug_
    
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter("%(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel("DEBUG" if debug else "INFO")

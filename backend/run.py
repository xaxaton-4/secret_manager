import logging

import uvicorn

from config import settings
import views


logger = logging.getLogger('secret_manager')


if __name__ == '__main__':
    logger.info("Run secret manager...")

    config = {
        'host': settings.HOST,
        'port': settings.PORT,
        'workers': settings.UVICORN_WORKERS,
        'log_level': settings.LOG_LEVEL,
        'log_config': settings.LOG_CONFIG,
        'reload': settings.DEBUG,
    }

    uvicorn.run('core:app', **config)

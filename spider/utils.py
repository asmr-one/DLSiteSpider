import logging

logger = logging.getLogger(__name__)


def onException(fallback_return):
    def warpFunc(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                return fallback_return
        return wrapper
    return warpFunc

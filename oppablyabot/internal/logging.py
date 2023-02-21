import logging
from typing import TypeVar

from oppablyabot.config import (
    AppConfig,
    LoggingHandler,
    LoggingFileHandler,
    LoggingStreamHandler,
)

L = TypeVar('L', bound=LoggingHandler)


def create_logger(config: AppConfig) -> logging.Logger:
    logger = logging.Logger(
        name=config.logging.base_name, level=config.logging.base_level
    )
    _add_handler(logger, config.logging.handlers.file)
    _add_handler(logger, config.logging.handlers.stdout)

    return logger


def _add_handler(logger: logging.Logger, handler_config: L):
    if handler_config.enabled:
        logger.addHandler(_create_handler(handler_config))


def _create_handler(handler_config: L) -> logging.FileHandler | logging.StreamHandler:
    res: logging.FileHandler | logging.StreamHandler

    match handler_config:
        case LoggingFileHandler():
            res = _create_file_handler(handler_config)
        case LoggingStreamHandler():
            res = _create_stream_handler(handler_config)
        case _:
            raise NotImplementedError('Unknown logging handler type')

    res.setFormatter(
        logging.Formatter(
            fmt=handler_config.strformat, datefmt=handler_config.dateformat
        )
    )

    return res


def _create_file_handler(handler_config: LoggingFileHandler) -> logging.FileHandler:
    file_handler = logging.FileHandler(handler_config.filename)
    file_handler.setLevel(handler_config.level)

    return file_handler


def _create_stream_handler(
    handler_config: LoggingStreamHandler,
) -> logging.StreamHandler:
    stream_handler = logging.StreamHandler(handler_config.stream)
    stream_handler.setLevel(handler_config.level)

    return stream_handler


def get_child(logger: logging.Logger, name: str) -> logging.Logger:
    res = logger.getChild(name)
    res.handlers = logger.handlers
    res.setLevel(logger.level)

    return res

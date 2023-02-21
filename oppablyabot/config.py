import logging
import sys
from dataclasses import dataclass
from typing import TextIO

import dotenv

from oppablyabot.util import paths

TG_BOT_TOKEN = dotenv.get_key(
    dotenv_path=paths.DOT_ENV,
    key_to_get='TG_BOT_TOKEN',
)


@dataclass
class BotConfig:
    token: str | None = None


@dataclass
class LoggingComponentConfig:
    name: str


@dataclass
class LoggingComponentsConfig:
    bot_creator: LoggingComponentConfig


@dataclass
class LoggingHandler:
    enabled: bool
    level: int
    strformat: str
    dateformat: str


@dataclass
class LoggingFileHandler(LoggingHandler):
    filename: str


@dataclass
class LoggingStreamHandler(LoggingHandler):
    stream: TextIO


@dataclass
class LoggingHandlers:
    file: LoggingFileHandler
    stdout: LoggingStreamHandler


@dataclass
class LoggingConfig:
    base_name: str
    base_level: int
    components: LoggingComponentsConfig
    handlers: LoggingHandlers


@dataclass
class AppConfig:
    bot: BotConfig
    logging: LoggingConfig


app_config = AppConfig(
    bot=BotConfig(),
    logging=LoggingConfig(
        base_name='OppaBlyaBot',
        base_level=logging.DEBUG,
        components=LoggingComponentsConfig(
            bot_creator=LoggingComponentConfig(
                name='BotCreator',
            )
        ),
        handlers=LoggingHandlers(
            file=LoggingFileHandler(
                enabled=True,
                level=logging.DEBUG,
                strformat='[%(asctime)s] [%(levelname)-8s] [%(name)-30s] > %(message)s',
                dateformat='%Y-%m-%d %H:%M:%S',
                filename='./oppablyabot.log',
            ),
            stdout=LoggingStreamHandler(
                enabled=False,
                level=logging.INFO,
                strformat='[%(asctime)s] [%(levelname)-8s] [%(name)-30s] > %(message)s',
                dateformat='%H:%M:%S',
                stream=sys.stdout,
            ),
        ),
    ),
)

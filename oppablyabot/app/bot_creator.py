import logging

import aiogram

from oppablyabot.config import AppConfig
from oppablyabot.internal.logging import get_child as get_child_logger


class BotCreator:
    def __init__(self, logger: logging.Logger, config: AppConfig):
        self._logger = get_child_logger(
            logger, config.logging.components.bot_creator.name
        )
        self._config = config

    def create_bot(self) -> aiogram.Bot:
        bot = aiogram.Bot(token=self._config.bot.token)

        self._logger.debug(f'Bot created.')

        return bot

    def create_dispatcher(self, bot: aiogram.Bot) -> aiogram.Dispatcher:
        dispatcher = aiogram.Dispatcher(bot)

        self._logger.debug(f'Dispatcher created.')

        return dispatcher

    def create_executor(
        self, dispatcher: aiogram.Dispatcher
    ) -> aiogram.executor.Executor:
        executor = aiogram.executor.Executor(
            dispatcher=dispatcher,
            # skip_updates=True,
        )

        self._logger.debug(f'Executor created.')

        return executor

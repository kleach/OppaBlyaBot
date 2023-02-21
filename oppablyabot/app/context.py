import aiogram

from oppablyabot.util.singleton import Singleton


# from src.bot.media_db import MediaLinksDB


class AppContext(metaclass=Singleton):
    bot: aiogram.Bot
    dispatcher: aiogram.Dispatcher
    executor: aiogram.executor.Executor

    # media: MediaLinksDB

    def set_bot(self, bot: aiogram.Bot):
        self.bot = bot

    def set_dispatcher(self, dispatcher: aiogram.Dispatcher):
        self.dispatcher = dispatcher

    def set_executor(self, executor: aiogram.executor.Executor):
        self.executor = executor

    # def set_media(self, media: MediaLinksDB):
    #     self.media = media

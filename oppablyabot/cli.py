import logging

import cloup
import dotenv

from oppablyabot.app import AppContext, BotCreator
from oppablyabot.config import app_config
from oppablyabot.internal.logging import create_logger

# import oppablyabot.utils.logging
#
# import oppablyabot.bot.creators as creators
# from oppablyabot.bot.media_db import MediaLinksDB
# from oppablyabot.utils.context import Context
# from oppablyabot.bot.cmd import post_load_cmds

app_context: AppContext
app_logger: logging.Logger

context_settings = cloup.Context.settings(
    terminal_width=120,
    help_option_names=['-h', '--help'],
    color=True,
    formatter_settings=cloup.HelpFormatter.settings(theme=cloup.HelpTheme.dark()),
)


@cloup.group(name='OppaBlyaBot', context_settings=context_settings)
@cloup.option_group(
    'Bot options',
    cloup.option(
        '-t',
        '--token',
        help='Telegram Bot token.',
        type=str,
    ),
    cloup.option(
        '--env-file',
        help='Path to the .env file containing Telegram Bot token.',
        type=cloup.types.file_path(),
        default='.env',
    ),
    constraint=cloup.constraints.mutually_exclusive,
)
@cloup.option_group(
    'Logging options',
    cloup.option(
        '--logging-file-enabled/--no-logging-file',
        help='Whether to log to the file.',
        is_flag=True,
        default=app_config.logging.handlers.file.enabled,
    ),
    cloup.option(
        '--logging-file',
        help='Path to the log file.',
        type=cloup.types.file_path(),
        default=app_config.logging.handlers.file.filename,
    ),
)
def cli(
    token: str | None, env_file: str, logging_file_enabled: bool, logging_file: str
):
    global app_logger

    if token:
        app_config.bot.token = token
    else:
        app_config.bot.token = dotenv.get_key(
            dotenv_path=env_file,
            key_to_get='TG_BOT_TOKEN',
        )

    app_config.logging.handlers.file.enabled = logging_file_enabled
    app_config.logging.handlers.file.filename = logging_file

    app_logger = create_logger(app_config)

    app_logger.debug(f'{app_config.bot.token=}')

    creator = BotCreator(app_logger, app_config)
    app_context = AppContext()
    app_context.set_bot(creator.create_bot())
    app_context.set_dispatcher(creator.create_dispatcher(app_context.bot))
    app_context.set_executor(creator.create_executor(app_context.dispatcher))
    # app_context.set_media(MediaLinksDB())
    # post_load_cmds()


@cli.command(name='run', help='Run bot')
def run():
    # app_context.executor.start_polling()
    pass

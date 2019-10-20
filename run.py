import logging

from decouple import config

from app import app
from bot import JerimumBot


if __name__ == '__main__':
    bot = JerimumBot(
        token=config('BOT_TOKEN', default='??'),
        port=config('PORT', default=8443, cast=int),
        server_url=config('SERVER_URL', default='??')
    )

    try:
        mode = config('MODE', default='cmd')
        if mode == 'cmd':
            bot.run_cmd()
        elif mode == 'web':
            bot.run_web()
        else:
            raise Exception('O modo passado não foi reconhecido')

    except Exception as e:
        logging.error(f'Modo: {config("MODE", default="cmd")}')
        logging.error(f'token: {bot.token}')
        logging.error(f'Port: {bot.port}')
        logging.error(f'heroku app name: {bot.server_url}')
        raise e

    app.run()

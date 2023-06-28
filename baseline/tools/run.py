import sys
import os
import asyncio
import signal
import functools
from loguru import logger


def shutdown(loop):
    logger.info(f'received stop signal, cancelling tasks...')
    loop.stop()


def asyncio_run(coroutine):
    loop = asyncio.get_event_loop()

    is_win32 = sys.platform == 'win32'
    if not is_win32:
        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(shutdown, loop))

    logger.info(f'Event loop running, press Ctrl+C to interrupt. Pid {os.getpid()}: send SIGINT or SIGTERM to exit.')

    try:
        loop.run_until_complete(coroutine)
    except asyncio.CancelledError as e:
        logger.info(
            f'Stop (cancel) session.')
    except RuntimeError as e:
        logger.error(f'RuntimeError: {e}')
        logger.opt(exception=True).debug(f'RuntimeError: {e}')
    except KeyboardInterrupt as e:
        logger.error(f'KeyboardInterrupt: {e}')
        logger.opt(exception=True).debug(f'KeyboardInterrupt: {e}')
    shutdown(loop)
    sys.exit(1)

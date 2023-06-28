import click
from loguru import logger
from typing import Optional

from baseline.tools.constants import SessionContestType, SessionStageType, SessionDatasetType, SessionMainType
from baseline.tools.run import asyncio_run
from baseline.session.dto import SessionStarterOptions
from baseline.session.session import Session


def min_validate(min_value):
    def inner_min_validate(ctx, param, value):
        if value:
            if value < min_value:
                raise click.BadParameter(f'{param} минимальное значение {min_value}')
            return value

    return inner_min_validate


@click.group(help="Baseline cli")
def cli():
    """
    Baseline cli
    """


@cli.group(help="Manages session")
def session():
    """Manages session """


@session.command('start', help="Use for start a session with params")
@click.option(
    '--sessiontype', '-st', 'sessiontype',
    type=click.Choice(list(SessionMainType.__args__)),
    default='training',
    # prompt=True,
    show_default=True,
    help="Тип сессии, по умолчанию запускается training")
@click.option(
    '--contest', '-c', 'contest',
    type=click.Choice(list(SessionContestType.__args__)),
    default='finder',
    # prompt=True,
    show_default=True,
    help="Тип конкурса, по умолчанию запускается finder")
@click.option(
    '--stage', '-stage', 'stage',
    type=click.Choice(list(SessionStageType.__args__)),
    default='qualifying',
    show_default=True,
    help="""
    Этап конкурса, который будет участвовать в обмене
    """)
@click.option(
    '--file-count', '-fc',
    type=int,
    show_default=True,
    callback=min_validate(1),
    help="Определяет, сколько файлов будет в сессии (применим только в алгоритмической сессии)")
@click.option(
    '--file-timeout', '-ft',
    type=int,
    callback=min_validate(10),
    show_default=True,
    help="Определяет, какой будет таймаут между доступностью файлов (применим только в тренировочной сессии)")
def session_start(
        sessiontype: SessionMainType,
        contest: SessionContestType,
        stage: SessionStageType,
        file_count: Optional[int],
        file_timeout: Optional[int]):
    opts = SessionStarterOptions(
        session_type=sessiontype,
        contest=contest,
        stage=stage,
        file_count=file_count,
        file_timeout=file_timeout
    )
    logger.info('Session start command')
    asyncio_run(Session().start(opts))


@session.command('abort', help="Use for abort the active session")
def session_abort():
    logger.info('Session abort command')
    asyncio_run(Session().abort())


@session.command('reconnect', help="Use for reconnect to the active session")
def session_reconnect():
    logger.info('Session reconnect command')
    asyncio_run(Session().reconnect())


if __name__ == '__main__':
    cli()

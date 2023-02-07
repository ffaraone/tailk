import asyncio
import copy
import logging
import uvloop

import click

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

from tailk.constants import DEFAULT_THEME
from tailk.highlighter import TailKHighlighter
from tailk.tail import TailK


@click.command()
@click.argument(
    'patterns',
    nargs=-1,
    required=True,
)
@click.option(
    '--max-podname-length',
    type=click.IntRange(min=5),
    default=20,
    help='Truncate the name of the pod to not exceed such length.',
)
@click.option(
    '--highlight',
    multiple=True,
    default=[],
    help='Regex pattern to highlight log content.',
)
@click.option(
    '--style',
    multiple=True,
    default=[],
    help='Custom style for given capturing group.',
)
def start(patterns, max_podname_length, highlight, style):
    uvloop.install()

    theme_data = copy.copy(DEFAULT_THEME)

    for style in style:
        name, style_info = style.split(':')
        theme_data[f'tailk.{name}'] = style_info

    theme = Theme(theme_data)


    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(
            show_time=False,
            show_level=False,
            show_path=False,
            markup=True,
            keywords=[],
            highlighter=TailKHighlighter(highlight),
            console=Console(theme=theme),
        )],
    )
    t = TailK(patterns, max_podname_length)
    asyncio.run(t.start())


def main(
):
    """
    Tail the log of pods that match the given PATTERNS.
    """
    try:
        start(prog_name='tailk', standalone_mode=False)
    except click.Abort:
        pass
    except Exception as e:
        click.secho(f'\n{e}', fg='red', err=True)


if __name__ == '__main__':  # pragma: no cover
    main()




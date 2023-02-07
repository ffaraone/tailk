import argparse
import asyncio
import logging
import signal
import uvloop

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

from tailk.constants import DEFAULT_THEME
from tailk.highlighter import TailKHighlighter
from tailk.tail import TailK


theme = Theme(DEFAULT_THEME)


def validate_podname_length(arg):
    try:
        value = int(arg)
    except ValueError: 
        raise argparse.ArgumentTypeError("Must be an integer.")
    if value < 5:
        raise argparse.ArgumentTypeError("Must be greater or equal to 5.")
    return value
    


def start(data):
    uvloop.install()

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
            highlighter=TailKHighlighter(data.highlight),
            console=Console(theme=theme),
        )],
    )
    t = TailK(data.patterns, data.max_podname_length)
    asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, t.stop)
    asyncio.run(t.start())


def main():
    parser = argparse.ArgumentParser(prog='tailk')
    parser.add_argument('patterns', nargs='*', help='pods search patterns')
    parser.add_argument(
        '--max-podname-length',
        type=validate_podname_length,
        default=20,
    )
    parser.add_argument('--highlight', nargs='*')
    data = parser.parse_args()
    start(data)


if __name__ == '__main__':  # pragma: no cover
    main()




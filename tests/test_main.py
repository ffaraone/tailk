import argparse
from collections import namedtuple

import pytest
from rich.logging import RichHandler
from tailk.highlighter import TailKHighlighter

from tailk.main import main, validate_podname_length, start


ParsedArgs = namedtuple('ParsedArgs', ('patterns', 'max_podname_length', 'highlight'))


def test_main(mocker):
    mocked_parser = mocker.MagicMock()
    mocked_parser.parse_args.return_value = mocker.MagicMock()

    mocker.patch('tailk.main.argparse.ArgumentParser', return_value=mocked_parser)
    mocked_start = mocker.patch('tailk.main.start')

    main()

    mocked_start.assert_called_once_with(mocked_parser.parse_args.return_value)


def test_validate_podname_length_ok():
    assert validate_podname_length('5') == 5
    assert validate_podname_length('15') == 15


@pytest.mark.parametrize(
        'value',
        ('4', '0', '-4', 'a'),
)
def test_validate_podname_length_ko(value):
    with pytest.raises(argparse.ArgumentTypeError):
        validate_podname_length(value)


@pytest.mark.asyncio
async def test_start(mocker):
    mocked_uvloop_install = mocker.patch('tailk.main.uvloop.install')
    mocked_basic_config = mocker.patch(
        'tailk.main.logging.basicConfig',
    )
    mocked_tailk = mocker.MagicMock()
    mocked_tailk.start.return_value = 'run_coro'

    mocked_tailk_constructor = mocker.patch(
        'tailk.main.TailK',
        return_value=mocked_tailk,
    )
    mocked_asyncio_run = mocker.patch(
        'tailk.main.asyncio.run',
    )

    start(ParsedArgs(['patterns'], 10, ['highlight']))

    mocked_uvloop_install.assert_called_once()
    assert mocked_basic_config.mock_calls[0].kwargs['level'] == 'NOTSET'
    assert mocked_basic_config.mock_calls[0].kwargs['format'] == '%(message)s'
    assert mocked_basic_config.mock_calls[0].kwargs['datefmt'] == '[%X]'
    assert isinstance(
        mocked_basic_config.mock_calls[0].kwargs['handlers'][0],
        RichHandler,
    )
    assert isinstance(
        mocked_basic_config.mock_calls[0].kwargs['handlers'][0].highlighter,
        TailKHighlighter,
    )
    mocked_tailk_constructor.assert_called_once_with(['patterns'], 10)
    mocked_asyncio_run.assert_called_once_with('run_coro')


@pytest.mark.asyncio
async def test_start_stop(mocker):
    mocked_uvloop_install = mocker.patch('tailk.main.uvloop.install')
    mocked_basic_config = mocker.patch(
        'tailk.main.logging.basicConfig',
    )
    mocked_tailk = mocker.MagicMock()
    mocked_tailk.start.return_value = 'run_coro'

    mocked_tailk_constructor = mocker.patch(
        'tailk.main.TailK',
        return_value=mocked_tailk,
    )
    mocked_asyncio_run = mocker.patch(
        'tailk.main.asyncio.run',
    )

    start(ParsedArgs(['patterns'], 10, ['highlight']))

    mocked_uvloop_install.assert_called_once()
    assert mocked_basic_config.mock_calls[0].kwargs['level'] == 'NOTSET'
    assert mocked_basic_config.mock_calls[0].kwargs['format'] == '%(message)s'
    assert mocked_basic_config.mock_calls[0].kwargs['datefmt'] == '[%X]'
    assert isinstance(
        mocked_basic_config.mock_calls[0].kwargs['handlers'][0],
        RichHandler,
    )
    assert isinstance(
        mocked_basic_config.mock_calls[0].kwargs['handlers'][0].highlighter,
        TailKHighlighter,
    )
    mocked_tailk_constructor.assert_called_once_with(['patterns'], 10)
    mocked_asyncio_run.assert_called_once_with('run_coro')
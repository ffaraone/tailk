import click
from click.testing import CliRunner
import pytest

from rich.logging import RichHandler

from tailk.highlighter import TailKHighlighter
from tailk.main import main, start


def test_main(mocker):
    mocked_start = mocker.patch('tailk.main.start')
    main()
    mocked_start.assert_called_once_with(prog_name='tailk', standalone_mode=False)


def test_main_abort(mocker, capsys):
    mocked_start = mocker.patch('tailk.main.start', side_effect=click.Abort)
    main()
    mocked_start.assert_called_once_with(prog_name='tailk', standalone_mode=False)
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


def test_main_exception(mocker, capsys):
    mocked_start = mocker.patch('tailk.main.start', side_effect=Exception('error'))
    main()
    mocked_start.assert_called_once_with(prog_name='tailk', standalone_mode=False)
    out, err = capsys.readouterr()
    assert out == ''
    assert err == '\nerror\n'


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
    mocked_theme = mocker.patch(
        'tailk.main.Theme',
    )

    runner = CliRunner()
    runner.invoke(
        start,
        [
            'patterns',
            '--highlight', 'highlight',
            '--style', 'name:style',
            '--max-podname-length', '10',
        ],
    )

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
    mocked_tailk_constructor.assert_called_once_with(('patterns',), 10)
    mocked_asyncio_run.assert_called_once_with('run_coro')
    assert mocked_theme.mock_calls[0].args[0]['tailk.name'] == 'style'


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

    runner = CliRunner()
    runner.invoke(
        start,
        [
            'patterns',
        ],
    )

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
    mocked_tailk_constructor.assert_called_once_with(('patterns',), 20)
    mocked_asyncio_run.assert_called_once_with('run_coro')

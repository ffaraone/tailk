import asyncio
import re

import pytest

from tailk.tail import TailK


def test_constructor():
    tailk = TailK(['pod1', 'pod2'], 10)
    assert tailk.patterns == ['pod1', 'pod2']
    assert tailk.max_podname_length == 10
    assert tailk.pod_selector == re.compile('(pod1|pod2)')


@pytest.mark.asyncio
async def test_start(mocker):
    mocked_process = mocker.AsyncMock()
    mocked_process.returncode = 0
    mocked_process.communicate.return_value = (
        b'pod1-abcd whatever\npod2-efgh whatever\npod3-ijkl whatever\n',
        b'',
    )
    mocked_subp = mocker.patch(
        'tailk.tail.asyncio.subprocess.create_subprocess_shell',
        return_value=mocked_process,
    )
    mocked_tail = mocker.patch.object(TailK, 'tail')
    
    tailk = TailK(['pod1', 'pod2'], 10)
    await tailk.start()

    mocked_subp.assert_awaited_once_with(
        'kubectl get pods --field-selector=status.phase=Running',
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        start_new_session=True,
    )
    assert mocked_tail.call_count == 2
    assert mocked_tail.mock_calls[0].args[0] == 'pod1-abcd'
    assert mocked_tail.mock_calls[1].args[0] == 'pod2-efgh'


@pytest.mark.asyncio
async def test_start_no_pod_found(mocker):
    mocked_process = mocker.AsyncMock()
    mocked_process.returncode = 0
    mocked_process.communicate.return_value = (
        b'pod1-abcd whatever\npod2-efgh whatever\npod3-ijkl whatever\n',
        b'',
    )
    mocker.patch(
        'tailk.tail.asyncio.subprocess.create_subprocess_shell',
        return_value=mocked_process,
    )
    mocked_tail = mocker.patch.object(TailK, 'tail')
    
    tailk = TailK(['pod4', 'pod5'], 10)
    await tailk.start()
    assert tailk.tasks == []
    assert mocked_tail.call_count == 0


@pytest.mark.asyncio
async def test_start_subprocess_error(mocker):
    mocked_process = mocker.AsyncMock()
    mocked_process.returncode = -1
    mocked_process.communicate.return_value = (
        b'',
        b'kubectl: command not found',
    )
    mocker.patch(
        'tailk.tail.asyncio.subprocess.create_subprocess_shell',
        return_value=mocked_process,
    )
    with pytest.raises(Exception) as cv:
        tailk = TailK(['pod4', 'pod5'], 10)
        await tailk.start()
    assert str(cv.value) == 'kubectl: command not found'


@pytest.mark.asyncio
async def test_tail(mocker):
    mocked_process = mocker.AsyncMock()
    mocked_process.stdout.readline = mocker.AsyncMock(return_value=b'log line\n')
    mocked_subp = mocker.patch(
        'tailk.tail.asyncio.subprocess.create_subprocess_shell',
        return_value=mocked_process,
    )
    mocked_logger = mocker.patch('tailk.tail.logger')

    tailk = TailK(['my-pod', 'pod5'], 10)
    tailk.run_event.set()
    task = asyncio.create_task(tailk.tail('my-pod', 'blue'))
    await asyncio.sleep(0)
    tailk.stop()
    await task

    mocked_subp.assert_awaited_once_with(
        'kubectl logs --since=1s -f my-pod',
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        start_new_session=True,
    )

    assert mocked_logger.info.mock_calls[0].args[0] == '[blue](my-pod)[/blue] log line'


@pytest.mark.asyncio
async def test_tail_log_pod_name(mocker):
    mocked_process = mocker.AsyncMock()
    mocked_process.stdout.readline = mocker.AsyncMock(return_value=b'log line\n')
    mocked_subp = mocker.patch(
        'tailk.tail.asyncio.subprocess.create_subprocess_shell',
        return_value=mocked_process,
    )
    mocked_logger = mocker.patch('tailk.tail.logger')

    tailk = TailK(['my-pod', 'pod5'], 5)
    tailk.run_event.set()
    task = asyncio.create_task(tailk.tail('my-pod-long-name-abcdef', 'blue'))
    await asyncio.sleep(0)
    tailk.stop()
    await task

    mocked_subp.assert_awaited_once_with(
        'kubectl logs --since=1s -f my-pod-long-name-abcdef',
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        start_new_session=True,
    )

    assert mocked_logger.info.mock_calls[0].args[0] == (
        '[blue](my-pod-long-name-ab...-abcdef)[/blue] log line'
    )
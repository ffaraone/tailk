import asyncio
import logging
import re

from rich.color import ANSI_COLOR_NAMES

logger = logging.getLogger('tailk')


COLORS = list(ANSI_COLOR_NAMES.keys())


class TailK:
    def __init__(self, patterns, max_podname_length):
        self.patterns = patterns
        self.pod_selector = re.compile(
            rf'({"|".join(self.patterns)})',
        )
        self.max_podname_length = max_podname_length
        self.tasks = []
        self.run_event = asyncio.Event()

    async def start(self):
        self.run_event.set()
        proc = await asyncio.subprocess.create_subprocess_shell(
            'kubectl get pods --field-selector=status.phase=Running',
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=True,
        )
        std_out, std_err = await proc.communicate()
        if proc.returncode == 0:
            lines = std_out.decode().splitlines()
            for idx, line in enumerate(lines):
                podname, _ = line.split(' ', 1)
                if not self.pod_selector.match(podname):
                    continue
                logger.info(f'tail from {podname}')
                color = COLORS[idx % len(COLORS)]
                self.tasks.append(asyncio.create_task(self.tail(podname, color)))
        else:
            raise Exception(std_err.decode())
        if self.tasks:
            await asyncio.gather(*self.tasks)

    def stop(self, *args, **kwargs):
        self.run_event.clear()

    async def tail(self, pod_name, color):
        proc = await asyncio.subprocess.create_subprocess_shell(
            f'kubectl logs --since=1s -f {pod_name}',
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=True,
        )
        if len(pod_name) <= self.max_podname_length:
            label = pod_name
        else:
            _, pod_id = pod_name.rsplit('-', 1)
            label = f'{pod_name[0:self.max_podname_length - 9]}...-{pod_id}'
        while self.run_event.is_set():
            message = (await proc.stdout.readline()).decode()[:-1] 
            line = f'[{color}]({label})[/{color}] {message}'
            logger.info(line)
            await asyncio.sleep(0)
import json
import sys
from pathlib import Path

import iterm2

REAL_ROOTDIR_PATH = Path(__file__).resolve().parent
sys.path.append(REAL_ROOTDIR_PATH.__str__())

import psutil


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}', f'{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}', f'Y{suffix}'


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='Disk Usage',
        detailed_description='Display the usage of disk.',
        knobs=[],
        exemplar=' 44.1 GB  179.7/233.5 GB (81.0%)',
        update_cadence=2,
        identifier='peinan.diskusage'
    )

    @iterm2.StatusBarRPC
    async def diskusage(knobs):
        disk_char = '\uE9B7'
        disk = psutil.disk_usage('/')
        unit = sizeof_fmt(disk.total)[1]
        usage = f'{disk_char} {" ".join(sizeof_fmt(disk.free))} ' \
                f'\uEB5D {sizeof_fmt(disk.used)[0]}/{sizeof_fmt(disk.total)[0]} {unit} ({disk.percent}%)'

        return usage

    await component.async_register(connection, diskusage)


iterm2.run_forever(main)

import shutil
from dataclasses import dataclass

import iterm2


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}', f'{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}', f'Y{suffix}'


@dataclass
class KnobOption:
    name: str
    v: bool


async def main(connection):
    knob_free = KnobOption('free', True)
    knob_usedtotal = KnobOption('usedtotal', True)
    knob_usedpercent = KnobOption('usedpercent', True)
    knobs = [
        iterm2.CheckboxKnob(name='Show Free Space', default_value=knob_free.v, key=knob_free.name),
        iterm2.CheckboxKnob(name='Show Used/Total Space', default_value=knob_usedtotal.v, key=knob_usedtotal.name),
        iterm2.CheckboxKnob(name='Show Used Space (%)', default_value=knob_usedpercent.v, key=knob_usedpercent.name),
    ]

    component = iterm2.StatusBarComponent(
        short_description='Disk Usage',
        detailed_description='Display the usage of disk.',
        knobs=knobs,
        exemplar=' 44.1 GB  179.7/233.5 GB (81.0%)',
        update_cadence=2,
        identifier='peinan.diskusage'
    )

    def is_true_knob(knobs, knob_option: KnobOption):
        return knob_option.name in knobs and knobs[knob_option.name]

    @iterm2.StatusBarRPC
    async def diskusage(knobs):
        true_free = is_true_knob(knobs, knob_free)
        true_usedtotal = is_true_knob(knobs, knob_usedtotal)
        true_usedpercent = is_true_knob(knobs, knob_usedpercent)

        disk_char = ''
        free_total_char = ' ' if true_free and true_usedtotal else ''
        disk = shutil.disk_usage('/')
        unit = sizeof_fmt(disk.total)[1]

        v_free = f' {" ".join(sizeof_fmt(disk.free))}' if true_free else ''
        v_usedtotal = f' {sizeof_fmt(disk.used)[0]}/{sizeof_fmt(disk.total)[0]} {unit}' if true_usedtotal else ''
        v_usedp = f' ({100 * disk.used / disk.total:.1f}%)' if (true_free or true_usedtotal) and true_usedpercent\
                  else f' {100 * disk.used / disk.total:.1f}%' if true_usedpercent else ''

        usage = f'{disk_char}{v_free}{free_total_char}{v_usedtotal}{v_usedp}'

        return usage

    await component.async_register(connection, diskusage)


iterm2.run_forever(main)

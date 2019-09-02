import shutil
from dataclasses import dataclass
from typing import Union

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
    v: Union[str, bool]


async def main(connection):
    knob_icons = KnobOption('icons', '')
    knob_free = KnobOption('free', True)
    knob_usedtotal = KnobOption('usedtotal', True)
    knob_usedpercent = KnobOption('usedpercent', True)
    knobs = [
        iterm2.StringKnob(name='Icons', default_value=knob_icons.v, placeholder=knob_icons.v, key=knob_icons.name),
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
        true_icons = is_true_knob(knobs, knob_icons)
        true_free = is_true_knob(knobs, knob_free)
        true_usedtotal = is_true_knob(knobs, knob_usedtotal)
        true_usedpercent = is_true_knob(knobs, knob_usedpercent)

        char_header = knobs[knob_icons.name][0] if true_icons else ''
        char_usedtotal = f' {knobs[knob_icons.name][-1]}' if true_icons and true_free and true_usedtotal else ''
        disk = shutil.disk_usage('/')
        unit = sizeof_fmt(disk.total)[1]

        v_free = f' {" ".join(sizeof_fmt(disk.free))}' if true_free else ''
        v_usedtotal = f' {sizeof_fmt(disk.used)[0]}/{sizeof_fmt(disk.total)[0]} {unit}' if true_usedtotal else ''
        v_usedp = f' ({100 * disk.used / disk.total:.1f}%)' if (true_free or true_usedtotal) and true_usedpercent\
                  else f' {100 * disk.used / disk.total:.1f}%' if true_usedpercent else ''

        usage = f'{char_header}{v_free}{char_usedtotal}{v_usedtotal}{v_usedp}'

        return usage

    await component.async_register(connection, diskusage)


iterm2.run_forever(main)

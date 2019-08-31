from datetime import datetime

import iterm2


async def main(connection):
    fmt = 'fmt'
    default_fmt = '%m/%d %a %H:%M:%S'
    knobs = [iterm2.StringKnob(name='format', placeholder=default_fmt,
                               default_value=default_fmt, key=fmt)]
    component = iterm2.StatusBarComponent(
        short_description='Clock',
        detailed_description='A customized clock.',
        knobs=knobs,
        exemplar=' 08/03 Sat 01:56:48',
        update_cadence=1,
        identifier='peinan.clock'
    )

    @iterm2.StatusBarRPC
    async def clock(knobs):
        n = datetime.now()
        clock_char = '\uE94F'
        if fmt in knobs and knobs[fmt]:
            clock_face = f'{clock_char} {n.strftime(knobs[fmt])}'
        else:
            clock_face = f'{clock_char} {n.strftime(default_fmt)}'

        return clock_face

    await component.async_register(connection, clock)


iterm2.run_forever(main)

from datetime import datetime

import iterm2


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='Clock',
        detailed_description='A customized clock.',
        knobs=[],
        exemplar=' 08/03 Sat 01:56:48',
        update_cadence=1,
        identifier='peinan.clock'
    )

    @iterm2.StatusBarRPC
    async def clock(knobs):
        n = datetime.now()
        weekid2lang = {
            0: 'Mon',
            1: 'Tue',
            2: 'Wed',
            3: 'Thu',
            4: 'Fri',
            5: 'Sat',
            6: 'Sun',
        }
        clock_char = '\uE94F'
        clock_face = f'{clock_char} {n.month:02d}/{n.day:02d} {weekid2lang[n.weekday()]} '\
                     f'{n.hour:02d}:{n.minute:02d}:{n.second:02d}'

        return clock_face

    await component.async_register(connection, clock)


iterm2.run_forever(main)

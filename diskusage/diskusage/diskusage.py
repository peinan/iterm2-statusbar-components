import iterm2
import shutil


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}', f'{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}', f'Y{suffix}'


async def main(connection):
    opt_free = 'opt_free'
    opt_ut = 'opt_ut'
    opt_usedp = 'opt_usedp'

    knobs = [
        iterm2.CheckboxKnob(name='Show Free Space', default_value=True, key=opt_free),
        iterm2.CheckboxKnob(name='Show Used/Total Space', default_value=True, key=opt_ut),
        iterm2.CheckboxKnob(name='Show Used Space (%)', default_value=True, key=opt_usedp),
    ]

    component = iterm2.StatusBarComponent(
        short_description='Disk Usage',
        detailed_description='Display the usage of disk.',
        knobs=knobs,
        exemplar=' 44.1 GB  179.7/233.5 GB (81.0%)',
        update_cadence=2,
        identifier='peinan.diskusage'
    )

    @iterm2.StatusBarRPC
    async def diskusage(knobs):
        true_opt_free = opt_free in knobs and knobs[opt_free]
        true_opt_ut = opt_ut in knobs and knobs[opt_ut]
        true_opt_usedp = opt_usedp in knobs and knobs[opt_usedp]

        disk_char = ''
        free_total_char = ' ' if (opt_free in knobs and knobs[opt_free]) and \
                                       (opt_ut in knobs and knobs[opt_ut]) else ''
        disk = shutil.disk_usage('/')
        unit = sizeof_fmt(disk.total)[1]

        v_free = f' {" ".join(sizeof_fmt(disk.free))}' if true_opt_free else ''
        v_usedtotal = f' {sizeof_fmt(disk.used)[0]}/{sizeof_fmt(disk.total)[0]} {unit}' if true_opt_ut else ''
        v_usedp = f' ({100 * disk.used / disk.total:.1f}%)' if (true_opt_free or true_opt_ut) and true_opt_usedp\
                  else f' {100 * disk.used / disk.total:.1f}%' if true_opt_usedp else ''

        usage = f'{disk_char}{v_free}{free_total_char}{v_usedtotal}{v_usedp}'

        return usage

    await component.async_register(connection, diskusage)


iterm2.run_forever(main)

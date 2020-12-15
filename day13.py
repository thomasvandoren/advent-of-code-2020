import click


@click.command()
@click.option('--f', type=click.File(), default='day13.txt')
def cli(f):
    lines = f.read().splitlines()
    earliest_leave_time = int(lines[0])
    bus_routes = [int(t) for t in lines[1].split(',') if t.strip() != 'x']

    leave_time = earliest_leave_time - 1
    bus_route = None
    while bus_route is None:
        leave_time += 1
        for r in bus_routes:
            if leave_time % r == 0:
                bus_route = r
                break

    # too high: 1004104 (starts at 1004098)
    p1_answer = bus_route * (leave_time - earliest_leave_time)
    click.echo(f'[part1] {p1_answer} (bus route: {bus_route}, leave time: {leave_time}, earliest leave time: {earliest_leave_time})')

    p2_bus_routes = [t.strip() for t in lines[1].split(',')]
    p2_bus_routes = [1 if t == 'x' else int(t) for t in p2_bus_routes]

    p2_time = 0  # 100000000000000
    step = 1
    for i, bus_route in enumerate(p2_bus_routes):
        target = _get_mod(i, bus_route)

        while p2_time % bus_route != target:
            p2_time += step

        step *= bus_route

    click.echo(f'[part2] {p2_time}')


def _get_mod(i, bus_route):
    r = i % bus_route
    if r != 0:
        r = bus_route - r
    return r


def _mods_in_order(p2_bus_routes, t, bus_routes):
    last_mod = None
    for br in p2_bus_routes:
        if last_mod is None:
            last_mod = t % br
            continue

        if br is not None:
            mod = t % br
            if mod <= last_mod:
                return False
            else:
                last_mod =  mod
        else:
            mod_gt_last = []
            for r in bus_routes:
                mod = t % r
                if mod >= last_mod:
                    mod_gt_last.append((mod, br))

            if not mod_gt_last:
                return False
            else:
                min_mod = list(sorted(mod_gt_last, key=lambda i: i[0]))[0]
                last_mod = min_mod[0]

    return True


if __name__ == '__main__':
    cli()

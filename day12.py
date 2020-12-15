import click


@click.command()
@click.option('--f', type=click.File(), default='day12.txt')
def cli(f):
    directions = [(l[0], int(l[1:])) for l in f.read().splitlines()]
    heading = (1, 0)
    start = (0, 0)
    cur = (0, 0)
    for direction in directions:
        action, value = direction

        if action == 'E':
            cur = (cur[0] + value, cur[1])
        elif action == 'N':
            cur = (cur[0], cur[1] + value)
        elif action == 'W':
            cur = (cur[0] - value, cur[1])
        elif action == 'S':
            cur = (cur[0], cur[1] - value)
        elif action == 'F':
            cur = (cur[0] + heading[0] * value, cur[1] + heading[1] * value)
        elif action in ('L', 'R') and value == 180:
            heading = heading[0] * -1, heading[1] * -1
        elif (action == 'L' and value == 90) or (action == 'R' and value == 270):
            # L90, R270
            # East  (1, 0) => (0, 1)
            # North (0, 1) => (-1, 0)
            # West  (-1, 0) => (0, -1)
            # South (0, -1) => (1, 0)
            if heading[0] == 0:
                heading = (heading[1] * -1, heading[0])
            else:
                heading = (heading[1], heading[0])
        elif (action == 'L' and value == 270) or (action == 'R' and value == 90):
            # L270, R90
            # East  (1, 0) => (0, -1)
            # South (0, -1) => (-1, 0)
            # West  (-1, 0) => (0, 1)
            # North (0, 1) => (1, 0)
            if heading[0] == 0:
                heading = (heading[1], heading[0])
            else:
                heading = (heading[1], heading[0] * -1)
        else:
            raise click.ClickException(f'Unrecognized action: {action}, {value}')

    x, y = abs(cur[0] - start[0]), abs(cur[1] - start[1])
    manhattan_dist = x + y

    # too high: 1004, 1036
    click.echo(f'[part1] {manhattan_dist} {x, y}')

    p2_ship = (0, 0)
    p2_waypoint = (10, 1)

    for direction in directions:
        action, value = direction
        delta = (p2_waypoint[0] - p2_ship[0]), (p2_waypoint[1] - p2_ship[1])

        if action == 'E':
            p2_waypoint = p2_waypoint[0] + value, p2_waypoint[1]
        elif action == 'N':
            p2_waypoint = p2_waypoint[0], p2_waypoint[1] + value
        elif action == 'W':
            p2_waypoint = p2_waypoint[0] - value, p2_waypoint[1]
        elif action == 'S':
            p2_waypoint = p2_waypoint[0], p2_waypoint[1] - value
        elif action == 'F':
            p2_ship = p2_ship[0] + delta[0] * value, p2_ship[1] + delta[1] * value
            p2_waypoint = p2_ship[0] + delta[0], p2_ship[1] + delta[1]
        elif action in ('L', 'R') and value == 180:
            p2_waypoint = (p2_ship[0] + delta[0] * -1), (p2_ship[1] + delta[1] * -1)
        elif (action == 'L' and value == 90) or (action == 'R' and value == 270):
            # L90, R270
            # (10, 4) => (-4, 10)
            # (-4, 10) => (-10, -4)
            # (-10, -4) => (4, -10)
            # (4, -10) => (10, 4)
            p2_waypoint = (p2_ship[0] + delta[1]*-1), (p2_ship[1] + delta[0])
        elif (action == 'L' and value == 270) or (action == 'R' and value == 90):
            # L270, R90
            # (10, 4) => (4, -10)
            # (4, -10) => (-10, -4)
            # (-10, -4) => (-4, 10)
            # (-4, 10) => (10, 4)
            p2_waypoint = (p2_ship[0] + delta[1]), (p2_ship[1] + delta[0] * -1)

        else:
            raise click.ClickException(f'Unrecognized action: {action}, {value}')

    # too low: 71543
    p2_manhattan = abs(p2_ship[0]) + abs(p2_ship[1])
    click.echo(f'[part2] {p2_manhattan} {p2_ship}')


if __name__ == '__main__':
    cli()

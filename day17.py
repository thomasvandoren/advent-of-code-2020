import click
import copy


@click.command()
@click.option('--f', type=click.File(), default='day17.txt')
def cli(f):
    lines = f.read().splitlines()
    x_range = (0, len(lines))
    y_range = (0, len(list(lines[0].strip())))
    z_range = (0, 1)
    start_grid = {}
    for x, l in enumerate(lines):
        for y, c in enumerate(list(l.strip())):
            start_grid[(x, y, 0)] = c

    directions = {(x, y, z) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)}
    directions.remove((0, 0, 0))

    cur_grid = start_grid
    for _ in range(6):
        prev_grid = cur_grid
        active_cells = _get_active_cells(prev_grid)
        cur_grid = copy.deepcopy(prev_grid)
        x_range = x_range[0]-1, x_range[1]+1
        y_range = y_range[0]-1, y_range[1]+1
        z_range = z_range[0]-1, z_range[1]+1
        for x in range(*x_range):
            for y in range(*y_range):
                for z in range(*z_range):
                    cur_coord = (x, y, z)
                    active_neighbors = _get_active_neighbors(cur_coord, active_cells, directions)
                    if cur_coord not in prev_grid:
                        v = '.'
                    else:
                        v = prev_grid[cur_coord]

                    if v == '#' and not (2 <= len(active_neighbors) <= 3):
                        cur_grid[cur_coord] = '.'
                    elif v == '.' and len(active_neighbors) == 3:
                        cur_grid[cur_coord] = '#'

    active_cells = _get_active_cells(cur_grid)
    click.echo(f'[part1] active cells after 6 passes: {len(active_cells)}')

    p2_active_cells = _solve_p2(lines)
    click.echo(f'[part2] active cells after 6 passes: {len(p2_active_cells)}')


def _solve_p2(lines):
    x_range = (0, len(lines))
    y_range = (0, len(list(lines[0].strip())))
    z_range = (0, 1)
    w_range = (0, 1)
    start_grid = {}
    for x, l in enumerate(lines):
        for y, c in enumerate(list(l.strip())):
            start_grid[(x, y, 0, 0)] = c

    directions = {(x, y, z, w) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2) for w in range(-1, 2)}
    directions.remove((0, 0, 0, 0))

    cur_grid = start_grid
    for _ in range(6):
        prev_grid = cur_grid
        active_cells = _get_active_cells(prev_grid)
        cur_grid = copy.deepcopy(prev_grid)
        x_range = x_range[0] - 1, x_range[1] + 1
        y_range = y_range[0] - 1, y_range[1] + 1
        z_range = z_range[0] - 1, z_range[1] + 1
        w_range = w_range[0] - 1, w_range[1] + 1
        for x in range(*x_range):
            for y in range(*y_range):
                for z in range(*z_range):
                    for w in range(*w_range):
                        cur_coord = (x, y, z, w)
                        active_neighbors = _p2_get_active_neighbors(cur_coord, active_cells, directions)
                        if cur_coord not in prev_grid:
                            v = '.'
                        else:
                            v = prev_grid[cur_coord]

                        if v == '#' and not (2 <= len(active_neighbors) <= 3):
                            cur_grid[cur_coord] = '.'
                        elif v == '.' and len(active_neighbors) == 3:
                            cur_grid[cur_coord] = '#'

    active_cells = _get_active_cells(cur_grid)
    return active_cells


def _p2_get_active_neighbors(cur_coord, active_cells, directions):
    x, y, z, w = cur_coord
    active_neighbors = set()
    for xd, yd, zd, wd in directions:
        coord = (x + xd, y + yd, z + zd, w + wd)
        if coord in active_cells:
            active_neighbors.add(coord)
    return active_neighbors


def _get_active_neighbors(cur_coord, active_cells, directions):
    x, y, z = cur_coord
    active_neighbors = set()
    for xd, yd, zd in directions:
        coord = (x+xd, y+yd, z+zd)
        if coord in active_cells:
            active_neighbors.add(coord)
    return active_neighbors


def _get_active_cells(start_grid):
    return {coord for coord, v in start_grid.items() if v == '#'}


if __name__ == '__main__':
    cli()

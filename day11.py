import click


@click.command()
@click.option('--f', type=click.File(), default='day11.txt')
def cli(f):
    seats = [list(l.strip()) for l in f.read().splitlines()]

    prev = seats.copy()
    cur = _apply_pass(seats)
    _print(cur)
    while _not_eq(cur, prev):
        prev = cur.copy()
        cur = _apply_pass(cur)
        _print(cur)
    chars = [v for l in cur for v in l]
    occupied_seats = chars.count('#')

    click.echo(f'[part1] {occupied_seats}')

    prev2 = None
    cur2 = seats
    while _not_eq(cur2, prev2):
        prev2 = cur2.copy()
        cur2 = _apply_pass2(cur2)
        _print(cur2)

    chars2 = [v for l in cur2 for v in l]
    occupied_seats2 = chars2.count('#')
    click.echo(f'[part2] {occupied_seats2}')


def _not_eq(a, b):
    if bool(a is None) != bool(b is None):
        return True

    for r in range(len(a)):
        for c in range(len(a[r])):
            if a[r][c] != b[r][c]:
                return True
    return False


def _print(l):
    click.echo('-' * len(l[0]))
    for i in l:
        click.echo(''.join(i))
    click.echo('-' * len(l[0]))
    click.echo()


def _deep_copy(a):
    b = [[i for i in l] for l in a]
    return b


def _apply_pass(cur_seats):
    new_seats = _deep_copy(cur_seats)
    for r in range(len(cur_seats)):
        l = cur_seats[r]
        for c, v in enumerate(l):
            new_seats[r][c] = _apply_rule(r, c, v, cur_seats)
    return new_seats


def _apply_pass2(cur_seats):
    new_seats = _deep_copy(cur_seats)
    for r in range(len(cur_seats)):
        l = cur_seats[r]
        for c, v in enumerate(l):
            new_seats[r][c] = _p2_apply_rule(r, c, v, cur_seats)
    return new_seats


def _p2_apply_rule(r, c, v, cur_seats):
    if v == '.':
        return '.'

    directions = [
        (-1, 0),  # left
        (-1, 1),  # upper left
        (0, 1),   # up
        (1, 1),   # upper rigth
        (1, 0),   # right
        (1, -1),  # lower right
        (0, -1),  # down
        (-1, -1)  # lower left
    ]

    adjacent_vals = {'#': 0, 'L': 0, '.': 0}
    for x, y in directions:
        seat_val = _get_seat(r, c, x, y, cur_seats)
        if seat_val is not None:
            adjacent_vals[seat_val] += 1

    if v == 'L' and adjacent_vals['#'] == 0:
        return '#'
    elif v == '#' and adjacent_vals['#'] >= 5:
        return 'L'
    else:
        return v


def _get_seat(r, c, x, y, cur_seats):
    a_r = r + x
    a_c = c + y
    while 0 <= a_r < len(cur_seats) and 0 <= a_c < len(cur_seats[0]):
        seat_val = cur_seats[a_r][a_c]
        if seat_val != '.':
            return seat_val
        a_r += x
        a_c += y
    return None


def _apply_rule(r, c, v, cur_seats):
    if v == '.':
        return '.'

    adjacent_indexes = [
        (r-1, c),    # left
        (r-1, c+1),  # upper left
        (r, c+1),    # up
        (r+1, c+1),  # upper rigth
        (r+1, c),    # right
        (r+1, c-1),  # lower right
        (r, c-1),    # down
        (r-1, c-1)   # lower left
    ]

    adjacent_vals = {'#': 0, 'L': 0, '.': 0}
    for a_r, a_c in adjacent_indexes:
        if 0 <= a_r < len(cur_seats) and 0 <= a_c < len(cur_seats[0]):
            seat_val = cur_seats[a_r][a_c]
            adjacent_vals[seat_val] += 1

    if v == 'L' and adjacent_vals['#'] == 0:
        return '#'
    elif v == '#' and adjacent_vals['#'] >= 4:
        return 'L'
    else:
        return v


if __name__ == '__main__':
    cli()

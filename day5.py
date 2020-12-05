import click
import typing


@click.command()
@click.option('--f', type=click.File(), default='day5.txt')
def cli(f):
    assert _seat_id('FBFBBFFRLR'), 357

    bsps = [l.strip() for l in f.read().splitlines()]
    max_id = 0
    all_seats = [False for _ in range(128*8)]
    for bsp in bsps:
        cur_id, row, col = _seat_id(bsp)
        all_seats[cur_id] = True
        max_id = max(cur_id, max_id)
    click.echo(f'[part1] highest seat id = {max_id}')

    found_first = False
    my_seat_id = None
    for seat_id, occupied in enumerate(all_seats):
        if not found_first:
            if occupied:
                found_first = True
            continue

        if not occupied:
            my_seat_id = seat_id
            break

    click.echo(f'[part2] my seat id = {my_seat_id}')


def _seat_id(bsp: str) -> typing.Tuple[int, int, int]:
    row = int(bsp[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(bsp[7:].replace('L', '0').replace('R', '1'), 2)
    return row * 8 + col, row, col


if __name__ == '__main__':
    cli()

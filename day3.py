import click
import typing

@click.command()
@click.option('--f', type=click.File(), default='day3.txt')
def cli(f):
    lines = [l.strip() for l in f.read().splitlines()]

    tree_count, open_space_count = trees_encountered(lines, 3, 1)

    click.echo(f'[part1] Tree count = {tree_count}')

    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]

    p2_answer = 1
    for h, v in slopes:
        t, _ = trees_encountered(lines, h, v)
        p2_answer *= t

    click.echo(f'[part2] Tree count = {p2_answer}')


def trees_encountered(lines: typing.List[str], h: int, v: int) -> typing.Tuple[int, int]:
    line_len = len(lines[0])
    cur_x = h
    cur_y = v
    tree_count = 0
    open_space_count = 0
    while cur_y < len(lines):
        cur_char = lines[cur_y][cur_x]
        if cur_char == '#':
            tree_count += 1
        elif cur_char == '.':
            open_space_count += 1
        else:
            raise click.ClickException(f'oops, unrecognized char at {cur_x}, {cur_y}: {cur_char}')

        cur_x = (cur_x + h) % line_len
        cur_y += v

    return tree_count, open_space_count


if __name__ == '__main__':
    cli()

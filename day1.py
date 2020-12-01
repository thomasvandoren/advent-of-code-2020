import click
import itertools

@click.command()
@click.option('--f', type=click.File(), default='day1.txt')
def cli(f):
    all_nums_str = f.read()
    all_nums = [int(i) for i in all_nums_str.split('\n')]
    all_combos = itertools.product(all_nums, all_nums)
    with click.progressbar(all_combos, label='part1') as pb:
        for x, y in pb:
            if x + y == 2020:
                click.echo(f'{x} + {y} = 2020')
                click.echo(f'answer is: {x} * {y} = {x * y}')
                break

    click.echo('starting on part 2')
    part_two_combos = itertools.product(all_nums, all_nums, all_nums)
    with click.progressbar(part_two_combos, label='part2') as pb2:
        for x, y, z in pb2:
            if x + y + z == 2020:
                click.echo(f'{x} + {y} + {z} = 2020')
                click.echo(f'answer is: {x} * {y} * {z} = {x * y * z}')
                break


if __name__ == '__main__':
    cli()

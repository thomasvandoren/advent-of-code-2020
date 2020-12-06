import click
import functools
import string


@click.command()
@click.option('--f', type=click.File(), default='day6.txt')
def cli(f):
    groups = [g.strip() for g in f.read().split('\n\n')]
    answer_sets = [set(filter(lambda a: a in string.ascii_lowercase, set(group))) for group in groups]
    sum_uniq_answers = functools.reduce(lambda a, b: a + b, [len(x) for x in answer_sets])
    click.echo(f'[part1] sum of unique answers = {sum_uniq_answers}')

    p2_uniq_sum = 0
    for group in groups:
        person_answers = [set(l.strip()) for l in group.splitlines()]
        uniq_answers_everyone_said = functools.reduce(lambda a, b: a.intersection(b), person_answers)
        p2_uniq_sum += len(uniq_answers_everyone_said)
    click.echo(f'[part2] sum unique consistent answers = {p2_uniq_sum}')


if __name__ == '__main__':
    cli()

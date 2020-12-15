import click


@click.command()
@click.option('--f', type=click.File(), default='day15.txt')
def cli(f):
    initial_turns = [int(i) for i in f.read().split(',')]

    turns = _get_num_said(initial_turns, 2020)
    click.echo(f'[part1] 2020th number said: {turns[-1]}')

    p2_turns = _get_num_said(initial_turns, 30000000)
    click.echo(f'[part2] 30000000th number said: {p2_turns[-1]}')


def _get_num_said(initial_turns, n=2020):
    turns = []
    last_turns = {}
    for i, v in enumerate(initial_turns):
        if i != 0:
            last_turns[turns[-1]] = i
        turns.append(v)
    for turn_num in range(len(turns) + 1, n+1):
        last_num = turns[-1]
        if last_num not in last_turns:
            cur_turn = 0
        else:
            prev_turn = last_turns[last_num]
            cur_turn = turn_num - 1 - prev_turn
        last_turns[last_num] = turn_num - 1
        turns.append(cur_turn)

        if turn_num <= 10 or turn_num % 1000 == 0:
            click.echo(f'[turn {turn_num}] num said: {cur_turn}')
    return turns


if __name__ == '__main__':
    cli()

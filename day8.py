import click
import typing


@click.command()
@click.option('--f', type=click.File(), default='day8.txt')
def cli(f):
    lines = [l.strip() for l in f.read().splitlines()]
    program = [(l[:3], int(l[4:])) for l in lines]

    acc, _, _ = _run_program(program)
    click.echo(f'[part1] last acc val = {acc}')

    # for i in range(len(program) - 1, -1, -1):
    for i in range(len(program)):
        p2_program = program.copy()
        if p2_program[i][0] == 'jmp':
            p2_program[i] = ('nop', p2_program[i][1])
        elif p2_program[i][0] == 'nop':
            p2_program[i] = ('jmp', p2_program[i][1])
        else:
            continue

        p2_acc, lines_run, finished = _run_program(p2_program)
        if finished:
            break

    # 571 is too low
    # 1867 is too high
    click.echo(f'[part2] last acc val = {p2_acc}')


def _run_program(program) -> typing.Tuple[int, list, bool]:
    acc = 0
    cur_inst = 0
    lines_runs = []
    finished = False
    while cur_inst not in lines_runs:
        inst, val = program[cur_inst]
        lines_runs.append(cur_inst)
        if inst == 'nop':
            cur_inst += 1
        elif inst == 'acc':
            acc += val
            cur_inst += 1
        elif inst == 'jmp':
            cur_inst += val

        if cur_inst == len(program):
            finished = True
            break

    return acc, lines_runs, finished


if __name__ == '__main__':
    cli()

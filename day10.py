import click
import itertools


@click.command()
@click.option('--f', type=click.File(), default='day10.txt')
def cli(f):
    nums = [int(l) for l in f.read().splitlines()]
    cur_jolt = 0
    diffs = {}
    # there is always one 3 jolt diff at the very end
    diffs[3] = 1
    sorted_nums = sorted(nums)
    for i, j in enumerate(sorted_nums):
        diff = j - cur_jolt
        if diff not in diffs:
            diffs[diff] = 0
        diffs[diff] += 1
        cur_jolt = j

    p1_answer = diffs[1] * diffs[3]
    click.echo(f'[part1] {p1_answer}')

    p2_nums = [0] + sorted_nums + [sorted_nums[-1] + 3]

    # combos =
    # [1, 2, 3] => 4
    # [1, 2]
    # [2, 3]
    # [1, 3]
    #
    # [1, 2] => 2
    # [1]
    # [2]
    #
    # [1, 2, 3, 4] => 7
    # [1, 2, 3]
    # [2, 3, 4]
    # [1, 2, 4]
    # [1, 3, 4]
    # [1,

    series_counts = {}
    cur_series_len = 0
    for i in range(1, len(p2_nums)):
        if p2_nums[i] - p2_nums[i-1] == 1:
            cur_series_len += 1
        elif cur_series_len >= 1:
            if cur_series_len >= 2:
                if cur_series_len not in series_counts:
                    series_counts[cur_series_len] = 0
                series_counts[cur_series_len] += 1
            cur_series_len = 0

    p2_answer = 2**series_counts[2] * 4**series_counts[3] * 7**series_counts[4] #* 15**series_counts[5]

    # too high: 562949953421312
    #           1125899906842624
    # too low: 156, 182
    click.echo(f'[part2] {p2_answer}')


if __name__ == '__main__':
    cli()

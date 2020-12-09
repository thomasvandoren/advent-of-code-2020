import click


@click.command()
@click.option('--f', type=click.File(), default='day9.txt')
@click.option('--start', default=25)
def cli(f, start):
    nums = [int(l) for l in f.readlines()]

    for i in range(start, len(nums)):
        prev_nums = nums[i-start:i]
        val = nums[i]
        s = set()
        found_a_couple = False
        for a in prev_nums:
            b = val - a
            if b in s:
                found_a_couple = True
                break
            s.add(a)

        if not found_a_couple:
            break

    invalid_number = val
    click.echo(f'[part1] first number that does not match XMAS format: {invalid_number}')

    left_l = nums[:i]
    right_l = nums[i+1:]

    p_sum = _partial_sum(invalid_number, left_l)
    if p_sum is None:
        p_sum = _partial_sum(invalid_number, right_l)
    l = min(p_sum)
    r = max(p_sum)
    p2_answer = l + r

    click.echo(f'[part2] min-max partial  array sum: {p2_answer}')


def _partial_sum(invalid_number, left_l):
    for i in range(len(left_l) - 1):
        for j in range(i + 2, len(left_l)):
            p_list = left_l[i:j]
            partial_sum = sum(p_list)
            if partial_sum == invalid_number:
                return p_list
    return None


if __name__ == '__main__':
    cli()

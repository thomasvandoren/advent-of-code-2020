import click
import re


@click.command()
@click.option('--f', type=click.File(), default='day16.txt')
def cli(f):
    sections = f.read().split('\n\n')
    constraints = [_parse_constraint(l.strip()) for l in sections[0].splitlines()]
    valid_tix_nums = set()
    for c in constraints:
        valid_tix_nums.update(set(range(c['low1'], c['hi1'] + 1)))
        valid_tix_nums.update(set(range(c['low2'], c['hi2'] + 1)))

    my_ticket = [int(n) for n in sections[1].splitlines()[1].split(',')]
    nearby_tickets = [[int(n) for n in l.strip().split(',')] for l in sections[2].splitlines()[1:]]

    ticket_scan_error_rate = 0
    for t in nearby_tickets:
        for n in t:
            if n not in valid_tix_nums:
                ticket_scan_error_rate += n

    click.echo(f'[part1] ticket scan error rate = {ticket_scan_error_rate}')

    valid_tix = []
    if (set(my_ticket)).issubset(valid_tix_nums):
        valid_tix.append(my_ticket)
    for t in nearby_tickets:
        this_t = set(t)
        if this_t.issubset(valid_tix_nums):
            valid_tix.append(t)

    valid_contraints = {}
    for t in valid_tix:
        for i, v in enumerate(t):
            if i not in valid_contraints:
                valid_contraints[i] = [c for c in constraints]
            constraints_to_test = valid_contraints[i]
            if len(constraints_to_test) == 1:
                continue
            valid_contraints_for_this_idx = []
            for c in constraints_to_test:
                if c['low1'] <= v <= c['hi1'] or c['low2'] <= v <= c['hi2']:
                    valid_contraints_for_this_idx.append(c)
            valid_contraints[i] = valid_contraints_for_this_idx

    rules = [None] * len(list(valid_contraints.keys()))
    sorted_constraints = sorted([(i, constraint_list) for i, constraint_list in valid_contraints.items()], key=lambda x: len(x[1]))
    seen_rules = set()
    for i, constraint_list in sorted_constraints:
        for c in constraint_list:
            name = c['name']
            if name not in seen_rules:
                rules[i] = c
                seen_rules.add(name)
                break

    val_count = 0
    p2_answer = 1
    for i, c in enumerate(rules):
        v = my_ticket[i]
        if c['name'].startswith('departure'):
            val_count += 1
            p2_answer *= v
            if val_count == 6:
                break

    click.echo(f'[part2] {p2_answer}')


pattern = re.compile('(?P<name>[^:]+): (?P<low1>\d+)-(?P<hi1>\d+) or (?P<low2>\d+)-(?P<hi2>\d+)')
def _parse_constraint(s):
    match = pattern.match(s)
    if match is None:
        raise click.ClickException(f'Unrecognized constraint: {s}')

    res = match.groupdict()
    for k in ('low1', 'hi1', 'low2', 'hi2'):
        res[k] = int(res[k])
    return res


if __name__ == '__main__':
    cli()

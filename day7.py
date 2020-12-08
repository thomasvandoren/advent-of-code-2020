import click
import re


@click.command()
@click.option('--f', type=click.File(), default='day7.txt')
def cli(f):
    lines = [l.strip() for l in f.read().splitlines()]
    bags_contained_by = {}
    contains = {}
    empty_bags = set()

    pattern = re.compile('^(?P<bag>[\w\s]+) contain (?P<insides>[^.]+)\.$')
    shiny_gold = []

    for l in lines:
        match = pattern.match(l)
        bag = match.group('bag')
        if bag.endswith('s'):
            bag = bag[:-1]

        insides_group = match.group('insides')
        insides = [b.strip() for b in insides_group.split(',')]

        for i in insides:
            if i == 'no other bags':
                empty_bags.add(bag)
                continue

            parts = i.split(' ', 1)
            count_str, inner_bag = parts[0], parts[1].strip()

            if inner_bag.endswith('s'):
                inner_bag = inner_bag[:-1]

            if inner_bag not in bags_contained_by:
                bags_contained_by[inner_bag] = set()

            count = int(count_str)
            bags_contained_by[inner_bag].add(bag)

            if bag not in contains:
                contains[bag] = {}

            contained_in = contains[bag]
            if inner_bag not in contained_in:
                contained_in[inner_bag] = 0
            contained_in[inner_bag] += count

    containers = set()
    start_bag = 'shiny gold bag'

    def _recurse(cur_bag: str):
        if cur_bag not in bags_contained_by:
            return

        cur_containers = bags_contained_by[cur_bag]
        unseen_containers = cur_containers.difference(containers)
        if len(unseen_containers) == 0:
            return

        containers.update(unseen_containers)
        for c in unseen_containers:
            _recurse(c)

    _recurse(start_bag)
    click.echo(f'[part1] container bags: {len(containers)}')

    def _bags_in(cur_bag: str) -> int:
        if cur_bag not in contains and cur_bag in empty_bags:
            return 1

        inner_bags = contains[cur_bag]
        this_count = 0
        for bag, count in inner_bags.items():
            inner_bag_cnt = _bags_in(bag)
            this_count += count * inner_bag_cnt

        return this_count + 1

    # 172287 is too low
    in_shiny_bag = _bags_in(start_bag) - 1
    click.echo(f'[part2] inside bags: {in_shiny_bag}')


if __name__ == '__main__':
    cli()

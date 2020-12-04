import click
import re


@click.command()
@click.option('--f', type=click.File(), default='day4.txt')
def cli(f):
    passports = [p.strip() for p in f.read().split('\n\n')]

    pattern = re.compile('(?P<key>[a-z]{3}):(?P<val>[^ \n]+)', re.MULTILINE)

    valid_count = 0
    p2_valid_count = 0
    for passport in passports:
        match = pattern.findall(passport)
        d = dict(match)
        if _is_valid(d):
            valid_count += 1
        if _is_valid_p2(d):
            p2_valid_count += 1
    click.echo(f'[part1] valid passport count = {valid_count}')
    click.echo(f'[part2] valid passport count = {p2_valid_count}')


REQ_KEYS_NO_CID = {
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # 'cid',
}

COLOR_PATTERN = re.compile('^#[a-f0-9]{6}$')
PID_PATTERN = re.compile('^[0-9]{9}$')


def _is_valid(d: dict) -> bool:
    actual_keys = set(d.keys())
    return actual_keys.issuperset(REQ_KEYS_NO_CID)


def _is_valid_p2(d: dict) -> bool:
    if not _is_valid(d):
        return False

    byr = int(d['byr'])
    if byr < 1920 or byr > 2020:
        return False

    iyr = int(d['iyr'])
    if iyr < 2010 or iyr > 2020:
        return False

    eyr = int(d['eyr'])
    if eyr < 2020 or eyr > 2030:
        return False

    hgt = d['hgt']
    if not (hgt[-2:] == 'cm' or hgt[-2:] == 'in'):
        return False
    elif not _is_int(hgt[:-2]):
        return False
    elif not ((hgt[-2:] == 'cm' and 150 <= int(hgt[:-2]) <= 193) or (hgt[-2:] == 'in' and 59 <= int(hgt[:-2]) <= 76)):
        return False

    if not COLOR_PATTERN.match(d['hcl']):
        return False

    if d['ecl'] not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
        return False

    if not PID_PATTERN.match(d['pid']):
        return False

    return True


def _is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    cli()

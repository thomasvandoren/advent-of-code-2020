import click
import re

@click.command()
@click.option('--f', type=click.File(), default='day2.txt')
def cli(f):
    pass_lines = f.read().split('\n')
    part1_compliant = []
    part2_compliant = []
    pattern = re.compile('(?P<min_letter>[0-9]+)-(?P<max_letter>[0-9]+) (?P<letter>[a-z]+): (?P<password>[a-z]+)')
    for pl in pass_lines:
        match = pattern.match(pl)
        if not match:
            raise click.ClickException(f'oops, invalid regex for: "{pl}"')

        min_letter = int(match.group('min_letter'))
        max_letter = int(match.group('max_letter'))
        letter = match.group('letter')
        password = match.group('password')

        if _is_valid_password_part1(password, letter, min_letter, max_letter):
            part1_compliant.append(pl)
        if _is_valid_password_part2(password, letter, min_letter, max_letter):
            part2_compliant.append(pl)

    click.echo(f'[part1] Compliant passwords: {len(part1_compliant)} Total lines: {len(pass_lines)}')
    click.echo(f'[part2] Compliant passwords: {len(part2_compliant)} Total lines: {len(pass_lines)}')



def _is_valid_password_part1(password: str, letter: str, min_letter: int, max_letter: int) -> bool:
    letter_count = password.count(letter)
    return min_letter <= letter_count <= max_letter


def _is_valid_password_part2(password: str, letter: str, min_letter: int, max_letter: int) -> bool:
    a = password[min_letter - 1]
    b = password[max_letter - 1]

    return bool(a == letter) != bool(b == letter)


if __name__ == '__main__':
    cli()

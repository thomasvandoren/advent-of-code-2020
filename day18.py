import click


@click.command()
@click.option('--f', type=click.File(), default='day18.txt')
def cli(f):
    lines = f.read().splitlines()
    sum = 0
    for line in lines:
        result = _eval(line)
        sum += result

    # too low: 236610664
    click.echo(f'[part1] sum of lines = {sum}')

    sum2 = 0
    for line in lines:
        result = _p2_eval(line)
        sum2 += result

    # too low: 4733019722379
    # ex2: 693,942
    click.echo(f'[part2] sum of lines = {sum2}')


def _p2_eval(line: str) -> int:
    chars = [c for c in line if c != ' ']
    result = _p2_calc(chars)
    return result


def _p2_calc(chars):
    last_val = None
    last_op = None
    i = 0
    while i < len(chars):
        c = chars[i]
        if c == '(':
            recurses = 0
            for j in range(i+1, len(chars)):
                if chars[j] == '(':
                    recurses += 1
                elif chars[j] == ')' and recurses == 0:
                    break
                elif chars[j] == ')':
                    recurses -= 1

                if recurses < 0:
                    raise click.ClickException(f'unmatched paren in this expr: {"".join(chars)} (start paren at index {i})')

            sub_expr = chars[i+1:j]
            val = _p2_calc(sub_expr)
            if last_val is None:
                last_val = val
            elif last_op == '*':
                last_val *= val
            elif last_op == '+':
                last_val += val
            last_op = None
            i = j+1
        elif c == '+':
            last_op = c
            i += 1
        elif c == '*':
            # 1 + 2 * (3 + 4) * 3
            # 1 * (2) + 3
            # 1 * (2 * (3))
            end_index = 0
            recurses = 0
            for j in range(i + 1, len(chars)):
                if chars[j] in ('*', ')') and recurses == 0:
                    end_index = j
                    break
                if chars[j] == '(':
                    recurses += 1
                if chars[j] == ')':
                    recurses -= 1

                if recurses < 0:
                    raise click.ClickException(f'unparseable multiplication: {"".join(chars)} (at index: {i}')
            else:
                end_index = len(chars)
            sub_expr = chars[i + 1:end_index]
            val = _p2_calc(sub_expr)
            last_val *= val
            i = end_index
            last_op = None
        elif last_val is None:
            last_val = int(c)
            i += 1
        elif last_op == '*':
            last_val *= int(c)
            last_op = None
            i += 1
        elif last_op == '+':
            last_val += int(c)
            last_op = None
            i += 1
        else:
            raise click.ClickException(f'unknown op: {c}')

    return last_val


def _eval(line: str) -> int:
    chars = [c for c in line if c != ' ']
    result = _calc(chars)
    return result


def _calc(chars):
    last_val = None
    last_op = None
    i = 0
    while i < len(chars):
        c = chars[i]
        if c == '(':
            close_paren = 0
            recurses = 0
            for j in range(i+1, len(chars)):
                if chars[j] == '(':
                    recurses += 1
                elif chars[j] == ')' and recurses == 0:
                    close_paren = j
                    break
                elif chars[j] == ')':
                    recurses -= 1

                if recurses < 0:
                    raise click.ClickException(f'unmatched paren in this expr: {"".join(chars)} (start paren at index {i})')

            sub_expr = chars[i+1:j]
            val = _calc(sub_expr)
            if last_val is None:
                last_val = val
            elif last_op == '*':
                last_val *= val
            elif last_op == '+':
                last_val += val
            last_op = None
            i = j+1
        elif c in ('*', '+'):
            last_op = c
            i += 1
        elif last_val is None:
            last_val = int(c)
            i += 1
        elif last_op == '*':
            last_val *= int(c)
            last_op = None
            i += 1
        elif last_op == '+':
            last_val += int(c)
            last_op = None
            i += 1
        else:
            raise click.ClickException(f'unknown op: {c}')
    return last_val


if __name__ == '__main__':
    cli()

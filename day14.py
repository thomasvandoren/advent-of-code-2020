import click


@click.command()
@click.option('--f', type=click.File(), default='day14.txt')
def cli(f):
    program = [l.strip().split(' = ', 1) for l in f.read().splitlines()]

    mask = {}
    memory = {}

    for inst in program:
        left, right = inst[0].strip(), inst[1].strip()

        if left == 'mask':
            mask = {}
            for i, v in enumerate(right):
                if v != 'X':
                    mask[i] = v
        else:
            mem_location = int(left[4:-1])
            value = int(right)
            bin_val = _get_bin_str(value)
            bin_val_with_mask = list(bin_val)
            for k, v in mask.items():
                bin_val_with_mask[k] = v
            str_with_mask = ''.join(bin_val_with_mask)
            memory[mem_location] = int(str_with_mask, 2)

    p1_answer = sum(memory.values())
    click.echo(f'[part1] {p1_answer}')

    p2_mask = {}
    p2_mem = {}

    for inst in program:
        left, right = inst[0].strip(), inst[1].strip()
        if left == 'mask':
            p2_mask = {}
            for i, v in enumerate(right):
                if v != '0':
                    if v not in p2_mask:
                        p2_mask[v] = []
                    p2_mask[v].append(i)
        else:
            mem_location = int(left[4:-1])
            value = int(right)

            bin_mem_loc = _get_bin_str(mem_location)
            masked_mem_loc = list(bin_mem_loc)
            if '1' in p2_mask:
                for i in p2_mask['1']:
                    masked_mem_loc[i] = '1'

            mem_locs = []
            if 'X' in p2_mask:
                x_masks = p2_mask['X']
                masked_mem_loc = ''.join(masked_mem_loc)
                l_x_masks = len(x_masks)
                bins = [_get_bin_str(i, l_x_masks) for i in range(2 ** l_x_masks)]
                for b in bins:
                    mem_loc = list(masked_mem_loc)
                    bb = list(b)
                    for i in range(len(x_masks)):
                        mem_loc[x_masks[i]] = bb[i]
                    mem_locs.append(''.join(mem_loc))

            for loc in mem_locs:
                mem_loc_int = int(loc, 2)
                p2_mem[mem_loc_int] = value

    p2_answer = sum(p2_mem.values())
    click.echo(f'[part2] {p2_answer}')


def _get_bin_str(i, l=36):
    b_s = bin(i)[2:]
    return '0' * (l-len(b_s)) + b_s


if __name__ == '__main__':
    cli()

import argparse
import collections
import dataclasses
import enum

import logging
from os import linesep
from pprint import pp
import re
import string
import sys
import textwrap
from typing import Union


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

from adlib.runnerz import get_input, get_demo
INPUT = get_input(__file__)
DEMO_INPUT, DEMO_OUTPUTS = get_demo(__file__)

def visibility(trees: list[list[int]]) -> list[list[bool]]:

    vis_grid = []
    debug_grid = []

    for row_i, row in enumerate(trees):
        vis_grid.append([])
        debug_grid.append([])
        for col_i, tree in enumerate(row):
            vis_grid[-1].append(None)
            logger.debug(f"it's me, the tree at {row_i}, {col_i}! {tree}")
            sightlines = (
                row[:col_i], [trees[r][col_i] for r in range(row_i)],
                row[col_i + 1:], [trees[r][col_i] for r in range(row_i + 1, len(trees) )]

            )
            vis_grid[row_i][col_i] = any(all(tree > o for o in line) for line in sightlines)
            debug_grid[row_i].append(str(vis_grid[row_i][col_i])[0] + str(tree))

    #logger.debug('\n'.join(' '.join(cell for cell in row) for row in debug_grid)
    import pdb
    pdb.set_trace()
    return sum(int(vis) for vis in sum(vis_grid, []))

def part_1(input_data: str) -> int:
    trees = [[int(tree) for tree in row.strip()] for row in input_data.splitlines() if row.strip()]
    #pp(trees)

    return (visibility(trees))

def run() -> None:
    parser =argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parsed = parser.parse_args()
    if parsed.test:
        part1_res = part_1(DEMO_INPUT)
        assert part1_res == DEMO_OUTPUTS[0], f'got {part1_res}, expected {DEMO_OUTPUTS[0]}'
    else:

        print(f'input is\n{INPUT}')
        input_data = INPUT

        part1_res = part_1(input_data)

    print(f'Part 1: {part1_res} 81813 is too low')
#    print(f'Part 2: {part2_res}')

    if parsed.test:
        assert part1_res == DEMO_OUTPUTS[0], f'part 1: expected {DEMO_OUTPUTS[0]}, got {part1_res}'
#        assert part2_res == DEMO_OUTPUTS[1], f'part 2: expected {DEMO_OUTPUTS[1]}, got {part2_res}'
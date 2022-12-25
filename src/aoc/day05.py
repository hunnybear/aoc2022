import argparse
import enum

import logging
import string
import sys


logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

logger = logging.getLogger()

from adlib.runnerz import get_input, get_demo
INPUT = get_input(__file__)
DEMO_INPUT, DEMO_OUTPUTS = get_demo(__file__)


def part_1(assignments) -> int:


def part_2(assignments):
    NotImplemented



def run() -> None:
    parser =argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parsed = parser.parse_args()


        input_data = DEMO_INPUT
    else:
        input_data = INPUT



    part1_res = part_1(input_data)
    #if not parsed.test:
    #    validate_part_1(part1_res)

    part2_res = part_2(input_data)
#    if not parsed.test:
#        validate_part_2(part2_res)

    print(f'Part 1: {part1_res}')
    print(f'Part 2: {part2_res}')

    if parsed.test:
        assert part1_res == DEMO_OUTPUTS[0], f'part 1: expected {DEMO_OUTPUTS[0]}, got {part1_res}'
#        assert part2_res == DEMO_OUTPUTS[1], f'part 2: expected {DEMO_OUTPUTS[1]}, got {part2_res}'
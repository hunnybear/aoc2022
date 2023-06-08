import argparse
import collections
import dataclasses
import enum

import logging
import re
import string
import sys
from typing import Union


logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

from adlib.runnerz import get_input, get_demo
INPUT = get_input(__file__)
DEMO_INPUT, DEMO_OUTPUTS = get_demo(__file__)


def part_1(input_data: str) -> int:
    return next(i for i in range(4, len(input_data) + 1) if len(set(input_data[i-4:i])) == 4)



def run() -> None:
    parser =argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parsed = parser.parse_args()
    if parsed.test:
        part1_res = [part_1(line.strip()) for line in DEMO_INPUT.splitlines()]
        assert part1_res == DEMO_OUTPUTS[0], f'got {part1_res}, expected {DEMO_OUTPUTS[0]}'
    else:
        input_data = INPUT

        part1_res = part_1(input_data)

    print(f'Part 1: {part1_res}')
#    print(f'Part 2: {part2_res}')

    if parsed.test:
        assert part1_res == DEMO_OUTPUTS[0], f'part 1: expected {DEMO_OUTPUTS[0]}, got {part1_res}'
#        assert part2_res == DEMO_OUTPUTS[1], f'part 2: expected {DEMO_OUTPUTS[1]}, got {part2_res}'
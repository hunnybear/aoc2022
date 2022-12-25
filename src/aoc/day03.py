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


def score_char(char: str) -> int:
    return string.ascii_letters.index(char) + 1

def validate_part_1(value) -> bool:

    """
    Use known results to validate results
    """

    if value != 8109:
        raise ValueError(f'{value} does not match known correct value of 8109')


def _split_ruck(in_string):
    return set(in_string[:int(len(in_string)/2)]), set(in_string[int(len(in_string)/2):])

def part_1(inval):
    to_score = []
    for ruck_a, ruck_b in [_split_ruck(line) for line in inval.strip().splitlines()]:
        common_items = ruck_a & ruck_b
        if len(common_items) != 1:
            # Lessons in ominous unhelpfulness
            raise ValueError('you know what you did')
        to_score.extend(common_items)

    char_scores = [(char, score_char(char)) for char in to_score]
    logging.debug(char_scores)
    return sum([score for _chr, score in char_scores])


def part_2(inval: str) -> None:

    groups = []

    group = []

    score = 0

    for line in [_line.strip() for _line in inval.splitlines()]:
        if not line:
            continue

        group.append(set(line))

        if len(group) == 3:

            groups.append(group)
            common_char = group[0] & group [1] & group[2]
            assert len(common_char) == 1

            score += score_char(common_char.pop())
            group = []

    return score



def run() -> None:
    parser =argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parsed = parser.parse_args()
    if parsed.test:
        input_data = DEMO_INPUT
    else:
        input_data = INPUT

    part1_res = part_1(input_data )
    if not parsed.test:
        validate_part_1(part1_res)

    part2_res = part_2(input_data)
#    if not parsed.test:
#        validate_part_2(part2_res)

    print(f'Part 1: {part1_res}')
    print(f'Part 2: {part2_res}')

    if parsed.test:
        assert part1_res == DEMO_OUTPUTS[0], f'part 1: expected {DEMO_OUTPUTS[0]}, got {part1_res}'
        assert part2_res == DEMO_OUTPUTS[1], f'part 2: expected {DEMO_OUTPUTS[1]}, got {part2_res}'
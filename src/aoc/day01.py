# aoc_01.py
# code for day one of advent of code 2022

import re

from adlib.runnerz import get_input, get_demo
INPUT = get_input(__file__)
DEMO_INPUT, DEMO_OUTPUTS = get_demo(__file__)


def _get_sections(input_data: str) -> list:

    sections = [s.split('\n') for s in re.split('\n\n', input_data) if s.strip()]

    return [sum(int(i) for i in sec if i.strip()) for sec in sections]

def part_1(input_data: str) -> None:
    sections = _get_sections(input_data)
    return max(sections)
    import pdb
    pdb.set_trace()
    print('sections')
    print(sections)

def part_2(input_data: str) -> None:
    sections = _get_sections(input_data)
    return sum(sorted(sections, reverse=True)[:3])

def run() -> None:

    demo_1_res = part_1(DEMO_INPUT)
    if demo_1_res != DEMO_OUTPUTS[0]:
        raise ValueError(f'expected {DEMO_OUTPUTS[0]}, got {demo_1_res}')

    part_1_res = part_1(INPUT)
    print(f'Part 1:{part_1_res}')

    demo_2_res = part_2(DEMO_INPUT)
    if demo_2_res != DEMO_OUTPUTS[1]:
        raise ValueError(f'expected {DEMO_OUTPUTS[1]}, got {demo_2_res}')

    part_2_res = part_2(INPUT)
    print(f'Part 2:{part_2_res}')
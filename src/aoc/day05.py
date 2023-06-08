import argparse
import collections
import dataclasses
import enum

import logging
import re
import string
import sys


logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

from adlib.runnerz import get_input, get_demo
INPUT = get_input(__file__)
DEMO_INPUT, DEMO_OUTPUTS = get_demo(__file__)


@dataclasses.dataclass
class Instruction:
    count: int
    source: str
    dest: str

    @classmethod
    def from_input(cls, input_line: str) -> 'Instruction':
        match = re.match(r'move\s*(\d+)\s*from\s*(\d+)\s*to\s*(\d+)\s*', input_line)
        assert match

        count, source, dest = match.groups()

        return cls(count=int(count), source=source, dest=dest)

    def __str__(self):
        return f'<Instruction: Move {self.count} crates from {self.source} to {self.dest}'


class Stack(list):

    def __init__(self, name, *args, **kwargs) -> None:
        self.name = name
        super().__init__(*args, **kwargs)

    def add(self, crate):
        self.append(crate)

    def move(self):
        return self.pop(-1)


class Crate(str):
    EMPTY = '   '

    def __new__(cls, inval):
        inval = inval.strip()
        if not inval.startswith('[') and inval.endswith(']'):
            raise ValueError(fr'Invalid crate {inval}! Correct format for crate is `[<a-z>]`')
        return super().__new__(cls, inval[1:-1].strip())

    def __str__(self):
        return f'[{super().__str__()}]'

    @property
    def contents(self):
        return super().__str__()


class Depot(dict):

    def CrateMover9000(self, instruction: Instruction) -> None:
        logger.debug(instruction)
        for crate_i in range(instruction.count):
            self[instruction.dest].append(self[instruction.source].pop(-1))

    def CrateMover9001(self, instruction: Instruction) -> None:
        logger.debug(instruction)
        self[instruction.dest].extend(self[instruction.source][-instruction.count:])
        self[instruction.source] = self[instruction.source][:-instruction.count]

    def render(self) -> str:

        rows = max([len(stack) for stack in self.values()])
        for row in reversed(range(rows)):

            line = ' '.join([
                f'{stack[row]}' if len(stack) > row else Crate.EMPTY
                for stack in self.values()])

            yield line

    def draw(self) -> None:

        print('\n'.join(self.render()))

    def __str__(self) -> str:

        return '\n'.join(self.render())

    @classmethod
    def parse(cls, drawing: str) -> 'Depot':
        stacks = {}
        lines = [line for line in drawing.splitlines() if line.strip()]
        names = lines.pop(-1).split()
        # make sure we get insertion order

        for name in names:
            stacks[name] = Stack(name)

        for row_num, line in enumerate(reversed(lines)):



            for stack_idx, crate in enumerate(
                    [Crate(line[n*4:n*4+3].strip()) or None for n in range(len(names))]):
                if crate is None:
                    continue
                stack = stacks[names[stack_idx]]
                assert len(stack) == row_num

                stack.append(crate)


        return cls(stacks)


def part_1(drawing, instructions) -> str:
    depot = Depot.parse(drawing)

    for instruction in instructions:
        depot.CrateMover9000(instruction)
        logger.debug(f'Part1 {instruction}:\n{depot}')


    return ''.join(stack[-1].contents for stack in depot.values())

def part_2(drawing, instructions):
    depot = Depot.parse(drawing)
    for instruction in instructions:
        depot.CrateMover9001(instruction)
        logger.debug(f'Part1 {instruction}:\n{depot}')

    return ''.join(stack[-1].contents for stack in depot.values())



def run() -> None:
    parser =argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parsed = parser.parse_args()

    if parsed.test:
        input_data = DEMO_INPUT
    else:
        input_data = INPUT
    drawing, instructions = (item for item in input_data.split('\n\n'))

    instructions = [Instruction.from_input(line.strip()) for line in instructions.splitlines()]

    part1_res = part_1(drawing, instructions)
    #if not parsed.test:
    #    validate_part_1(part1_res)

    part2_res = part_2(drawing, instructions)
#    if not parsed.test:
#        validate_part_2(part2_res)

    print(f'Part 1: {part1_res}')
    print(f'Part 2: {part2_res}')

    if parsed.test:
        assert part1_res == DEMO_OUTPUTS[0], f'part 1: expected {DEMO_OUTPUTS[0]}, got {part1_res}'
#        assert part2_res == DEMO_OUTPUTS[1], f'part 2: expected {DEMO_OUTPUTS[1]}, got {part2_res}'
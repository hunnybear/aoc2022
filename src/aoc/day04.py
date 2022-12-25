import argparse
import enum

import logging
import string
import sys

from adlib.runnerz import get_input, get_demo
INPUT = get_input(__file__)
DEMO_INPUT, DEMO_OUTPUTS = get_demo(__file__)

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

logger = logging.getLogger()


class Assignment(tuple):

    def __new__(cls, start, end):
        start = int(start)
        end = int(end)
        return super().__new__(Assignment, (start, end))

    @property
    def start(self):
        return self[0]

    @property
    def end(self):
        return self[1]

    def __or__(self, other):

        a, b = sorted([self, other], key=lambda asgn: tuple(asgn))
        if not a & b:
            return False
        return Assignment(a.start, b.end)

    def __and__(self, other):
        a, b = sorted([self,other], key=lambda asgn: tuple(asgn))
        if a.end < b.start:
            return None
        return Assignment(b.start, a.end)

    def __gt__(self, other):
        """
        Return whether this Assignment fully contains some other assignment
        """

        if self == other:
            return False
        return self.__ge__(other)

    def __ge__(self, other):
        return other.start >= self.start and other.end <= self.end

    def __lt__(self, other):
        """
        Return whether this Assignment is fully contained within some other assignment,
        but is not equal
        """

        if self == other:
            return False
        return self.__le__(other)

    def __le__(self, other):

        if other.start <= self.start and other.end >= self.end:
            return True
        return False

    def __or__(self, other):
        """
        Return the intersetion of two Assignments
        """

        a, b = sorted(self, other, key=lambda asgn: tuple(asgn))

        if a.end < b.start:
            return None

        start = max(self.start, other.start)
        end = min(self.end, other.end)

        return Assignment(start, end)

def part_1(assignments) -> int:
    logger.debug('  ==  ,  >   ,  >=  , <    , <=')
    for assignment_a, assignment_b in assignments:
        logger.debug((assignment_a, assignment_b))
        logger.debug((
            assignment_a == assignment_b,
            assignment_a > assignment_b,
            assignment_a >= assignment_b,
            assignment_a < assignment_b,
            assignment_a <= assignment_b))

    return len([True for ass1, ass2 in assignments if (ass1 <= ass2) or (ass1 >= ass2)])

def part_2(assignments):
    return len([True for a1, a2 in assignments if (a1 & a2)])



def run() -> None:
    parser =argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parsed = parser.parse_args()
    if parsed.test:

        assert Assignment(1,5) >= Assignment(2,4)
        assert Assignment(1,5) > Assignment(2,4)
        assert not Assignment(1,5) > Assignment(1,5)
        assert not Assignment(2,4) > Assignment(1,5)

        assert Assignment(2,4) <= Assignment(1,5)
        assert Assignment(2,4) < Assignment(1,5)
        assert not Assignment(1,5) < Assignment(1,5)
        assert not Assignment(1,5) < Assignment(2,4)

        assert Assignment(1,4) & Assignment(4, 10)
        assert Assignment(1,10) & Assignment(5,15)
        assert Assignment(1,10) & Assignment(5,6)
        assert Assignment(1,10) & Assignment(6,6)
        assert Assignment(6,6) & Assignment(1,10)

        assert not Assignment(1,4) & Assignment(5,10)
        assert not Assignment(5,10) & Assignment(1,4)

        input_data = DEMO_INPUT
    else:
        input_data = INPUT

    assignments = []
    for line in input_data.splitlines():
        assignment_a, assignment_b = (Assignment(*asgn.split('-')) for asgn in line.split(','))
        assignments.append((assignment_a, assignment_b))

    part1_res = part_1(assignments )
    #if not parsed.test:
    #    validate_part_1(part1_res)

    part2_res = part_2(assignments)
#    if not parsed.test:
#        validate_part_2(part2_res)

    if part2_res >= 952:
        raise ValueError(f'Part 2 answer is {part_2_res}, which is too high! must be less than 952')

    print(f'Part 1: {part1_res}')
    print(f'Part 2: {part2_res}')

    if parsed.test:
        assert part1_res == DEMO_OUTPUTS[0], f'part 1: expected {DEMO_OUTPUTS[0]}, got {part1_res}'
#        assert part2_res == DEMO_OUTPUTS[1], f'part 2: expected {DEMO_OUTPUTS[1]}, got {part2_res}'
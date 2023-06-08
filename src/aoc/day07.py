import argparse
import collections
import dataclasses
import enum

import logging
from os import linesep
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


def part_1(input_data: str) -> int:
    tree = Tree.parse_cli(input_data)
    for itm in tree.walk():
        print(itm)
    print(tree)

    size = 0

    for files, directories in tree.walk():
        for directory in directories:
            if directory.size <= 100000:
                print(directory.tree())
                size += directory.size
    return size


WalkRes = collections.namedtuple('WalkRes', ['files', 'directories'])

PROMPT = '$ '

@dataclasses.dataclass
class File:
    name: str
    size: int
    parent: 'Dir'

    def __str__(self) -> str:
        return f'(File {self.name} ({self.size}))'

    def __repr__(self) -> str:
        return str(self)

    @property
    def is_dir(self):
        return False
    @property
    def is_file(self):
        return True

    @property
    def full_name(self):
        return f'{self.parent.full_name}/{self.name}'

    def tree(self) -> str:
        return str(self)

@dataclasses.dataclass
class Dir:
    name: str
    contents: list[Union['File', 'Dir']] = None
    parent: 'Dir' = None

    def __str__(self) -> str:
        return f'Dir({self.full_name} size={self.size})'

    def __repr__(self) -> str:
        return str(self)

    def __post_init__(self):
        if self.contents is None:
            self.contents = []
        if self.parent is None:
            assert self.name == '/'

    def tree(self) -> str:
        return f"{self}:{linesep}{textwrap.indent(linesep.join([child.tree() for child in self]), '  ')}"

    @property
    def size(self) -> int:
        return sum([item.size for item in self])

    @property
    def full_name(self) -> str:
        if self.parent is None:
            return self.name
        parent_name = self.parent.full_name
        if parent_name == '/':
            parent_name = ''
        return f'{parent_name}/{self.name}'

    @property
    def is_dir(self):
        return True
    @property
    def is_file(self):
        return False

    def walk(self):
        to_walk = [self]
        while to_walk:
            here = to_walk.pop(0)
            to_walk.extend([d for d in here if d.is_dir])
            yield WalkRes([f for f in here if f.is_file], [d for d in here if d.is_dir])

    def __iter__(self):
        for item in self.contents:
            yield item

class Tree:

    def __init__(self, root: Dir):
        self.root = root

    def __str__(self):

        start, end1, end2 = super().__str__().rsplit(maxsplit=2)
        end = f'{end1} {end2}'

        return f'{start}\n{self.root.tree()}\n{end}'

    def walk(self):
        return self.root.walk()

    @classmethod
    def parse_cli(cls, cli: str) -> 'Tree':
        current_dir = None
        parent_dir = None
        dirs = {}
        lines = list(cli.splitlines())

        while lines:
            line = lines.pop(0)
            logger.debug(f'PARSING:\n\tcwd: `{current_dir.full_name if current_dir is not None else None}\n\tcmd: `{line}`')
            assert line.startswith(PROMPT)
            prompt_match = re.match(r'\$ ([a-z]+)\s*(.*)$', line)
            if prompt_match is None:
               raise ValueError('invalid prompt')
            cmd, args = prompt_match.groups()
            output = []
            while lines and not lines[0].startswith(PROMPT):

                output.append(lines.pop(0))

            if output:
                nltab = '\n\t'
                logger.debug(f'PARSING: output:\n\t`{nltab.join(output)}`')

            if cmd == 'cd':
                assert not output
                if current_dir is None:
                    assert args == '/' # over engineering much? or args[0] == '.'
                if args == '..':
                    current_dir = parent_dir
                    parent_dir = current_dir.parent
                    continue

                parent_dir = current_dir
                this_dir = Dir(args, parent=current_dir)
                current_dir = dirs.setdefault(this_dir.full_name, this_dir)
            elif cmd == 'ls':
                for info, name in [out.split() for out in output]:
                    if info == 'dir':
                        child = Dir(name, parent=current_dir)
                        child = dirs.setdefault(child.full_name, child)
                    else:
                        child = File(name, int(info), parent=current_dir)
                    current_dir.contents.append(child)
            else:
                raise ValueError("unrecognized command!")

            print(f'\ncommand {cmd} {args}\n\n{output}\n\n\n')

        return cls(dirs['/'])


def run() -> None:
    parser =argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parsed = parser.parse_args()
    if parsed.test:
        part1_res = part_1(DEMO_INPUT)
        assert part1_res == DEMO_OUTPUTS[0], f'got {part1_res}, expected {DEMO_OUTPUTS[0]}'
    else:
        input_data = INPUT

        part1_res = part_1(input_data)

    print(f'Part 1: {part1_res} 81813 is too low')
#    print(f'Part 2: {part2_res}')

    if parsed.test:
        assert part1_res == DEMO_OUTPUTS[0], f'part 1: expected {DEMO_OUTPUTS[0]}, got {part1_res}'
#        assert part2_res == DEMO_OUTPUTS[1], f'part 2: expected {DEMO_OUTPUTS[1]}, got {part2_res}'
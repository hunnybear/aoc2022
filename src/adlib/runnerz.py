from importlib.resources import files
from pathlib import Path
import re

import yaml

def _get_day_from_filename(file_name: str) -> str:

    day_match = re.match(r'day(\d{2}).py', file_name)
    if day_match is None:
        raise ValueError('filename must match the day regex!')
    return day_match.groups()[0]


def get_demo(filename: str, part: int = None) -> tuple:

    filepath = Path(filename)
    day = _get_day_from_filename(filepath.name)

    demo_file = files('aoc.demo_data').joinpath(day).with_suffix('.yml')
    demo_data = yaml.safe_load(demo_file.read_text())

    outputs = demo_data['outputs']
    if part is not None:
        if part > 2:
            raise ValueError('Only two parts (one-indexed) per day')
        elif part < 1:
            raise ValueError(f"invalid part int (was {part}, must be `1` or `2`)")
        outputs = outputs[part -1]
    return (demo_data['input'], outputs)

def get_input(filename):

    filepath = Path(filename)
    day = _get_day_from_filename(filepath.name)

    input_file = files('aoc.input').joinpath(day)

    if not input_file.exists():
        import pdb
        pdb.set_trace()


    return input_file.read_text()
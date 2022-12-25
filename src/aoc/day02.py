import argparse
import enum

import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

logger = logging.getLogger()


from adlib.runnerz import get_input, get_demo
INPUT = get_input(__file__)
DEMO_INPUT, DEMO_OUTPUTS = get_demo(__file__)

class Outcome(enum.IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0

class Instruction(enum.IntEnum):

    ROCK = A = X = 1 # Rock
    PAPER = B = Y = 2 # Paper
    SCISSORS = C = Z = 3 # Scissors

    def __str__(self):
        return self.name

    def __gt__(self, other):
        res = other == list(range(1,4))[(self + 1) % 3]
        logger.debug(f'{self} > {other} = {res}')
        #import pdb
        #pdb.set_trace()
        return res

    def __lt__(self, other):
        res = other == list(range(1,4))[self % 3]
        logger.debug(f'{self} < {other} = {res}')
        #import pdb
        #pdb.set_trace()
        return res


class Part2Outcome(enum.IntEnum):
    I_LOSE = THEY_WIN = A = X = -1
    DRAW = B = Y = 0
    I_WIN = C = THEY_LOSE = Z = 1

    def solve(self, instruction:Instruction) -> Instruction:

        # ok brute force am lazy
        if self is self.DRAW:
            return instruction
        elif self is self.I_LOSE:
            if instruction is Instruction.ROCK:
                return instruction.SCISSORS
            elif instruction is Instruction.PAPER:
                return instruction.ROCK
            elif instruction is Instruction.SCISSORS:
                return instruction.PAPER
            assert False, "This shouldn't happen"
        else:
            if instruction is Instruction.ROCK:
                return Instruction.PAPER
            elif instruction is Instruction.PAPER:
                return Instruction.SCISSORS
            elif instruction is Instruction.SCISSORS:
                return instruction.ROCK
            assert False, "This should not happen"
        assert False, "This should not happen"

def score(parsed):
    my_score = their_score = 0
    round = 1
    for their_play, my_play in parsed:
        logger.debug(f'Round {round}:\nMy score/their score: {my_score}/{their_score}\nMy play/their_play: {my_play}/{their_play}')
        my_score += my_play
        their_score += their_play

        if my_play == their_play:
            logger.debug('tie!')
            my_score += Outcome.DRAW
            their_score += Outcome.DRAW

        elif my_play > their_play:
            logger.debug('I win!')
            my_score += Outcome.WIN
            their_score += Outcome.LOSS

        elif my_play < their_play:
            logger.debug('You win!')
            my_score += Outcome.LOSS
            their_score += Outcome.WIN

        else:
            pass
        round += 1

    return my_score, their_score


def _prep(inval):
    return [tuple(Instruction[play] for play in round.split()) for round in inval.splitlines()]

def _prep_2(inval):
    return [(Instruction[their_play], Part2Outcome[outcome]) for their_play, outcome in [round.split() for round in inval.splitlines()]]

def plan_part_2(parsed):
    return [(their_play, outcome.solve(their_play)) for their_play, outcome in parsed]

def run():

    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parsed = parser.parse_args()

    if parsed.test:
        test()
        return

    # Test
    demo_1_res = score(_prep(DEMO_INPUT))
    prep2 = _prep_2(DEMO_INPUT)
    part_2_plan = plan_part_2(prep2)
    demo_2_res = score(part_2_plan)
    if demo_1_res[0] != DEMO_OUTPUTS[0] or demo_2_res[0] != DEMO_OUTPUTS[1]:
        raise ValueError(f'Test Failed! expected: {DEMO_OUTPUTS[0]}, got: {demo_1_res[0]}')
    else:
        print(f'demo check passed! {demo_1_res}, {demo_2_res}')

    part1 = score(_prep(INPUT))
    if part1[0] != 12586:
        raise RuntimeError('Correct answer for part 1 is 12586')
    print(f'Part 1 score: my score: {part1[0]}, their_score: {part1[1]}')

    prepped_2 = _prep_2(INPUT)
    part2_plays = plan_part_2(prepped_2)
    part2_score = score(part2_plays)
    print(f'Part 2 score: my score (must be less than 14133): {part2_score[0]}, their_score: {part2_score[1]}')


def test() -> None:
    try:
        print('self-identity')
        assert Instruction.ROCK is Instruction.ROCK, "rock is identical to itself"
        assert Instruction.PAPER is Instruction.PAPER, "paper is identical to itself"
        assert Instruction.SCISSORS is Instruction.SCISSORS, "scissors is identical to itself"

        print('greater than')
        assert Instruction.ROCK > Instruction.SCISSORS, "rock beats scissors"
        assert Instruction.SCISSORS > Instruction.PAPER, "scissors beats paper"
        assert Instruction.PAPER > Instruction.ROCK, "Paper beats rock"
        assert not Instruction.PAPER > Instruction.SCISSORS, "Scissors does not lose to paper"
        assert not Instruction.SCISSORS > Instruction.ROCK, "Rock does not lose to scissors"
        assert not Instruction.ROCK > Instruction.PAPER, "Paper does not lose to rock"


        print('less than')
        assert Instruction.ROCK < Instruction.PAPER, "Rock loses to paper"
        assert Instruction.PAPER < Instruction.SCISSORS, "Paper loses to Scissors"
        assert Instruction.SCISSORS < Instruction.ROCK, "Scissors loses to rock"

        assert not Instruction.PAPER < Instruction.ROCK, "Paper does not lose to rock"
        assert not Instruction.ROCK < Instruction.SCISSORS, "Rock does not lose to scissors"
        assert not Instruction.SCISSORS < Instruction.PAPER, "Scissors does not lose to paper"

        print('solving')

        assert Part2Outcome.I_LOSE.solve(Instruction.PAPER) == Instruction.ROCK, "I lose to Paper with Rock"
        assert Part2Outcome.I_LOSE.solve(Instruction.SCISSORS) == Instruction.PAPER, "I lose to Scissors with Paper"
        assert Part2Outcome.I_LOSE.solve(Instruction.ROCK) == Instruction.SCISSORS, "I lose to Rock with Scissors"

        assert Part2Outcome.I_WIN.solve(Instruction.PAPER) == Instruction.SCISSORS, "I beat paper with scissors"
        assert Part2Outcome.I_WIN.solve(Instruction.SCISSORS) == Instruction.ROCK, "I beat scissors with rock"
        assert Part2Outcome.I_WIN.solve(Instruction.ROCK) == Instruction.PAPER, "I beat rock with paper"



    except Exception as exc:
        import pdb
        pdb.set_trace()
        print(exc)
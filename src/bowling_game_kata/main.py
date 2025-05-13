from abc import ABC, abstractmethod
from typing import Tuple
from pydantic import BaseModel, field_validator
from pydantic.dataclasses import dataclass


class Rolls(BaseModel):
    rolls: list[int]

    @field_validator("rolls")
    def validate_rolls(cls, rolls):
        # Check length first
        if not 12 <= len(rolls) <= 21:
            raise ValueError("Number of rolls must be between 12 and 21")

        # Then check each roll
        for roll in rolls:
            if not 0 <= roll <= 10:
                raise ValueError("Each roll must be between 0 and 10")
        return rolls


class FrameScoreResult(BaseModel):
    score: int
    next_roll_index: int


@dataclass
class FrameScorer(ABC):
    @abstractmethod
    def score(self, rolls: list[int], roll_index: int) -> FrameScoreResult:
        """Calculates score and returns the next roll index"""
        pass


class NormalFrameScorer(FrameScorer):
    def score(self, rolls: list[int], roll_index: int) -> FrameScoreResult:
        if roll_index + 1 >= len(rolls):
            raise ValueError("Not enough rolls for normal frame")
        return FrameScoreResult(
            score=rolls[roll_index] + rolls[roll_index + 1],
            next_roll_index=roll_index + 2,
        )


class SpareFrameScorer(FrameScorer):
    def score(self, rolls: list[int], roll_index: int) -> FrameScoreResult:
        if roll_index + 2 >= len(rolls):
            raise ValueError("Not enough rolls for spare frame")
        return FrameScoreResult(
            score=10 + rolls[roll_index + 2], next_roll_index=roll_index + 2
        )


class StrikeFrameScorer(FrameScorer):
    def score(self, rolls: list[int], roll_index: int) -> FrameScoreResult:
        if roll_index + 2 >= len(rolls):
            raise ValueError("Not enough rolls for strike frame")
        return FrameScoreResult(
            score=10 + rolls[roll_index + 1] + rolls[roll_index + 2],
            next_roll_index=roll_index + 1,
        )


class FrameScorerFactory:
    @staticmethod
    def create_scorer(rolls: list[int], roll_index: int) -> FrameScorer:
        if roll_index >= len(rolls):
            raise ValueError("Roll index out of bounds")

        if rolls[roll_index] == 10:
            return StrikeFrameScorer()
        elif rolls[roll_index] + rolls[roll_index + 1] == 10:
            return SpareFrameScorer()
        else:
            return NormalFrameScorer()


class BowlingGame:
    def __init__(self, rolls: Rolls):
        self.rolls: Rolls = rolls

    def score(self) -> int:
        total = 0
        rolls = self.rolls.rolls
        roll_index = 0
        frame = 1

        while frame <= 10:
            scorer = FrameScorerFactory.create_scorer(rolls, roll_index)
            result = scorer.score(rolls, roll_index)
            total += result.score
            roll_index = result.next_roll_index
            frame += 1

        return total


if __name__ == "__main__":
    # Example game
    rolls = Rolls(rolls=[10 for _ in range(12)])  # Perfect game
    game = BowlingGame(rolls)
    print(f"Score: {game.score()}")

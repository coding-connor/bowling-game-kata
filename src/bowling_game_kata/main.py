from typing import Optional
from pydantic import BaseModel


class Frame(BaseModel):
    first_roll: int
    second_roll: Optional[int] = None
    third_roll: Optional[int] = None

    def is_strike(self) -> bool:
        return self.first_roll == 10

    def is_spare(self) -> bool:
        if self.second_roll is None:
            return False
        return self.first_roll + self.second_roll == 10

    def get_score(self, include_third_roll: bool = True) -> int:
        score = self.first_roll
        if self.second_roll is not None:
            score += self.second_roll
        if self.third_roll is not None and include_third_roll:
            score += self.third_roll
        return score


class BowlingGame:
    def __init__(self):
        self.frames: list[Frame] = []

    def roll(self, pins: int):
        if not self.frames:
            self.frames.append(Frame(first_roll=pins))
            return

        previous_frame = self.frames[-1]

        # Handle last frame
        if len(self.frames) == 10:
            if previous_frame.second_roll is not None:
                previous_frame.third_roll = pins
            else:
                previous_frame.second_roll = pins
            return

        # Handle normal frames
        if previous_frame.second_roll is not None or previous_frame.first_roll == 10:
            self.frames.append(Frame(first_roll=pins))
        else:
            previous_frame.second_roll = pins

    def score(self) -> int:
        total = 0
        for index, frame in enumerate(self.frames):
            # Add the current frame's score
            total += frame.get_score()

            # Add bonus points for previous frame's spare or strike
            if index > 0:
                previous_frame = self.frames[index - 1]
                if previous_frame.is_spare():
                    total += frame.first_roll
                elif previous_frame.is_strike():
                    total += frame.get_score(include_third_roll=False)
                    if index > 1 and self.frames[index - 2].is_strike():
                        total += frame.first_roll
        return total


if __name__ == "__main__":
    pass

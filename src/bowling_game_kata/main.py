from typing import Optional
from pydantic import BaseModel


class Frame(BaseModel):
    first_roll: int
    second_roll: Optional[int] = None

    def is_strike(self) -> bool:
        return self.first_roll == 10

    def is_spare(self) -> bool:
        if not self.first_roll and self.second_roll:
            return False
        return self.first_roll + (self.second_roll if self.second_roll else 0) == 10


class BowlingGame:
    def __init__(self):
        self.last_roll: int = 0
        self.frames: list[Frame] = []
        self.spare_bonus: bool = False
        self.strike_first_bonus: bool = False
        self.strike_second_bonus: bool = False

    def roll(self, pins: int):
        if self.frames:
            last_frame = self.frames[-1]

            if last_frame.second_roll or last_frame.first_roll == 10:
                self.frames.append(Frame(first_roll=pins))
            else:
                last_frame.second_roll = pins
        else:
            self.frames.append(Frame(first_roll=pins))

        self.last_roll = pins

    def score(self) -> int:
        total = 0
        for index, frame in enumerate(self.frames):
            # add spare bonus when previous roll resulted in spare
            if self.spare_bonus:
                total += self.last_roll
                self.spare_bonus = False
            if self.strike_first_bonus and not frame.second_roll:
                total += self.last_roll
                self.strike_first_bonus = False
            if self.strike_second_bonus and frame.second_roll:
                total += self.last_roll
                self.strike_second_bonus = False
            # spare
            if frame.is_spare():
                self.spare_bonus = True

            # strike
            if frame.is_strike():
                self.strike_first_bonus = True
                self.strike_second_bonus = True

            total = (
                total
                + frame.first_roll
                + (frame.second_roll if frame.second_roll else 0)
            )
        return total

        ## Spare
        ## If: Roll + Roll[-1] == 10


if __name__ == "__main__":
    pass

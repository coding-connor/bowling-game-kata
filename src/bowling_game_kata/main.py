from typing import Optional, List, Union
from pydantic import BaseModel

# Bowling game constants
STRIKE_PINS = 10
TOTAL_FRAMES = 10
LAST_FRAME_INDEX = 9  # 0-based index of the last frame


class Frame(BaseModel):
    first_roll: int
    second_roll: Optional[int] = None

    def is_strike(self) -> bool:
        return self.first_roll == STRIKE_PINS

    def is_spare(self) -> bool:
        if self.second_roll is None:
            return False
        return self.first_roll + self.second_roll == STRIKE_PINS

    def is_complete(self) -> bool:
        return self.is_strike() or self.second_roll is not None

    def get_base_score(self) -> int:
        score = self.first_roll
        if self.second_roll is not None:
            score += self.second_roll
        return score

    def get_strike_bonus_score(self) -> int:
        return self.get_base_score()


class LastFrame(Frame):
    third_roll: Optional[int] = None

    def is_complete(self) -> bool:
        if self.is_strike() or self.is_spare():
            return self.third_roll is not None
        return self.second_roll is not None

    def get_base_score(self) -> int:
        score = super().get_base_score()
        if self.third_roll is not None:
            score += self.third_roll
        return score

    def get_strike_bonus_score(self) -> int:
        # For strike bonus calculations, we only want the first two rolls
        return super().get_base_score()


class BowlingGame:
    def __init__(self):
        self.frames: List[Union[Frame, LastFrame]] = []

    # Public interface
    def roll(self, pins: int) -> None:
        if self._is_last_frame():
            self._add_roll_to_last_frame(pins)
        else:
            self._add_roll_or_create_new_frame(pins)

    def score(self) -> int:
        total = 0
        for index, frame in enumerate(self.frames):
            total += frame.get_base_score()

            if index > 0:
                total += self._add_bonus_for_previous_frame(index)
        return total

    # Frame management
    def _add_new_frame(self, first_roll: int) -> None:
        if len(self.frames) == LAST_FRAME_INDEX:
            self.frames.append(LastFrame(first_roll=first_roll))
        else:
            self.frames.append(Frame(first_roll=first_roll))

    def _is_last_frame(self) -> bool:
        return len(self.frames) == TOTAL_FRAMES

    # Roll handling
    def _add_roll_to_last_frame(self, pins: int) -> None:
        last_frame = self.frames[-1]
        if not isinstance(last_frame, LastFrame):
            raise TypeError("Expected LastFrame")

        if last_frame.second_roll is not None:
            last_frame.third_roll = pins
        else:
            last_frame.second_roll = pins

    def _add_roll_or_create_new_frame(self, pins: int) -> None:
        if not self.frames:
            self._add_new_frame(pins)
            return

        existing_frame = self.frames[-1]
        if not existing_frame.is_complete():
            existing_frame.second_roll = pins
        else:
            self._add_new_frame(pins)

    # Scoring
    def _add_bonus_for_previous_frame(self, current_index: int) -> int:
        previous_frame = self.frames[current_index - 1]
        current_frame = self.frames[current_index]

        if previous_frame.is_spare():
            return self._add_spare_bonus(current_frame)
        elif previous_frame.is_strike():
            return self._add_strike_bonus(current_index)

        return 0

    def _add_spare_bonus(self, frame: Frame) -> int:
        return frame.first_roll

    def _add_strike_bonus(self, current_index: int) -> int:
        current_frame = self.frames[current_index]
        bonus = current_frame.get_strike_bonus_score()

        # Add bonus for consecutive strikes
        if current_index > 1 and self.frames[current_index - 2].is_strike():
            bonus += current_frame.first_roll

        return bonus


if __name__ == "__main__":
    # Example of a perfect game (300 points)
    game = BowlingGame()
    rolls = [STRIKE_PINS] * 12  # 12 strikes for a perfect game

    # Roll the balls
    for roll in rolls:
        game.roll(roll)

    # Print the game result
    print("\nPerfect Bowling Game (300 points):")
    print("Rolls:", " ".join(str(roll) for roll in rolls))
    print("Final Score:", game.score())

from pydantic import BaseModel, field_validator


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


class BowlingGame:
    def __init__(self, rolls: Rolls):
        self.rolls: Rolls = rolls

    def score(self) -> int:
        total = 0
        rolls = self.rolls.rolls
        frame = 1
        roll_index = 0

        while frame <= 10:
            # strike
            if rolls[roll_index] == 10:
                total += 10 + rolls[roll_index + 1] + rolls[roll_index + 2]
                roll_index += 1
            # spare
            elif rolls[roll_index] + rolls[roll_index + 1] == 10:
                total += 10 + rolls[roll_index + 2]
                roll_index += 2
            else:
                total += rolls[roll_index] + rolls[roll_index + 1]
                roll_index += 2
            frame += 1
        return total


if __name__ == "__main__":
    # Example game
    rolls = Rolls(rolls=[10 for _ in range(12)])  # Perfect game
    game = BowlingGame(rolls)
    print(f"Score: {game.score()}")

from bowling_game_kata.main import (
    BowlingGame,
    Rolls,
    NormalFrameScorer,
    SpareFrameScorer,
    StrikeFrameScorer,
)
from pytest import raises


class TestBowlingGame:
    def test_game_instantiates_with_rolls(self):
        rolls = Rolls(rolls=[0 for _ in range(20)])
        game = BowlingGame(rolls)
        assert game.rolls == rolls

    def test_all_gutter_balls(self):
        rolls = Rolls(rolls=[0 for _ in range(20)])
        game = BowlingGame(rolls)
        assert game.score() == 0

    def test_all_threes(self):
        roll_list = [3 for _ in range(20)]
        rolls = Rolls(rolls=roll_list)
        game = BowlingGame(rolls=rolls)
        assert game.score() == 60

    def test_rolls_under_length_min(self):
        with raises(ValueError):
            Rolls(rolls=[1, 2, 3])

    def test_rolls_over_length_max(self):
        with raises(ValueError):
            Rolls(rolls=[1 for _ in range(30)])

    def test_invalid_roll_values(self):
        with raises(ValueError):
            Rolls(rolls=[11] + [0 for _ in range(19)])
        with raises(ValueError):
            Rolls(rolls=[-1] + [0 for _ in range(19)])

    def test_single_strike(self):
        rolls = Rolls(rolls=[10] + [1 for _ in range(18)])
        game = BowlingGame(rolls=rolls)
        assert game.score() == 30

    def test_consecutive_strikes(self):
        rolls = Rolls(rolls=[10, 10] + [1 for _ in range(16)])
        game = BowlingGame(rolls=rolls)
        assert game.score() == 49

    def test_single_spare(self):
        rolls = Rolls(rolls=[9, 1] + [1 for _ in range(18)])
        game = BowlingGame(rolls=rolls)
        assert game.score() == 29

    def test_consecutive_spares(self):
        rolls = Rolls(rolls=[9, 1, 9, 1] + [1 for _ in range(16)])
        game = BowlingGame(rolls=rolls)
        assert game.score() == 46

    def test_mixed_strikes_and_spares(self):
        # Strike, spare, regular frame
        rolls = Rolls(rolls=[10, 5, 5, 3, 4] + [0 for _ in range(14)])
        game = BowlingGame(rolls)
        assert game.score() == 40  # (10 + 5 + 5) + (5 + 5 + 3) + (3 + 4)

    def test_spare_in_last_frame(self):
        # All zeros until last frame, then spare
        rolls = Rolls(rolls=[0 for _ in range(18)] + [5, 5, 5])
        game = BowlingGame(rolls)
        assert game.score() == 15  # (5 + 5 + 5)

    def test_strike_in_last_frame(self):
        # All zeros until last frame, then strike
        rolls = Rolls(rolls=[0 for _ in range(18)] + [10, 10, 10])
        game = BowlingGame(rolls)
        assert game.score() == 30  # (10 + 10 + 10)

    def test_perfect_game(self):
        rolls = Rolls(rolls=[10 for _ in range(12)])
        game = BowlingGame(rolls)
        assert game.score() == 300

    def test_example_game(self):
        # Test the example game from the main block
        rolls = Rolls(rolls=[10 for _ in range(12)])  # Perfect game
        game = BowlingGame(rolls)
        assert game.score() == 300


class TestFrameScorers:
    def test_normal_frame_scorer(self):
        scorer = NormalFrameScorer()
        rolls = [3, 4]
        result = scorer.score(rolls, 0)
        assert result.score == 7
        assert result.next_roll_index == 2

    def test_normal_frame_scorer_out_of_bounds(self):
        scorer = NormalFrameScorer()
        rolls = [3]
        import pytest

        with pytest.raises(ValueError, match="Not enough rolls for normal frame"):
            scorer.score(rolls, 0)

    def test_spare_frame_scorer(self):
        scorer = SpareFrameScorer()
        rolls = [5, 5, 7]
        result = scorer.score(rolls, 0)
        assert result.score == 17
        assert result.next_roll_index == 2

    def test_spare_frame_scorer_out_of_bounds(self):
        scorer = SpareFrameScorer()
        rolls = [5, 5]
        import pytest

        with pytest.raises(ValueError, match="Not enough rolls for spare frame"):
            scorer.score(rolls, 0)

    def test_strike_frame_scorer(self):
        scorer = StrikeFrameScorer()
        rolls = [10, 3, 6]
        result = scorer.score(rolls, 0)
        assert result.score == 19
        assert result.next_roll_index == 1

    def test_strike_frame_scorer_out_of_bounds(self):
        scorer = StrikeFrameScorer()
        rolls = [10, 3]
        import pytest

        with pytest.raises(ValueError, match="Not enough rolls for strike frame"):
            scorer.score(rolls, 0)

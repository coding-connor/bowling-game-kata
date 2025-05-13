import pytest
from bowling_game_kata.main import BowlingGame


def build_game(rolls: list[int]) -> BowlingGame:
    game = BowlingGame()
    for pins in rolls:
        game.roll(pins)
    return game


class TestBowlingGame:
    def test_game_initializes_with_score_of_zero(self):
        game = BowlingGame()
        assert game.score() == 0

    def test_scores_single_normal_roll(self):
        game = build_game([4])
        assert game.score() == 4

    def test_scores_two_normal_rolls(self):
        game = build_game([4, 4])
        assert game.score() == 8

    def test_scores_single_spare(self):
        game = build_game([5, 5, 4])
        assert game.score() == 18

    def test_scores_single_strike(self):
        game = build_game([10, 5, 4])
        assert game.score() == 28

    def test_correctly_identify_spares(self):
        game = build_game([3, 5, 5])
        assert game.score() == 13

    def test_correctly_handle_last_frame_spare(self):
        rolls = [1] * 18 + [5, 5, 5]  # 9 frames of ones, then spare with bonus
        game = build_game(rolls)
        assert game.score() == 33

    def test_correctly_handle_last_frame_strike(self):
        rolls = [1] * 18 + [10, 1, 1]  # 9 frames of ones, then strike with bonus
        game = build_game(rolls)
        assert game.score() == 30

    def test_perfect_game(self):
        rolls = [10] * 12  # 12 strikes
        game = build_game(rolls)
        assert game.score() == 300

    def test_gutter_ball_game(self):
        rolls = [0] * 20  # 20 zeros
        game = build_game(rolls)
        assert game.score() == 0

    def test_all_spares_game(self):
        rolls = [5, 5] * 10 + [5]  # 10 frames of spares (5,5) plus bonus roll
        game = build_game(rolls)
        assert game.score() == 150

    def test_three_strikes_in_last_frame(self):
        rolls = [0] * 18 + [10, 10, 10]  # 9 frames of zeros, then three strikes
        game = build_game(rolls)
        assert game.score() == 30

    def test_three_consecutive_strikes(self):
        rolls = [0] * 12 + [
            10,
            10,
            10,
            5,
            4,
        ]  # 6 frames of zeros, three strikes, then 5,4
        game = build_game(rolls)
        assert game.score() == 83

    def test_strike_followed_by_spare_in_last_frame(self):
        rolls = [0] * 18 + [
            10,
            5,
            5,
        ]  # 9 frames of zeros, then strike followed by spare
        game = build_game(rolls)
        assert game.score() == 20

    def test_spare_followed_by_strike_in_last_frame(self):
        rolls = [0] * 18 + [
            5,
            5,
            10,
        ]  # 9 frames of zeros, then spare followed by strike
        game = build_game(rolls)
        assert game.score() == 20

    # Scores validated using https://www.bowlinggenius.com/
    @pytest.mark.parametrize(
        "rolls,expected_score,description",
        [
            (
                [10, 5, 5, 10, 3, 4, 7, 3, 10, 2, 3, 10, 10, 8, 2, 5],
                167,
                "Mixed game with strikes, spares, and normal frames",
            ),
            (
                [0, 0, 3, 6, 5, 5, 10, 10, 10, 8, 2, 0, 9, 1, 9, 10, 5, 5],
                166,
                "Another mixed game with different patterns",
            ),
            (
                [10, 5, 5, 10, 5, 5, 10, 5, 5, 10, 5, 5, 10, 5, 5, 10, 5, 5, 10, 5, 5],
                195,
                "Alternating strikes and spares",
            ),
            (
                [3, 0, 4, 6, 10, 6, 0, 1, 5, 9, 1, 4, 6, 0, 0, 10, 3, 3],
                97,
                "Another mixed game with strikes, spares, and normal frames",
            ),
        ],
    )
    def test_partial_games(self, rolls, expected_score, description):
        game = build_game(rolls)
        assert game.score() == expected_score

    @pytest.mark.parametrize(
        "rolls,expected_score,description",
        [
            (
                [5, 4, 2, 4, 6, 4, 7, 2, 7, 3],
                51,
                "Mixed partialgame with strikes, spares, and normal frames",
            ),
            (
                [10, 10, 5, 5, 3, 6, 0, 10, 10],
                97,
                "Another partial mixed game with different patterns",
            ),
            (
                [10, 5, 5, 10, 5, 5, 10, 5, 5, 10, 5, 5],
                150,
                "Alternating strikes and spares for partial game",
            ),
        ],
    )
    def test_mixed_games(self, rolls, expected_score, description):
        game = build_game(rolls)
        assert game.score() == expected_score

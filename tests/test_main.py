from bowling_game_kata.main import BowlingGame


class TestBowlingGame:
    def test_game_initializes_with_score_of_zero(self):
        game = BowlingGame()
        assert game.score() == 0

    def test_scores_single_normal_roll(self):
        game = BowlingGame()
        game.roll(4)
        assert game.score() == 4

    def test_scores_two_normal_rolls(self):
        game = BowlingGame()
        game.roll(4)
        game.roll(4)
        assert game.score() == 8

    def test_scores_single_spare(self):
        game = BowlingGame()
        game.roll(5)
        game.roll(5)
        game.roll(4)
        assert game.score() == 18

    def test_scores_single_strike(self):
        game = BowlingGame()
        game.roll(10)
        game.roll(5)
        game.roll(4)
        assert game.score() == 28

    def test_correctly_identify_spares(self):
        game = BowlingGame()
        game.roll(3)
        game.roll(5)
        game.roll(5)
        assert game.score() == 13

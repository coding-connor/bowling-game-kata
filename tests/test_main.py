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

    def test_correctly_handle_last_frame_spare(self):
        game = BowlingGame()
        for _ in range(18):
            game.roll(1)
        game.roll(5)
        game.roll(5)
        game.roll(5)
        assert game.score() == 33

    def test_correctly_handle_last_frame_strike(self):
        game = BowlingGame()
        for _ in range(18):
            game.roll(1)
        game.roll(10)
        game.roll(1)
        game.roll(1)
        assert game.score() == 30

    def test_consecutive_strikes(self):
        game = BowlingGame()
        game.roll(10)
        game.roll(10)
        game.roll(10)
        assert game.score() == 60

    def test_perfect_game(self):
        game = BowlingGame()
        for _ in range(12):
            game.roll(10)
        assert game.score() == 300

    def test_gutter_ball_game(self):
        game = BowlingGame()
        for _ in range(20):
            game.roll(0)
        assert game.score() == 0

    def test_mixed_game(self):
        game = BowlingGame()
        # Frame 1: Strike
        game.roll(10)
        # Frame 2: Spare (5,5)
        game.roll(5)
        game.roll(5)
        # Frame 3: Strike
        game.roll(10)
        # Frame 4: Normal (3,4)
        game.roll(3)
        game.roll(4)
        # Frame 5: Spare (7,3)
        game.roll(7)
        game.roll(3)
        # Frame 6: Strike
        game.roll(10)
        # Frame 7: Normal (2,3)
        game.roll(2)
        game.roll(3)
        # Frame 8: Strike
        game.roll(10)
        # Frame 9: Strike
        game.roll(10)
        # Frame 10: Spare with bonus (8,2,5)
        game.roll(8)
        game.roll(2)
        game.roll(5)

        assert game.score() == 167

    def test_another_mixed_game(self):
        game = BowlingGame()
        # Frame 1: (0,0)
        game.roll(0)
        game.roll(0)
        # Frame 2: (3,6))
        game.roll(3)
        game.roll(6)
        # Frame 3: Spare (5,5)
        game.roll(5)
        game.roll(5)
        # Frame 4: Strike (10)
        game.roll(10)
        # Frame 5: Strike (10)
        game.roll(10)
        # Frame 6: Strike
        game.roll(10)
        # Frame 7: Spare (8,2)
        game.roll(8)
        game.roll(2)
        # Frame 8: (0,9)
        game.roll(0)
        game.roll(9)
        # Frame 9: Spare (1,9)
        game.roll(1)
        game.roll(9)
        # Frame 10: Strike, Spare (10,5,5)
        game.roll(10)
        game.roll(5)
        game.roll(5)

        assert game.score() == 166

    def test_three_strikes_in_last_frame(self):
        game = BowlingGame()
        # First 9 frames of zeros
        for _ in range(18):
            game.roll(0)
        # Last frame: three strikes
        game.roll(10)
        game.roll(10)
        game.roll(10)

        assert game.score() == 30

    def test_three_consecutive_strikes(self):
        game = BowlingGame()
        # First 6 frames of zeros
        for _ in range(12):
            game.roll(0)
        # Three consecutive strikes
        game.roll(10)
        game.roll(10)
        game.roll(10)
        # Last frame: normal
        game.roll(5)
        game.roll(4)

        assert game.score() == 83

    def test_strike_followed_by_spare_in_last_frame(self):
        game = BowlingGame()
        # First 9 frames of zeros
        for _ in range(18):
            game.roll(0)
        # Last frame: strike followed by spare
        game.roll(10)
        game.roll(5)
        game.roll(5)

        assert game.score() == 20

    def test_spare_followed_by_strike_in_last_frame(self):
        game = BowlingGame()
        # First 9 frames of zeros
        for _ in range(18):
            game.roll(0)
        # Last frame: spare followed by strike
        game.roll(5)
        game.roll(5)
        game.roll(10)

        assert game.score() == 20

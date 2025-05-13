from bowling_game_kata.main import hello_world


class TestBowlingGame:
    def test_hello_world(self):
        test = hello_world()
        assert test == "hello world"

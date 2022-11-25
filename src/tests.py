import unittest
from unittest.mock import patch

from pygame import Rect, Vector2

from utils import load_skeleton, read_file
from entities import Player
from blocks import Block


class TestLoading(unittest.TestCase):

    # read file
    def test_read_file(self):
        self.assertEqual(read_file("tests/read_file.txt"), "Test\n")

    # load skeleton
    @patch("utils.loading.read_file")
    def test_load_skeleton(self, mock_read_file):

        with open("tests/load_skeleton.txt", "r") as f:
            mock_read_file.return_value = f.read()

        self.assertEqual(str(load_skeleton("path")), "Origin: 800.0, 500.0\n1:\n\t1\n\t2\n0\n")

class TestPlayer(unittest.TestCase):

    # calculate leg target position
    def test_calculate_target_pos(self):

        blocks = [Block((100,100), (100,100), 1)]

        self.assertEqual(Player.calculate_target_pos(None, blocks, Vector2(90,110), 1), Vector2(140,100))   # collision and can lift leg up
        self.assertEqual(Player.calculate_target_pos(None, blocks, Vector2(40,40), 1), Vector2(90,40))      # no collision 
        self.assertEqual(Player.calculate_target_pos(None, blocks, Vector2(160,200), 1), Vector2(210, 200)) # collision but cant lift leg up



if __name__ == "__main__":
    unittest.main()
import unittest
from connectz import Frame
from connectz import reformat_file_content
from connectz import isolate_game_parameters
from connectz import validate_game_termination
from connectz import validate_column_move
from connectz import validate_row_move
from connectz import reformat_move_data
from connectz import win_check
from connectz import draw_check
from connectz import simulate_gameplay
from connectz import check_game

class FrameFunctionalityTests(unittest.TestCase):

    def setUp(self):
        self.frame_instance = Frame(2, 3)

    def test_initialise_frame(self):
        expected_width = 2
        actual_width = self.frame_instance.width

        expected_height = 3
        actual_height = self.frame_instance.height

        expected_grid = [[0, 0], [0, 0], [0, 0]]
        actual_grid = self.frame_instance.grid

        self.assertEqual(expected_width, actual_width)
        self.assertEqual(expected_height, actual_height)
        self.assertEqual(expected_grid, actual_grid)

    def test_update_grid(self):
        self.frame_instance.update_grid(0, 1, 1)

        expected_grid = [[0, 1], [0, 0], [0, 0]]
        actual_grid = self.frame_instance.grid

        self.assertEqual(expected_grid, actual_grid)

class ReformatFileContentTests(unittest.TestCase):

    def setUp(self):
        self.valid_string_file_content = '7 6 4\n1\n2\n1\n2\n1\n2\n1'
        self.invalid_string_file_content = string_file_content = '7 6 4\n1\n2\n1notvalid\n2\n1\n2\n1'

    def test_valid_file_content(self):
        expected_output_content = [7, 6, 4, 1, 2, 1, 2, 1, 2, 1]
        actual_output_content = reformat_file_content(self.valid_string_file_content)

        self.assertEqual(expected_output_content, actual_output_content)

    def test_file_content_with_strings(self):
        expected_output_content = 'Output: 8'
        actual_output_content = reformat_file_content(self.invalid_string_file_content)

        self.assertEqual(expected_output_content, actual_output_content)

class IsolateGameParametersTests(unittest.TestCase):
    
    def test_isolate_game_parameters(self):
        test_int_list_input = [7, 6, 5, 1, 2, 1, 2, 1]

        expected_output = (7, 6, 5, [1, 2, 1, 2, 1])
        actual_output = isolate_game_parameters(test_int_list_input)

        self.assertEqual(expected_output, actual_output)

class ValidateGameTerminationTests(unittest.TestCase):

    def test_game_that_can_be_won(self):
        expected_output = None
        actual_output = validate_game_termination(3, 3, 3)

        self.assertEqual(expected_output, actual_output)

    def test_game_that_cannot_be_won(self):
        expected_output = 'Output: 7'
        actual_output = validate_game_termination(2, 2, 3)

        self.assertEqual(expected_output, actual_output)

class ValidateColummnMoveTests(unittest.TestCase):

    def setUp(self):
        self.frame_width = 3

    def test_valid_column_move(self):
        column_move = 2

        expected_output = None
        actual_output = validate_column_move(column_move, self.frame_width)

        self.assertEqual(expected_output, actual_output)

    def test_column_move_too_large(self):
        column_move = 3

        expected_output = 'Output: 6'
        actual_output = validate_column_move(column_move, self.frame_width)

        self.assertEqual(expected_output, actual_output)

    def test_column_move_too_small(self):
        column_move = -1

        expected_output = 'Output: 6'
        actual_output = validate_column_move(column_move, self.frame_width)

        self.assertEqual(expected_output, actual_output)
        
class ValidateRowMoveTests(unittest.TestCase):
    
    def setUp(self):
        self.frame_height = 3
    
    def test_valid_row_move(self):
        row_move = 0

        expected_output = None
        actual_output = validate_row_move(row_move, self.frame_height)

        self.assertEqual(expected_output, actual_output)

    def test_column_overflow(self):
        row_move = 3

        expected_output = 'Output: 5'
        actual_output = validate_row_move(row_move, self.frame_height)

        self.assertEqual(expected_output, actual_output)

class ReformatMoveData(unittest.TestCase):

    def setUp(self):
        self.frame_width = 3
        self.frame_height = 3

    def test_valid_input_reformat_move_data(self):
        test_column_move_input = [1, 2, 1, 2, 1]

        expected_output = ([0, 0, 1, 1, 2], [0, 1, 0, 1, 0])
        actual_output = reformat_move_data(test_column_move_input, self.frame_width, self.frame_height)

        self.assertEqual(expected_output, actual_output)

    def test_invalid_column_move_reformat_move_data(self):
        test_column_move_input = [6, 2, 1, 2, 1]

        expected_output = 'Output: 6'
        actual_output = reformat_move_data(test_column_move_input, self.frame_width, self.frame_height)

        self.assertEqual(expected_output, actual_output)

    def test_invalid_row_move_reformat_move_data(self):
        test_column_move_input = [1, 1, 1, 1, 1]

        expected_output = 'Output: 5'
        actual_output = reformat_move_data(test_column_move_input, self.frame_width, self.frame_height)

        self.assertEqual(expected_output, actual_output)

class WinCheckTests(unittest.TestCase):

    def setUp(self):
        self.frame_instance = Frame(3, 3)
        self.min_counters_to_win = 2

    def test_player_1_row_win(self):
        self.frame_instance.grid = [[1, 2, 0], [1, 0, 0], [0, 0, 0]]
        grid_row = 1
        grid_column = 0
        moves_remaining = 0

        expected_output = 'Output: 1'
        actual_output = win_check(self.frame_instance, grid_row, grid_column, self.min_counters_to_win, moves_remaining)

        self.assertEqual(expected_output, actual_output)

    def test_player_1_column_win(self):
        self.frame_instance.grid = [[1, 1, 0], [2, 0, 0], [0, 0, 0]]
        grid_row = 0
        grid_column = 1
        moves_remaining = 0

        expected_output = 'Output: 1'
        actual_output = win_check(self.frame_instance, grid_row, grid_column, self.min_counters_to_win, moves_remaining)

        self.assertEqual(expected_output, actual_output)

    def test_player_1_diagonal_win(self):
        self.frame_instance.grid = [[1, 2, 0], [1, 0, 0], [0, 0, 0]]
        grid_row = 1
        grid_column = 0
        moves_remaining = 0

        expected_output = 'Output: 1'
        actual_output = win_check(self.frame_instance, grid_row, grid_column, self.min_counters_to_win, moves_remaining)

        self.assertEqual(expected_output, actual_output)

    def test_player_2_win(self):
        self.frame_instance.grid = [[1, 0, 0], [2, 2, 0], [1, 0, 0]]
        grid_row = 1
        grid_column = 1
        moves_remaining = 0

        expected_output = 'Output: 2'
        actual_output = win_check(self.frame_instance, grid_row, grid_column, self.min_counters_to_win, moves_remaining)

        self.assertEqual(expected_output, actual_output)

class IllegalContinueCheck(unittest.TestCase):

    def setUp(self):
        self.frame_instance = Frame(3, 3)
        self.min_counters_to_win = 2

    def test_illegal_continue(self):
        self.frame_instance.grid = [[1, 0, 0], [2, 2, 0], [1, 0, 0]]
        grid_row = 1
        grid_column = 1
        moves_remaining = 1

        expected_output = 'Output: 4'
        actual_output = win_check(self.frame_instance, grid_row, grid_column, self.min_counters_to_win, moves_remaining)

        self.assertEqual(expected_output, actual_output)

class DrawCheck(unittest.TestCase):

    def setUp(self):
        self.frame_instance = Frame(2, 1)

    def test_not_draw(self):
        self.frame_instance.grid = [[1], [0]]

        expected_output = False
        actual_output = draw_check(self.frame_instance)

        self.assertEqual(expected_output, actual_output)

    def test_draw(self):
        self.frame_instance.grid = [[1], [2]]
        
        expected_output = True
        actual_output = draw_check(self.frame_instance)

        self.assertEqual(expected_output, actual_output)

class SimulateGamePlayTests(unittest.TestCase):

    def setUp(self):
        self.frame_width = 3
        self.frame_height = 3
        self.min_counters_to_win = 2

    def test_draw_simulate_gameplay(self):
        self.frame_width = 3
        self.frame_height = 3
        self.min_counters_to_win = 3

        row_moves = [0, 0, 0,   1, 1, 1,   2, 2, 2]
        column_moves = [0, 1, 2,   0, 2, 1,   0, 2, 1]

        expected_output = 'Output: 0'
        actual_output = simulate_gameplay(self.frame_width, self.frame_height, row_moves, column_moves, self.min_counters_to_win)

        self.assertEqual(expected_output, actual_output)

    def test__player_1_win_simulate_gameplay(self):
        row_moves = [0, 0, 0]
        column_moves = [0, 2, 1]

        expected_output = 'Output: 1'
        actual_output = simulate_gameplay(self.frame_width, self.frame_height, row_moves, column_moves, self.min_counters_to_win)

        self.assertEqual(expected_output, actual_output)

    def test_player_2_win_simulate_gameplay(self):
        row_moves = [0, 0, 0, 1]
        column_moves = [0, 1, 2, 1]

        expected_output = 'Output: 2'
        actual_output = simulate_gameplay(self.frame_width, self.frame_height, row_moves, column_moves, self.min_counters_to_win)

        self.assertEqual(expected_output, actual_output)

    def test_incomplete_game_simulate_gameplay(self):
        row_moves = [0]
        column_moves = [0]

        expected_output = 'Output: 3'
        actual_output = simulate_gameplay(self.frame_width, self.frame_height, row_moves, column_moves, self.min_counters_to_win)

        self.assertEqual(expected_output, actual_output)

    def test_empty_game_simulate_gameplay(self):
        row_moves = []
        column_moves = []

        expected_output = 'Output: 3'
        actual_output = simulate_gameplay(self.frame_width, self.frame_height, row_moves, column_moves, self.min_counters_to_win)

        self.assertEqual(expected_output, actual_output)

    def test_illegal_continue_simulate_gameplay(self):
        row_moves = [0, 0, 0, 1]
        column_moves = [0, 2, 1, 0]

        expected_output = 'Output: 4'
        actual_output = simulate_gameplay(self.frame_width, self.frame_height, row_moves, column_moves, self.min_counters_to_win)

        self.assertEqual(expected_output, actual_output)

class CheckGameTests(unittest.TestCase):
    
    def test_invalid_file_path(self):
        file_path = 'non-existant-file.txt'

        expected_output = 'Output: 9'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_draw(self):
        file_path = 'TestFiles/2.1_Draw.txt'

        expected_output = 'Output: 0'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_player_1_win(self):
        file_path = 'TestFiles/2.2_Player_1_Win.txt'

        expected_output = 'Output: 1'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_player_2_win(self):
        file_path = 'TestFiles/2.3_Player_2_Win.txt'

        expected_output = 'Output: 2'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_incomplete(self):
        file_path = 'TestFiles/2.4_Incomplete.txt'

        expected_output = 'Output: 3'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_illegal_continue(self):
        file_path = 'TestFiles/2.5_Illegal_Continue.txt'

        expected_output = 'Output: 4'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_illegal_row(self):
        file_path = 'TestFiles/2.6_Illegal_Row.txt'

        expected_output = 'Output: 5'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_illegal_column(self):
        file_path = 'TestFiles/2.7_Illegal_Column.txt'

        expected_output = 'Output: 6'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_illegal_game(self):
        file_path = 'TestFiles/2.8_Illegal_Game.txt'

        expected_output = 'Output: 7'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_illegal_game(self):
        file_path = 'TestFiles/2.9_Invalid_File.txt'

        expected_output = 'Output: 8'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)
    
    def test_illegal_game(self):
        file_path = 'TestFiles/Player_1_Win_by_Middle_Placement.txt'

        expected_output = 'Output: 1'
        actual_output = check_game(file_path)

        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()
import sys

class Frame():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for row in range(width)] for column in range(height)]
    
    def display_frame(self):
        '''display the current state of the frame'''
        for row in self.grid:
            print(row)
    
    def update_grid(self, row_placement, column_placement, player):
        '''update the given row and column of the frame grid with the integer representing the given player'''
        self.grid[row_placement][column_placement] = player

def termination_point(output):
    '''determines if the progrram should as it has reached one of the specified end states'''
    if isinstance(output, str) and output[:8] == 'Output: ':
        return True
    else: return False

def action_output(output):
    '''If output is a string and begins with "Output: " return the integer that follows to std out. If the object cannot be vast to an integer, print the object'''
    try:
        print(int(output[8:]))
    except ValueError:
        print(output[8:])

def load_game_file(input_file_path=None):
    '''Upload and read text file from a given file path if available,
       output 9 to std if file cannot be found,
       else output the file content as a string.
       Do not allow for 0 or multiple arguments to be given through command line
       '''
    if input_file_path == None:
        cli_arguments = sys.argv
        if len(cli_arguments) != 2:
            return 'Output: Provide one input file'
        input_file_path = sys.argv[-1]

    try:
        with open(input_file_path) as input_file:
            file_content = input_file.read()
        return file_content
    except FileNotFoundError:
        return 'Output: 9'

def reformat_file_content(string_file_content):
    '''Reformat string input to a list of integers, 
       output 9 if file content does not conform to correct format
       '''
    try:
        # seperate string input into a list of strings then cast these strings to integers
        return [int(number) for number in string_file_content.split()]
    except ValueError:
        # non integer value included in file
        return 'Output: 8'

def isolate_game_parameters(int_list_file_content):
    '''given the game input given as integers, return the:
        frame width, 
        frame heigh, 
        minimum counters in a row needed to win,
        chosen columns for each move
        '''
    frame_width = int_list_file_content.pop(0)
    frame_height = int_list_file_content.pop(0)
    min_counters_to_win = int_list_file_content.pop(0)
    column_move_list = int_list_file_content

    return frame_width, frame_height, min_counters_to_win, column_move_list

### initialise the total number of moves specified

def validate_game_termination(frame_width, frame_height, min_counters_to_win):
    '''indicate if given integer game parameters create a game that cannot be won'''
    if min_counters_to_win > frame_width and min_counters_to_win > frame_height:
        return 'Output: 7'


def validate_column_move(column_move, frame_width):
    '''indicate if a chosen column placement does not exist in the chosen frame'''
    if column_move < 0 or column_move >= frame_width:
        return 'Output: 6'

def validate_row_move(row_move, frame_height):
    '''indicate if a chosen row placement does not exist in the chosen frame'''
    if row_move >= frame_height:
        return 'Output: 5'

def reformat_move_data(column_moves, frame_width, frame_height):
    '''zero index columns moves and determine row moves given a list of intger column moves, indicate if move is invalid, 
       return a tuple of row and column move lists.'''
    # zero index column moves
    column_moves = [columnn_move-1 for columnn_move in column_moves]

    # initialise dictionary to store the current height of each frame column and row move list
    current_column_row = {}
    row_moves = []

    # determine row moves based on column move chosen and all previous moves
    for column_move in column_moves:

        # if a new column is selected for counter placement, validate the column and add it as a key to current column row dictionary or output 6 to the user
        if current_column_row.get(column_move) == None:
            invalid_column_move = validate_column_move(column_move, frame_width)
            if invalid_column_move:
                return invalid_column_move
            current_column_row[column_move] = 0
        
        # otherwise increment the row counter for the given column
        else: current_column_row[column_move] += 1

        # validate the resulting row move and add it to the list of row moves
        invalid_row_move = validate_row_move(current_column_row[column_move], frame_height)
        if invalid_row_move:
            return invalid_row_move
        row_moves.append(current_column_row[column_move])
    
    return row_moves, column_moves

def win_check(frame_instance, grid_row, grid_column, min_counters_to_win, moves_remaining):
    '''determines if and which player wins given a frame grid instance and returns an integer representing that player'''
    # build lists of 1's and 2's to compare against current board positions to determine if a player wins
    player_1_win_list = [1 for index in range(min_counters_to_win)]
    player_2_win_list = [2 for index in range(min_counters_to_win)]

    # create lists for each way in which each player can win from their counter placement
    possible_win_list_groups = [# check horizontal
                                [[frame_instance.grid[grid_row][grid_column - major_offset + minor_offset] for minor_offset in range(min_counters_to_win) if grid_column - major_offset + minor_offset >= 0 and grid_column - major_offset + minor_offset <= frame_instance.width-1] for major_offset in range(min_counters_to_win)]
                                # vertical
                               ,[[frame_instance.grid[grid_row - major_offset + minor_offset][grid_column] for minor_offset in range(min_counters_to_win) if grid_row - major_offset + minor_offset >= 0 and grid_row - major_offset + minor_offset <= frame_instance.height-1] for major_offset in range(min_counters_to_win)]
                                # up / right diagonal
                               ,[[frame_instance.grid[grid_row - major_offset + minor_offset][grid_column - major_offset + minor_offset] for minor_offset in range(min_counters_to_win) if grid_column - major_offset + minor_offset >= 0 and grid_column - major_offset + minor_offset <= frame_instance.width-1 and grid_row - major_offset + minor_offset >= 0 and grid_row - major_offset + minor_offset <= frame_instance.height-1] for major_offset in range(min_counters_to_win)]
                                # down / right diagonal
                               ,[[frame_instance.grid[grid_row + major_offset - minor_offset][grid_column - major_offset + minor_offset] for minor_offset in range(min_counters_to_win) if grid_column - major_offset + minor_offset >= 0 and grid_column - major_offset + minor_offset <= frame_instance.width-1 and grid_row + major_offset - minor_offset >= 0 and grid_row + major_offset - minor_offset <= frame_instance.height-1] for major_offset in range(min_counters_to_win)]
                                ]

    # determine the appropriate output if a winning move has been found depending on the winner and if there are moves after a win has occured
    for possible_win_list_group in possible_win_list_groups:
        for possible_win_list in possible_win_list_group:
            if possible_win_list == player_1_win_list:
                if moves_remaining > 0:
                    return 'Output: 4'
                return 'Output: 1'
            if possible_win_list == player_2_win_list:
                if moves_remaining > 0:
                    return 'Output: 4'
                return 'Output: 2'

def draw_check(frame_instance):
    '''determine if frame grid has any zeros'''
    for row in frame_instance.grid:
        for value in row:
            if value == 0:
                return False
    return True

def simulate_gameplay(frame_width, frame_height, row_moves, column_moves, min_counters_to_win):
    '''simulate game moves using an instance of the Frame class 
        returns:
            0 in the case of a draw,
            1 if player 1 wins, 
            2 if player 2 wins, 
            3 in the case of an incomplete game
            '''
    frame_instance = Frame(frame_width, frame_height)
    num_moves_remaining = len(row_moves)

    for move, move_coordinates in enumerate(zip(row_moves, column_moves)):
        num_moves_remaining -= 1

        # determine whos turn it is
        current_player = 1
        if move % 2 == 1:
            current_player = 2
        
        row_placement, column_placement = move_coordinates
        frame_instance.update_grid(row_placement, column_placement, current_player)
        winner = win_check(frame_instance, row_placement, column_placement, min_counters_to_win, num_moves_remaining)
        if winner:
            return winner
    if draw_check(frame_instance):
        return 'Output: 0'
    # else incomplete game
    return 'Output: 3'

def check_game(input_file_path=None):
    '''returns the appropriate output from the below list depending on a date given plain text file specified as a command line argument

        Code Reason Description
        0   Draw                This happens when every possible space in the frame was filled with
                                    a counter, but neither player achieved a line of the required length.
        1   Win for player 1    The first player achieved a line of the required length.
        2   Win for player 2    The second player achieved a line of the required length.
        3   Incomplete          The file conforms to the format and contains only legal moves, but
                                    the game is neither won nor drawn by either player and there are
                                    remaining available moves in the frame. Note that a file with only a
                                    dimensions line constitues an incomplete game.
        4   Illegal continue    All moves are valid in all other respects but the game has already
                                    been won on a previous turn so continued play is considered an illegal move.
        5   Illegal row         The file conforms to the format and all moves are for legal columns
                                    but the move is for a column that is already full due to previous
                                    moves.
        6   Illegal column      The file conforms to the format but contains a move for a column
                                    that is out side the dimensions of the board. i.e. the column selected
                                    is greater than X
        7   Illegal game        The file conforms to the format but the dimensions describe a game
                                    that can never be won.
        8   Invalid file        The file is opened but does not conform the format.
        9   File error          The file can not be found, opened or read for some reason
        '''

    string_file_content = None
    if input_file_path != None:
        string_file_content = load_game_file(input_file_path=input_file_path)
    else:
        string_file_content = load_game_file()
    if termination_point(string_file_content):
        return string_file_content
    
    int_list_file_content = reformat_file_content(string_file_content)
    if termination_point(int_list_file_content):
        return int_list_file_content
    
    frame_width, frame_height, min_counters_to_win, column_move_list = isolate_game_parameters(int_list_file_content)
    total_number_of_moves = len(column_move_list)

    cannot_terminate = validate_game_termination(frame_width, frame_height, min_counters_to_win)
    if termination_point(cannot_terminate):
        return cannot_terminate

    move_lists = reformat_move_data(column_move_list, frame_width, frame_height)
    if termination_point(move_lists):
        return move_lists
    
    row_move_list, column_move_list = move_lists    
    game_result = simulate_gameplay(frame_width, frame_height, row_move_list, column_move_list, min_counters_to_win)
    return game_result

result = check_game()
action_output(result)
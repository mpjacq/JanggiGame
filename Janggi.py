# Author: Madeline Jacques
# Description: This program contains an implementation of Janggi, a Korean variant
# of chess. The JanggiGame class is where the game is essentially played, and contains
# the way to initialize a new game, keep track of pieces on the board, make moves,
# determine if the game has been won by one of the players, etc. Each piece type
# is defined in their own class, and the logic for checking the special move patterns
# of each type of piece is contained in those classes. The JanggiGame class' board
# contains the Piece objects of various types in a list of lists, with the pieces
# "positioned" (indexed) at certain spots which correspond to their positions if
# they were to be laid out on a physical game board.

import pygame

class JanggiGame():
    """Represents a game of Janggi, a Korean chess variant. This class includes
    an initializer for the game board, which sets up all pieces in their default
    starting positions. The first turn defaults to Blue. This class needs to
    communicate with all other classes (the pieces) in order to gain information
    about each piece on the board. The board is stored as a list of lists, with one
    list per row. The elements of the lists are all Piece class objects. There are
    different classes for each type of Piece, including NoPiece, which is used to
    represent an open position on the board."""

    def __init__(self):
        """Initializes the game of Janggi with a starting board, containing all pieces
        as Piece objects (there are several sub-types) in default positions. The game
        state will always default to UNFINISHED and with Blue ("B") team having the first
        turn when a new game is initialized. Piece objects on the board can be accessed
        by converting their algebraic notation to a list-coordinate system. Having the
        entire Piece objects stored in the board data allows us to access all the attributes
        and methods of each type of piece, allowing these classes to communicate.
        A JanggiGame has a "has-a" relationship with the pieces, not an "is-a" relationship."""

        # Board structure:
        #     A    B    C        I
        # [ [ P1,  P2,  P3,  ... P9 ]      # row 1
        #   [ P10, P11, P12, ... P18 ]     # row 2
        #    ... ... ... ... ... ...       # rows 3-9
        #   [ P81, P82, P83, ... P89, ] ]  # row 10
        # Example: Space 'a5' would be located at board[4][0], 'c3' at board[2][2], etc.
        # a5 --> row 5 (index = 4), col a --> convert a to number by using ord(a)-97 to start at 0 index
        # General formula is board[row-1][ord(col)-97], returns a Piece object

        self._board = []
        self._game_state = "UNFINISHED"
        self._turn = "B"

        # Set up the board structure using all NoPiece/blanks at first,
        # this is just to get the rows and columns set up. Starting pieces
        # will replace the NoPiece at specified locations in next step.
        for row in range(0, 10):
            row_list = []
            for col in range(0, 9):
                row_list.append(NoPiece(str(col) + str(row)))
            self._board.append(row_list)

        # Set up Red's pieces
        self._board[0][0] = Chariot('R', 'a1')
        self._board[0][1] = Elephant('R', 'b1')
        self._board[0][2] = Horse('R', 'c1')
        self._board[0][3] = Guard('R', 'd1')
        self._board[0][5] = Guard('R', 'f1')
        self._board[0][6] = Elephant('R', 'g1')
        self._board[0][7] = Horse('R', 'h1')
        self._board[0][8] = Chariot('R', 'i1')
        self._board[1][4] = General('R', 'e2')
        self._board[2][1] = Cannon('R', 'b3')
        self._board[2][7] = Cannon('R', 'h3')
        self._board[3][0] = Soldier('R', 'a4')
        self._board[3][2] = Soldier('R', 'c4')
        self._board[3][4] = Soldier('R', 'e4')
        self._board[3][6] = Soldier('R', 'g4')
        self._board[3][8] = Soldier('R', 'i4')

        # Set up Blue's pieces
        self._board[9][0] = Chariot('B', 'a10')
        self._board[9][1] = Elephant('B', 'b10')
        self._board[9][2] = Horse('B', 'c10')
        self._board[9][3] = Guard('B', 'd10')
        self._board[9][5] = Guard('B', 'f10')
        self._board[9][6] = Elephant('B', 'g10')
        self._board[9][7] = Horse('B', 'h10')
        self._board[9][8] = Chariot('B', 'i10')
        self._board[8][4] = General('B', 'e9')
        self._board[7][1] = Cannon('B', 'b8')
        self._board[7][7] = Cannon('B', 'h8')
        self._board[6][0] = Soldier('B', 'a7')
        self._board[6][2] = Soldier('B', 'c7')
        self._board[6][4] = Soldier('B', 'e7')
        self._board[6][6] = Soldier('B', 'g7')
        self._board[6][8] = Soldier('B', 'i7')

    # ***** GETTERS *****

    def get_board(self):
        """Returns the current game's board (list of lists)."""
        return self._board

    def get_game_state(self):
        """Returns the current game state (string). This can be
        UNFINISHED, RED_WON, or BLUE_WON."""
        return self._game_state

    def get_turn(self):
        """Returns R or B (string) depending on which team's turn it is."""
        return self._turn

    # ***** SETTERS *****

    def set_game_state(self, state):
        """Sets the game state to whatever is passed in as 'state'. This should
        only be UNFINISHED, RED_WON, or BLUE_WON. A game is UNFINISHED until
        one of the team's Generals is in checkmate. Returns nothing."""
        self._game_state = state

    def set_turn(self, color):
        """Updates the JanggiGame object's turn attribute. This should be either
        "R" for red team or "B" for blue team. Returns nothing."""
        self._turn = color

    # ***** METHODS *****

    def change_turn(self):
        """Changes which team's turn it is. If Red's turn, will switch to Blue,
        and vice versa. Returns nothing."""
        if self.get_turn() == "R":
            self.set_turn("B")
        else:
            self.set_turn("R")

    def shorten_color(self, color):
        """When given input of "red" or "blue", converts to "R" or "B" respectively
        and returns that as a string."""

        if color.lower() not in ["red", "blue"]:
            return "Please enter a valid color, \"red\" or \"blue\" only."

        short_color = "B"
        if color.lower() == "red":
            short_color = "R"

        return short_color

    def translate_to_list_coords(self, pos):
        """Translates coordinates given in algebraic notation to a form
        which can be used to access the corresponding board coordinates.
        Returns a list with [row, col] numbers."""

        # pos is passed in as a string with the column letter first, then row number.
        # Example: 'a10' --> a = first column, 10 = 10th row
        # ord() returns the unicode number, subtract 97 so that a = 0, b = 1...

        col_letter = pos[0].lower()
        col_to_int = int(ord(col_letter) - 97)
        row_to_int = int(pos[1:]) - 1

        # Return row first, since we access the board list via board[row][col]
        return [row_to_int, col_to_int]

    def path_ok_non_cannon(self, path):
        """Given a path (a list containing board positions in algebraic notation),
        looks at each position in the path to determine if the entire path is clear
        of pieces. This method should only be used for non-Cannon type pieces,
        since Cannons can have 1 other piece in their path to jump over."""

        path_is_clear = True

        for pos in range(0, len(path)):

            # Translate from alg to list coordinates
            pos_translated = self.translate_to_list_coords(path[pos])
            row = pos_translated[0]
            col = pos_translated[1]

            # If there is a piece present at any square along the way to pos2, path is blocked
            if type(self.get_board()[row][col]) != NoPiece:
                path_is_clear = False

        return path_is_clear

    def path_ok_cannon(self, path):
        """Given a path (a list containing board positions in algebraic notation),
        looks at each position in the path to determine if the entire path has
        one jump-able piece (which is required for Cannon movement.) This method
        should only be used for Cannon type pieces, since other piece types
        must have a clear path between start and end points."""

        jump_piece = []

        for pos in range(0, len(path)):

            # Translate from alg to list coordinates
            pos_translated = self.translate_to_list_coords(path[pos])
            row = pos_translated[0]
            col = pos_translated[1]

            if type(self.get_board()[row][col]) != NoPiece:
                jump_piece.append(self.get_board()[row][col])

        # There are no pieces in the path for the Cannon to jump over
        if len(jump_piece) == 0:
            return False

        # The Cannon can only jump over 1 piece.
        elif len(jump_piece) > 1:
            return False

        # Cannons cannot jump over other Cannons.
        elif len(jump_piece) == 1 and type(jump_piece[0]) == Cannon:
            return False

        # This will only be reached if there is 1 piece in the path
        # which is not a Cannon.
        else:
            return True

    def check_move(self, pos1, pos2):
        """Checks if there is a valid move for the piece located at pos1 to pos2,
        where both are specified in algebraic notation. A move with the same pos1
        and pos2 is considered a pass. There must be a piece at pos1. This method
        will check that the move pattern is legal for the type of piece being moved.
        Returns a list containing the legal move sequence for the piece to traverse
        from pos1 to pos2 if there is one, otherwise returns an error message.
        There will never be 2 ways for a single piece to traverse to another
        position in 1 move, so this will return 1 move sequence only."""

        # Translate from algebraic to list/index notation
        start_pos = self.translate_to_list_coords(pos1)
        end_pos = self.translate_to_list_coords(pos2)

        # Get the start and end pieces (end piece may be blank/NoPiece type)
        start_piece = self.get_board()[start_pos[0]][start_pos[1]]
        end_piece = self.get_board()[end_pos[0]][end_pos[1]]

        # Check if pos1 = pos2 - if so this is a pass. Turn is changed in make_move
        # OK to use an empty position or enemy occupied position to pass
        # Cannot pass if team's General is in check currently (this is checked in make_move)
        if pos1 == pos2:
            return "PASS"

        # If start piece type is NoPiece, no move can occur
        if type(start_piece) == NoPiece:
            return "You must select a piece to move or pass."

        # Is pos2 within the list of possible moves from pos1? (Varies by type.)
        # Utilized polymorphism so that same method name of "possible_moves" used
        # for all piece types. Each have different logic for their own type.
        possible_moves = start_piece.possible_moves()
        path_to_pos2 = None
        in_legal_moves = False

        for moves in range(0, len(possible_moves)):

            # See if the last position in each move sequence is pos2 (where we are trying to get to)
            if possible_moves[moves][-1] == pos2:

                in_legal_moves = True
                path_to_pos2 = possible_moves[moves]

        if not in_legal_moves:
            return "Not a valid move."

        # For multi-step moves (more than 1 space), check if the rest of path is clear
        # in_between = every move in path except start and end squares
        in_between = path_to_pos2[:-1]

        # The path must be clear for non-Cannon pieces
        if type(start_piece) != Cannon and not self.path_ok_non_cannon(in_between):
            return "Path is blocked."

        # Cannons must have a piece to jump over (but can't jump other Cannons)
        if type(start_piece) == Cannon and not self.path_ok_cannon(in_between):
            return "Cannons need another piece to jump over."

        # Check is pos2 is blocked by piece of the current player's color
        # We will check if pos2 is empty or has a piece to capture in make_move
        if end_piece.get_color() == start_piece.get_color():
            return "End position blocked by same team's piece."

        # Cannon logic - Cannons can't capture other Cannons
        if type(start_piece) == Cannon and type(end_piece) == Cannon:
            return "Cannons can't capture other cannons."

        # There will never be 2 ways for a single piece to traverse to another
        # position in 1 move, this will return 1 move sequence only.
        return path_to_pos2

    def threat_list(self, team):
        """When given a team of either "red" or "blue" as a parameter, finds that
        team's General and returns a list of any pieces from the opposite team that
        could potentially capture the General on their next turn."""

        # Translate "red" and "blue" to R and B
        color = self.shorten_color(team)

        # Find the location of that team's General on the board.
        gen_pos_alg = None

        for row in range(0, len(self.get_board())):

            for col in range(0, len(self.get_board()[row])):

                piece = self.get_board()[row][col]

                # Look for General type of piece in the correct color
                if type(piece) == General and piece.get_color() == color:
                    gen_pos_alg = piece.get_pos()

        # For each enemy piece on the board, see if they could move to the
        # General's current position on their next turn. If not, General is safe
        threats = []

        for row in range(0, len(self.get_board())):

            for col in range(0, len(self.get_board()[row])):

                piece = self.get_board()[row][col]

                # Find a piece (not blank) of the OPPOSITE color
                if type(piece) != NoPiece and piece.get_color() != color:

                    # Check the proposed move from current pos to General's pos
                    check_move_result = self.check_move(piece.get_pos(), gen_pos_alg)

                    # Check_move returns a list if there is a valid path for the piece
                    # to traverse from pos1 to pos2
                    if type(check_move_result) == list:
                        threats.append(piece)

        return threats

    def is_in_check(self, team):
        """When given a team of either "red" or "blue" as a parameter, returns True
        if that team is in check, returns False otherwise. A General is in check if
        it could be captured on the opposing player's next move."""

        threats = self.threat_list(team)

        # If the General is threatened, threats_list will return a non-empty list
        if len(threats) > 0:
            return True

        else:
            return False

    def general_can_escape(self, color_name):
        """Returns True if the General of color passed in ("red" or "blue") can move
        to a position where they will not be in check. This method looks at all the
        possible moves that the General could make on their next turn, and analyzes
        if the General would still be in check at the new location. No move is
        actually executed in this method."""

        # Convert the color to R/B
        color = self.shorten_color(color_name)

        # Find the General
        gen_pos_alg = None

        for row in range(0, len(self.get_board())):

            for col in range(0, len(self.get_board()[row])):

                # pos is the board square we are looking at
                pos = self.get_board()[row][col]

                if type(pos) == General and pos.get_color() == color:
                    gen_pos_alg = pos.get_pos()

        # Translate the General's position to list coordinates
        gen_coords = self.translate_to_list_coords(gen_pos_alg)

        # Store the General piece
        gen = self.get_board()[gen_coords[0]][gen_coords[1]]

        # Obtain the list of possible moves the General could make
        gen_moves = gen.possible_moves()

        # We'll store results here after checking the moves
        gen_valid_moves = []

        # Check which moves are OK and add them to gen_checked_moves list
        for move in range(0, len(gen_moves)):

            # Check the move from current pos all possible pos
            # Since the General can only move one square at a time,
            # check_move will return a list of single-element lists
            current_move = self.check_move(gen_pos_alg, gen_moves[move][0])

            # check_move returns a list if the move is valid
            if type(current_move) == list:
                gen_valid_moves.append(gen_moves[move])

        # For each valid move, see if the General would still be in check at the new pos
        # safe_moves will increment with each valid, not-in-check end pos reached
        safe_moves = 0

        for pos in range(0, len(gen_valid_moves)):

            # Translate to list coordinates
            coords = self.translate_to_list_coords(gen_valid_moves[pos][0])
            new_row = coords[0]
            new_col = coords[1]

            # Save the piece currently at the end
            end_piece = self.get_board()[new_row][new_col]

            # Put the General in the new/end pos and update pos attribute
            self.get_board()[new_row][new_col] = gen
            gen.set_pos(gen_valid_moves[pos][0])

            # Put NoPiece at General's former position
            self.get_board()[gen_coords[0]][gen_coords[1]] = NoPiece(gen_pos_alg)

            # If not in check at the new pos, increment safe_moves
            if not self.is_in_check(color_name):
                safe_moves += 1

            # Put the end piece back at its original pos
            self.get_board()[new_row][new_col] = end_piece

            # Put the General back at its original pos
            self.get_board()[gen_coords[0]][gen_coords[1]] = gen
            gen.set_pos(gen_pos_alg)

        # If there was at least 1 safe move, the General can move to escape check
        if safe_moves > 0:
            return True
        else:
            return False

    def general_can_capture(self, color):
        """Returns True if a piece of color passed in ("red" or "blue") can capture a
        piece that is placing their General in check, avoiding a checkmate scenario.
        Uses the threat_list method to determine which pieces could potentially capture
        the General of the given color, and looks at all same-team pieces on the board
        to determine if they have a valid move to capture that piece. Returns False if
        there is more than 1 threat, since you can only capture 1 piece per move."""

        # Convert the color
        short_color = self.shorten_color(color)

        # Determine which pieces of the opposite color could capture the General
        threats = self.threat_list(color)

        # If there is more than 1 threatening piece, can't capture more than 1 in next turn
        if len(threats) > 1:
            return False

        # Otherwise, see if any of that team's pieces can capture the enemy piece on their turn
        else:

            enemy_piece = threats[0]
            enemy_pos = enemy_piece.get_pos()       # Returns alg. notation
            ways_to_capture = []

            # Cycle through the entire board
            for row in range(0, len(self.get_board())):

                for col in range(0, len(self.get_board()[row])):

                    # See if that piece is the team's color we need
                    if self.get_board()[row][col].get_color() == short_color:

                        team_piece = self.get_board()[row][col]

                        # Call check move on the team piece's position to see if
                        # it can traverse to the enemy piece position (capture)
                        result = self.check_move(team_piece.get_pos(), enemy_pos)

                        # Check move result will be a list if the move can be made
                        if type(result) == list:

                            # We need to add the first space back in so we know
                            # which piece to try the move from in the next step
                            result.insert(0, team_piece.get_pos())
                            ways_to_capture.append(result)

            # If there's no way to capture, General will still be in check.
            if len(ways_to_capture) == 0:
                return False

            # For each checked move, see if the General would still be in check with the
            # proposed piece making their move.

            else:
                safe_moves = 0

                for path in range(0, len(ways_to_capture)):

                    # Save the starting piece information
                    start_coords_alg = ways_to_capture[path][0]
                    start_coords = self.translate_to_list_coords(start_coords_alg)
                    start_row = start_coords[0]
                    start_col = start_coords[1]
                    start_piece = self.get_board()[start_row][start_col]

                    #Save the ending/capture piece information
                    end_coords_alg = ways_to_capture[path][-1]
                    end_coords = self.translate_to_list_coords(end_coords_alg)
                    end_row = end_coords[0]
                    end_col = end_coords[1]
                    end_piece = self.get_board()[end_row][end_col]

                    # Put the start piece in the new/end pos
                    self.get_board()[end_row][end_col] = start_piece
                    start_piece.set_pos(end_coords_alg)

                    # Put NoPiece at piece's former position
                    self.get_board()[start_row][start_col] = NoPiece(start_coords_alg)

                    # Increment safe_moves counter if General no longer in check after move
                    if not self.is_in_check(color):
                        safe_moves += 1

                    # Put the end piece back at its original pos
                    self.get_board()[end_row][end_col] = end_piece
                    end_piece.set_pos(end_coords_alg)

                    # Put the moving piece back at its original pos
                    self.get_board()[start_row][start_col] = start_piece
                    start_piece.set_pos(start_coords_alg)

                if safe_moves > 0:
                    return True

                else:
                    return False

    def general_can_block(self, color):
        """Returns True if a piece of color passed in ("red" or "blue") can block a
        piece that is placing their General in check, avoiding a checkmate scenario.
        Uses the threat_list method to determine which pieces could potentially capture
        the General of the given color, and looks at all same-team pieces on the board
        to determine if they have a valid move to block that piece (by placing themself
        in the path that the threatening piece would need to take in order to capture
        the General."""

        short_color = self.shorten_color(color)

        threats = self.threat_list(color)

        # Find the General
        gen_pos_alg = None

        for row in range(0, len(self.get_board())):

            for col in range(0, len(self.get_board()[row])):

                # pos is the space on the board we are looking at
                pos = self.get_board()[row][col]

                if type(pos) == General and pos.get_color() == short_color:
                    # Returns position in algebraic notation
                    gen_pos_alg = self.get_board()[row][col].get_pos()

        # Store the paths for each of the threat pieces to the General's position
        all_capture_paths = []

        for enemy_piece in range(0, len(threats)):
            # check_move returns a list if there's a valid path
            path_to_capture = self.check_move(threats[enemy_piece].get_pos(), gen_pos_alg)
            all_capture_paths.append(path_to_capture)

        blocked_positions = []

        # if len(all_capture_paths) > 1:

        for path in range(0, len(all_capture_paths)):

            # Evaluate each path - see if there is a friendly piece that
            # can move into any part of the threat-piece's path, blocking it
            current_path = all_capture_paths[path]

            # A capture path length of 1 means that the threatening piece is 1 space
            # away, so there is no way to block it (you would need to move the General
            # or capture the threatening piece instead.
            if len(current_path) == 1:
                blocked_positions.append(current_path)

            else:
                # Look at each position in the capture path
                for pos in range(0, len(current_path)):

                    # Look at all friendly pieces on the board
                    for row in range(0, len(self.get_board())):

                        for col in range(0, len(self.get_board()[row])):

                            team_piece = self.get_board()[row][col]

                            # See if that piece is the team's color we need
                            # Exclude moving the General - this is checked in another method
                            if team_piece.get_color() == short_color and type(team_piece) != General:

                                # See if that piece can move from it's current pos
                                # to the part of the capture path we are looking at
                                result = self.check_move(team_piece.get_pos(), current_path[pos])

                                # If check_move returns a list, there is a way to get
                                # to that pos (a way to block)
                                if type(result) == list and all_capture_paths[path][pos]:
                                    blocked_positions.append(all_capture_paths[path][pos])

        # Check if any of the potential capture paths contain one of the positions
        # that a friendly piece could move to - path can be blocked if so

        # Automatically add 1 move paths since they can't be blocked
        unblocked_capture_paths = [path for path in all_capture_paths if len(path) == 1]

        # If no blocked positions were generated, skip next filtering step
        # This means we have no piece that could move in the way to block.
        if len(blocked_positions) == 0:
            return False

        for path in range(0, len(all_capture_paths)):

            block_found = False

            for pos in range(0, len(blocked_positions)):

                if blocked_positions[pos] in all_capture_paths[path]:
                    block_found = True

                if not block_found and all_capture_paths[path] not in unblocked_capture_paths:
                    unblocked_capture_paths.append(all_capture_paths[path])

        # If there are any unblocked capture paths, there is a way for an enemy
        # piece to get to the General unblocked.
        if len(unblocked_capture_paths) > 0:
            return False

        else:
            return True

    def checkmate(self, color):
        """Given a team color (string "red" or "blue"), returns True if that team's
        General is in a checkmate scenario, meaning they are in check and cannot
        escape being in check on their next turn by moving the General, capturing
        the threat piece, or blocking the path of the threat piece."""

        checkmate = True

        # If the team's General is in check, can they escape?
        if self.is_in_check(color):

            # See if the General could escape by moving to a different square
            if self.general_can_escape(color) is True:
                checkmate = False

            # Next check if any of the op_team's pieces could capture the threat on next turn
            elif self.general_can_capture(color) is True:
                checkmate = False

            # Next check if any of the op_team's pieces could block the threat on their next turn
            elif self.general_can_block(color) is True:
                checkmate = False

        # If the General wasn't in check yet, can't jump straight to checkmate
        else:
            checkmate = False

        return checkmate

    def make_move(self, pos1, pos2):
        """Returns True if the move can be completed, otherwise returns False.
        First, uses the check_move method to determine if there is a legal path
        from pos1 to pos2 for the piece type. If there is, completes the move by
        updating the moved piece's position both on the board and within it's own
        attributes. A move will not be completed if it places or leaves that team's
        General in check. If an enemy piece is captured as part of this move, removes
        the captured piece from the board. Updates which player's turn it is upon
        completion of the move. If pos1 == pos2 and the piece at that location
        matches which player's turn it is, this is considered a pass. No change to
        the positions of pieces on the board, but the game will switch to it being
        the other player's turn in this case and allow them to enter a move. A player
        may not pass if their General is in check. This method also checks if the
        opposing team's General has been put into checkmate as a result of the move,
        and will update the game state to RED_WON or BLUE_WON if this is the case."""

        # Do not allow a move if a player has already won
        if self.get_game_state() != "UNFINISHED":
            return "Game over!"
        
        start_pos = self.translate_to_list_coords(pos1)
        start_row = start_pos[0]
        start_col = start_pos[1]
        start_piece = self.get_board()[start_row][start_col]

        end_pos = self.translate_to_list_coords(pos2)
        end_row = end_pos[0]
        end_col = end_pos[1]
        end_piece = self.get_board()[end_row][end_col]

        check_move_result = self.check_move(pos1, pos2)
        color = ""
        op_color = ""

        # Set up color and opposite color
        if self.get_turn() == "R":
            color = "red"
            op_color = "blue"
        elif self.get_turn() == "B":
            color = "blue"
            op_color = "red"

        # If a valid move is available, check_move will return a list
        if type(check_move_result) != list and check_move_result != "PASS":
            
            # Return contents of msg from check_move_result to display to screen 
            return check_move_result

        # If the result was a pass, just change the turn.
        # ONLY if it doesn't put/leave current team's General in check
        if check_move_result == "PASS" and self.is_in_check(color) is False:
            
            # Get current turn
            prev_turn = self.get_turn()

            # Translate to full word for screen display message
            if prev_turn == "B":
                prev_turn = "Blue"
            else:
                prev_turn = "Red"

            # Change the game's turn ingo
            self.change_turn()

            # Deliver confirmation message
            return f"{prev_turn} has passed on their turn."

        # Cannot pass if General is in check
        elif check_move_result == "PASS" and self.is_in_check(color) is True:
            return "You may not pass when the General is in check."

        # Piece being moved must be same color as which team's turn it is
        # unless passing (already handled above)
        if start_piece.get_color() != self.get_turn():
            return "You may not move another team's piece."

        # Try making the move - store pieces and previous positions in case
        # we need to undo the move.
        start_piece_prev_pos = start_piece.get_pos()
        end_piece_prev_pos = end_piece.get_pos()

        # Update the start piece's location on the board and pos attribute to pos2
        self.get_board()[end_row][end_col] = start_piece
        start_piece.set_pos(pos2)

        # Clear the square on the board that the moving piece just left and
        # update the end piece's pos attribute to avoid any confusion
        if type(end_piece) != NoPiece:
            end_piece.set_pos('CAPTURED')
        
        self.get_board()[start_row][start_col] = NoPiece(pos1)

        # With the pieces moved, check if the current team's general has been placed in check
        if self.is_in_check(color):

            # Update board and pos attribute to put start piece back at start position
            self.get_board()[start_pos[0]][start_pos[1]] = start_piece
            start_piece.set_pos(start_piece_prev_pos)

            # Update board and pos attribute to put end piece back at end position
            self.get_board()[end_pos[0]][end_pos[1]] = end_piece
            end_piece.set_pos(end_piece_prev_pos)

            # You cannot make a move that puts/leaves the General in check
            return "You can't make a move that puts/leaves your General in check."

        # See if the opposing team's General is in checkmate
        if self.checkmate(op_color):

            # If it is checkmate, change the game state to reflect winner
            if op_color == "red":
                self.set_game_state("BLUE_WON")
            else:
                self.set_game_state("RED_WON")

            return "Game over!"

        # If no checkmate - game can go on
        else:

            # Change which team's turn it is
            self.change_turn()

            # Return confirmation message
            return f"Move from {pos1} to {pos2} completed."

    def translate_to_alg_coords(self, list_pos):
        """Translates coordinates given as a list with [row, col] numbers
        back to algebraic notation (such as [0, 0] to 'a1'). Returns the
        algebraic coordinates as a string."""

        # list_pos would be something like [1, 3]
        # first element = row, second element = column
        row = list_pos[0]
        col = list_pos[1]

        # Add one for row since list coordinates start at zero but alg.
        # notation starts at 1
        row_str = str(row + 1)

        # Add 97 to get the character code. 0 -> a, 1 -> b, etc.
        col_str = str(chr(col + 97))

        return col_str + row_str

    def display_board(self):
        """Displays the board in the console with locations of all current pieces.
        Returns nothing but prints to console."""

        header = "     [a] [b] [c] [d] [e] [f] [g] [h] [i]"
        print(header)

        for i in range(len(self.get_board())):
            row_print = ""
            if i <= 8:
                row_print = f"[{i + 1} ] "
            else:
                row_print = f"[{i + 1}] "
            for j in range(len(self.get_board()[i])):
                row_print += str(self.get_board()[i][j]) + " "
            print(row_print)

    def draw_pieces(self, win):
        for row in range(0, 10):
            for col in range(0, 9):
                piece = self.get_board()[row][col]
                if type(piece) != NoPiece:
                    piece.draw(win)

    def draw_possible_moves(self, selected_piece, win):
        """Highlights possible moves for a selected piece on the board. Only
        displays moves if the color of the piece clicked matches which team's
        turn it is."""

        if type(selected_piece) == NoPiece or selected_piece.get_color() != self.get_turn():
            return

        else:
            moves = selected_piece.possible_moves()
            color = selected_piece.get_color()
            rgb = None

            if color == "R":
                rgb = (255, 0, 0)
            else:
                rgb = (0, 0, 255)

            for move in range(0, len(moves)):

                end_pos = moves[move][-1]
                check_move_result = self.check_move(selected_piece.get_pos(), end_pos)

                if type(check_move_result) == list:
                    # Plot the last/end position only
                    list_coords = self.translate_to_list_coords(end_pos)
                    x_pos = (list_coords[1] * 50) + 50
                    y_pos = (list_coords[0] * 50) + 50
                    pygame.draw.circle(win, rgb, (x_pos, y_pos), 5)

class Piece():
    """Represents a generic piece which can be "placed on" the Janggi game board.
    The relationship between the JanggiGame class and the Piece classes is a
    "has-a" relationship, the game has Piece objects as part of it's attributes,
    specifically, a series of Piece objects within the board. Pieces have a color
    to specify which team they are on and a position (in algebraic notation) which
    helps track their location on the board without having access to the board
    information directly (since that is part of the JanggiGame class.) The generic
    Piece class contains methods that are used for all types of pieces, such as
    how to get their color and position attributes, how to set the attributes,
    whether a piece has a position which is in the Palace area, a method to check
    that their own position is within the board's spaces, and ways to translate
    from algebraic coordinates to list/board coordinates. The translation methods
    are important for communicating positions to and from the JanggiGame class, since
    the game board is represented as a list of lists, so that we can access board
    locations appropriately."""

    def __init__(self, color, pos):
        """Initializes a basic game piece. The parameter "color" is used to set the
        piece's team and should be passed in as "R" for red team and "B" for blue team.
        The parameter "pos" is the position of the piece in algebraic notation. The role
        is not taken as a parameter. You should not be creating generic piece
        objects, rather you should be creating new pieces using the initializers from each
        of the classes that inherit from the generic piece class. Those initializers will
        provide the appropriate role information as a 2-letter notation."""

        self._color = color
        self._pos = pos
        self._role = "ge"

    def __repr__(self):
        """Defines how the piece object is represented in the console. The general
        format is a 3 character string with 1 letter for the team color and 2 letters
        to denote the type of piece. Returns a string."""

        # Color is R/B and role is 2 characters
        return str(self.get_color() + self.get_role())

    # ***** GETTERS *****

    def get_color(self):
        """Returns the color (team) of the piece as a string, which would be "R" or "B"."""
        return self._color

    def get_pos(self):
        """Returns the current position of the piece in algebraic notation (string)."""
        return self._pos

    def get_role(self):
        """Returns the current role/type of the piece (string)."""
        return self._role

    # ***** SETTERS *****

    def set_pos(self, pos):
        """Sets the piece's position attribute to value passed in as a parameter.
        The position should be a string in algebraic notation. Returns nothing."""
        self._pos = pos

    # ***** METHODS *****

    def in_palace(self, pos):
        """Returns True if the given position is within the palace of either team,
        otherwise returns False. The position should be given as a string in
        algebraic notation."""

        palace_areas = ['d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3',
                        'd8', 'e8', 'f8', 'd9', 'e9', 'f9', 'd10', 'e10', 'f10']

        return pos in palace_areas

    def within_board(self, pos):
        """Given a position in algebraic notation, returns True if the pos is
        within the boundaries of the game board and False if not. The game
        board has columns a-i and rows 1-10."""

        # Column (first character in string of alg position) between a-i
        # Row (rest of string, number) between 1-10
        if pos[0].lower() > "i" or pos[0].lower() < "a" \
                or int(pos[1:]) > 10 or int(pos[1:]) < 1:

            return False

        return True

    def translate_to_list_coords(self, pos):
        """Translates coordinates given in algebraic notation (pos) to a form
        which can be used to access the corresponding board coordinates.
        Returns a list with [row, col] numbers."""

        # pos is passed in as a string with the column letter first, then row number.
        # Example: 'a10' --> a = first column, 10 = 10th row
        col_letter = pos[0].lower()
        col_to_int = int(ord(col_letter) - 97)
        row_to_int = int(pos[1:]) - 1

        # Return row first, since we access the board list via board[row][col]
        return [row_to_int, col_to_int]

    def translate_to_alg_coords(self, list_pos):
        """Translates coordinates given as a list with [row, col] numbers
        back to algebraic notation (such as [0, 0] to 'a1'). Returns the
        algebraic coordinates as a string."""

        # list_pos would be something like [1, 3]
        # first element = row, second element = column
        row = list_pos[0]
        col = list_pos[1]

        # Add one for row since list coordinates start at zero but alg.
        # notation starts at 1
        row_str = str(row + 1)

        # Add 97 to get the character code. 0 -> a, 1 -> b, etc.
        col_str = str(chr(col + 97))

        return col_str + row_str

    def calc_x_pos(self):
        pos = self.translate_to_list_coords(self.get_pos())
        x_pos = (pos[1] * 50) + 50
        return x_pos

    def calc_y_pos(self):
        pos = self.translate_to_list_coords(self.get_pos())
        y_pos = (pos[0] * 50) + 50
        return y_pos

    def draw(self, win):
        if type(self) == General:
            if self.get_color() == "R":
                gen = pygame.image.load("images/RedGG.png")
                pygame.Surface.blit(win, gen, (self.calc_x_pos() - 23, self.calc_y_pos() - 23))
            if self.get_color() == "B":
                gen = pygame.image.load("images/BlueGG.png")
                pygame.Surface.blit(win, gen, (self.calc_x_pos() - 23, self.calc_y_pos() - 23))

        elif type(self) == Soldier:
            if self.get_color() == "R":
                piece = pygame.image.load("images/RedSO.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 14, self.calc_y_pos() - 14))
            if self.get_color() == "B":
                piece = pygame.image.load("images/BlueSO.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 14, self.calc_y_pos() - 14))

        elif type(self) == Guard:
            if self.get_color() == "R":
                piece = pygame.image.load("images/RedGD.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 14, self.calc_y_pos() - 14))
            if self.get_color() == "B":
                piece = pygame.image.load("images/BlueGD.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 14, self.calc_y_pos() - 14))

        elif type(self) == Chariot:
            if self.get_color() == "R":
                piece = pygame.image.load("images/RedCH.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 22, self.calc_y_pos() - 22))
            if self.get_color() == "B":
                piece = pygame.image.load("images/BlueCH.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 22, self.calc_y_pos() - 22))

        elif type(self) == Elephant:
            if self.get_color() == "R":
                piece = pygame.image.load("images/RedEL.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 22, self.calc_y_pos() - 22))
            if self.get_color() == "B":
                piece = pygame.image.load("images/BlueEL.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 22, self.calc_y_pos() - 22))

        elif type(self) == Horse:
            if self.get_color() == "R":
                piece = pygame.image.load("images/RedHO.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 22, self.calc_y_pos() - 22))
            if self.get_color() == "B":
                piece = pygame.image.load("images/BlueHO.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 22, self.calc_y_pos() - 22))

        elif type(self) == Cannon:
            if self.get_color() == "R":
                piece = pygame.image.load("images/RedCN.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 22, self.calc_y_pos() - 22))
            if self.get_color() == "B":
                piece = pygame.image.load("images/BlueCN.png")
                pygame.Surface.blit(win, piece, (self.calc_x_pos() - 22, self.calc_y_pos() - 22))


        else:
            pygame.draw.circle(win, (0, 0, 0), (self.calc_x_pos(), self.calc_y_pos()), 20)

    def what_is_selected(self, win):
        """Highlights a piece that is clicked on, displays the English name of the piece."""
        if type(self) == General:
            return "General"

        elif type(self) == Soldier:
            return "Soldier"

        elif type(self) == Guard:
            return "Guard"

        elif type(self) == Chariot:
            return "Chariot"

        elif type(self) == Elephant:
            return "Elephant"

        elif type(self) == Horse:
            return "Horse"

        elif type(self) == Cannon:
            return "Cannon"


class Soldier(Piece):
    """Represents a Soldier piece in the game. Inherits from the Piece class.
    Please see Piece class description for details on how this object type
    interacts with the JanggiGame class and for descriptions of all the
    common Piece methods the Soldier has access to. Contains a method to determine
    possible moves for this piece type based on the piece's current location.
    The possible moves follow the rules for the Soldier's allowed move pattern,
    but does not take into account the current conditions/state of the board
    currently in play. Please see possible_moves for additional details on this."""

    def __init__(self, color, pos):
        """Initializes a game piece of the Soldier type. Color and starting
        position are passed in as parameters. Role is set automatically to SO."""
        super().__init__(color, pos)
        self._role = "SO"

    def possible_moves(self):
        """Returns a list of allowed moves based on the Soldier's current position.
        does not check if the space is occupied, but does omit spaces off-board.
        Soldiers may only advance toward the opposing team's side and may only do so
        one square at a time. Soldiers may move forward along diagonals if they are
        within the Palace area.

        This method does not communicate with the JanggiGame class to take into
        account the position of other pieces on the board, instead it simply provides
        a list of all possible positions the Soldier could move to on an empty board.
        Methods in the JanggiGame class then use this information to determine which
        of the possible moves are actually valid given the current setup of pieces
        on the active game board."""

        pos = self.get_pos()
        coords = self.translate_to_list_coords(pos)
        row = coords[0]
        col = coords[1]
        possible_moves = []
        possible_moves_alg = []
        possible_moves_final = []

        if self.get_color() == "R":
            possible_moves.append([row + 1, col])
            possible_moves.append([row, col + 1])
            possible_moves.append([row, col - 1])

            # If they are in the palace, a diagonal move is allowed,
            # from the corner spots or the center, but the soldier
            # must still only move forward, therefore this only applies
            # if the soldier's current position is d8, f8, or e9
            if pos == 'd8':
                possible_moves.append([row + 1, col + 1])
            elif pos == 'f8':
                possible_moves.append([row + 1, col - 1])
            elif pos == 'e9':
                possible_moves.append([row + 1, col + 1])
                possible_moves.append([row + 1, col - 1])

        # Advancing direction switches for Blue
        if self.get_color() == "B":
            possible_moves.append([row - 1, col])
            possible_moves.append([row, col + 1])
            possible_moves.append([row, col - 1])

            # If they are in the palace, a diagonal move is allowed,
            # from the corner spots or the center, but the soldier
            # must still only move forward, therefore this only applies
            # if the soldier's current position is d3, f3, or e2
            if pos == 'd3':
                possible_moves.append([row - 1, col + 1])
            elif pos == 'f3':
                possible_moves.append([row - 1, col - 1])
            elif pos == 'e2':
                possible_moves.append([row - 1, col + 1])
                possible_moves.append([row - 1, col - 1])

        # Translate from list coords to algebraic
        for move in possible_moves:
            possible_moves_alg.append(self.translate_to_alg_coords(move))

        # Check that the moves returned are within the board limits
        for i in range(len(possible_moves_alg)):
            if self.within_board(possible_moves_alg[i]):
                possible_moves_final.append([possible_moves_alg[i]])

        return possible_moves_final

class Horse(Piece):
    """Represents a Horse piece in the game. Inherits from the Piece class.
    Please see Piece class description for details on how this object type
    interacts with the JanggiGame class and for descriptions of all the
    common Piece methods the Horse has access to. Contains a method to determine
    possible moves for this piece type based on the piece's current location.
    A Horse can move one step orthogonally (left, right, up, down) and one step
    diagonally, in that order only. The possible moves follow the rules for
    the Horse's allowed move pattern, but does not take into account the current
    conditions/state of the board currently in play. Please see possible_moves
    for additional details on this."""

    def __init__(self, color, pos):
        """Initializes a game piece of the Horse type. Color and starting
        position are passed in as parameters. Role is automatically set."""

        super().__init__(color, pos)
        self._role = "HO"

    def possible_moves(self):
        """Returns a list of allowed moves and their path to get there (not including
        the starting space) based on the Horse's current position. This method
        does not check if the space is occupied, but does omit spaces off-board.
        A Horse can move one step orthogonally (left, right, up, down) and one step
        diagonally, in that order only. The diagonal portion of the move must be "outward",
        that is, in the direction the Horse was already heading (like a Y). The Horse
        cannot jump over other pieces, the entire pathway must be clear in order to
        complete the move (unless it's capturing an enemy piece on the last position
        of it's move, but it cannot be blocked by a piece of either color on its way there).

        This method does not communicate with the JanggiGame class to take into
        account the position of other pieces on the board, instead it simply provides
        a list of all possible positions the Horse could move to on an empty board.
        Methods in the JanggiGame class then use this information to determine which
        of the possible moves are actually valid given the current setup of pieces
        on the active game board."""

        pos = self.get_pos()
        coords = self.translate_to_list_coords(pos)
        row = coords[0]
        col = coords[1]
        possible_moves = []
        possible_moves_alg = []
        possible_moves_final = []

        # Horses are not limited to forward only motion like soldiers,
        # so we do not need to check the piece color.

        # "U" (up) in the notes below means closer to the red side of the board
        possible_moves.append([[row - 1, col], [row - 2, col + 1]])     # 1U 1R
        possible_moves.append([[row - 1, col], [row - 2, col - 1]])     # 1U 1L
        possible_moves.append([[row, col + 1], [row - 1, col + 2]])     # 1R 1U
        possible_moves.append([[row, col + 1], [row + 1, col + 2]])     # 1R 1D
        possible_moves.append([[row, col - 1], [row - 1, col - 2]])     # 1L 1U
        possible_moves.append([[row, col - 1], [row + 1, col - 2]])     # 1L 1D
        possible_moves.append([[row + 1, col], [row + 2, col + 1]])     # 1D 1R
        possible_moves.append([[row + 1, col], [row + 2, col - 1]])     # 1D 1L

        for move in range(len(possible_moves)):
            temp = []
            for square in range(len(possible_moves[move])):
                temp.append(self.translate_to_alg_coords(possible_moves[move][square]))
            possible_moves_alg.append(temp)

        # Check if any part of each possible move is outside the board
        for move in range(len(possible_moves_alg)):
            temp = []
            if self.within_board(possible_moves_alg[move][0]) and self.within_board(possible_moves_alg[move][1]):
                temp.append(possible_moves_alg[move][0])
                temp.append(possible_moves_alg[move][1])
            # Do not add empty lists to the results
            if temp:
                possible_moves_final.append(temp)

        # Final list is in format [ [ step 1, step 2 ] , [ step 1, step 2 ] ],
        # where step 1 is an intermediate stop along the way to step 2
        return possible_moves_final

class General(Piece):
    """Represents a General piece in the game. Inherits from the Piece class.
    Please see Piece class description for details on how this object type
    interacts with the JanggiGame class and for descriptions of all the
    common Piece methods the General has access to.

    Contains a method to determine possible moves for this piece type based
    on the piece's current location. A General can move only within the
    Palace, and only one step at a time. The General can move orthogonally within
    the Palace or diagonally (where there is a diagonal line within the Palace).
    The possible moves follow the rules for the General's allowed move pattern,
    but does not take into account the current conditions/state of the board
    currently in play. Please see possible_moves for additional details on this.

    Methods to handle special situation involving the Generals (such as seeing
    if the General is in check or is in checkmate) is included in the JanggiGame
    class, which has knowledge of the current state/layout/other pieces present
    on the board."""

    def __init__(self, color, pos):
        """Initializes a game piece of the General type. Color and starting
        position are passed in as parameters. Role is set automatically."""

        super().__init__(color, pos)
        self._role = "GG"

    def possible_moves(self):
        """Returns a list of allowed moves and their path to get there (not including
        the starting space) based on the General's current position. This method
        does not check if the space is occupied, but does omit spaces off-board.
        A General can move only within the Palace, and only one step at a time.
        The General can move orthogonally within the Palace or diagonally (where
        there is a diagonal line within the Palace). For the purposes of this assignment,
        Generals are allowed to be "in sight" of one another, meaning if they are
        in the same column, there does not need to be another piece also in that
        column obstructing the "line of sight" between the Generals.

        This method does not communicate with the JanggiGame class to take into
        account the position of other pieces on the board, instead it simply provides
        a list of all possible positions the General could move to on an empty board.
        Methods in the JanggiGame class then use this information to determine which
        of the possible moves are actually valid given the current setup of pieces
        on the active game board."""

        pos = self.get_pos()
        coords = self.translate_to_list_coords(pos)
        row = coords[0]
        col = coords[1]
        possible_moves = []
        possible_moves_alg = []
        possible_moves_final = []

        # Orthagonal moves for General
        possible_moves.append([row - 1, col])       # 1U
        possible_moves.append([row + 1, col])       # 1D
        possible_moves.append([row, col + 1])       # 1R
        possible_moves.append([row, col - 1])       # 1L

        # If in a pos where diagonal moves are possible within the Palace, add those
        if pos == 'd1' or pos == 'd8':
            possible_moves.append([row + 1, col + 1])     # 1D 1R
        elif pos == 'f1' or pos == 'f8':
            possible_moves.append([row + 1, col - 1])     # 1D 1L
        elif pos == 'd3' or pos == 'd10':
            possible_moves.append([row - 1, col + 1])     # 1U 1R
        elif pos == 'f3' or pos == 'f10':
            possible_moves.append([row - 1, col - 1])     # 1U 1L
        # Can move along any diagonal if in center of Palace
        elif pos == 'e2' or pos == 'e9':
            possible_moves.append([row + 1, col + 1])     # 1D 1R
            possible_moves.append([row + 1, col - 1])     # 1D 1L
            possible_moves.append([row - 1, col + 1])     # 1U 1R
            possible_moves.append([row - 1, col - 1])     # 1U 1L

        for move in possible_moves:
            possible_moves_alg.append(self.translate_to_alg_coords(move))

        # When list of possible moves is generated, check on board AND in palace.
        for i in range(len(possible_moves_alg)):
            if self.within_board(possible_moves_alg[i]):
                if self.in_palace(possible_moves_alg[i]):
                    possible_moves_final.append([possible_moves_alg[i]])

        return possible_moves_final

class Guard(General):
    """Guards inherit from the General class, since a Guard moves with the same
    restrictions/patterns as the General, therefore the same possible_moves logic
    may be used. Please see the General class for further detail on move logic.
    This class also has access to all the methods in the generic Piece class.

    A Guard can move only within the Palace, and only one step at a time.
    The Guard can move orthogonally within the Palace or diagonally
    (where there is a diagonal line within the Palace)."""

    def __init__(self, color, pos):
        """Initializes a game piece of the General type. Color and starting
        position are passed in as parameters. Role set automatically."""

        super().__init__(color, pos)
        self._role = "GD"

class Chariot(Piece):
    """Represents a Chariot piece in the game. Inherits from the Piece class.
    Please see Piece class description for details on how this object type
    interacts with the JanggiGame class and for descriptions of all the
    common Piece methods the General has access to.

    Contains a method to determine possible moves for this piece type based
    on the piece's current location. The Chariot moves in a straight line
    either horizontally or vertically to capture other pieces. It may move diagonally
    within the Palace, but only in a straight line (can't switch from diagonal to
    orthogonal). The Chariot may move as many spaces as they wish and do not have to
    keep going till they are at the end of the game board or are obstructed by another
    piece. The Chariot is not limited to advancing only, and can move backwards.
    The possible moves follow the rules for the Chariot's allowed move pattern,
    but does not take into account the current conditions/state of the board
    currently in play. Please see possible_moves for additional details on this.
    """

    def __init__(self, color, pos):
        """Initializes a game piece of the Chariot type. Color and starting
        position are passed in as parameters. Role is set automatically."""

        super().__init__(color, pos)
        self._role = "CH"

    def possible_moves(self):
        """Returns a list of allowed moves and their path to get there (not including
        the starting space) based on the Chariot's current position. This method
        does not check if the space or path is occupied, but does omit spaces off-board.
        Chariots may move as many spaces as they wish (orthogonal, or diagonal within Palace)
        and do not have to keep going till they are at the end of the game board or
        are obstructed by another piece. The Chariot is not limited to advancing only,
        and can move backwards. *Note that this same method is used for determining
        possible Cannon moves.*

        This method does not communicate with the JanggiGame class to take into
        account the position of other pieces on the board, instead it simply provides
        a list of all possible positions the Chariot could move to on an empty board.
        Methods in the JanggiGame class then use this information to determine which
        of the possible moves are actually valid given the current setup of pieces
        on the active game board."""

        pos = self.get_pos()
        coords = self.translate_to_list_coords(pos)
        row = coords[0]
        col = coords[1]
        possible_moves = []
        possible_moves_alg = []

        # Moving up (max move length = current row to 0 = # of current row)
        move_len_up = 1
        for i in range(0, row + 1):
            temp = []
            for j in range(1, move_len_up):
                temp.append([row - j, col])
            move_len_up += 1
            if temp:
                possible_moves.append(temp)

        # Moving down (max move length = current row to 9 = 9-current row)
        move_len_down = 1
        for i in range(0, (9 - row) + 1):
            temp = []
            for j in range(1, move_len_down):
                temp.append([row + j, col])
            move_len_down += 1
            if temp:
                possible_moves.append(temp)

        # Moving right (max move length = current col to i(8) = 8-current col)
        move_len_right = 1
        for i in range(0, (8 - col) + 1):
            temp = []
            for j in range(1, move_len_right):
                temp.append([row, col + j])
            move_len_right += 1
            if temp:
                possible_moves.append(temp)

        # Moving left (max move length = current col to a(0) = # of current col)
        move_len_left = 1
        for i in range(0, col + 1):
            temp = []
            for j in range(1, move_len_left):
                temp.append([row, col - j])
            move_len_left += 1
            if temp:
                possible_moves.append(temp)

        # If the chariot is starting within the Palace, limited diagonal moves are available.
        if pos == 'd1' or pos == 'd8':
            first_step = [row + 1, col + 1]
            possible_moves.append([first_step])
            possible_moves.append([first_step, [row + 2, col + 2]])
        elif pos == 'f1' or pos == 'f8':
            first_step = [row + 1, col - 1]
            possible_moves.append([first_step])
            possible_moves.append([first_step, [row + 2, col - 2]])
        elif pos == 'd3' or pos == 'd10':
            first_step = [row - 1, col + 1]
            possible_moves.append([first_step])
            possible_moves.append([first_step, [row - 2, col + 2]])
        elif pos == 'f3' or pos == 'f10':
            first_step = [row - 1, col - 1]
            possible_moves.append([first_step])
            possible_moves.append([first_step, [row - 2, col - 2]])
        elif pos == 'e2' or pos == 'e9':
            possible_moves.append([[row - 1, col + 1]])   # 1U 1R
            possible_moves.append([[row - 1, col - 1]])   # 1U 1L
            possible_moves.append([[row + 1, col + 1]])   # 1D 1R
            possible_moves.append([[row + 1, col - 1]])   # 1D 1L

        # Translate to alg space numbers
        for move in range(len(possible_moves)):
            temp = []
            for square in range(len(possible_moves[move])):
                temp.append(self.translate_to_alg_coords(possible_moves[move][square]))
            possible_moves_alg.append(temp)

        # Above logic only generates spaces on board, do not need extra check
        return possible_moves_alg

class Cannon(Chariot):
    """Represents a Cannon piece in the game. Inherits from the Chariot class,
    which also inherits from the generic Piece class. Please see Piece class
    description for details on how this object type interacts with the JanggiGame
    class and for descriptions of all the common Piece methods the Cannon has access to.

    This piece moves similarly to the Chariot, except that there must be another
    piece in the Cannon's path for the Cannon to "jump" over. As long as there
    is a piece to jump over, the Cannon may move in a straight line either horizontally
    or vertically to capture other pieces. It may move diagonally within the Palace,
    but only in a straight line (can't switch from diagonal to orthogonal). Cannons
    may not jump over other Cannons nor may they capture another Cannon.

    Note that the possible_moves method is inherited from the Chariot class, and
    DOES NOT check if there is an appropriate piece to jump over, rather this is
    checked in the JanggiGame class which has knowledge of the other pieces on the
    board/current positions/game state in the check_move and make_move methods."""

    def __init__(self, color, pos):
        """Initializes a game piece of the Cannon type. Color and starting
        position are passed in as parameters. Role is set automatically."""

        super().__init__(color, pos)
        self._role = "CN"

class Elephant(Piece):
    """Represents an Elephant piece in the game. Inherits from the Piece class.
    Please see Piece class description for details on how this object type
    interacts with the JanggiGame class and for descriptions of all the
    common Piece methods the General has access to.

    Contains a method to determine possible moves for this piece type based
    on the piece's current location. An Elephant can move one step orthogonally
    (left, right, up, down) and two steps diagonally (in the same direction),
    in that order only. The possible moves follow the rules for the Elephant's
    allowed move pattern, but does not take into account the current
    conditions/state of the board currently in play. Please see possible_moves
    for additional details on this."""

    def __init__(self, color, pos):
        """Initializes a game piece of the Elephant type. Color and starting
        position are passed in as parameters. Role is set automatically."""

        super().__init__(color, pos)
        self._role = "EL"

    def possible_moves(self):
        """Returns a list of allowed moves and their path to get there (not including
        the starting space) based on the Elephant's current position. This method
        does not check if the space is occupied, but does omit spaces off-board.
        An Elephant can move one step orthogonally (left, right, up, down) and two
        steps diagonally (in the same direction), in that order only. The diagonal
        portion of the move must be "outward", that is, in the direction the
        Elephant was already heading (like a Y). The Elephant cannot jump over other
        pieces, the entire pathway must be clear in order to complete the move
        (unless it's capturing an enemy piece on the last position of its move,
        but it cannot be blocked by a  piece of either color on its way there).

        This method does not communicate with the JanggiGame class to take into
        account the position of other pieces on the board, instead it simply provides
        a list of all possible positions the Elephant could move to on an empty board.
        Methods in the JanggiGame class then use this information to determine which
        of the possible moves are actually valid given the current setup of pieces
        on the active game board."""

        pos = self.get_pos()
        coords = self.translate_to_list_coords(pos)
        row = coords[0]
        col = coords[1]
        possible_moves = []
        possible_moves_alg = []
        possible_moves_final = []

        # Elephants are not limited to forward only motion like soldiers,
        # so we do not need to check the piece color.

        # "U" (up) in the notes below means closer to the red side of the board
        possible_moves.append([[row - 1, col], [row - 2, col + 1], [row - 3, col + 2]])  # 1U 2R
        possible_moves.append([[row - 1, col], [row - 2, col - 1], [row - 3, col - 2]])  # 1U 2L
        possible_moves.append([[row, col + 1], [row - 1, col + 2], [row - 2, col + 3]])  # 1R 2U
        possible_moves.append([[row, col + 1], [row + 1, col + 2], [row + 2, col + 3]])  # 1R 2D
        possible_moves.append([[row, col - 1], [row - 1, col - 2], [row - 2, col - 3]])  # 1L 2U
        possible_moves.append([[row, col - 1], [row + 1, col - 2], [row + 2, col - 3]])  # 1L 2D
        possible_moves.append([[row + 1, col], [row + 2, col + 1], [row + 3, col + 2]])  # 1D 2R
        possible_moves.append([[row + 1, col], [row + 2, col - 1], [row + 3, col - 2]])  # 1D 2L

        for move in range(0, len(possible_moves)):
            temp = []
            for square in range(0, len(possible_moves[move])):
                temp.append(self.translate_to_alg_coords(possible_moves[move][square]))
            possible_moves_alg.append(temp)

        # Check if any part of each possible move is outside the board
        for move in range(0, len(possible_moves_alg)):
            temp = []
            for square in range(0, len(possible_moves_alg[move])):
                if self.within_board(possible_moves_alg[move][square]):
                    temp.append(possible_moves_alg[move][square])
            # Do not add incomplete lists to the results (Elephant can't execute
            # only part of its move, whole sequence has to be completed)
            if len(temp) >= 3:
                possible_moves_final.append(temp)

        # Final list is in format [ [ step 1, step 2, step 3 ] , [ step 1, step 2, step 3 ] ],
        # where steps 1 and 2 are intermediate stops along the way to final square.
        return possible_moves_final

class NoPiece(Piece):
    """Represents a placeholder for a blank/open space in the game. NoPiece objects are
    represented as a " + " on the board display. They have no valid role or team/color
    affiliation. NoPiece objects cannot be moved, and logic in the JanggiGame class will
    not permit this action. NoPiece objects are utilized in the JanggiGame class when
    a piece moves to a new location, to fill the position the piece just vacated."""

    def __init__(self, pos):
        """Initializes a game piece of the NoPiece type. Only the pos (in algebraic
        notation is needed for initialization, since the NoPiece has no valid color
        or role information."""

        self._color = "X"
        self._pos = pos
        self._role = "XX"

    def __repr__(self):
        """Defines how the NoPiece object is represented , a 3 character string
        to match the length of the other piece types and make aligning the board
        display simpler. Returns a string " + ". """

        return str(" + ")








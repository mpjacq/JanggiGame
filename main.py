# Author: Madeline Jacques
# Date: March 2021
#
# Janggi is an implementation of a Korean variant of chess by the same name,
# built in Python. My version includes a GUI (via PyGame) for a clickable
# interface. The interface includes some useful features such as move
# highlighting according to a piece's allowed move pattern and the state
# of other pieces on the board.
#
# Background image is public domain, source:
# https://www.publicdomainpictures.net/en/view-image.php?image=209094&picture=natural-wood-grain-background
# Game piece images are from Wikimedia Commons, source:
# https://commons.wikimedia.org/wiki/Category:Janggi_pieces

import pygame
import Janggi

pygame.init()

# Some defaults needed for the game
run_speed = 60
WIDTH = 500
HEIGHT = 620
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Janggi by mpjacq")
font = pygame.font.SysFont("georgia", 15)
help_font = pygame.font.SysFont("georgia", 25)
big_font = pygame.font.SysFont("georgia", 80)

def draw_board(win):
    """Draws the game board, which is a 10h x 9w grid. Pieces are placed
    at the intersections of lines. The Palace is a special area on the board
    where the Generals and Guards reside. Some pieces are able to make special
    moves along the diagonals in the Palace."""

    background = pygame.image.load("images/natural-wood-grain-background-14903911355WD.jpg")

    win.blit(background, (0, 0))

    # Draw vertical lines
    for i in range(49, 450, 50):
        pygame.draw.line(win, (0, 0, 0), (i, 49), (i, 499), width=2)

    # Draw horizontal lines
    for j in range(49, 500, 50):
        pygame.draw.line(win, (0, 0, 0), (49, j), (449, j), width=2)

    # Draw Palace diagonals
    pygame.draw.line(win, (0, 0, 0), (199, 49), (299, 149), width=2)
    pygame.draw.line(win, (0, 0, 0), (299, 49), (200, 149), width=2)
    pygame.draw.line(win, (0, 0, 0), (200, 399), (299, 499), width=2)
    pygame.draw.line(win, (0, 0, 0), (200, 499), (299, 399), width=2)

    # # Draw re-set button
    # re_set = font.render("Start Over", True, (0, 0, 0))
    # re_set_rect = re_set.get_rect(center=(WIDTH/ 2, 540))
    # pygame.draw.rect(win, (255, 255, 255), re_set_rect)
    # window.blit(re_set, re_set_rect)

def get_coords_from_click(pos):
    """When given a position in mouse-click coordinates (as a tuple),
    translates to a row, column position on the game board, and
    returns these simplified coordinates."""

    # pos will come in as a tuple
    x, y = pos
    row = (y - 25) // 50
    col = (x - 25) // 50

    return row, col

def main():
    """Main game loop. Games start by showing the help screen."""

    run = True
    clock = pygame.time.Clock()
    game = Janggi.JanggiGame()
    selected_piece = None
    help_bkg = pygame.image.load("images/Help_Screen.jpg")
    tips_open = True
    re_start_game = False

    move_msg = ""

    while run:

        clock.tick(run_speed)

        # Draw the board and pieces
        draw_board(window)
        game.draw_pieces(window)

        # Draw the help button
        help_me = help_font.render("?", True, (0, 0, 0))
        help_me_rect = help_me.get_rect(center=(WIDTH - 15, 15))

        # help_button is referred to later to detect collision/click
        help_button = window.blit(help_me, help_me_rect)

        # Draw re-set button
        re_set = font.render("Start Over", True, (0, 0, 0))
        re_set_rect = re_set.get_rect(center=(WIDTH/ 2, 540))
        
        # re_set_button is referred to later to detect collision/click
        re_set_button = window.blit(re_set, re_set_rect)

        # Draw the help menu, exit by clicking anywhere
        # Will always display when game is first opened
        if tips_open:

            # Re-set move message so it does not overlay help info
            move_msg = ""

            window.blit(help_bkg, (25, 28))

            for help_event in pygame.event.get():

                if help_event.type == pygame.MOUSEBUTTONDOWN:
                    tips_open = False

        # Click Start Over to re-set the game
        if re_start_game:

            # Create a new Janggi Game/overwrite current
            game = Janggi.JanggiGame()

            # Clear selected piece
            selected_piece = None

            # Switch back re_start_game bool 
            re_start_game = False

            # Confirmation message
            move_msg = "Game re-started."

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            # Left click to select a piece and see possible moves
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                
                pos = pygame.mouse.get_pos()

                # Clicking help button allows help info to display
                if help_button.collidepoint(pos):
                    tips_open = True

                # Clicking re-set button starts game over
                if re_set_button.collidepoint(pos):
                    re_start_game = True

                # Translate from precise mouse position to general row/col notation
                row1, col1 = get_coords_from_click(pos)

                # Janggi game logic relies on algebraic coordinates such as
                # 'a1', 'b3', to define positions on the game board and make moves
                alg1 = game.translate_to_alg_coords([row1, col1])

                # Display a message if clicking outside the board bounds
                if (row1 < 0 or row1 > 9) or (col1 < 0 or col1 > 8):
                    move_msg = "Clicked position is outside of game board."

                # Confirm if a valid position was selected, store the piece
                # at that location if applicable
                else:
                    move_msg = f"Selected position at {alg1}"
                    selected_piece = game.get_board()[row1][col1]

            # Right click to make a move
            # Check if there is actually a piece there before attempting move
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and type(selected_piece) != Janggi.NoPiece:

                # Store end position
                pos2 = pygame.mouse.get_pos()

                # Get row/col coordinates
                row2, col2 = get_coords_from_click(pos2)

                # Translate to algebraic coordinates
                alg2 = game.translate_to_alg_coords([row2, col2])

                # make_move in Janggi.py returns a message depending on if move
                # was successful, if it was not allowed, etc.
                move_msg = str(game.make_move(alg1, alg2))

                # Clear stored piece so next one can be selected
                selected_piece = None

        # Display piece name if one is selected, show possible moves on board
        # Pieces are selected when first (left) click has been executed, but not
        # yet right clicked to complete a move.
        if selected_piece:
            move_msg = selected_piece.what_is_selected()
            game.draw_possible_moves(selected_piece, window)

        # Draw move message (confirming move or showing why move can't be made)
        move_result = font.render(move_msg, True, (0, 0, 0))
        move_result_rect = move_result.get_rect(center=(WIDTH / 2, 575))
        window.blit(move_result, move_result_rect)

        # Turn indicator at top of screen
        if game.get_turn() == "B":
            pygame.draw.circle(window, (0, 0, 255), ((WIDTH/2) + 1, 15), 10)
        else:
            pygame.draw.circle(window, (255, 0, 0), ((WIDTH/2) + 1, 15), 10)

        # Warning message if either General is in check
        if game.is_in_check("red"):
            chk_msg = "Red General is in check!"
        
        elif game.is_in_check("blue"):
            chk_msg = "Blue General is in check!"
        
        else:
            chk_msg = None

        # Win message if a player has won
        if game.get_game_state() == "RED_WON":
            win_msg = "RED WON!"
            win_msg_color = (255, 0, 0)
        
        elif game.get_game_state() == "BLUE_WON":
            win_msg = "BLUE WON!"
            win_msg_color = (0, 0, 255)
        
        else:
            win_msg = None
            win_msg_color = None

        # Display message if a General is in check
        if chk_msg is not None:
            
            line2 = font.render(chk_msg, True, (0, 0, 0))
            center_line2 = line2.get_rect(center=(WIDTH / 2, 600))
            window.blit(line2, center_line2)

        # Display message if we have a winner
        if win_msg is not None:
            
            win_banner = big_font.render(win_msg, True, win_msg_color)
            center_win_banner = win_banner.get_rect(center=(WIDTH / 2, 250))
            window.blit(win_banner, center_win_banner)

        pygame.display.update()

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
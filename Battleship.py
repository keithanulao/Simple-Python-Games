import random
import pygame

# Define some colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define board size
BOARD_SIZE = 7

# Define cell size
CELL_SIZE = 50

# Define ship sizes (length)
SHIP_SIZES = [5, 4, 3, 3, 2]


def create_board():
  """
  Creates a 2D list representing the game board.
  0 - Empty cell
  1 - Player's ship
  2 - Missed shot
  3 - Hit ship
  """
  board = []
  for _ in range(BOARD_SIZE):
    row = [0] * BOARD_SIZE
    board.append(row)
  return board


def draw_board(screen, board):
  """
  Draws the game board on the screen, including grid lines.
  """
  # Draw cell colors based on board state
  for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
      color = GRAY
      if board[row][col] == 2:
        color = RED  # Missed shot
      elif board[row][col] == 3:
        color = GREEN  # Hit ship
      pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

  # Draw grid lines
  for i in range(1, BOARD_SIZE):
    # Horizontal lines
    pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (BOARD_SIZE * CELL_SIZE, i * CELL_SIZE), 1)
    # Vertical lines
    pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE * CELL_SIZE), 1)


def place_ships(board, ship_sizes):
  """
  Randomly places ships on the board following the specified sizes.
  """
  for ship_size in ship_sizes:
    # Keep trying until a valid placement is found
    while True:
      row = random.randint(0, BOARD_SIZE - 1)
      col = random.randint(0, BOARD_SIZE - 1)
      horizontal = random.randint(0, 1)  # 0 - Vertical, 1 - Horizontal

      # Check if placement is valid (doesn't overlap other ships)
      valid = True
      for i in range(ship_size):
        if horizontal:
          if col + i >= BOARD_SIZE or board[row][col + i] != 0:
            valid = False
            break
        else:
          if row + i >= BOARD_SIZE or board[row + i][col] != 0:
            valid = False
            break

      if valid:
        # Place the ship on the board
        for i in range(ship_size):
          if horizontal:
            board[row][col + i] = 1
          else:
            board[row + i][col] = 1
        break


def get_player_move(screen, board=None):
  cell_size = CELL_SIZE
  cells = []  # List of rectangles for each cell
  for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
      x = col * cell_size
      y = row * cell_size
      cells.append(pygame.Rect(x, y, cell_size, cell_size))

  while True:
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        for i, cell in enumerate(cells):
          if cell.collidepoint(pos):
            cell_x, cell_y = i // BOARD_SIZE, i % BOARD_SIZE  # Calculate cell index from list position
            return cell_x, cell_y
    screen.fill(BLACK)
    draw_board(screen, board)
    pygame.display.flip()


def check_win(board):
  """
  Checks if all the player's ships have been sunk.
  """
  for row in board:
    for cell in row:
      if cell == 1:  # Player's ship still afloat
        return False
  return True


def main():
  pygame.init()

  # Set screen size
  screen_width = BOARD_SIZE * CELL_SIZE
  screen_height = BOARD_SIZE * CELL_SIZE
  screen = pygame.display.set_mode((screen_width, screen_height))
  pygame.display.set_caption("Battleship (Practice)")

  # Create the game board
  board = create_board()
  place_ships(board, SHIP_SIZES.copy())  # Copy to avoid modifying original list

  # Game loop
  game_over = False
  while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:  # Added mouse click event
        # Handle events (e.g., exit game on QUIT, get player move on click)
            if event.type == pygame.QUIT:
                game_over = True

        # Player's turn
        row, col = get_player_move(screen, board)

        # Check if player's shot hit a ship
        if board[row][col] == 1:
            board[row][col] = 3  # Mark the hit ship
            # Check if all ships sunk
            if check_win(board):
                game_over = True
                print("You win!")
        else:
            board[row][col] = 2  # Mark the missed shot

        # Update the screen
        screen.fill(BLACK)
        draw_board(screen, board)
        pygame.display.flip()

    # Quit pygame
    pygame.quit()


if __name__ == "__main__":
  main()
  pygame.quit()

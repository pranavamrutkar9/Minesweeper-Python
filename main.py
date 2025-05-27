import random
import re

class Board:
    def __init__(self, board_size, mines):
        self.board_size = board_size
        self.mines = mines

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        mines_planted = 0
        while mines_planted < self.mines:
            loc = random.randint(0, self.board_size**2 - 1)
            row = loc//self.board_size
            col = loc%self.board_size

            if board[row][col] =='*':
                continue

            board[row][col]='*'
            mines_planted += 1

        return board

    def assign_values_to_board(self):
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_mines(r,c)

    def get_num_neighboring_mines(self, row,col):
        num_neighboring_mines = 0
        for r in range(max(0, row-1), min(self.board_size, row+2)):
            for c in range(max(0, col-1), min(self.board_size, col+2)):
                if r==row and c==col:
                    continue
                if self.board[r][c]=='*':
                    num_neighboring_mines+=1

        return num_neighboring_mines
    
    def dig(self, row, col):

        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0, row-1), min(self.board_size, row+2)):
            for c in range(max(0, col-1), min(self.board_size, col+2)):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)

        return True 

    def __str__(self):
        visible_board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range (self.board_size):
            for col in range (self.board_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        string_rep = ''
        widths = []
        for idx in range(self.board_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )
        
        indices = [i for i in range(self.board_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.board_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
    
def play(board_size = 10, mines = 10):
    board = Board(board_size, mines)

    safe = True
    while len(board.dug) < (board.board_size**2 - board.mines):
        print(board)
        user_input = input("Where to dig (row,col)?: ")
        try:
            row_str, col_str = user_input.split(',')
            row, col = int(row_str.strip()), int(col_str.strip())
        except ValueError:
            print("Invalid input! Please enter two numbers separated by a comma, e.g., 3,4.")
            continue

        if row < 0 or row >= board.board_size or col < 0 or col >= board.board_size:
            print("Invalid location")
            continue

        safe = board.dig(row,col)
        if not safe:
            break

    if safe:
        print("You won")
    else:
        print("Sorry! Game Over")

        board.dug = [(r,c) for r in range(board.board_size) for c in range(board.board_size)]
        print(board)


if __name__ == "__main__":
    play()

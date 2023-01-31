from pydantic import BaseModel
from enum import Enum
from fastapi import status, HTTPException


class Symbol(Enum):
    cross = 'x'
    zero = 'o'
    null = '*'


class CellName(Enum):
    top_left = 'top_left'
    top = 'top'
    top_right = 'top_right'

    left = 'left'
    center = 'center'
    right = 'right'

    bottom_left = 'bottom_left'
    bottom = 'bottom'
    bottom_right = 'bottom_right'


class GameField(BaseModel):
    top_left: str = Symbol.null.value
    top: str = Symbol.null.value
    top_right: str = Symbol.null.value

    left: str = Symbol.null.value
    center: str = Symbol.null.value
    right: str = Symbol.null.value

    bottom_left: str = Symbol.null.value
    bottom: str = Symbol.null.value
    bottom_right: str = Symbol.null.value

    waiting_symbol: str = Symbol.cross.value


    def show_field(self):
        field = f'{self.top_left} {self.top} {self.top_right}\n'\
                f'{self.left} {self.center} {self.right}\n'\
                f'{self.bottom_left} {self.bottom} {self.bottom_right}\n'\
                f'Wait for move: {self.waiting_symbol}'
        return field

    def update_field(self, cell_name: str, symbol: str):
        self.check_end_game('Your opponent has won.')
        self.check_bad_move(cell_name, symbol)

        self.__dict__[cell_name] = symbol
        if symbol == Symbol.cross.value:
            self.waiting_symbol = Symbol.zero.value
        else:
            self.waiting_symbol = Symbol.cross.value
        
        self.check_end_game('You win.')
        
    def check_bad_move(self, cell_name: str, symbol: str):
        if self.waiting_symbol != symbol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Wait for your turn'
            )
        if self.__dict__[cell_name] != Symbol.null.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='This cell is already busy'
            )

    def check_end_game(self, detail: str):
        if self.check_win_game():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=detail
            )
        if self.check_draw_game():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=detail
            )

    def check_win_game(self):
        if any([
            self.top_left == self.top == self.top_right != Symbol.null.value,
            self.left == self.center == self.right != Symbol.null.value,
            self.bottom_left == self.bottom == self.bottom_right != Symbol.null.value,
            self.top_left == self.center == self.bottom_right != Symbol.null.value,
            self.bottom_left == self.center == self.top_right != Symbol.null.value,
        ]):
            return True
    
    def check_draw_game(self):
        if Symbol.null.value not in self.__dict__.values():
            return True

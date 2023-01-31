from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from routers.user_auth import get_current_user
from schemas.game_field import CellName, GameField
from schemas.users import User


router = APIRouter(
    prefix='/game',
    )


game_field = GameField()


@router.get('/')
async def get_game_field() -> PlainTextResponse:
    return PlainTextResponse(
        content=game_field.show_field()
    )


@router.put('/update/{field_name}')
async def update_game_field(cell_name: CellName, User: User = Depends(get_current_user)) -> PlainTextResponse:
    game_field.update_field(cell_name.value, User.symbol)
    return PlainTextResponse(game_field.show_field())
    
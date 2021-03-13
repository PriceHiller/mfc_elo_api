from pydantic import BaseModel
from typing import Optional


class PlayerBase(BaseModel):
    pass


class Player(PlayerBase):
    player_name: Optional[str] = None
    steam_64: Optional[int] = None
    playfab_id: str


class GameData(Player):
    kills: int
    deaths: int
    assists: int
    rounds_played: int

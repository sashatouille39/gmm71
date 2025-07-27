from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class PlayerRole(str, Enum):
    NORMAL = "normal"
    SPORTIF = "sportif"
    PEUREUX = "peureux"
    BRUTE = "brute"
    INTELLIGENT = "intelligent"
    ZERO = "zero"

class EventType(str, Enum):
    INTELLIGENCE = "intelligence"
    FORCE = "force"
    AGILITE = "agilité"

class PlayerStats(BaseModel):
    intelligence: int = Field(..., ge=0, le=10)
    force: int = Field(..., ge=0, le=10)
    agilite: int = Field(..., ge=0, le=10)

class PlayerPortrait(BaseModel):
    face_shape: str
    skin_color: str
    hairstyle: str
    hair_color: str
    eye_color: str
    eye_shape: str

class PlayerUniform(BaseModel):
    style: str
    color: str
    pattern: str

class Player(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    number: str
    name: str
    nationality: str
    gender: str  # 'M' or 'F'
    role: PlayerRole
    stats: PlayerStats
    portrait: PlayerPortrait
    uniform: PlayerUniform
    alive: bool = True
    kills: int = 0
    betrayals: int = 0
    survived_events: int = 0
    total_score: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GameEvent(BaseModel):
    id: int
    name: str
    type: EventType
    difficulty: int = Field(..., ge=1, le=10)
    description: str

class EventResult(BaseModel):
    event_id: int
    event_name: str
    survivors: List[Dict[str, Any]]
    eliminated: List[Dict[str, Any]]
    total_participants: int

class Game(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    players: List[Player]
    events: List[GameEvent]
    current_event_index: int = 0
    completed: bool = False
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    event_results: List[EventResult] = []
    winner: Optional[Player] = None
    total_cost: int = 0
    earnings: int = 0

class GameStats(BaseModel):
    total_games_played: int = 0
    total_kills: int = 0
    total_betrayals: int = 0
    total_earnings: int = 0
    favorite_celebrity: Optional[str] = None
    has_seen_zero: bool = False

class GameState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = "default_user"  # Pour l'instant un seul utilisateur
    money: int = 50000
    vip_salon_level: int = 1
    unlocked_uniforms: List[str] = []
    unlocked_patterns: List[str] = []
    owned_celebrities: List[str] = []
    game_stats: GameStats = Field(default_factory=GameStats)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# VIP Models
class VipCharacter(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    mask: str
    personality: str
    dialogues: List[str]
    bets: int = 0
    favorite_player: Optional[str] = None
    total_winnings: int = 0

class Celebrity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: str
    stars: int = Field(..., ge=2, le=5)
    price: int
    nationality: str
    wins: int = 0
    stats: PlayerStats
    biography: str
    is_owned: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models
class PlayerCreateRequest(BaseModel):
    name: str
    nationality: str
    gender: str
    role: PlayerRole
    stats: PlayerStats
    portrait: PlayerPortrait
    uniform: PlayerUniform

class GameCreateRequest(BaseModel):
    player_count: int = Field(..., ge=20, le=1000)
    game_mode: str = "standard"
    selected_events: List[int]
    manual_players: List[PlayerCreateRequest] = []

class GameStateUpdate(BaseModel):
    money: Optional[int] = None
    vip_salon_level: Optional[int] = None
    unlocked_uniforms: Optional[List[str]] = None
    unlocked_patterns: Optional[List[str]] = None
    owned_celebrities: Optional[List[str]] = None
    game_stats: Optional[GameStats] = None

class PurchaseRequest(BaseModel):
    item_type: str  # 'uniform', 'pattern', 'celebrity'
    item_id: str
    price: int
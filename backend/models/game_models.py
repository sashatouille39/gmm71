from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
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
    AGILITÉ = "agilité"

class EventCategory(str, Enum):
    CLASSIQUES = "classiques"
    COMBAT = "combat"
    SURVIE = "survie"
    PSYCHOLOGIQUE = "psychologique"
    ATHLETIQUE = "athletique"
    TECHNOLOGIQUE = "technologique"
    EXTREME = "extreme"
    FINALE = "finale"

class PlayerStats(BaseModel):
    intelligence: int = Field(..., ge=0, le=10)
    force: int = Field(..., ge=0, le=10)
    agilité: int = Field(..., ge=0, le=10)

class PlayerPortrait(BaseModel):
    face_shape: str
    skin_color: str
    hairstyle: str
    hair_color: str
    eye_color: str
    eye_shape: str
    # Calques PNG pour portraits générés par IA
    layer_base: Optional[str] = None  # Chemin vers le calque de base (tête)
    layer_eyes: Optional[str] = None  # Chemin vers le calque des yeux
    layer_hair: Optional[str] = None  # Chemin vers le calque des cheveux
    layer_mouth: Optional[str] = None  # Chemin vers le calque de la bouche
    layer_nose: Optional[str] = None  # Chemin vers le calque du nez

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
    killed_players: List[str] = []  # IDs des joueurs éliminés par ce joueur
    betrayals: int = 0
    survived_events: int = 0
    total_score: int = 0
    group_id: Optional[str] = None  # ID du groupe auquel appartient ce joueur
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PlayerGroup(BaseModel):
    """Modèle pour les groupes de joueurs qui s'aident mutuellement"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # Nom du groupe (ex: "Groupe 1", "Les Alliés", etc.)
    member_ids: List[str] = []  # IDs des joueurs membres
    allow_betrayals: bool = False  # Si les trahisons sont autorisées dans ce groupe
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GroupCreateRequest(BaseModel):
    """Requête pour créer un groupe"""
    name: str
    member_ids: List[str]
    allow_betrayals: bool = False

class GroupUpdateRequest(BaseModel):
    """Requête pour modifier un groupe"""
    name: Optional[str] = None
    member_ids: Optional[List[str]] = None
    allow_betrayals: Optional[bool] = None

class AutoGroupRequest(BaseModel):
    """Requête pour créer des groupes automatiquement"""
    num_groups: int = Field(..., ge=1, le=20)  # Nombre de groupes à créer
    min_members: int = Field(default=2, ge=2, le=8)  # Minimum de membres par groupe
    max_members: int = Field(default=8, ge=2, le=8)  # Maximum de membres par groupe
    allow_betrayals: bool = Field(default=False)  # Trahisons autorisées par défaut

class GameEvent(BaseModel):
    id: int
    name: str
    type: EventType
    category: EventCategory = EventCategory.CLASSIQUES
    difficulty: int = Field(..., ge=1, le=10)
    description: str
    decor: str = "Décor standard"
    death_animations: List[str] = []
    survival_time_min: int = 60  # secondes minimum
    survival_time_max: int = 300  # secondes maximum
    elimination_rate: float = Field(..., ge=0.1, le=0.99)  # taux d'élimination
    special_mechanics: List[str] = []
    is_final: bool = False  # Épreuve finale (2-4 joueurs, 1 seul gagnant)
    min_players_for_final: int = 2  # Nombre min de joueurs pour déclencher une finale

class EventResult(BaseModel):
    event_id: int
    event_name: str
    survivors: List[Dict[str, Any]]
    eliminated: List[Dict[str, Any]]
    total_participants: int

class RealtimeEventUpdate(BaseModel):
    """Mise à jour en temps réel d'un événement"""
    event_id: int
    event_name: str
    elapsed_time: float  # Temps écoulé en secondes
    total_duration: float  # Durée totale en secondes
    progress: float  # Pourcentage de progression (0-100)
    deaths: List[Dict[str, Any]]  # Nouvelles morts depuis la dernière mise à jour
    is_complete: bool = False
    is_paused: bool = False  # Nouvel état pour la pause
    final_result: Optional[EventResult] = None

class RealtimeSimulationRequest(BaseModel):
    """Demande de simulation en temps réel"""
    speed_multiplier: float = Field(default=1.0, ge=0.1, le=20.0)  # Vitesse de simulation

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
    vip_salon_level: int = 0  # Niveau de salon VIP utilisé pour cette partie
    vip_earnings_collected: bool = False  # Flag pour indiquer si les gains VIP ont été collectés automatiquement

class GameStats(BaseModel):
    total_games_played: int = 0
    total_kills: int = 0
    total_betrayals: int = 0
    total_earnings: int = 0
    favorite_celebrity: Optional[str] = None
    has_seen_zero: bool = False

class CompletedGame(BaseModel):
    """Modèle pour une partie terminée"""
    id: str
    date: str
    duration: str
    total_players: int
    survivors: int
    winner: Optional[Union[str, Dict[str, Any], Player]] = None  # Peut être string (legacy) ou objet Player complet
    earnings: int = 0
    events_played: List[str] = []
    final_ranking: List[Dict[str, Any]] = []

class RoleStats(BaseModel):
    """Statistiques pour un rôle spécifique"""
    role: str
    appearances: int = 0
    survival_rate: float = 0.0
    wins: int = 0
    average_score: float = 0.0

class DetailedGameStats(BaseModel):
    """Statistiques détaillées incluant l'historique"""
    basic_stats: GameStats
    completed_games: List[CompletedGame] = []
    role_statistics: List[RoleStats] = []
    event_statistics: List[Dict[str, Any]] = []

class GameState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = "default_user"  # Pour l'instant un seul utilisateur
    money: int = 1000000  # 1 million comme demandé par l'utilisateur
    vip_salon_level: int = 0  # Commencer avec 0 VIP - le joueur doit acheter le salon standard
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
    viewing_fee: int = 0  # Montant payé pour regarder cette partie
    
class VipBet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vip_id: str
    game_id: str
    player_id: str
    amount: int
    event_id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

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
    is_dead: bool = False  # True si la célébrité est morte dans un jeu
    died_in_game_id: Optional[str] = None  # ID du jeu où elle est morte
    death_date: Optional[datetime] = None  # Date de mort
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
    all_players: List[PlayerCreateRequest] = []  # Nouveau champ pour tous les joueurs
    preserve_event_order: bool = True  # Nouveau champ pour préserver l'ordre choisi
    vip_salon_level: Optional[int] = None  # Niveau de salon VIP spécifique pour la partie

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
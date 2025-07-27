from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
import random

from models.game_models import (
    Game, Player, GameState, GameStats, GameCreateRequest, 
    PlayerCreateRequest, GameStateUpdate, PurchaseRequest,
    Celebrity, VipCharacter, EventType
)
from services.game_service import GameService
from services.vip_service import VipService
from services.events_service import EventsService

router = APIRouter(prefix="/api/games", tags=["games"])

# Stockage temporaire en mémoire (à remplacer par MongoDB plus tard)
games_db = {}
game_states_db = {}
celebrities_db = []
vips_db = []

# Initialiser les données par défaut
def init_default_data():
    global celebrities_db, vips_db
    if not celebrities_db:
        celebrities_db = GameService.generate_celebrities(1000)
    if not vips_db:
        vips_db = VipService.get_default_vips()

init_default_data()

@router.post("/create", response_model=Game)
async def create_game(request: GameCreateRequest):
    """Crée une nouvelle partie avec les joueurs spécifiés"""
    try:
        players = []
        
        # Ajouter les joueurs manuels
        for i, manual_player in enumerate(request.manual_players):
            player = Player(
                number=str(i + 1).zfill(3),
                name=manual_player.name,
                nationality=manual_player.nationality,
                gender=manual_player.gender,
                role=manual_player.role,
                stats=manual_player.stats,
                portrait=manual_player.portrait,
                uniform=manual_player.uniform
            )
            players.append(player)
        
        # Générer les joueurs automatiques restants
        remaining_count = request.player_count - len(request.manual_players)
        for i in range(remaining_count):
            player_id = len(request.manual_players) + i + 1
            player = GameService.generate_random_player(player_id)
            players.append(player)
        
        # Sélectionner les événements
        selected_events = [
            event for event in GameService.GAME_EVENTS 
            if event.id in request.selected_events
        ]
        
        if not selected_events:
            raise HTTPException(status_code=400, detail="Aucun événement sélectionné")
        
        # Calculer le coût
        game_modes_cost = {"standard": 1000, "hardcore": 2500, "custom": 1500}
        base_cost = game_modes_cost.get(request.game_mode, 1000)
        player_cost = len(players) * 10
        event_cost = len(selected_events) * 500
        total_cost = base_cost + player_cost + event_cost
        
        # Créer la partie
        game = Game(
            players=players,
            events=selected_events,
            total_cost=total_cost
        )
        
        games_db[game.id] = game
        return game
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")

@router.get("/{game_id}", response_model=Game)
async def get_game(game_id: str):
    """Récupère une partie par son ID"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    return games_db[game_id]

@router.post("/{game_id}/simulate-event")
async def simulate_event(game_id: str):
    """Simule l'événement actuel d'une partie"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    if game.completed:
        raise HTTPException(status_code=400, detail="La partie est terminée")
    
    if game.current_event_index >= len(game.events):
        raise HTTPException(status_code=400, detail="Plus d'événements disponibles")
    
    current_event = game.events[game.current_event_index]
    
    # Simuler l'événement
    result = GameService.simulate_event(game.players, current_event)
    game.event_results.append(result)
    
    # Mettre à jour les joueurs dans la partie
    for i, player in enumerate(game.players):
        # Chercher le joueur dans les résultats pour mettre à jour ses stats
        for survivor_data in result.survivors:
            if survivor_data["number"] == player.number:
                # Mettre à jour depuis les résultats
                game.players[i].kills = survivor_data.get("kills", player.kills)
                game.players[i].total_score = survivor_data.get("total_score", player.total_score)
                game.players[i].survived_events = survivor_data.get("survived_events", player.survived_events)
                break
        
        for eliminated_data in result.eliminated:
            if eliminated_data["number"] == player.number:
                game.players[i].alive = False
                break
    
    # Passer à l'événement suivant
    game.current_event_index += 1
    
    # Vérifier si la partie est terminée
    if game.current_event_index >= len(game.events):
        game.completed = True
        game.end_time = datetime.utcnow()
        
        # Déterminer le gagnant
        alive_players = [p for p in game.players if p.alive]
        if alive_players:
            game.winner = max(alive_players, key=lambda p: p.total_score)
        
        # Calculer les gains
        game.earnings = 10000 + (len(game.players) - len(alive_players)) * 100
    
    games_db[game_id] = game
    return {"result": result, "game": game}

@router.get("/", response_model=List[Game])
async def list_games():
    """Liste toutes les parties"""
    return list(games_db.values())

@router.delete("/{game_id}")
async def delete_game(game_id: str):
    """Supprime une partie"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    del games_db[game_id]
    return {"message": "Partie supprimée"}

@router.post("/generate-players", response_model=List[Player])
async def generate_players(count: int = 100):
    """Génère une liste de joueurs aléatoires"""
    if count < 1 or count > 1000:
        raise HTTPException(status_code=400, detail="Le nombre doit être entre 1 et 1000")
    
    players = []
    for i in range(1, count + 1):
        player = GameService.generate_random_player(i)
        players.append(player)
    
    return players

@router.get("/events/available", response_model=List[dict])
async def get_available_events():
    """Récupère la liste des événements disponibles"""
    return [event.dict() for event in GameService.GAME_EVENTS]
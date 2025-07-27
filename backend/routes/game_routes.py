from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
import random

from models.game_models import (
    Game, Player, GameState, GameStats, GameCreateRequest, 
    PlayerCreateRequest, GameStateUpdate, PurchaseRequest,
    Celebrity, VipCharacter, EventType, EventResult
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
    
    # Vérifier si on a déjà 1 survivant avant simulation
    alive_players_before = [p for p in game.players if p.alive]
    if len(alive_players_before) <= 1:
        game.completed = True
        game.end_time = datetime.utcnow()
        
        # Déterminer le gagnant
        if alive_players_before:
            game.winner = max(alive_players_before, key=lambda p: p.total_score)
        
        # Calculer les gains
        game.earnings = 10000 + (len(game.players) - len(alive_players_before)) * 100
        
        games_db[game_id] = game
        
        # Retourner un résultat vide car aucun événement n'a été simulé
        return {
            "result": EventResult(
                event_id=current_event.id,
                event_name=current_event.name,
                survivors=[{
                    "player": p,
                    "number": p.number,
                    "name": p.name,
                    "time_remaining": 0,
                    "event_kills": 0,
                    "betrayed": False,
                    "score": 0,
                    "kills": p.kills,
                    "total_score": p.total_score,
                    "survived_events": p.survived_events
                } for p in alive_players_before],
                eliminated=[],
                total_participants=len(alive_players_before)
            ),
            "game": game
        }
    
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
    
    # Vérifier si la partie est terminée après simulation
    alive_players_after = [p for p in game.players if p.alive]
    
    # CORRECTION CRITIQUE: Si l'événement a éliminé tous les joueurs, ressusciter le meilleur
    if len(alive_players_after) == 0 and len(result.eliminated) > 0:
        # Ressusciter le joueur éliminé avec le meilleur score total
        best_eliminated = max(result.eliminated, key=lambda x: x.get("player").total_score)
        best_eliminated_player = best_eliminated["player"]
        
        # Trouver le joueur dans la liste et le ressusciter
        for i, player in enumerate(game.players):
            if player.number == best_eliminated_player.number:
                game.players[i].alive = True
                break
        
        # Mettre à jour la liste des survivants
        alive_players_after = [p for p in game.players if p.alive]
        
        # Retirer ce joueur de la liste des éliminés et l'ajouter aux survivants
        result.eliminated = [e for e in result.eliminated if e["number"] != best_eliminated_player.number]
        result.survivors.append({
            "player": best_eliminated_player,
            "number": best_eliminated_player.number,
            "name": best_eliminated_player.name,
            "time_remaining": 1,  # Survie de justesse
            "event_kills": 0,
            "betrayed": False,
            "score": 1,
            "kills": best_eliminated_player.kills,
            "total_score": best_eliminated_player.total_score,
            "survived_events": best_eliminated_player.survived_events
        })
    
    # Condition d'arrêt : 1 survivant OU tous les événements terminés
    if len(alive_players_after) <= 1 or game.current_event_index >= len(game.events):
        game.completed = True
        game.end_time = datetime.utcnow()
        
        # Déterminer le gagnant
        if alive_players_after:
            game.winner = max(alive_players_after, key=lambda p: p.total_score)
        
        # Calculer les gains
        game.earnings = 10000 + (len(game.players) - len(alive_players_after)) * 100
    
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
    """Récupère la liste des 81 événements disponibles avec détails complets"""
    return [event.dict() for event in EventsService.GAME_EVENTS]

@router.get("/events/statistics")
async def get_events_statistics():
    """Récupère les statistiques des épreuves"""
    return EventsService.get_event_statistics()

@router.get("/events/by-type/{event_type}")
async def get_events_by_type(event_type: str):
    """Récupère les épreuves par type (intelligence, force, agilité)"""
    try:
        event_type_enum = EventType(event_type)
        events = EventsService.get_events_by_type(event_type_enum)
        return [event.dict() for event in events]
    except ValueError:
        raise HTTPException(status_code=400, detail="Type d'événement invalide")

@router.get("/events/by-difficulty")
async def get_events_by_difficulty(min_difficulty: int = 1, max_difficulty: int = 10):
    """Récupère les épreuves par niveau de difficulté"""
    if not (1 <= min_difficulty <= 10) or not (1 <= max_difficulty <= 10):
        raise HTTPException(status_code=400, detail="Difficulté doit être entre 1 et 10")
    
    events = EventsService.get_events_by_difficulty(min_difficulty, max_difficulty)
    return [event.dict() for event in events]
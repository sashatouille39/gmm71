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
        
        # Sélectionner et organiser les événements selon les préférences utilisateur
        organized_events = EventsService.organize_events_for_game(
            request.selected_events, 
            preserve_order=request.preserve_event_order
        )
        
        if not organized_events:
            raise HTTPException(status_code=400, detail="Aucun événement sélectionné")
        
        # Calculer le coût total - CORRECTION DES VALEURS ÉCONOMIQUES
        game_modes_cost = {
            "standard": 2200000,   # 2.2 millions (corrigé)
            "hardcore": 4500000,   # 4.5 millions (corrigé)
            "custom": 5000000      # 5 millions (corrigé)
        }
        
        base_cost = game_modes_cost.get(request.game_mode, 2200000)
        player_cost = len(players) * 100000  # 100k par joueur (corrigé de 10k)
        event_cost = len(organized_events) * 5000000  # 5M par épreuve (corrigé de 500k)
        total_cost = base_cost + player_cost + event_cost
        
        # Créer la partie
        game = Game(
            players=players,
            events=organized_events,
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
        
        # Calculer les gains - CORRECTION DES GAINS VIP
        # Les VIPs paient des frais de visionnage variables selon leur statut
        base_vip_fee = 100000  # 100k de base par joueur
        total_players = len(game.players)
        
        # Calculer les gains VIP réels basés sur les VIPs présents
        vip_viewing_fees = total_players * base_vip_fee  # Gain minimum
        bonus_vip_earnings = total_players * 50000  # Bonus pour les morts dramatiques
        
        game.earnings = vip_viewing_fees + bonus_vip_earnings
        
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
    
    # Logique spéciale pour les épreuves finales
    if current_event.is_final:
        # Les finales ne se déclenchent que s'il y a 2-4 joueurs
        if len(alive_players_before) > current_event.min_players_for_final:
            # Trop de joueurs pour une finale, passer à l'événement suivant
            game.current_event_index += 1
            
            # Vérifier si il y a encore des événements
            if game.current_event_index >= len(game.events):
                # Plus d'événements, terminer la partie avec les survivants actuels
                game.completed = True
                game.end_time = datetime.utcnow()
                game.winner = max(alive_players_before, key=lambda p: p.total_score) if alive_players_before else None
                vip_viewing_fees = len(game.players) * 100000  # 100k par joueur pour les VIPs
                bonus_earnings = (len(game.players) - len(alive_players_before)) * 50000  # 50k par mort
                game.earnings = vip_viewing_fees + bonus_earnings
                games_db[game_id] = game
                
                return {
                    "result": EventResult(
                        event_id=current_event.id,
                        event_name=f"Finale reportée - {current_event.name}",
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
                    "game": game,
                    "message": f"Finale reportée: trop de joueurs ({len(alive_players_before)}) pour une finale (max {current_event.min_players_for_final})"
                }
            else:
                # Récursivement essayer le prochain événement
                return await simulate_event(game_id)
    
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
        
        # Calculer les gains - CORRECTION FINALE DES GAINS VIP
        base_vip_fee = 100000  # 100k de base par joueur
        total_players = len(game.players)
        deaths_count = len(game.players) - len(alive_players_after)
        
        # Gains VIP calculés correctement
        vip_viewing_fees = total_players * base_vip_fee  # Frais de visionnage
        death_bonus = deaths_count * 50000  # Bonus pour les morts dramatiques
        
        game.earnings = vip_viewing_fees + death_bonus
    
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

@router.get("/{game_id}/final-ranking")
async def get_final_ranking(game_id: str):
    """Récupère le classement final complet d'une partie terminée"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    if not game.completed:
        raise HTTPException(status_code=400, detail="La partie n'est pas encore terminée")
    
    # Trier tous les joueurs par score décroissant, puis par événements survécus
    all_players_ranking = sorted(
        game.players,
        key=lambda p: (p.total_score, p.survived_events, -p.betrayals),
        reverse=True
    )
    
    # Créer le classement avec positions
    ranking = []
    for position, player in enumerate(all_players_ranking, 1):
        ranking.append({
            "position": position,
            "player": {
                "id": player.id,
                "name": player.name,
                "number": player.number,
                "nationality": player.nationality,
                "role": player.role,
                "alive": player.alive,
                "is_celebrity": getattr(player, 'isCelebrity', False),
                "celebrity_id": getattr(player, 'celebrityId', None)
            },
            "stats": {
                "total_score": player.total_score,
                "survived_events": player.survived_events,
                "kills": player.kills,
                "betrayals": player.betrayals
            },
            "player_stats": {
                "intelligence": player.stats.intelligence,
                "force": player.stats.force,
                "agilite": player.stats.agilite
            }
        })
    
    return {
        "game_id": game_id,
        "completed": game.completed,
        "winner": {
            "id": game.winner.id,
            "name": game.winner.name,
            "number": game.winner.number
        } if game.winner else None,
        "total_players": len(game.players),
        "total_events": len(game.events),
        "events_completed": game.current_event_index,
        "ranking": ranking,
        "game_stats": {
            "start_time": game.start_time,
            "end_time": game.end_time,
            "total_cost": game.total_cost,
            "earnings": game.earnings
        }
    }
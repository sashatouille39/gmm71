from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict
from datetime import datetime
import random

from models.game_models import (
    Game, Player, GameState, GameStats, GameCreateRequest, 
    PlayerCreateRequest, GameStateUpdate, PurchaseRequest,
    Celebrity, VipCharacter, EventType, EventResult, PlayerGroup,
    RealtimeEventUpdate, RealtimeSimulationRequest
)
from services.game_service import GameService
from services.vip_service import VipService
from services.events_service import EventsService

router = APIRouter(prefix="/api/games", tags=["games"])

# Stockage temporaire en mémoire (à remplacer par MongoDB plus tard)
games_db = {}
groups_db = {}  # Stockage des groupes par partie
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
            "standard": 100000,     # 100k au lieu de 2.2M
            "hardcore": 500000,     # 500k au lieu de 4.5M
            "custom": 1000000       # 1M au lieu de 5M
        }
        
        base_cost = game_modes_cost.get(request.game_mode, 2200000)
        player_cost = len(players) * 100  # 100$ par joueur comme demandé
        event_cost = len(organized_events) * 5000  # 5,000$ par épreuve comme demandé
        total_cost = base_cost + player_cost + event_cost
        
        # Créer la partie
        game = Game(
            players=players,
            events=organized_events,
            total_cost=total_cost
        )
        
        # CORRECTION PROBLÈME 1: Déduire l'argent du gamestate après création
        from routes.gamestate_routes import game_states_db
        user_id = "default_user"  # ID utilisateur par défaut
        
        if user_id not in game_states_db:
            from models.game_models import GameState
            game_state = GameState(user_id=user_id)
            game_states_db[user_id] = game_state
        else:
            game_state = game_states_db[user_id]
        
        # Vérifier si l'utilisateur a assez d'argent
        if game_state.money < total_cost:
            raise HTTPException(status_code=400, detail=f"Fonds insuffisants. Coût: {total_cost}$, Disponible: {game_state.money}$")
        
        # Déduire l'argent
        game_state.money -= total_cost
        game_state.updated_at = datetime.utcnow()
        game_states_db[user_id] = game_state
        
        # NOUVEAU : Assigner automatiquement des VIPs à la partie
        from routes.vip_routes import active_vips_by_game
        from services.vip_service import VipService
        
        # Récupérer le niveau de salon VIP du joueur (par défaut 1)
        salon_level = game_state.vip_salon_level
        capacity_map = {1: 3, 2: 5, 3: 8, 4: 12}
        vip_capacity = capacity_map.get(salon_level, 3)
        
        # Assigner des VIPs avec leurs viewing_fee (200k-3M)
        game_vips = VipService.get_random_vips(vip_capacity)
        active_vips_by_game[game.id] = game_vips
        
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
        
        # Calculer les gains - CORRECTION : UTILISER LES VRAIS MONTANTS VIP
        from routes.vip_routes import active_vips_by_game
        
        game_vips = active_vips_by_game.get(game_id, [])
        if game_vips:
            # Sommer les viewing_fee réels des VIPs (entre 200k et 3M chacun)
            game.earnings = sum(vip.viewing_fee for vip in game_vips)
        else:
            # Pas de VIPs assignés, aucun gain
            game.earnings = 0
        
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
                
                # Calculer les gains réels des VIPs
                from routes.vip_routes import active_vips_by_game
                game_vips = active_vips_by_game.get(game_id, [])
                if game_vips:
                    game.earnings = sum(vip.viewing_fee for vip in game_vips)
                else:
                    game.earnings = 0
                    
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
    
    # Simuler l'événement avec support des groupes
    game_groups = {gid: g for gid, g in groups_db.items() if gid.startswith(f"{game_id}_")}
    result = GameService.simulate_event(game.players, current_event, game_groups)
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
        
        # Calculer les gains - CORRECTION FINALE : UTILISER LES VRAIS MONTANTS VIP
        # Récupérer les VIPs assignés à cette partie pour leurs viewing_fee réels
        from routes.vip_routes import active_vips_by_game
        
        game_vips = active_vips_by_game.get(game_id, [])
        if game_vips:
            # Sommer les viewing_fee réels des VIPs (entre 200k et 3M chacun)
            game.earnings = sum(vip.viewing_fee for vip in game_vips)
        else:
            # Pas de VIPs assignés, aucun gain
            game.earnings = 0
    else:
        # NOUVEAU: Calculer les gains partiels même si le jeu n'est pas terminé
        # en utilisant les VRAIS montants VIP (200k-3M chacun)
        from routes.vip_routes import active_vips_by_game
        
        game_vips = active_vips_by_game.get(game_id, [])
        if game_vips:
            # Sommer les viewing_fee réels des VIPs assignés à cette partie
            game.earnings = sum(vip.viewing_fee for vip in game_vips)
        else:
            # Pas de VIPs assignés, aucun gain
            game.earnings = 0
    
    games_db[game_id] = game
    return {"result": result, "game": game}

# Stockage pour les simulations en temps réel
active_simulations = {}

@router.post("/{game_id}/simulate-event-realtime")
async def simulate_event_realtime(game_id: str, request: RealtimeSimulationRequest):
    """Démarre une simulation d'événement en temps réel"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    if game.completed:
        raise HTTPException(status_code=400, detail="La partie est terminée")
    
    if game.current_event_index >= len(game.events):
        raise HTTPException(status_code=400, detail="Plus d'événements disponibles")
    
    # Vérifier si une simulation est déjà en cours
    if game_id in active_simulations:
        raise HTTPException(status_code=400, detail="Une simulation est déjà en cours pour cette partie")
    
    current_event = game.events[game.current_event_index]
    alive_players = [p for p in game.players if p.alive]
    
    if len(alive_players) <= 1:
        game.completed = True
        game.end_time = datetime.utcnow()
        if alive_players:
            game.winner = max(alive_players, key=lambda p: p.total_score)
        games_db[game_id] = game
        raise HTTPException(status_code=400, detail="Partie terminée - pas assez de joueurs")
    
    # Calculer la durée réelle de l'événement
    import random
    event_duration = random.randint(current_event.survival_time_min, current_event.survival_time_max)
    
    # Pré-calculer tous les résultats de la simulation
    game_groups = {gid: g for gid, g in groups_db.items() if gid.startswith(f"{game_id}_")}
    final_result = GameService.simulate_event(game.players, current_event, game_groups)
    
    # Créer la timeline des morts
    deaths_timeline = []
    total_deaths = len(final_result.eliminated)
    
    for i, eliminated_player in enumerate(final_result.eliminated):
        # Répartir les morts sur la durée de l'événement (éviter la fin pour le suspense)
        death_time = random.uniform(10, event_duration * 0.85)  # Entre 10 sec et 85% de la durée
        
        death_info = {
            "time": death_time,
            "player": eliminated_player,
            "message": f"{eliminated_player['name']} ({eliminated_player['number']}) est mort"
        }
        
        # Vérifier s'il y a un tueur pour ce joueur
        for survivor in final_result.survivors:
            survivor_player = survivor["player"]
            if eliminated_player["player"].id in survivor_player.killed_players:
                death_info["message"] = f"{eliminated_player['name']} ({eliminated_player['number']}) a été tué par {survivor_player.name} ({survivor_player.number})"
                break
        
        deaths_timeline.append(death_info)
    
    # Trier par temps de mort
    deaths_timeline.sort(key=lambda x: x["time"])
    
    # Sauvegarder la simulation active
    active_simulations[game_id] = {
        "event": current_event,
        "start_time": datetime.utcnow(),
        "duration": event_duration,
        "speed_multiplier": request.speed_multiplier,
        "deaths_timeline": deaths_timeline,
        "final_result": final_result,
        "deaths_sent": 0  # Compteur des morts déjà envoyées
    }
    
    return {
        "message": "Simulation en temps réel démarrée",
        "event_name": current_event.name,
        "duration": event_duration,
        "speed_multiplier": request.speed_multiplier,
        "total_participants": len(alive_players)
    }

@router.get("/{game_id}/realtime-updates")
async def get_realtime_updates(game_id: str):
    """Récupère les mises à jour en temps réel d'une simulation"""
    if game_id not in active_simulations:
        raise HTTPException(status_code=404, detail="Aucune simulation en cours")
    
    simulation = active_simulations[game_id]
    current_time = datetime.utcnow()
    elapsed_real_time = (current_time - simulation["start_time"]).total_seconds()
    
    # Calculer le temps écoulé dans la simulation (avec multiplicateur de vitesse)
    elapsed_sim_time = elapsed_real_time * simulation["speed_multiplier"]
    
    # Calculer la progression
    progress = min(100.0, (elapsed_sim_time / simulation["duration"]) * 100)
    
    # Trouver les nouvelles morts à envoyer
    new_deaths = []
    deaths_timeline = simulation["deaths_timeline"]
    deaths_sent = simulation["deaths_sent"]
    
    for i in range(deaths_sent, len(deaths_timeline)):
        death = deaths_timeline[i]
        if death["time"] <= elapsed_sim_time:
            new_deaths.append({
                "message": death["message"],
                "player_name": death["player"]["name"],
                "player_number": death["player"]["number"]
            })
            simulation["deaths_sent"] = i + 1
        else:
            break
    
    # Vérifier si l'événement est terminé
    is_complete = elapsed_sim_time >= simulation["duration"]
    final_result = None
    
    if is_complete:
        # Appliquer les résultats finaux au jeu
        game = games_db[game_id]
        
        # Mettre à jour les joueurs dans la partie
        for i, player in enumerate(game.players):
            # Chercher le joueur dans les résultats pour mettre à jour ses stats
            for survivor_data in simulation["final_result"].survivors:
                if survivor_data["number"] == player.number:
                    game.players[i].kills = survivor_data.get("kills", player.kills)
                    game.players[i].total_score = survivor_data.get("total_score", player.total_score)
                    game.players[i].survived_events = survivor_data.get("survived_events", player.survived_events)
                    break
            
            for eliminated_data in simulation["final_result"].eliminated:
                if eliminated_data["number"] == player.number:
                    game.players[i].alive = False
                    break
        
        game.event_results.append(simulation["final_result"])
        game.current_event_index += 1
        
        # Vérifier si la partie est terminée
        alive_players_after = [p for p in game.players if p.alive]
        if len(alive_players_after) <= 1 or game.current_event_index >= len(game.events):
            game.completed = True
            game.end_time = datetime.utcnow()
            if alive_players_after:
                game.winner = max(alive_players_after, key=lambda p: p.total_score)
        
        games_db[game_id] = game
        final_result = simulation["final_result"]
        
        # Nettoyer la simulation active
        del active_simulations[game_id]
    
    return RealtimeEventUpdate(
        event_id=simulation["event"].id,
        event_name=simulation["event"].name,
        elapsed_time=elapsed_sim_time,
        total_duration=simulation["duration"],
        progress=progress,
        deaths=new_deaths,
        is_complete=is_complete,
        final_result=final_result
    )

@router.post("/{game_id}/update-simulation-speed")
async def update_simulation_speed(game_id: str, request: RealtimeSimulationRequest):
    """Met à jour la vitesse de simulation en cours"""
    if game_id not in active_simulations:
        raise HTTPException(status_code=404, detail="Aucune simulation en cours")
    
    simulation = active_simulations[game_id]
    old_speed = simulation["speed_multiplier"]
    
    # Calculer le temps écoulé avec l'ancienne vitesse
    current_time = datetime.utcnow()
    elapsed_real_time = (current_time - simulation["start_time"]).total_seconds()
    elapsed_sim_time = elapsed_real_time * old_speed
    
    # Mettre à jour pour la nouvelle vitesse
    simulation["speed_multiplier"] = request.speed_multiplier
    # Ajuster le temps de début pour maintenir la continuité
    if request.speed_multiplier > 0:
        # Calculer le nouveau temps de début nécessaire
        new_elapsed_real_time = elapsed_sim_time / request.speed_multiplier
        new_start_time = current_time - datetime.timedelta(seconds=new_elapsed_real_time)
        simulation["start_time"] = new_start_time
    
    active_simulations[game_id] = simulation
    
    return {
        "message": f"Vitesse mise à jour de x{old_speed} à x{request.speed_multiplier}",
        "new_speed": request.speed_multiplier
    }

@router.delete("/{game_id}/stop-simulation")
async def stop_simulation(game_id: str):
    """Arrête une simulation en cours"""
    if game_id not in active_simulations:
        raise HTTPException(status_code=404, detail="Aucune simulation en cours")
    
    del active_simulations[game_id]
    return {"message": "Simulation arrêtée"}

@router.get("/{game_id}/vip-earnings-status")
async def get_vip_earnings_status(game_id: str):
    """Obtient le statut des gains VIP d'une partie"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    return {
        "game_id": game_id,
        "completed": game.completed,
        "earnings_available": game.earnings,
        "can_collect": game.completed and game.earnings > 0,
        "winner": game.winner.name if game.winner else None,
        "total_players": len(game.players),
        "alive_players": len([p for p in game.players if p.alive])
    }

@router.post("/{game_id}/collect-vip-earnings")
async def collect_vip_earnings(game_id: str, user_id: str = "default_user"):
    """NOUVEAU : Collecte les gains VIP d'une partie terminée et les ajoute au gamestate"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    if not game.completed:
        raise HTTPException(status_code=400, detail="La partie n'est pas terminée, impossible de collecter les gains")
    
    if game.earnings <= 0:
        raise HTTPException(status_code=400, detail="Aucun gain à collecter pour cette partie")
    
    # CORRECTION PROBLÈME 2: Ajouter les gains VIP au gamestate
    from routes.gamestate_routes import game_states_db
    
    if user_id not in game_states_db:
        from models.game_models import GameState
        game_state = GameState(user_id=user_id)
        game_states_db[user_id] = game_state
    else:
        game_state = game_states_db[user_id]
    
    # Ajouter les gains au portefeuille du joueur
    earnings_to_collect = game.earnings
    game_state.money += earnings_to_collect
    game_state.game_stats.total_earnings += earnings_to_collect
    game_state.updated_at = datetime.utcnow()
    game_states_db[user_id] = game_state
    
    # Marquer les gains comme collectés pour éviter la double collecte
    game.earnings = 0
    games_db[game_id] = game
    
    return {
        "message": f"Gains VIP collectés: {earnings_to_collect}$",
        "earnings_collected": earnings_to_collect,
        "new_total_money": game_state.money
    }

@router.get("/", response_model=List[Game])
async def list_games():
    """Liste toutes les parties"""
    return list(games_db.values())

@router.delete("/{game_id}")
async def delete_game(game_id: str, user_id: str = "default_user"):
    """Supprime une partie et rembourse si elle n'est pas terminée"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    # CORRECTION PROBLÈME 3: Remboursement si le jeu n'est pas terminé
    if not game.completed:
        # Rembourser l'argent dépensé pour créer la partie
        from routes.gamestate_routes import game_states_db
        
        if user_id not in game_states_db:
            from models.game_models import GameState
            game_state = GameState(user_id=user_id)
            game_states_db[user_id] = game_state
        else:
            game_state = game_states_db[user_id]
        
        # Rembourser le coût total de la partie
        refund_amount = game.total_cost
        game_state.money += refund_amount
        game_state.updated_at = datetime.utcnow()
        game_states_db[user_id] = game_state
        
        del games_db[game_id]
        
        return {
            "message": "Partie supprimée et argent remboursé", 
            "refund_amount": refund_amount,
            "new_total_money": game_state.money
        }
    else:
        # Partie terminée, pas de remboursement
        del games_db[game_id]
        return {"message": "Partie terminée supprimée (pas de remboursement)"}

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
    """Récupère le classement final d'une partie terminée"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    # Trier les joueurs par score décroissant
    sorted_players = sorted(game.players, key=lambda p: (p.total_score, p.survived_events, -p.betrayals), reverse=True)
    
    # Créer le classement avec positions
    ranking = []
    for i, player in enumerate(sorted_players):
        ranking.append({
            "position": i + 1,
            "player": {
                "id": player.id,
                "number": player.number,
                "name": player.name,
                "nationality": player.nationality,
                "gender": player.gender,
                "role": player.role,
                "alive": player.alive
            },
            "game_stats": {
                "total_score": player.total_score,
                "survived_events": player.survived_events,
                "kills": player.kills,
                "betrayals": player.betrayals,
                "killed_players": player.killed_players
            },
            "player_stats": {
                "intelligence": player.stats.intelligence,
                "force": player.stats.force,
                "agilité": player.stats.agilité,
                "charisme": player.stats.charisme,
                "instinct": player.stats.instinct
            }
        })
    
    return {
        "game_id": game_id,
        "completed": game.completed,
        "winner": game.winner,
        "total_players": len(game.players),
        "ranking": ranking
    }

# Storage pour les groupes pré-configurés (indépendants des parties)
preconfigured_groups_db: Dict[str, PlayerGroup] = {}

# Routes pour les groupes pré-configurés (indépendants des parties)
@router.post("/groups/preconfigured")
async def create_preconfigured_groups(request: dict):
    """Crée des groupes pré-configurés (indépendamment d'une partie)"""
    groups_data = request.get("groups", [])
    
    if not groups_data:
        raise HTTPException(status_code=400, detail="Aucun groupe fourni")
    
    created_groups = []
    
    for group_data in groups_data:
        name = group_data.get("name", "Groupe sans nom")
        member_ids = group_data.get("member_ids", [])
        allow_betrayals = group_data.get("allow_betrayals", False)
        
        if not member_ids:
            continue
            
        group = PlayerGroup(
            name=name,
            member_ids=member_ids,
            allow_betrayals=allow_betrayals
        )
        
        created_groups.append(group)
        preconfigured_groups_db[group.id] = group
    
    return {
        "groups": created_groups,
        "message": f"{len(created_groups)} groupes pré-configurés créés avec succès"
    }

@router.get("/groups/preconfigured")
async def get_preconfigured_groups():
    """Récupère tous les groupes pré-configurés"""
    return {
        "groups": list(preconfigured_groups_db.values())
    }

@router.delete("/groups/preconfigured")
async def clear_preconfigured_groups():
    """Supprime tous les groupes pré-configurés"""
    global preconfigured_groups_db
    preconfigured_groups_db = {}
    return {"message": "Tous les groupes pré-configurés ont été supprimés"}

@router.put("/groups/preconfigured/{group_id}")
async def update_preconfigured_group(group_id: str, request: dict):
    """Met à jour un groupe pré-configuré"""
    if group_id not in preconfigured_groups_db:
        raise HTTPException(status_code=404, detail="Groupe pré-configuré non trouvé")
    
    group = preconfigured_groups_db[group_id]
    
    if "name" in request:
        group.name = request["name"]
    if "member_ids" in request:
        group.member_ids = request["member_ids"]
    if "allow_betrayals" in request:
        group.allow_betrayals = request["allow_betrayals"]
    
    preconfigured_groups_db[group_id] = group
    
    return {
        "message": "Groupe pré-configuré mis à jour avec succès",
        "group": group
    }

@router.delete("/groups/preconfigured/{group_id}")
async def delete_preconfigured_group(group_id: str):
    """Supprime un groupe pré-configuré"""
    if group_id not in preconfigured_groups_db:
        raise HTTPException(status_code=404, detail="Groupe pré-configuré non trouvé")
    
    del preconfigured_groups_db[group_id]
    return {"message": "Groupe pré-configuré supprimé avec succès"}

# Routes pour les groupes dans le contexte des parties
@router.post("/{game_id}/groups")
async def create_game_groups(game_id: str, request: dict):
    """Crée des groupes pour une partie spécifique"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    num_groups = request.get("num_groups", 2)
    min_members = request.get("min_members", 2)
    max_members = request.get("max_members", 8)
    allow_betrayals = request.get("allow_betrayals", False)
    
    # Récupérer les joueurs vivants
    alive_players = [p for p in game.players if p.alive]
    
    if len(alive_players) < num_groups * min_members:
        raise HTTPException(
            status_code=400,
            detail=f"Pas assez de joueurs vivants pour créer {num_groups} groupes"
        )
    
    # Mélanger les joueurs
    random.shuffle(alive_players)
    
    groups = []
    player_index = 0
    
    # Créer les groupes
    for i in range(num_groups):
        # Calculer le nombre de membres pour ce groupe
        remaining_players = len(alive_players) - player_index
        remaining_groups = num_groups - i
        
        min_needed = remaining_groups * min_members
        available_for_this_group = remaining_players - min_needed + min_members
        
        members_count = min(
            random.randint(min_members, max_members),
            available_for_this_group,
            remaining_players
        )
        
        # Créer le groupe
        group_members = []
        for _ in range(members_count):
            if player_index < len(alive_players):
                player = alive_players[player_index]
                group_members.append(player.id)
                # Assigner le group_id au joueur
                player.group_id = f"{game_id}_group_{i+1}"
                player_index += 1
        
        group = PlayerGroup(
            id=f"{game_id}_group_{i+1}",
            name=f"Groupe {i + 1}",
            member_ids=group_members,
            allow_betrayals=allow_betrayals
        )
        
        groups.append(group)
        groups_db[group.id] = group
    
    return {
        "game_id": game_id,
        "groups": groups,
        "message": f"{len(groups)} groupes créés avec succès"
    }

@router.post("/{game_id}/groups/apply-preconfigured")
async def apply_preconfigured_groups_to_game(game_id: str):
    """Applique les groupes pré-configurés à une partie"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    if not preconfigured_groups_db:
        raise HTTPException(status_code=400, detail="Aucun groupe pré-configuré disponible")
    
    applied_groups = []
    
    for group in preconfigured_groups_db.values():
        # Vérifier que tous les joueurs du groupe existent dans la partie
        valid_member_ids = []
        for member_id in group.member_ids:
            # Trouver le joueur par ID dans la partie
            player_found = False
            for player in game.players:
                if player.id == member_id:
                    valid_member_ids.append(member_id)
                    player.group_id = f"{game_id}_{group.id}"
                    player_found = True
                    break
            
            if not player_found:
                print(f"Attention: Joueur {member_id} du groupe {group.name} non trouvé dans la partie")
        
        # Créer le groupe pour cette partie seulement si on a des membres valides
        if valid_member_ids:
            game_group = PlayerGroup(
                id=f"{game_id}_{group.id}",
                name=group.name,
                member_ids=valid_member_ids,
                allow_betrayals=group.allow_betrayals
            )
            
            applied_groups.append(game_group)
            groups_db[game_group.id] = game_group
    
    return {
        "game_id": game_id,
        "applied_groups": applied_groups,
        "message": f"{len(applied_groups)} groupes pré-configurés appliqués à la partie"
    }

@router.get("/{game_id}/groups")
async def get_game_groups(game_id: str):
    """Récupère les groupes d'une partie"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game_groups = []
    for group_id, group in groups_db.items():
        if group_id.startswith(f"{game_id}_"):
            # Ajouter les informations des joueurs
            members = []
            for member_id in group.member_ids:
                for player in games_db[game_id].players:
                    if player.id == member_id:
                        members.append({
                            "id": player.id,
                            "name": player.name,
                            "number": player.number,
                            "alive": player.alive
                        })
                        break
            
            game_groups.append({
                "id": group.id,
                "name": group.name,
                "members": members,
                "allow_betrayals": group.allow_betrayals,
                "created_at": group.created_at
            })
    
    return {
        "game_id": game_id,
        "groups": game_groups
    }

@router.put("/{game_id}/groups/{group_id}")
async def update_game_group(game_id: str, group_id: str, request: dict):
    """Met à jour un groupe d'une partie"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    if group_id not in groups_db:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    group = groups_db[group_id]
    
    # Mettre à jour les champs si fournis
    if "name" in request:
        group.name = request["name"]
    
    if "allow_betrayals" in request:
        group.allow_betrayals = request["allow_betrayals"]
    
    groups_db[group_id] = group
    
    return {
        "message": "Groupe mis à jour avec succès",
        "group": group
    }

@router.post("/{game_id}/groups/toggle-betrayals")
async def toggle_betrayals_for_all_groups(game_id: str, request: dict):
    """Active/désactive les trahisons pour tous les groupes d'une partie"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    allow_betrayals = request.get("allow_betrayals", False)
    
    # Mettre à jour tous les groupes de cette partie
    updated_groups = []
    for group_id, group in groups_db.items():
        if group_id.startswith(f"{game_id}_"):
            group.allow_betrayals = allow_betrayals
            groups_db[group_id] = group
            updated_groups.append(group)
    
    return {
        "message": f"Trahisons {'activées' if allow_betrayals else 'désactivées'} pour tous les groupes",
        "updated_groups": len(updated_groups),
        "allow_betrayals": allow_betrayals
    }

@router.delete("/{game_id}/groups")
async def clear_game_groups(game_id: str):
    """Supprime tous les groupes d'une partie"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    # Supprimer les groupes de la base
    groups_to_remove = []
    for group_id in groups_db.keys():
        if group_id.startswith(f"{game_id}_"):
            groups_to_remove.append(group_id)
    
    for group_id in groups_to_remove:
        del groups_db[group_id]
    
    # Retirer les group_id des joueurs
    for player in game.players:
        player.group_id = None
    
    return {
        "message": f"{len(groups_to_remove)} groupes supprimés avec succès"
    }

@router.get("/{game_id}/player/{player_id}/eliminated-players")
async def get_eliminated_players(game_id: str, player_id: str):
    """Récupère la liste des joueurs éliminés par un joueur spécifique"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    
    game = games_db[game_id]
    
    # Trouver le joueur
    killer_player = None
    for player in game.players:
        if player.id == player_id:
            killer_player = player
            break
    
    if not killer_player:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    
    # Récupérer les joueurs éliminés
    eliminated_players = []
    for eliminated_player_id in killer_player.killed_players:
        for player in game.players:
            if player.id == eliminated_player_id:
                eliminated_players.append({
                    "id": player.id,
                    "name": player.name,
                    "number": player.number,
                    "nationality": player.nationality,
                    "role": player.role,
                    "stats": {
                        "intelligence": player.stats.intelligence,
                        "force": player.stats.force,
                        "agilité": player.stats.agilité
                    }
                })
                break
    
    return {
        "killer": {
            "id": killer_player.id,
            "name": killer_player.name,
            "number": killer_player.number,
            "total_kills": killer_player.kills
        },
        "eliminated_players": eliminated_players
    }
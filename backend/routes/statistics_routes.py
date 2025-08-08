from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from models.game_models import DetailedGameStats, CompletedGame, RoleStats
from services.statistics_service import StatisticsService
from routes.gamestate_routes import game_states_db

class SaveCompletedGameRequest(BaseModel):
    game_id: str
    user_id: str = "default_user"

router = APIRouter(prefix="/api/statistics", tags=["statistics"])

@router.get("/detailed", response_model=DetailedGameStats)
async def get_detailed_statistics(user_id: str = "default_user"):
    """Récupère toutes les statistiques détaillées"""
    try:
        # Récupérer les stats de base depuis gamestate
        if user_id not in game_states_db:
            from models.game_models import GameState
            game_state = GameState(user_id=user_id)
            game_states_db[user_id] = game_state
        else:
            game_state = game_states_db[user_id]
        
        # Obtenir les statistiques détaillées
        detailed_stats = StatisticsService.get_detailed_statistics(
            user_id, 
            game_state.game_stats
        )
        
        return detailed_stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul des statistiques: {str(e)}")

@router.get("/completed-games", response_model=List[CompletedGame])
async def get_completed_games(
    user_id: str = "default_user",
    limit: int = Query(20, ge=1, le=100)
):
    """Récupère l'historique des parties terminées"""
    try:
        completed_games = StatisticsService.get_completed_games(user_id, limit)
        return completed_games
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'historique: {str(e)}")

@router.get("/winners", response_model=List[Dict[str, Any]])
async def get_past_winners(user_id: str = "default_user"):
    """Récupère les vrais anciens gagnants des parties terminées avec leurs stats améliorées"""
    try:
        import random
        completed_games = StatisticsService.get_completed_games(user_id, limit=100)
        
        winners = []
        for game in completed_games:
            if game.winner and game.final_ranking:
                # CORRECTION : Récupérer le VRAI gagnant (winner) au lieu du premier du classement
                winner_data = None
                winner_name = game.winner.get('name') if isinstance(game.winner, dict) else getattr(game.winner, 'name', None)
                
                # Chercher le vrai gagnant dans le classement final
                for ranking_entry in game.final_ranking:
                    player_info = ranking_entry.get('player', {})
                    if player_info.get('name') == winner_name:
                        winner_data = ranking_entry
                        break
                
                # Fallback : si on ne trouve pas le gagnant par nom, utiliser l'objet winner directement
                if not winner_data and isinstance(game.winner, dict):
                    winner_data = {
                        'player': game.winner,
                        'player_stats': getattr(game.winner, 'stats', {}),
                        'total_score': getattr(game.winner, 'total_score', 0)
                    }
                elif not winner_data and hasattr(game.winner, 'name'):
                    winner_data = {
                        'player': {
                            'name': game.winner.name,
                            'nationality': getattr(game.winner, 'nationality', 'Inconnue')
                        },
                        'player_stats': getattr(game.winner, 'stats', {}),
                        'total_score': getattr(game.winner, 'total_score', 0)
                    }
                
                if winner_data and winner_data.get('player'):
                    player_info = winner_data['player']
                    player_stats = winner_data.get('player_stats', {})
                    
                    # Stats de base (ou valeurs par défaut si manquantes)
                    base_intelligence = player_stats.get('intelligence', 5)
                    base_force = player_stats.get('force', 5)
                    base_agilite = player_stats.get('agilite', 5)
                    
                    # Ajouter 5 points aléatoirement répartis sur les 3 habiletés
                    bonus_points = 5
                    bonus_intelligence = random.randint(0, bonus_points)
                    remaining_points = bonus_points - bonus_intelligence
                    bonus_force = random.randint(0, remaining_points)
                    bonus_agilite = remaining_points - bonus_force
                    
                    # Calculer les stats finales (max 10 par habileté)
                    final_intelligence = min(10, base_intelligence + bonus_intelligence)
                    final_force = min(10, base_force + bonus_force)
                    final_agilite = min(10, base_agilite + bonus_agilite)
                    
                    # Calculer le nombre d'étoiles basé sur les stats finales
                    total_stats = final_intelligence + final_force + final_agilite
                    if total_stats >= 27:
                        stars = 5
                    elif total_stats >= 24:
                        stars = 4
                    elif total_stats >= 21:
                        stars = 3
                    elif total_stats >= 18:
                        stars = 2
                    else:
                        stars = 1
                    
                    # Calculer le prix basé sur les étoiles et les victoires
                    base_price = stars * 10000000  # 10M par étoile
                    final_price = base_price + (1000000 * (winner_data.get('wins', 1) - 1))  # +1M par victoire supplémentaire
                    
                    winner = {
                        "id": f"winner_{game.id}",
                        "name": player_info.get('name', 'Gagnant Inconnu'),
                        "category": "Ancien gagnant",
                        "stars": stars,
                        "price": final_price,
                        "nationality": player_info.get('nationality', 'Inconnue'),
                        "wins": 1,  # Au moins 1 victoire (cette partie)
                        "stats": {
                            "intelligence": final_intelligence,
                            "force": final_force,
                            "agilité": final_agilite
                        },
                        "biography": f"Vainqueur du jeu {game.id} le {game.date}. Score total: {winner_data.get('total_score', 0)}",
                        "game_data": {
                            "game_id": game.id,
                            "date": game.date,
                            "total_players": game.total_players,
                            "survivors": game.survivors,
                            "final_score": winner_data.get('total_score', 0)
                        }
                    }
                    winners.append(winner)
        
        return winners
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des gagnants: {str(e)}")

@router.get("/roles", response_model=List[RoleStats])
async def get_role_statistics(user_id: str = "default_user"):
    """Récupère les statistiques par rôle"""
    try:
        role_stats = StatisticsService.calculate_role_statistics(user_id)
        return role_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul des stats de rôles: {str(e)}")

@router.post("/save-completed-game")
async def save_completed_game(request: SaveCompletedGameRequest):
    """Sauvegarde une partie terminée (appelé automatiquement à la fin d'une partie)"""
    try:
        # Importer game_db pour récupérer la partie
        from routes.game_routes import games_db
        
        if request.game_id not in games_db:
            raise HTTPException(status_code=404, detail="Partie non trouvée")
        
        game = games_db[request.game_id]
        
        if not game.completed:
            raise HTTPException(status_code=400, detail="La partie n'est pas terminée")
        
        # Récupérer le classement final
        try:
            import requests
            backendUrl = "http://localhost:8001"  # URL interne
            ranking_response = requests.get(f"{backendUrl}/api/games/{request.game_id}/final-ranking", timeout=5)
            
            if ranking_response.status_code == 200:
                ranking_data = ranking_response.json()
                final_ranking = ranking_data.get('ranking', [])
            else:
                final_ranking = []
        except:
            final_ranking = []
        
        # Sauvegarder la partie
        completed_game = StatisticsService.save_completed_game(request.user_id, game, final_ranking)
        
        # Mettre à jour les stats de base dans gamestate
        if request.user_id in game_states_db:
            game_state = game_states_db[request.user_id]
            game_state.game_stats.total_games_played += 1
            
            # Compter les kills réels effectués par les survivants
            total_kills_made = sum([p.kills for p in game.players])
            game_state.game_stats.total_kills += total_kills_made
            
            # Compter les trahisons
            total_betrayals = sum([p.betrayals for p in game.players])
            game_state.game_stats.total_betrayals += total_betrayals
            
            # Ajouter les gains
            if hasattr(game, 'earnings'):
                game_state.game_stats.total_earnings += game.earnings
            
            # Vérifier si Le Zéro était présent
            has_zero = any(p.role == "zero" for p in game.players)
            if has_zero:
                game_state.game_stats.has_seen_zero = True
            
            # Mettre à jour la célébrité favorite si nécessaire
            # (pourrait être ajouté plus tard selon les besoins)
            
            print(f"✅ GameStats mis à jour: {game_state.game_stats.total_games_played} parties, {game_state.game_stats.total_kills} éliminations")
        
        return {
            "message": "Partie sauvegardée avec succès",
            "completed_game": completed_game
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde: {str(e)}")
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from models.game_models import (
    CompletedGame, RoleStats, DetailedGameStats, GameStats,
    Player, PlayerRole, Game
)

class StatisticsService:
    """Service pour calculer et gérer les statistiques détaillées"""
    
    # Stockage temporaire des parties terminées (en attendant MongoDB)
    completed_games_db: Dict[str, List[CompletedGame]] = defaultdict(list)
    
    @classmethod
    def save_completed_game(cls, user_id: str, game: Game, final_ranking: List[Dict[str, Any]]) -> CompletedGame:
        """Sauvegarde une partie terminée et retourne l'objet CompletedGame"""
        
        # Calculer la durée approximative
        duration = "15-30 min"  # Placeholder - peut être calculé selon les événements
        
        # Trouver le gagnant
        winner = None
        if final_ranking:
            winner_data = final_ranking[0]  # Premier dans le classement
            winner = f"{winner_data.get('player', {}).get('name', 'Inconnu')} (#{winner_data.get('player', {}).get('number', '000')})"
        
        # Compter les survivants
        survivors = len([p for p in game.players if p.alive])
        
        # Calculer les gains (simplifié)
        earnings = game.earnings if hasattr(game, 'earnings') else 0
        
        # Créer l'objet partie terminée
        completed_game = CompletedGame(
            id=game.id,
            date=datetime.now().strftime("%d/%m/%Y %H:%M"),
            duration=duration,
            total_players=len(game.players),
            survivors=survivors,
            winner=winner,
            earnings=earnings,
            events_played=[event.name for event in game.events],
            final_ranking=final_ranking
        )
        
        # Sauvegarder dans le "pseudo-database"
        cls.completed_games_db[user_id].append(completed_game)
        
        # Garder seulement les 50 dernières parties pour éviter une surcharge mémoire
        if len(cls.completed_games_db[user_id]) > 50:
            cls.completed_games_db[user_id] = cls.completed_games_db[user_id][-50:]
        
        return completed_game
    
    @classmethod
    def calculate_role_statistics(cls, user_id: str) -> List[RoleStats]:
        """Calcule les statistiques pour chaque rôle basé sur l'historique des parties"""
        
        completed_games = cls.completed_games_db.get(user_id, [])
        
        if not completed_games:
            # Retourner des statistiques vides si aucune partie
            return [
                RoleStats(role="normal", appearances=0, survival_rate=0.0, wins=0, average_score=0.0),
                RoleStats(role="sportif", appearances=0, survival_rate=0.0, wins=0, average_score=0.0),
                RoleStats(role="intelligent", appearances=0, survival_rate=0.0, wins=0, average_score=0.0),
                RoleStats(role="brute", appearances=0, survival_rate=0.0, wins=0, average_score=0.0),
                RoleStats(role="peureux", appearances=0, survival_rate=0.0, wins=0, average_score=0.0),
                RoleStats(role="zero", appearances=0, survival_rate=0.0, wins=0, average_score=0.0)
            ]
        
        # Analyser les données des parties
        role_data = defaultdict(lambda: {
            'appearances': 0,
            'survivals': 0,
            'wins': 0,
            'total_score': 0
        })
        
        for game in completed_games:
            # Analyser le classement final pour les statistiques
            for rank_entry in game.final_ranking:
                player_data = rank_entry.get('player', {})
                role = player_data.get('role', 'normal').lower()
                
                role_data[role]['appearances'] += 1
                role_data[role]['total_score'] += rank_entry.get('total_score', 0)
                
                # Le joueur a survécu s'il est dans le classement et alive
                if rank_entry.get('alive', False):
                    role_data[role]['survivals'] += 1
                
                # Le gagnant est le premier du classement
                if rank_entry == game.final_ranking[0]:
                    role_data[role]['wins'] += 1
        
        # Convertir en objets RoleStats
        role_stats = []
        for role_name in ['normal', 'sportif', 'intelligent', 'brute', 'peureux', 'zero']:
            data = role_data[role_name]
            appearances = data['appearances']
            
            survival_rate = (data['survivals'] / appearances * 100) if appearances > 0 else 0.0
            average_score = (data['total_score'] / appearances) if appearances > 0 else 0.0
            
            role_stats.append(RoleStats(
                role=role_name,
                appearances=appearances,
                survival_rate=round(survival_rate, 1),
                wins=data['wins'],
                average_score=round(average_score, 1)
            ))
        
        return role_stats
    
    @classmethod
    def calculate_event_statistics(cls, user_id: str) -> List[Dict[str, Any]]:
        """Calcule les statistiques pour chaque épreuve et retourne un tableau trié"""
        
        completed_games = cls.completed_games_db.get(user_id, [])
        
        if not completed_games:
            return []
        
        event_stats = defaultdict(lambda: {
            'name': '',
            'played_count': 0,
            'total_participants': 0,
            'total_eliminations': 0,
            'deaths': 0,
            'survival_rate': 0.0,
            'average_elimination_rate': 0.0
        })
        
        total_events_data = {}
        
        for game in completed_games:
            for event_name in game.events_played:
                if event_name not in event_stats:
                    event_stats[event_name]['name'] = event_name
                
                event_stats[event_name]['played_count'] += 1
                
                # Calculer les statistiques basées sur les données disponibles
                # En utilisant les données du jeu pour estimer les participants et éliminations
                if hasattr(game, 'total_players') and game.total_players:
                    avg_participants_per_event = game.total_players // len(game.events_played) if game.events_played else game.total_players
                    event_stats[event_name]['total_participants'] += avg_participants_per_event
                    
                    # Estimer les éliminations (approximation basée sur les survivants)
                    if hasattr(game, 'survivors') and game.survivors:
                        total_eliminations = game.total_players - game.survivors
                        avg_eliminations_per_event = total_eliminations // len(game.events_played) if game.events_played else 0
                        event_stats[event_name]['deaths'] += avg_eliminations_per_event
                        event_stats[event_name]['total_eliminations'] += avg_eliminations_per_event
        
        # Calculer les taux de survie et organiser en tableau
        event_list = []
        for event_name, stats in event_stats.items():
            if stats['total_participants'] > 0:
                survival_rate = max(0, (stats['total_participants'] - stats['deaths']) / stats['total_participants'])
                stats['survival_rate'] = survival_rate
                stats['average_elimination_rate'] = 1.0 - survival_rate
            
            event_list.append(stats)
        
        # Trier par nombre de morts (événements les plus mortels en premier)
        event_list.sort(key=lambda x: x['deaths'], reverse=True)
        
        return event_list
    
    @classmethod
    def get_detailed_statistics(cls, user_id: str, basic_stats: GameStats) -> DetailedGameStats:
        """Retourne toutes les statistiques détaillées pour un utilisateur"""
        
        completed_games = cls.completed_games_db.get(user_id, [])
        role_statistics = cls.calculate_role_statistics(user_id)
        event_statistics = cls.calculate_event_statistics(user_id)
        
        return DetailedGameStats(
            basic_stats=basic_stats,
            completed_games=completed_games,
            role_statistics=role_statistics,
            event_statistics=event_statistics
        )
    
    @classmethod
    def get_completed_games(cls, user_id: str, limit: int = 20) -> List[CompletedGame]:
        """Retourne la liste des parties terminées pour un utilisateur"""
        completed_games = cls.completed_games_db.get(user_id, [])
        return completed_games[-limit:] if limit else completed_games
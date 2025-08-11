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
        
        # CORRECTION CRITIQUE : Utiliser le VRAI gagnant de game.winner au lieu du premier du classement
        winner = None
        if hasattr(game, 'winner') and game.winner:
            # Le gagnant est déjà déterminé correctement dans game_routes.py
            # On sauvegarde l'objet winner complet pour pouvoir l'utiliser dans la boutique de célébrités
            if isinstance(game.winner, dict):
                winner = game.winner
            elif hasattr(game.winner, '__dict__'):
                # Convertir l'objet Player en dictionnaire
                winner_dict = {
                    'name': getattr(game.winner, 'name', 'Gagnant Inconnu'),
                    'nationality': getattr(game.winner, 'nationality', 'Inconnue'),
                    'role': getattr(game.winner, 'role', 'normal'),
                    'number': getattr(game.winner, 'number', '000'),
                    'total_score': getattr(game.winner, 'total_score', 0),
                    'kills': getattr(game.winner, 'kills', 0),
                    'betrayals': getattr(game.winner, 'betrayals', 0),
                    'survived_events': getattr(game.winner, 'survived_events', 0)
                }
                # Ajouter les stats si disponibles
                if hasattr(game.winner, 'stats'):
                    winner_dict['stats'] = {
                        'intelligence': getattr(game.winner.stats, 'intelligence', 5),
                        'force': getattr(game.winner.stats, 'force', 5),
                        'agilite': getattr(game.winner.stats, 'agilite', 5)
                    }
                elif hasattr(game.winner, 'intelligence'):
                    # Stats directes sur l'objet Player
                    winner_dict['stats'] = {
                        'intelligence': getattr(game.winner, 'intelligence', 5),
                        'force': getattr(game.winner, 'force', 5),
                        'agilite': getattr(game.winner, 'agilite', 5)
                    }
                
                # Ajouter le portrait si disponible
                if hasattr(game.winner, 'portrait'):
                    portrait = game.winner.portrait
                    winner_dict['portrait'] = {
                        'gender': getattr(portrait, 'gender', 'male'),
                        'face_shape': getattr(portrait, 'face_shape', 'round'),
                        'skin_color': getattr(portrait, 'skin_color', 'light'),
                        'hair_color': getattr(portrait, 'hair_color', 'brown'),
                        'hair_style': getattr(portrait, 'hair_style', 'short'),
                        'eye_color': getattr(portrait, 'eye_color', 'brown')
                    }
                
                winner = winner_dict
            else:
                # Fallback - créer un objet basique si on ne peut pas extraire les données
                winner = {
                    'name': str(game.winner) if game.winner else 'Gagnant Inconnu',
                    'nationality': 'Inconnue',
                    'total_score': 0
                }
        elif final_ranking:
            # Fallback legacy : utiliser le premier du classement seulement si pas de game.winner
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
            winner=winner,  # Maintenant on sauvegarde l'objet winner complet
            earnings=earnings,
            events_played=[event.name for event in game.events],
            final_ranking=final_ranking
        )
        
        # CORRECTION DOUBLONS : Vérifier si la partie n'est pas déjà sauvegardée
        existing_game_ids = [game.id for game in cls.completed_games_db[user_id]]
        
        if completed_game.id not in existing_game_ids:
            # Sauvegarder seulement si pas déjà présente
            cls.completed_games_db[user_id].append(completed_game)
            print(f"✅ Partie {completed_game.id} sauvegardée (nouvelles stats)")
        else:
            print(f"⚠️ Partie {completed_game.id} déjà sauvegardée, ignorée pour éviter doublon")
        
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
            # AMÉLIORATION : Si pas de final_ranking, utiliser directement les données des joueurs
            if not game.final_ranking or len(game.final_ranking) == 0:
                # Essayer de récupérer les données depuis games_db pour obtenir les joueurs
                try:
                    from routes.game_routes import games_db
                    if game.id in games_db:
                        full_game = games_db[game.id]
                        if hasattr(full_game, 'players') and full_game.players:
                            # Créer un final_ranking temporaire depuis les joueurs
                            temp_ranking = []
                            for player in full_game.players:
                                temp_ranking.append({
                                    'player': {
                                        'role': getattr(player, 'role', 'normal'),
                                        'name': getattr(player, 'name', 'Inconnu')
                                    },
                                    'alive': getattr(player, 'alive', False),
                                    'total_score': getattr(player, 'total_score', 0)
                                })
                            game.final_ranking = temp_ranking
                            print(f"📊 Statistiques rôles: Créé ranking temporaire pour partie {game.id} avec {len(temp_ranking)} joueurs")
                except:
                    print(f"⚠️ Impossible de récupérer les données des joueurs pour la partie {game.id}")
                    continue
            
            # Analyser le classement final pour les statistiques
            for rank_entry in game.final_ranking:
                player_data = rank_entry.get('player', {})
                role = player_data.get('role', 'normal')
                
                # Normaliser le rôle (enlever les majuscules, espaces, etc.)
                if isinstance(role, str):
                    role = role.lower().strip()
                
                role_data[role]['appearances'] += 1
                role_data[role]['total_score'] += rank_entry.get('total_score', 0)
                
                # Le joueur a survécu s'il est dans le classement et alive
                # CORRECTION BUG : Vérifier aussi dans les game_stats si disponible
                is_alive = rank_entry.get('alive', False)
                if not is_alive and 'game_stats' in rank_entry:
                    # Fallback - si pas d'info "alive", vérifier si survived_events > 0
                    is_alive = rank_entry['game_stats'].get('survived_events', 0) > 0
                    
                if is_alive:
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
        """Calcule les statistiques pour chaque épreuve en utilisant les vraies données de jeu"""
        
        completed_games = cls.completed_games_db.get(user_id, [])
        
        if not completed_games:
            return []
        
        event_stats = defaultdict(lambda: {
            'name': '',
            'event_type': '',  # Ajouter le type d'événement
            'played_count': 0,
            'total_participants': 0,
            'total_eliminations': 0,
            'deaths': 0,
            'survival_rate': 0.0,
            'average_elimination_rate': 0.0
        })
        
        # Importer les données des parties pour accéder aux event_results détaillés
        try:
            from routes.game_routes import games_db
            
            # Parcourir toutes les parties terminées pour obtenir les vraies données
            for completed_game in completed_games:
                if completed_game.id in games_db:
                    full_game = games_db[completed_game.id]
                    
                    # Utiliser les event_results réels si disponibles
                    if hasattr(full_game, 'event_results') and full_game.event_results:
                        for event_result in full_game.event_results:
                            event_name = event_result.event_name
                            
                            if event_name not in event_stats:
                                event_stats[event_name]['name'] = event_name
                                
                                # Récupérer le type d'événement depuis EventsService
                                try:
                                    from services.events_service import EventsService
                                    matching_events = [e for e in EventsService.GAME_EVENTS if e.name == event_name]
                                    if matching_events:
                                        event_stats[event_name]['event_type'] = matching_events[0].type.value
                                except:
                                    event_stats[event_name]['event_type'] = 'unknown'
                            
                            event_stats[event_name]['played_count'] += 1
                            event_stats[event_name]['total_participants'] += event_result.total_participants
                            event_stats[event_name]['deaths'] += len(event_result.eliminated)
                            event_stats[event_name]['total_eliminations'] += len(event_result.eliminated)
                    
                    # Fallback sur les events_played si pas d'event_results
                    elif hasattr(completed_game, 'events_played') and completed_game.events_played:
                        for event_name in completed_game.events_played:
                            if event_name not in event_stats:
                                event_stats[event_name]['name'] = event_name
                                
                                # Récupérer le type d'événement depuis EventsService
                                try:
                                    from services.events_service import EventsService
                                    matching_events = [e for e in EventsService.GAME_EVENTS if e.name == event_name]
                                    if matching_events:
                                        event_stats[event_name]['event_type'] = matching_events[0].type.value
                                except:
                                    event_stats[event_name]['event_type'] = 'unknown'
                            
                            event_stats[event_name]['played_count'] += 1
                            
                            # Estimation basée sur les données disponibles
                            if hasattr(completed_game, 'total_players') and completed_game.total_players:
                                avg_participants_per_event = completed_game.total_players // len(completed_game.events_played) if completed_game.events_played else completed_game.total_players
                                event_stats[event_name]['total_participants'] += avg_participants_per_event
                                
                                # Estimer les éliminations
                                if hasattr(completed_game, 'survivors') and completed_game.survivors:
                                    total_eliminations = completed_game.total_players - completed_game.survivors
                                    avg_eliminations_per_event = total_eliminations // len(completed_game.events_played) if completed_game.events_played else 0
                                    event_stats[event_name]['deaths'] += avg_eliminations_per_event
                                    event_stats[event_name]['total_eliminations'] += avg_eliminations_per_event
        
        except ImportError:
            # Si on ne peut pas importer games_db, utiliser la méthode d'estimation
            for game in completed_games:
                for event_name in game.events_played:
                    if event_name not in event_stats:
                        event_stats[event_name]['name'] = event_name
                        
                        # Récupérer le type d'événement depuis EventsService
                        try:
                            from services.events_service import EventsService
                            matching_events = [e for e in EventsService.GAME_EVENTS if e.name == event_name]
                            if matching_events:
                                event_stats[event_name]['event_type'] = matching_events[0].type.value
                        except:
                            event_stats[event_name]['event_type'] = 'unknown'
                    
                    event_stats[event_name]['played_count'] += 1
                    
                    # Estimation basée sur les données disponibles
                    if hasattr(game, 'total_players') and game.total_players:
                        avg_participants_per_event = game.total_players // len(game.events_played) if game.events_played else game.total_players
                        event_stats[event_name]['total_participants'] += avg_participants_per_event
                        
                        # Estimer les éliminations
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
import random
from typing import List, Dict, Optional, Tuple
from models.game_models import Player, PlayerGroup, EventResult, GameEvent
from enum import Enum

class GroupService:
    """Service pour gérer les groupes de joueurs et leurs interactions"""
    
    @staticmethod
    def can_attack_target(attacker: Player, target: Player, groups: Dict[str, PlayerGroup]) -> bool:
        """
        Vérifie si un joueur peut attaquer un autre joueur en tenant compte des groupes
        
        Args:
            attacker: Le joueur qui attaque
            target: Le joueur ciblé
            groups: Dictionnaire des groupes actifs
            
        Returns:
            bool: True si l'attaque est autorisée, False sinon
        """
        # Si aucun des deux n'est dans un groupe, l'attaque est autorisée
        if not attacker.group_id and not target.group_id:
            return True
        
        # Si ils ne sont pas dans le même groupe, l'attaque est autorisée
        if attacker.group_id != target.group_id:
            return True
        
        # S'ils sont dans le même groupe, vérifier si les trahisons sont autorisées
        if attacker.group_id and attacker.group_id in groups:
            group = groups[attacker.group_id]
            return group.allow_betrayals
        
        # Par défaut, empêcher l'attaque entre membres du même groupe
        return False
    
    @staticmethod
    def calculate_group_survival_bonus(player: Player, groups: Dict[str, PlayerGroup]) -> float:
        """
        Calcule le bonus de survie pour un joueur basé sur son groupe
        
        Args:
            player: Le joueur
            groups: Dictionnaire des groupes actifs
            
        Returns:
            float: Bonus de survie (0.0 à 2.0)
        """
        if not player.group_id or player.group_id not in groups:
            return 0.0
        
        group = groups[player.group_id]
        
        # Compter les membres vivants du groupe
        # Note: Dans une vraie implémentation, il faudrait avoir accès à tous les joueurs
        # Pour l'instant, on estime basé sur la taille du groupe
        alive_members = len(group.member_ids)  # Simplification
        
        # Plus il y a de membres vivants, plus le bonus est important
        bonus = 0.1 * alive_members  # 0.1 point par membre vivant
        return min(bonus, 2.0)  # Limiter le bonus à 2.0
    
    @staticmethod
    def handle_group_betrayal(betrayer: Player, victim: Player, groups: Dict[str, PlayerGroup]) -> bool:
        """
        Gère une trahison entre membres d'un même groupe
        
        Args:
            betrayer: Le joueur qui trahit
            victim: Le joueur trahi
            groups: Dictionnaire des groupes actifs
            
        Returns:
            bool: True si c'est considéré comme une trahison, False sinon
        """
        # Vérifier si ils sont dans le même groupe
        if not betrayer.group_id or betrayer.group_id != victim.group_id:
            return False
        
        # Vérifier si les trahisons sont autorisées dans ce groupe
        if betrayer.group_id in groups:
            group = groups[betrayer.group_id]
            if group.allow_betrayals:
                # C'est une trahison autorisée
                betrayer.betrayals += 1
                return True
        
        # Ce ne devrait pas arriver si les règles sont respectées
        return False
    
    @staticmethod
    def get_group_allies(player: Player, all_players: List[Player]) -> List[Player]:
        """
        Récupère les alliés d'un joueur (membres du même groupe)
        
        Args:
            player: Le joueur
            all_players: Liste de tous les joueurs
            
        Returns:
            List[Player]: Liste des alliés
        """
        if not player.group_id:
            return []
        
        allies = []
        for other_player in all_players:
            if (other_player.id != player.id and 
                other_player.group_id == player.group_id and 
                other_player.alive):
                allies.append(other_player)
        
        return allies
    
    @staticmethod
    def assign_players_to_groups(players: List[Player], groups: List[PlayerGroup]) -> List[Player]:
        """
        Assigne les joueurs à leurs groupes respectifs
        
        Args:
            players: Liste des joueurs
            groups: Liste des groupes
            
        Returns:
            List[Player]: Liste des joueurs avec group_id mis à jour
        """
        # Créer un mapping des IDs de joueurs vers les IDs de groupes
        player_to_group = {}
        for group in groups:
            for member_id in group.member_ids:
                player_to_group[member_id] = group.id
        
        # Assigner les group_id aux joueurs
        updated_players = []
        for player in players:
            player.group_id = player_to_group.get(player.id)
            updated_players.append(player)
        
        return updated_players
    
    @staticmethod
    def simulate_group_cooperation_event(
        players: List[Player], 
        event: GameEvent, 
        groups: Dict[str, PlayerGroup]
    ) -> EventResult:
        """
        Simule un événement en tenant compte de la coopération entre groupes
        
        Args:
            players: Liste des joueurs participants
            event: L'événement à simuler
            groups: Dictionnaire des groupes actifs
            
        Returns:
            EventResult: Résultat de l'événement modifié par la coopération de groupe
        """
        alive_players = [p for p in players if p.alive]
        
        if not alive_players:
            return EventResult(
                event_id=event.id,
                event_name=event.name,
                survivors=[],
                eliminated=[],
                total_participants=0
            )
        
        # Calculer les scores de survie avec bonus de groupe
        player_scores = []
        for player in alive_players:
            base_score = random.uniform(1, 10)  # Score de base
            group_bonus = GroupService.calculate_group_survival_bonus(player, groups)
            total_score = base_score + group_bonus
            
            player_scores.append((player, total_score))
        
        # Trier par score (les meilleurs survivent)
        player_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Calculer le nombre de survivants selon le taux d'élimination
        num_survivors = max(1, int(len(alive_players) * (1 - event.elimination_rate)))
        
        survivors = [player for player, _ in player_scores[:num_survivors]]
        eliminated = [player for player, _ in player_scores[num_survivors:]]
        
        # Mettre à jour les stats des joueurs
        for player in survivors:
            player.survived_events += 1
        
        return EventResult(
            event_id=event.id,
            event_name=event.name,
            survivors=survivors,
            eliminated=eliminated,
            total_participants=len(alive_players)
        )
    
    @staticmethod
    def generate_group_names(count: int) -> List[str]:
        """
        Génère des noms de groupes créatifs
        
        Args:
            count: Nombre de noms à générer
            
        Returns:
            List[str]: Liste des noms de groupes
        """
        base_names = [
            "Les Inséparables", "Les Résistants", "L'Alliance", "La Confrérie",
            "Les Protecteurs", "Les Loyaux", "La Coalition", "Les Unis",
            "L'Entente", "Les Gardiens", "La Fraternité", "Les Défenseurs",
            "L'Union", "Les Fidèles", "La Ligue", "Les Compagnons",
            "Les Solidaires", "L'Équipe", "La Bande", "Les Camarades"
        ]
        
        if count <= len(base_names):
            return random.sample(base_names, count)
        else:
            # Si on a besoin de plus de noms, utiliser des numéros
            names = base_names.copy()
            for i in range(len(base_names) + 1, count + 1):
                names.append(f"Groupe {i}")
            return names[:count]
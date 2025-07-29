from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import random
from typing import List, Dict, Any
from models.game_models import (
    PlayerGroup, 
    GroupCreateRequest, 
    GroupUpdateRequest, 
    AutoGroupRequest,
    Player
)

router = APIRouter()

# Stockage temporaire en mémoire (en attendant MongoDB)
groups_storage: Dict[str, PlayerGroup] = {}

@router.post("/groups", response_model=PlayerGroup)
async def create_group(request: GroupCreateRequest):
    """Créer un nouveau groupe de joueurs"""
    group = PlayerGroup(
        name=request.name,
        member_ids=request.member_ids,
        allow_betrayals=request.allow_betrayals
    )
    groups_storage[group.id] = group
    return group

@router.get("/groups", response_model=List[PlayerGroup])
async def get_all_groups():
    """Récupérer tous les groupes"""
    return list(groups_storage.values())

@router.get("/groups/{group_id}", response_model=PlayerGroup)
async def get_group(group_id: str):
    """Récupérer un groupe par son ID"""
    if group_id not in groups_storage:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    return groups_storage[group_id]

@router.put("/groups/{group_id}", response_model=PlayerGroup)
async def update_group(group_id: str, request: GroupUpdateRequest):
    """Modifier un groupe existant"""
    if group_id not in groups_storage:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    group = groups_storage[group_id]
    
    if request.name is not None:
        group.name = request.name
    if request.member_ids is not None:
        group.member_ids = request.member_ids
    if request.allow_betrayals is not None:
        group.allow_betrayals = request.allow_betrayals
    
    groups_storage[group_id] = group
    return group

@router.delete("/groups/{group_id}")
async def delete_group(group_id: str):
    """Supprimer un groupe"""
    if group_id not in groups_storage:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    del groups_storage[group_id]
    return {"message": "Groupe supprimé avec succès"}

class AutoGroupWithPlayersRequest(BaseModel):
    """Requête pour créer des groupes automatiquement avec les joueurs"""
    players: List[Player]
    num_groups: int = Field(..., ge=1, le=20)
    min_members: int = Field(default=2, ge=2, le=8)
    max_members: int = Field(default=8, ge=2, le=8)
    allow_betrayals: bool = Field(default=False)

@router.post("/groups/auto-create", response_model=List[PlayerGroup])
async def create_groups_automatically(request: AutoGroupWithPlayersRequest):
    """Créer des groupes automatiquement avec répartition aléatoire"""
    players = request.players
    
    if not players:
        raise HTTPException(status_code=400, detail="Aucun joueur fourni")
    
    if len(players) < request.num_groups * request.min_members:
        raise HTTPException(
            status_code=400, 
            detail=f"Pas assez de joueurs pour créer {request.num_groups} groupes avec minimum {request.min_members} membres chacun"
        )
    
    # Mélanger la liste des joueurs
    available_players = players.copy()
    random.shuffle(available_players)
    
    groups = []
    player_index = 0
    
    # Créer les groupes
    for i in range(request.num_groups):
        # Calculer le nombre de membres pour ce groupe
        remaining_players = len(available_players) - player_index
        remaining_groups = request.num_groups - i
        
        # Assurer au moins min_members par groupe restant
        min_needed = remaining_groups * request.min_members
        available_for_this_group = remaining_players - min_needed + request.min_members
        
        # Limiter par max_members
        members_count = min(
            random.randint(request.min_members, request.max_members),
            available_for_this_group,
            remaining_players
        )
        
        # Créer le groupe
        group_members = []
        for _ in range(members_count):
            if player_index < len(available_players):
                group_members.append(available_players[player_index].id)
                player_index += 1
        
        group = PlayerGroup(
            name=f"Groupe {i + 1}",
            member_ids=group_members,
            allow_betrayals=request.allow_betrayals
        )
        
        groups.append(group)
        groups_storage[group.id] = group
    
    return groups

@router.get("/groups/{group_id}/members", response_model=List[str])
async def get_group_members(group_id: str):
    """Récupérer les IDs des membres d'un groupe"""
    if group_id not in groups_storage:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    return groups_storage[group_id].member_ids

@router.post("/groups/{group_id}/add-member")
async def add_member_to_group(group_id: str, player_id: str):
    """Ajouter un joueur à un groupe"""
    if group_id not in groups_storage:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    group = groups_storage[group_id] 
    if player_id not in group.member_ids:
        group.member_ids.append(player_id)
        groups_storage[group_id] = group
    
    return {"message": "Joueur ajouté au groupe avec succès"}

@router.post("/groups/{group_id}/remove-member")
async def remove_member_from_group(group_id: str, player_id: str):
    """Retirer un joueur d'un groupe"""
    if group_id not in groups_storage:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    group = groups_storage[group_id]
    if player_id in group.member_ids:
        group.member_ids.remove(player_id)
        groups_storage[group_id] = group
    
    return {"message": "Joueur retiré du groupe avec succès"}

@router.post("/groups/clear-all")
async def clear_all_groups():
    """Supprimer tous les groupes"""
    global groups_storage
    groups_storage = {}
    return {"message": "Tous les groupes ont été supprimés"}

@router.get("/groups/player/{player_id}/group", response_model=PlayerGroup)
async def get_player_group(player_id: str):
    """Récupérer le groupe d'un joueur spécifique"""
    for group in groups_storage.values():
        if player_id in group.member_ids:
            return group
    
    raise HTTPException(status_code=404, detail="Joueur ne fait partie d'aucun groupe")

@router.get("/groups/stats")
async def get_groups_stats():
    """Récupérer les statistiques des groupes"""
    total_groups = len(groups_storage)
    total_members = sum(len(group.member_ids) for group in groups_storage.values())
    groups_with_betrayals = sum(1 for group in groups_storage.values() if group.allow_betrayals)
    
    return {
        "total_groups": total_groups,
        "total_members_in_groups": total_members,
        "groups_with_betrayals_enabled": groups_with_betrayals,
        "average_group_size": round(total_members / total_groups, 2) if total_groups > 0 else 0
    }
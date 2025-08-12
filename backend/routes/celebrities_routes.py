from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import random

from models.game_models import Celebrity
from services.game_service import GameService

router = APIRouter(prefix="/api/celebrities", tags=["celebrities"])

class CelebrityDeathRequest(BaseModel):
    game_id: str

# Stockage temporaire en mémoire
celebrities_db = []

def init_celebrities():
    global celebrities_db
    if not celebrities_db:
        celebrities_db = GameService.generate_celebrities(1000)

init_celebrities()

@router.get("/", response_model=List[Celebrity])
async def get_celebrities(
    category: Optional[str] = None,
    stars: Optional[int] = Query(None, ge=2, le=5),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    include_dead: bool = Query(False, description="Inclure les célébrités mortes")
):
    """Récupère la liste des célébrités avec filtrage optionnel"""
    # Filtrer les célébrités mortes sauf si explicitement demandé
    if include_dead:
        filtered_celebrities = celebrities_db
    else:
        filtered_celebrities = [c for c in celebrities_db if not c.is_dead]
    
    # Filtrer par catégorie
    if category:
        filtered_celebrities = [c for c in filtered_celebrities if c.category.lower() == category.lower()]
    
    # Filtrer par nombre d'étoiles
    if stars is not None:
        filtered_celebrities = [c for c in filtered_celebrities if c.stars == stars]
    
    # Pagination
    return filtered_celebrities[offset:offset + limit]

@router.get("/{celebrity_id}", response_model=Celebrity)
async def get_celebrity(celebrity_id: str):
    """Récupère une célébrité par son ID"""
    celebrity = next((c for c in celebrities_db if c.id == celebrity_id), None)
    if not celebrity:
        raise HTTPException(status_code=404, detail="Célébrité non trouvée")
    return celebrity

@router.get("/categories/available", response_model=List[str])
async def get_categories():
    """Récupère la liste des catégories de célébrités disponibles"""
    categories = list(set(c.category for c in celebrities_db))
    return sorted(categories)

@router.post("/{celebrity_id}/purchase")
async def purchase_celebrity(celebrity_id: str):
    """Marque une célébrité comme achetée (logique simplifiée)"""
    celebrity = next((c for c in celebrities_db if c.id == celebrity_id), None)
    if not celebrity:
        raise HTTPException(status_code=404, detail="Célébrité non trouvée")
    
    celebrity.is_owned = True
    return {"message": f"Célébrité {celebrity.name} achetée avec succès"}

@router.get("/owned/list", response_model=List[Celebrity])
async def get_owned_celebrities(include_dead: bool = Query(False, description="Inclure les célébrités mortes")):
    """Récupère la liste des célébrités possédées"""
    owned_celebrities = [c for c in celebrities_db if c.is_owned]
    
    # Filtrer les célébrités mortes sauf si explicitement demandé
    if not include_dead:
        owned_celebrities = [c for c in owned_celebrities if not c.is_dead]
    
    return owned_celebrities

@router.post("/generate-new")
async def generate_new_celebrities(count: int = 100):
    """Génère de nouvelles célébrités"""
    global celebrities_db
    
    if count < 1 or count > 500:
        raise HTTPException(status_code=400, detail="Le nombre doit être entre 1 et 500")
    
    new_celebrities = GameService.generate_celebrities(count)
    celebrities_db.extend(new_celebrities)
    
    return {"message": f"{count} nouvelles célébrités générées", "total": len(celebrities_db)}

@router.get("/search/by-name", response_model=List[Celebrity])
async def search_celebrities_by_name(name: str, limit: int = 20):
    """Recherche des célébrités par nom"""
    matching_celebrities = [
        c for c in celebrities_db 
        if name.lower() in c.name.lower()
    ]
    return matching_celebrities[:limit]

@router.get("/random/selection", response_model=List[Celebrity])
async def get_random_celebrities(count: int = 10):
    """Récupère une sélection aléatoire de célébrités"""
    if count > len(celebrities_db):
        count = len(celebrities_db)
    
    return random.sample(celebrities_db, count)

@router.put("/{celebrity_id}/victory")
async def record_celebrity_victory(celebrity_id: str):
    """Enregistre une victoire pour une célébrité"""
    celebrity = next((c for c in celebrities_db if c.id == celebrity_id), None)
    if not celebrity:
        raise HTTPException(status_code=404, detail="Célébrité non trouvée")
    
    celebrity.wins += 1
    
    # Améliorer les stats après une victoire (bonus mineur)
    if celebrity.wins % 3 == 0:  # Tous les 3 victoires
        if celebrity.stats.intelligence < 10:
            celebrity.stats.intelligence += 1
        elif celebrity.stats.force < 10:
            celebrity.stats.force += 1
        elif celebrity.stats.agilité < 10:
            celebrity.stats.agilité += 1
    
    return {
        "message": f"Victoire enregistrée pour {celebrity.name}",
        "total_wins": celebrity.wins,
        "stats": celebrity.stats
    }

@router.put("/{celebrity_id}/participation")
async def record_celebrity_participation(celebrity_id: str, participation_data: dict):
    """Enregistre la participation d'une célébrité à un jeu"""
    celebrity = next((c for c in celebrities_db if c.id == celebrity_id), None)
    if not celebrity:
        raise HTTPException(status_code=404, detail="Célébrité non trouvée")
    
    # Enregistrer la participation même si elle n'a pas gagné
    # Cela peut inclure amélioration mineure des stats selon les performances
    survived_events = participation_data.get('survived_events', 0)
    total_score = participation_data.get('total_score', 0)
    
    # Amélioration mineure des stats en fonction des performances
    if survived_events >= 3:  # Si elle a survécu à au moins 3 épreuves
        if total_score > 100:  # Bon score
            # Améliorer légèrement les stats
            if celebrity.stats.intelligence < 10:
                celebrity.stats.intelligence += 1
            elif celebrity.stats.force < 10:
                celebrity.stats.force += 1
            elif celebrity.stats.agilité < 10:
                celebrity.stats.agilité += 1
    
    return {
        "message": f"Participation enregistrée pour {celebrity.name}",
        "performance": {
            "survived_events": survived_events,
            "total_score": total_score
        },
        "updated_stats": celebrity.stats
    }

@router.get("/stats/summary")
async def get_celebrities_stats():
    """Récupère des statistiques sur les célébrités"""
    total_celebrities = len(celebrities_db)
    owned_count = len([c for c in celebrities_db if c.is_owned])
    
    by_category = {}
    by_stars = {2: 0, 3: 0, 4: 0, 5: 0}
    total_wins = 0
    
    for celebrity in celebrities_db:
        # Par catégorie
        if celebrity.category not in by_category:
            by_category[celebrity.category] = 0
        by_category[celebrity.category] += 1
        
        # Par étoiles
        by_stars[celebrity.stars] += 1
        
        # Victoires totales
        total_wins += celebrity.wins
    
    return {
        "total_celebrities": total_celebrities,
        "owned_celebrities": owned_count,
        "by_category": by_category,
        "by_stars": by_stars,
        "total_wins": total_wins,
        "average_wins": total_wins / total_celebrities if total_celebrities > 0 else 0
    }

@router.post("/{celebrity_id}/death")
async def record_celebrity_death(celebrity_id: str, game_id: str):
    """Enregistre la mort d'une célébrité et génère automatiquement un remplacement"""
    global celebrities_db
    from datetime import datetime
    
    celebrity = next((c for c in celebrities_db if c.id == celebrity_id), None)
    if not celebrity:
        raise HTTPException(status_code=404, detail="Célébrité non trouvée")
    
    if celebrity.is_dead:
        return {"message": f"Célébrité {celebrity.name} est déjà marquée comme morte"}
    
    # Marquer la célébrité comme morte
    celebrity.is_dead = True
    celebrity.died_in_game_id = game_id
    celebrity.death_date = datetime.utcnow()
    
    # Générer automatiquement une nouvelle célébrité du même métier/catégorie
    new_celebrity = GameService.generate_single_celebrity(
        category=celebrity.category,
        stars=celebrity.stars
    )
    
    # L'ajouter à la base de données
    celebrities_db.append(new_celebrity)
    
    return {
        "message": f"Célébrité {celebrity.name} marquée comme morte dans le jeu {game_id}",
        "dead_celebrity": {
            "id": celebrity.id,
            "name": celebrity.name,
            "category": celebrity.category,
            "death_date": celebrity.death_date
        },
        "replacement_celebrity": {
            "id": new_celebrity.id,
            "name": new_celebrity.name,
            "category": new_celebrity.category,
            "stars": new_celebrity.stars,
            "price": new_celebrity.price
        }
    }

@router.get("/alive/list", response_model=List[Celebrity])
async def get_alive_celebrities():
    """Récupère la liste des célébrités vivantes (pour la boutique et la sélection)"""
    return [c for c in celebrities_db if not c.is_dead]

@router.get("/dead/list", response_model=List[Celebrity])
async def get_dead_celebrities():
    """Récupère la liste des célébrités mortes (pour les statistiques)"""
    return [c for c in celebrities_db if c.is_dead]
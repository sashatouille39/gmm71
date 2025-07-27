from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import random

from models.game_models import Celebrity
from services.game_service import GameService

router = APIRouter(prefix="/api/celebrities", tags=["celebrities"])

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
    offset: int = Query(0, ge=0)
):
    """Récupère la liste des célébrités avec filtrage optionnel"""
    filtered_celebrities = celebrities_db
    
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
async def get_owned_celebrities():
    """Récupère la liste des célébrités possédées"""
    return [c for c in celebrities_db if c.is_owned]

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
        elif celebrity.stats.agilite < 10:
            celebrity.stats.agilite += 1
    
    return {
        "message": f"Victoire enregistrée pour {celebrity.name}",
        "total_wins": celebrity.wins,
        "stats": celebrity.stats
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
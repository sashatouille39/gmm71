import random
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.game_models import (
    Player, PlayerRole, PlayerStats, PlayerPortrait, PlayerUniform,
    Game, GameEvent, EventResult, Celebrity, VipCharacter, EventType
)
from services.events_service import EventsService

class GameService:
    
    # Données statiques pour la génération
    NATIONALITIES = [
        "Coréenne", "Japonaise", "Chinoise", "Américaine", "Française", "Allemande", 
        "Britannique", "Italienne", "Espagnole", "Russe", "Brésilienne", "Indienne",
        "Australienne", "Canadienne", "Mexicaine", "Turque", "Égyptienne", "Nigériane"
    ]
    
    FACE_SHAPES = [
        "Ovale", "Rond", "Carré", "Rectangulaire", "Triangulaire", "Cœur", 
        "Losange", "Oblong", "Poire", "Hexagonal", "Pentagonal", "Allongé",
        "Large", "Étroit", "Angular", "Doux"
    ]
    
    SKIN_COLORS = [
        "#FDF2E9", "#FAE7D0", "#F8D7C0", "#F6C8A0", "#F4B980", "#E8A456",
        "#D49156", "#C07D46", "#AC6A36", "#985726", "#844516", "#703306",
        "#5C2100", "#481000", "#340000", "#FFEEE6", "#FFE4D6", "#FFDAC6",
        "#FFD0B6", "#FFC6A6", "#FFBC96", "#FFB286", "#FFA876", "#FF9E66",
        "#FF9456", "#E88A46", "#D18036", "#BA7626", "#A36C16"
    ]
    
    HAIRSTYLES = [
        "Cheveux courts", "Cheveux longs", "Bob", "Pixie", "Afro", "Dreadlocks",
        "Tresses", "Queue de cheval", "Chignon", "Mohawk", "Undercut", "Fade",
        "Pompadour", "Quiff", "Buzz cut", "Crew cut", "Slicked back", "Wavy",
        "Curly", "Straight", "Layered", "Shag", "Mullet", "Top knot", "Man bun",
        "Cornrows", "Bangs", "Side swept", "Spiky", "Messy", "Sleek", "Volume",
        "Textured", "Choppy", "Blunt", "Asymmetrical", "Retro", "Modern",
        "Classic", "Edgy", "Romantic", "Bohemian", "Punk", "Gothic", "Vintage",
        "Contemporary", "Trendy", "Timeless", "Elegant", "Casual", "Formal",
        "Sporty", "Artistic", "Creative", "Bold", "Subtle", "Natural", "Styled",
        "Wild", "Tame", "Flowing", "Structured", "Loose", "Tight", "Soft",
        "Hard", "Smooth", "Rough", "Fine", "Thick", "Thin", "Full", "Sparse",
        "Dense", "Light", "Heavy", "Bouncy", "Flat", "Voluminous", "Sleek"
    ]
    
    HAIR_COLORS = [
        "#2C1B18", "#3C2414", "#4A2C20", "#5D4037", "#6D4C41", "#8D6E63",
        "#A1887F", "#BCAAA4", "#D7CCC8", "#EFEBE9", "#FFF3E0", "#FFE0B2",
        "#FFCC02", "#FFA000", "#FF8F00", "#FF6F00", "#E65100", "#D84315",
        "#BF360C", "#A0522D", "#8B4513", "#654321", "#800080", "#9932CC",
        "#BA55D3", "#DA70D6", "#EE82EE", "#FF1493", "#FF69B4", "#FFB6C1"
    ]
    
    UNIFORM_STYLES = ["Classic", "Moderne", "Vintage", "Sport", "Élégant"]
    UNIFORM_COLORS = ["Rouge", "Bleu", "Vert", "Jaune", "Rose", "Violet", "Orange", "Noir", "Blanc"]
    UNIFORM_PATTERNS = ["Uni", "Rayures", "Carreaux", "Points", "Floral", "Géométrique"]
    
    # Utiliser le service d'événements pour les 80+ épreuves
    GAME_EVENTS = EventsService.GAME_EVENTS
    
    ROLE_PROBABILITIES = {
        PlayerRole.NORMAL: 0.60,
        PlayerRole.SPORTIF: 0.11,
        PlayerRole.PEUREUX: 0.10,
        PlayerRole.BRUTE: 0.11,
        PlayerRole.INTELLIGENT: 0.07,
        PlayerRole.ZERO: 0.01
    }
    
    @classmethod
    def generate_random_player(cls, player_id: int) -> Player:
        """Génère un joueur aléatoire selon les probabilités des rôles"""
        # Sélection du rôle selon les probabilités
        rand = random.random()
        cumulative_probability = 0
        selected_role = PlayerRole.NORMAL
        
        for role, probability in cls.ROLE_PROBABILITIES.items():
            cumulative_probability += probability
            if rand <= cumulative_probability:
                selected_role = role
                break
        
        nationality = random.choice(cls.NATIONALITIES)
        gender = random.choice(['M', 'F'])
        
        # Génération des stats selon le rôle
        stats = cls._generate_stats_by_role(selected_role)
        
        return Player(
            number=str(player_id).zfill(3),
            name=cls._generate_random_name(nationality, gender),
            nationality=nationality,
            gender=gender,
            role=selected_role,
            stats=stats,
            portrait=cls._generate_portrait(nationality),
            uniform=cls._generate_uniform()
        )
    
    @classmethod
    def _generate_stats_by_role(cls, role: PlayerRole) -> PlayerStats:
        """Génère les statistiques selon le rôle"""
        if role == PlayerRole.SPORTIF:
            agilite = random.randint(4, 8)
            force = max(2, min(10, agilite - 2 + random.randint(0, 3)))
            intelligence = max(0, 12 - agilite - force)
        elif role == PlayerRole.BRUTE:
            force = random.randint(4, 8)
            agilite = max(2, min(10, force - 2 + random.randint(0, 3)))
            intelligence = max(0, 12 - force - agilite)
        elif role == PlayerRole.INTELLIGENT:
            intelligence = random.randint(4, 8)
            # Bonus +2 aléatoire
            bonus_stat = random.choice(['intelligence', 'force', 'agilite'])
            force = random.randint(1, 4)
            agilite = random.randint(1, 4)
            if bonus_stat == 'force':
                force += 2
            elif bonus_stat == 'agilite':
                agilite += 2
            else:
                intelligence += 2
            # Ajuster pour totaliser 14 points
            total = intelligence + force + agilite
            if total > 14:
                excess = total - 14
                if agilite >= excess:
                    agilite -= excess
                elif force >= excess - agilite:
                    excess -= agilite
                    agilite = 0
                    force -= excess
                else:
                    intelligence -= excess
        elif role == PlayerRole.PEUREUX:
            # 8 points totaux
            intelligence = random.randint(0, 4)
            force = random.randint(0, 4)
            agilite = max(0, 8 - intelligence - force)
        elif role == PlayerRole.ZERO:
            intelligence = random.randint(4, 10)
            force = random.randint(4, 10)
            agilite = random.randint(4, 10)
        else:  # NORMAL
            # Distribution équilibrée de 12 points
            intelligence = random.randint(2, 6)
            force = random.randint(2, 6)
            agilite = max(0, min(10, 12 - intelligence - force))
        
        return PlayerStats(
            intelligence=max(0, min(10, intelligence)),
            force=max(0, min(10, force)),
            agilite=max(0, min(10, agilite))
        )
    
    @classmethod
    def _generate_random_name(cls, nationality: str, gender: str) -> str:
        """Génère un nom aléatoire selon la nationalité et le genre"""
        names = {
            'Coréenne': {
                'M': ['Min-jun', 'Seo-jun', 'Do-yoon', 'Si-woo', 'Joon-ho', 'Hyun-woo', 'Jin-woo', 'Sung-min'],
                'F': ['Seo-yeon', 'Min-seo', 'Ji-woo', 'Ha-eun', 'Soo-jin', 'Ye-jin', 'Su-bin', 'Na-eun']
            },
            'Japonaise': {
                'M': ['Hiroshi', 'Takeshi', 'Akira', 'Yuki', 'Daiki', 'Haruto', 'Sota', 'Ren'],
                'F': ['Sakura', 'Yuki', 'Ai', 'Rei', 'Mana', 'Yui', 'Hina', 'Emi']
            },
            'Française': {
                'M': ['Pierre', 'Jean', 'Michel', 'Alain', 'Philippe', 'Nicolas', 'Antoine', 'Julien'],
                'F': ['Marie', 'Nathalie', 'Isabelle', 'Sylvie', 'Catherine', 'Valérie', 'Christine', 'Sophie']
            },
            'Américaine': {
                'M': ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Christopher', 'Matthew'],
                'F': ['Mary', 'Jennifer', 'Linda', 'Patricia', 'Susan', 'Jessica', 'Sarah', 'Karen']
            },
            'Chinoise': {
                'M': ['Wei', 'Jun', 'Ming', 'Hao', 'Lei', 'Qiang', 'Yang', 'Bin'],
                'F': ['Li', 'Wang', 'Zhang', 'Liu', 'Chen', 'Yang', 'Zhao', 'Huang']
            }
        }
        
        nationality_names = names.get(nationality, names['Française'])
        gender_names = nationality_names[gender]
        return random.choice(gender_names)
    
    @classmethod
    def _generate_portrait(cls, nationality: str) -> PlayerPortrait:
        """Génère un portrait cohérent avec la nationalité"""
        skin_color_ranges = {
            'Coréenne': (0, 8),
            'Japonaise': (0, 8),
            'Chinoise': (2, 10),
            'Française': (0, 5),
            'Allemande': (0, 5),
            'Britannique': (0, 5),
            'Nigériane': (15, 24),
            'Indienne': (8, 18),
        }
        
        skin_range = skin_color_ranges.get(nationality, (0, 15))
        skin_color_index = random.randint(skin_range[0], min(skin_range[1], len(cls.SKIN_COLORS) - 1))
        
        return PlayerPortrait(
            face_shape=random.choice(cls.FACE_SHAPES),
            skin_color=cls.SKIN_COLORS[skin_color_index],
            hairstyle=random.choice(cls.HAIRSTYLES),
            hair_color=random.choice(cls.HAIR_COLORS),
            eye_color=random.choice(['#8B4513', '#654321', '#2F4F2F', '#483D8B', '#556B2F', '#000000']),
            eye_shape=random.choice(['Amande', 'Rond', 'Allongé', 'Tombant', 'Relevé', 'Petit', 'Grand'])
        )
    
    @classmethod
    def _generate_uniform(cls) -> PlayerUniform:
        """Génère un uniforme aléatoire"""
        return PlayerUniform(
            style=random.choice(cls.UNIFORM_STYLES),
            color=random.choice(cls.UNIFORM_COLORS),
            pattern=random.choice(cls.UNIFORM_PATTERNS)
        )
    
    @classmethod
    def simulate_event(cls, players: List[Player], event: GameEvent) -> EventResult:
        """Simule une épreuve et retourne les résultats"""
        alive_players = [p for p in players if p.alive]
        survivors = []
        eliminated = []
        
        for player in alive_players:
            # Calcul des chances de survie selon les stats et le rôle
            stat_bonus = cls._get_stat_bonus_for_event(player, event)
            role_bonus = cls._get_role_bonus_for_event(player, event)
            survive_chance = min(0.9, 0.3 + (stat_bonus * 0.06) + role_bonus)
            
            if random.random() < survive_chance:
                # Survie
                time_remaining = random.randint(20, 120)
                event_kills = random.randint(0, 2) if event.type == EventType.FORCE else random.randint(0, 1)
                betrayed = random.random() < 0.1
                
                player.survived_events += 1
                player.kills += event_kills
                if betrayed:
                    player.betrayals += 1
                
                score = time_remaining + (event_kills * 10) - (5 if betrayed else 0)
                player.total_score += score
                
                survivors.append({
                    "player": player,
                    "time_remaining": time_remaining,
                    "event_kills": event_kills,
                    "betrayed": betrayed,
                    "score": score
                })
            else:
                # Élimination
                player.alive = False
                eliminated.append({
                    "player": player,
                    "elimination_time": random.randint(10, 120),
                    "cause": cls._get_random_death_cause(event)
                })
        
        # Trier les survivants par score
        survivors.sort(key=lambda x: x["score"], reverse=True)
        
        return EventResult(
            event_id=event.id,
            event_name=event.name,
            survivors=[s["player"].dict() for s in survivors],
            eliminated=[e["player"].dict() for e in eliminated],
            total_participants=len(alive_players)
        )
    
    @classmethod
    def _get_stat_bonus_for_event(cls, player: Player, event: GameEvent) -> int:
        """Retourne le bonus de stat pour une épreuve"""
        if event.type == EventType.INTELLIGENCE:
            return player.stats.intelligence
        elif event.type == EventType.FORCE:
            return player.stats.force
        elif event.type == EventType.AGILITE:
            return player.stats.agilite
        else:
            return (player.stats.intelligence + player.stats.force + player.stats.agilite) // 3
    
    @classmethod
    def _get_role_bonus_for_event(cls, player: Player, event: GameEvent) -> float:
        """Retourne le bonus de rôle pour une épreuve"""
        if player.role == PlayerRole.INTELLIGENT and event.type == EventType.INTELLIGENCE:
            return 0.2
        elif player.role == PlayerRole.BRUTE and event.type == EventType.FORCE:
            return 0.2
        elif player.role == PlayerRole.SPORTIF and event.type == EventType.AGILITE:
            return 0.2
        elif player.role == PlayerRole.ZERO:
            return 0.15  # Bonus universel
        elif player.role == PlayerRole.PEUREUX:
            return -0.1
        else:
            return 0.05 if event.type in [EventType.INTELLIGENCE, EventType.FORCE, EventType.AGILITE] else 0
    
    @classmethod
    def _get_random_death_cause(cls, event: GameEvent) -> str:
        """Retourne une cause de mort aléatoire selon l'épreuve"""
        causes = {
            "Feu rouge, Feu vert": ['Abattu en mouvement', 'Panique collective', 'Tentative de fuite'],
            "Pont de verre": ['Chute mortelle', 'Verre brisé', 'Poussé par un autre joueur'],
            "Combat de gladiateurs": ['Coup fatal', 'Hémorragie', 'Épuisement'],
            "Bataille royale": ['Éliminé au combat', 'Blessures multiples', 'Abandon'],
            "Arène sanglante": ['Mort au combat', 'Coup de grâce', 'Saignement']
        }
        
        event_causes = causes.get(event.name, ['Élimination standard', 'Erreur fatale', 'Mauvaise décision'])
        return random.choice(event_causes)
    
    @classmethod
    def generate_celebrities(cls, count: int = 1000) -> List[Celebrity]:
        """Génère une liste de célébrités fictives"""
        celebrities = []
        categories = [
            ("Ancien vainqueur", 5, 45000, 55000),
            ("Sportif", 4, 20000, 30000),
            ("Scientifique", 4, 18000, 28000),
            ("Acteur", 3, 12000, 20000),
            ("Chanteuse", 3, 10000, 18000),
            ("Influenceur", 2, 6000, 12000),
            ("Chef", 2, 5000, 10000),
            ("Politicien", 3, 15000, 25000),
            ("Écrivain", 2, 8000, 15000),
            ("Artiste", 3, 10000, 20000)
        ]
        
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn', 
                      'Sage', 'River', 'Phoenix', 'Skyler', 'Rowan', 'Kai', 'Nova', 'Zara',
                      'Luna', 'Atlas', 'Iris', 'Orion', 'Maya', 'Leo', 'Aria', 'Max', 'Zoe']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                     'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 
                     'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
        
        for i in range(count):
            category, stars, min_price, max_price = random.choice(categories)
            price = random.randint(min_price, max_price)
            
            # Générer des stats selon la catégorie
            if category == "Ancien vainqueur":
                stats = PlayerStats(
                    intelligence=random.randint(7, 10),
                    force=random.randint(6, 9),
                    agilite=random.randint(7, 10)
                )
                wins = random.randint(1, 3)
            elif category == "Sportif":
                stats = PlayerStats(
                    intelligence=random.randint(4, 7),
                    force=random.randint(8, 10),
                    agilite=random.randint(8, 10)
                )
                wins = 0
            elif category == "Scientifique":
                stats = PlayerStats(
                    intelligence=random.randint(9, 10),
                    force=random.randint(2, 5),
                    agilite=random.randint(3, 6)
                )
                wins = 0
            else:
                stats = PlayerStats(
                    intelligence=random.randint(4, 8),
                    force=random.randint(3, 7),
                    agilite=random.randint(4, 8)
                )
                wins = 0
            
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            nationality = random.choice(cls.NATIONALITIES)
            
            biography = cls._generate_biography(category, name)
            
            celebrities.append(Celebrity(
                name=name,
                category=category,
                stars=stars,
                price=price,
                nationality=nationality,
                wins=wins,
                stats=stats,
                biography=biography
            ))
        
        return celebrities
    
    @classmethod
    def _generate_biography(cls, category: str, name: str) -> str:
        """Génère une biographie pour une célébrité"""
        bios = {
            "Ancien vainqueur": [
                f"{name} est un survivant légendaire qui a triomphé dans les jeux les plus brutaux.",
                f"Maître stratège, {name} a survécu à trois éditions consécutives des jeux.",
                f"{name} possède une expérience inégalée des épreuves mortelles."
            ],
            "Sportif": [
                f"Champion olympique, {name} excelle dans toutes les disciplines physiques.",
                f"{name} détient plusieurs records mondiaux en athlétisme.",
                f"La condition physique exceptionnelle de {name} est sa plus grande force."
            ],
            "Scientifique": [
                f"Génie reconnu mondialement, {name} a révolutionné son domaine.",
                f"{name} possède un QI exceptionnel et une logique implacable.",
                f"Prix Nobel, {name} résout les problèmes les plus complexes."
            ],
            "Acteur": [
                f"Star internationale, {name} a joué dans de nombreux films d'action.",
                f"{name} maîtrise les arts martiaux et les cascades.",
                f"Habitué des rôles de héros, {name} sait affronter le danger."
            ]
        }
        
        category_bios = bios.get(category, [f"{name} est une personnalité reconnue dans son domaine."])
        return random.choice(category_bios)
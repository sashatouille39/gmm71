import random
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.game_models import (
    Player, PlayerRole, PlayerStats, PlayerPortrait, PlayerUniform,
    Game, GameEvent, EventResult, Celebrity, VipCharacter, EventType, EventCategory
)
from services.events_service import EventsService
from services.portrait_generator_service import portrait_service

class GameService:
    
    # Données statiques pour la génération - Nationalités avec formes masculines et féminines
    NATIONALITIES = {
        "Afghan": {"M": "Afghan", "F": "Afghane"},
        "Allemand": {"M": "Allemand", "F": "Allemande"},
        "Argentin": {"M": "Argentin", "F": "Argentine"},
        "Australien": {"M": "Australien", "F": "Australienne"},
        "Autrichien": {"M": "Autrichien", "F": "Autrichienne"},
        "Belge": {"M": "Belge", "F": "Belge"},
        "Brésilien": {"M": "Brésilien", "F": "Brésilienne"},
        "Britannique": {"M": "Britannique", "F": "Britannique"},
        "Bulgare": {"M": "Bulgare", "F": "Bulgare"},
        "Canadien": {"M": "Canadien", "F": "Canadienne"},
        "Chinois": {"M": "Chinois", "F": "Chinoise"},
        "Coréen": {"M": "Coréen", "F": "Coréenne"},
        "Croate": {"M": "Croate", "F": "Croate"},
        "Danois": {"M": "Danois", "F": "Danoise"},
        "Égyptien": {"M": "Égyptien", "F": "Égyptienne"},
        "Espagnol": {"M": "Espagnol", "F": "Espagnole"},
        "Estonien": {"M": "Estonien", "F": "Estonienne"},
        "Finlandais": {"M": "Finlandais", "F": "Finlandaise"},
        "Français": {"M": "Français", "F": "Française"},
        "Grec": {"M": "Grec", "F": "Grecque"},
        "Hongrois": {"M": "Hongrois", "F": "Hongroise"},
        "Indien": {"M": "Indien", "F": "Indienne"},
        "Indonésien": {"M": "Indonésien", "F": "Indonésienne"},
        "Iranien": {"M": "Iranien", "F": "Iranienne"},
        "Irlandais": {"M": "Irlandais", "F": "Irlandaise"},
        "Islandais": {"M": "Islandais", "F": "Islandaise"},
        "Italien": {"M": "Italien", "F": "Italienne"},
        "Japonais": {"M": "Japonais", "F": "Japonaise"},
        "Marocain": {"M": "Marocain", "F": "Marocaine"},
        "Mexicain": {"M": "Mexicain", "F": "Mexicaine"},
        "Néerlandais": {"M": "Néerlandais", "F": "Néerlandaise"},
        "Nigérian": {"M": "Nigérian", "F": "Nigériane"},
        "Norvégien": {"M": "Norvégien", "F": "Norvégienne"},
        "Polonais": {"M": "Polonais", "F": "Polonaise"},
        "Portugais": {"M": "Portugais", "F": "Portugaise"},
        "Roumain": {"M": "Roumain", "F": "Roumaine"},
        "Russe": {"M": "Russe", "F": "Russe"},
        "Suédois": {"M": "Suédois", "F": "Suédoise"},
        "Suisse": {"M": "Suisse", "F": "Suisse"},
        "Tchèque": {"M": "Tchèque", "F": "Tchèque"},
        "Thaïlandais": {"M": "Thaïlandais", "F": "Thaïlandaise"},
        "Turc": {"M": "Turc", "F": "Turque"},
        "Américain": {"M": "Américain", "F": "Américaine"}
    }
    
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
        
        nationality_key = random.choice(list(cls.NATIONALITIES.keys()))
        gender = random.choice(['M', 'F'])
        nationality_display = cls.NATIONALITIES[nationality_key][gender]
        
        # Génération des stats selon le rôle
        stats = cls._generate_stats_by_role(selected_role)
        
        return Player(
            number=str(player_id).zfill(3),
            name=cls._generate_random_name(nationality_key, gender),
            nationality=nationality_display,
            gender=gender,
            role=selected_role,
            stats=stats,
            portrait=cls._generate_portrait(nationality_key, gender),
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
            agilité=max(0, min(10, agilite))
        )
    
    @classmethod
    def _generate_random_name(cls, nationality: str, gender: str) -> str:
        """Génère un nom complet aléatoire selon la nationalité et le genre"""
        first_names = {
            'Afghan': {
                'M': ['Ahmad', 'Mohammed', 'Abdul', 'Hassan', 'Omar', 'Ali', 'Mahmud', 'Rashid'],
                'F': ['Fatima', 'Aisha', 'Zara', 'Maryam', 'Layla', 'Nadia', 'Soraya', 'Jamila']
            },
            'Allemand': {
                'M': ['Hans', 'Klaus', 'Jürgen', 'Wolfgang', 'Dieter', 'Günter', 'Helmut', 'Manfred'],
                'F': ['Ursula', 'Ingrid', 'Gisela', 'Christa', 'Helga', 'Monika', 'Renate', 'Brigitte']
            },
            'Argentin': {
                'M': ['Carlos', 'Juan', 'José', 'Luis', 'Miguel', 'Jorge', 'Roberto', 'Diego'],
                'F': ['María', 'Ana', 'Carmen', 'Rosa', 'Isabel', 'Teresa', 'Cristina', 'Patricia']
            },
            'Australien': {
                'M': ['Jack', 'William', 'James', 'Benjamin', 'Luke', 'Henry', 'Alexander', 'Mason'],
                'F': ['Charlotte', 'Ruby', 'Lily', 'Sophie', 'Emily', 'Chloe', 'Mia', 'Grace']
            },
            'Autrichien': {
                'M': ['Johann', 'Franz', 'Karl', 'Josef', 'Georg', 'Anton', 'Heinrich', 'Paul'],
                'F': ['Maria', 'Anna', 'Elisabeth', 'Theresia', 'Johanna', 'Franziska', 'Katharina', 'Barbara']
            },
            'Belge': {
                'M': ['Jean', 'Pierre', 'Marc', 'Philippe', 'Michel', 'Paul', 'Luc', 'André'],
                'F': ['Marie', 'Anne', 'Catherine', 'Martine', 'Françoise', 'Monique', 'Christine', 'Isabelle']
            },
            'Brésilien': {
                'M': ['João', 'José', 'Carlos', 'Paulo', 'Pedro', 'Francisco', 'Luiz', 'Marcos'],
                'F': ['Maria', 'Ana', 'Francisca', 'Antônia', 'Adriana', 'Juliana', 'Márcia', 'Fernanda']
            },
            'Britannique': {
                'M': ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles'],
                'F': ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica']
            },
            'Bulgare': {
                'M': ['Georgi', 'Ivan', 'Dimitar', 'Nikolai', 'Stoyan', 'Petar', 'Hristo', 'Stefan'],
                'F': ['Maria', 'Elena', 'Valentina', 'Gergana', 'Daniela', 'Svetlana', 'Milena', 'Tsveta']
            },
            'Canadien': {
                'M': ['Liam', 'Noah', 'William', 'James', 'Logan', 'Benjamin', 'Mason', 'Ethan'],
                'F': ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Charlotte', 'Mia', 'Amelia']
            },
            'Chinois': {
                'M': ['Wei', 'Jun', 'Ming', 'Hao', 'Lei', 'Qiang', 'Yang', 'Bin'],
                'F': ['Li', 'Wang', 'Zhang', 'Liu', 'Chen', 'Yang', 'Zhao', 'Huang']
            },
            'Coréen': {
                'M': ['Min-jun', 'Seo-jun', 'Do-yoon', 'Si-woo', 'Joon-ho', 'Hyun-woo', 'Jin-woo', 'Sung-min'],
                'F': ['Seo-yeon', 'Min-seo', 'Ji-woo', 'Ha-eun', 'Soo-jin', 'Ye-jin', 'Su-bin', 'Na-eun']
            },
            'Croate': {
                'M': ['Marko', 'Ante', 'Josip', 'Ivan', 'Luka', 'Matej', 'Tomislav', 'Petar'],
                'F': ['Ana', 'Marija', 'Petra', 'Marijana', 'Ivana', 'Katarina', 'Nikolina', 'Sara']
            },
            'Danois': {
                'M': ['Lars', 'Niels', 'Jens', 'Peter', 'Henrik', 'Thomas', 'Christian', 'Martin'],
                'F': ['Anne', 'Kirsten', 'Mette', 'Hanne', 'Lene', 'Susanne', 'Camilla', 'Maria']
            },
            'Égyptien': {
                'M': ['Mohamed', 'Ahmed', 'Mahmoud', 'Omar', 'Ali', 'Hassan', 'Khaled', 'Amr'],
                'F': ['Fatima', 'Aisha', 'Maryam', 'Zeinab', 'Nour', 'Salma', 'Yasmin', 'Nadia']
            },
            'Espagnol': {
                'M': ['Antonio', 'José', 'Francisco', 'David', 'Juan', 'Javier', 'Daniel', 'Carlos'],
                'F': ['Carmen', 'María', 'Josefa', 'Isabel', 'Ana', 'Pilar', 'Mercedes', 'Dolores']
            },
            'Estonien': {
                'M': ['Jaan', 'Toomas', 'Andres', 'Mart', 'Ants', 'Peeter', 'Kalev', 'Rein'],
                'F': ['Kadri', 'Kristiina', 'Liis', 'Mari', 'Karin', 'Helen', 'Piret', 'Anne']
            },
            'Finlandais': {
                'M': ['Jukka', 'Mikael', 'Juha', 'Matti', 'Pekka', 'Antti', 'Jari', 'Heikki'],
                'F': ['Maria', 'Helena', 'Johanna', 'Anna', 'Kaarina', 'Kristiina', 'Margareta', 'Elisabeth']
            },
            'Français': {
                'M': ['Pierre', 'Jean', 'Michel', 'Alain', 'Philippe', 'Nicolas', 'Antoine', 'Julien'],
                'F': ['Marie', 'Nathalie', 'Isabelle', 'Sylvie', 'Catherine', 'Valérie', 'Christine', 'Sophie']
            },
            'Grec': {
                'M': ['Georgios', 'Ioannis', 'Konstantinos', 'Dimitrios', 'Nikolaos', 'Panagiotis', 'Vasileios', 'Christos'],
                'F': ['Maria', 'Eleni', 'Aikaterini', 'Vasiliki', 'Sofia', 'Angeliki', 'Georgia', 'Dimitra']
            },
            'Hongrois': {
                'M': ['László', 'József', 'János', 'Zoltán', 'Sándor', 'Gábor', 'Ferenc', 'Attila'],
                'F': ['Mária', 'Erzsébet', 'Katalin', 'Ilona', 'Éva', 'Anna', 'Zsuzsanna', 'Margit']
            },
            'Indien': {
                'M': ['Rahul', 'Amit', 'Raj', 'Vikash', 'Sunil', 'Ravi', 'Anil', 'Sanjay'],
                'F': ['Priya', 'Sunita', 'Pooja', 'Kavita', 'Neetu', 'Rekha', 'Geeta', 'Seema']
            },
            'Indonésien': {
                'M': ['Budi', 'Ahmad', 'Agus', 'Andi', 'Bambang', 'Dedi', 'Eko', 'Hadi'],
                'F': ['Sari', 'Sri', 'Indira', 'Dewi', 'Rina', 'Maya', 'Lestari', 'Wati']
            },
            'Iranien': {
                'M': ['Mohammad', 'Ali', 'Hassan', 'Hossein', 'Reza', 'Ahmad', 'Mehdi', 'Abbas'],
                'F': ['Fatima', 'Zahra', 'Maryam', 'Narges', 'Somayeh', 'Fatemeh', 'Leila', 'Nasrin']
            },
            'Irlandais': {
                'M': ['Sean', 'Patrick', 'Michael', 'John', 'David', 'Daniel', 'Paul', 'Mark'],
                'F': ['Mary', 'Margaret', 'Catherine', 'Bridget', 'Anne', 'Patricia', 'Helen', 'Elizabeth']
            },
            'Islandais': {
                'M': ['Jón', 'Sigurdur', 'Guðmundur', 'Gunnar', 'Ólafur', 'Einar', 'Kristján', 'Magnús'],
                'F': ['Guðrún', 'Anna', 'Kristín', 'Margrét', 'Sigríður', 'Helga', 'Ragnhildur', 'Jóhanna']
            },
            'Italien': {
                'M': ['Giuseppe', 'Antonio', 'Giovanni', 'Mario', 'Francesco', 'Luigi', 'Angelo', 'Vincenzo'],
                'F': ['Maria', 'Anna', 'Giuseppina', 'Rosa', 'Angela', 'Giovanna', 'Teresa', 'Lucia']
            },
            'Japonais': {
                'M': ['Hiroshi', 'Takeshi', 'Akira', 'Yuki', 'Daiki', 'Haruto', 'Sota', 'Ren'],
                'F': ['Sakura', 'Yuki', 'Ai', 'Rei', 'Mana', 'Yui', 'Hina', 'Emi']
            },
            'Marocain': {
                'M': ['Mohamed', 'Ahmed', 'Ali', 'Hassan', 'Omar', 'Youssef', 'Khalid', 'Abdelkader'],
                'F': ['Fatima', 'Aisha', 'Khadija', 'Zahra', 'Amina', 'Nadia', 'Malika', 'Samira']
            },
            'Mexicain': {
                'M': ['José', 'Juan', 'Antonio', 'Jesús', 'Miguel', 'Pedro', 'Alejandro', 'Manuel'],
                'F': ['María', 'Guadalupe', 'Juana', 'Margarita', 'Francisca', 'Rosa', 'Isabel', 'Teresa']
            },
            'Néerlandais': {
                'M': ['Johannes', 'Gerrit', 'Jan', 'Pieter', 'Cornelis', 'Hendrikus', 'Jacobus', 'Adrianus'],
                'F': ['Maria', 'Anna', 'Johanna', 'Cornelia', 'Elisabeth', 'Catharina', 'Geertruida', 'Margaretha']
            },
            'Nigérian': {
                'M': ['Chukwu', 'Emeka', 'Ikechukwu', 'Nnamdi', 'Obinna', 'Chijioke', 'Kelechi', 'Chidi'],
                'F': ['Ngozi', 'Chioma', 'Ifeoma', 'Adaeze', 'Chinwe', 'Nneka', 'Chiamaka', 'Uchechi']
            },
            'Norvégien': {
                'M': ['Ole', 'Lars', 'Nils', 'Erik', 'Hans', 'Knut', 'Magnus', 'Bjørn'],
                'F': ['Anna', 'Marie', 'Ingrid', 'Karen', 'Astrid', 'Solveig', 'Kari', 'Liv']
            },
            'Polonais': {
                'M': ['Jan', 'Andrzej', 'Krzysztof', 'Stanisław', 'Tomasz', 'Paweł', 'Józef', 'Marcin'],
                'F': ['Anna', 'Maria', 'Katarzyna', 'Małgorzata', 'Agnieszka', 'Barbara', 'Ewa', 'Elżbieta']
            },
            'Portugais': {
                'M': ['José', 'António', 'João', 'Manuel', 'Francisco', 'Carlos', 'Joaquim', 'Luís'],
                'F': ['Maria', 'Ana', 'Manuela', 'Helena', 'Fernanda', 'Isabel', 'Paula', 'Conceição']
            },
            'Roumain': {
                'M': ['Ion', 'Gheorghe', 'Nicolae', 'Vasile', 'Dumitru', 'Petre', 'Florin', 'Marian'],
                'F': ['Maria', 'Ana', 'Elena', 'Ioana', 'Mihaela', 'Cristina', 'Daniela', 'Andreea']
            },
            'Russe': {
                'M': ['Aleksandr', 'Sergei', 'Vladimir', 'Dmitri', 'Andrei', 'Alexei', 'Nikolai', 'Ivan'],
                'F': ['Elena', 'Olga', 'Irina', 'Tatyana', 'Svetlana', 'Natasha', 'Marina', 'Lyudmila']
            },
            'Suédois': {
                'M': ['Lars', 'Karl', 'Nils', 'Erik', 'Anders', 'Johan', 'Per', 'Olof'],
                'F': ['Anna', 'Maria', 'Margareta', 'Elisabeth', 'Eva', 'Birgitta', 'Kristina', 'Karin']
            },
            'Suisse': {
                'M': ['Hans', 'Peter', 'Franz', 'Johann', 'Jakob', 'Rudolf', 'Karl', 'Fritz'],
                'F': ['Maria', 'Anna', 'Elisabeth', 'Rosa', 'Emma', 'Bertha', 'Martha', 'Marie']
            },
            'Tchèque': {
                'M': ['Jan', 'Pavel', 'Petr', 'Tomáš', 'Jiří', 'Josef', 'Miroslav', 'Zdeněk'],
                'F': ['Marie', 'Jiřina', 'Anna', 'Věra', 'Alena', 'Lenka', 'Hana', 'Jaroslava']
            },
            'Thaïlandais': {
                'M': ['Somchai', 'Surasak', 'Sombat', 'Suwan', 'Prasert', 'Wichai', 'Pornchai', 'Thawatchai'],
                'F': ['Siriporn', 'Sunisa', 'Pranee', 'Suwanna', 'Malee', 'Pimchai', 'Wanna', 'Sirikul']
            },
            'Turc': {
                'M': ['Mehmet', 'Mustafa', 'Ahmed', 'Ali', 'Hasan', 'İbrahim', 'Osman', 'Süleyman'],
                'F': ['Fatma', 'Ayşe', 'Emine', 'Hatice', 'Zeynep', 'Elif', 'Meryem', 'Özlem']
            },
            'Américain': {
                'M': ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Christopher', 'Matthew'],
                'F': ['Mary', 'Jennifer', 'Linda', 'Patricia', 'Susan', 'Jessica', 'Sarah', 'Karen']
            }
        }
        
        last_names = {
            'Afghan': ['Ahmad', 'Khan', 'Shah', 'Ali', 'Rahman', 'Hassan', 'Hussain', 'Mahmud', 'Omar', 'Yusuf'],
            'Allemand': ['Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann'],
            'Argentin': ['González', 'Rodríguez', 'Gómez', 'Fernández', 'López', 'Díaz', 'Martínez', 'Pérez', 'García', 'Sánchez'],
            'Australien': ['Smith', 'Jones', 'Williams', 'Brown', 'Wilson', 'Taylor', 'Johnson', 'White', 'Martin', 'Anderson'],
            'Autrichien': ['Gruber', 'Huber', 'Bauer', 'Wagner', 'Müller', 'Pichler', 'Steiner', 'Moser', 'Mayer', 'Hofer'],
            'Belge': ['Peeters', 'Janssens', 'Maes', 'Jacobs', 'Mertens', 'Willems', 'Claes', 'Goossens', 'Wouters', 'De Smet'],
            'Brésilien': ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira', 'Lima', 'Gomes'],
            'Britannique': ['Smith', 'Jones', 'Taylor', 'Williams', 'Brown', 'Davies', 'Evans', 'Wilson', 'Thomas', 'Roberts'],
            'Bulgare': ['Ivanov', 'Petrov', 'Dimitrov', 'Georgiev', 'Nikolov', 'Todorov', 'Hristov', 'Stoyanov', 'Marinov', 'Angelov'],
            'Canadien': ['Smith', 'Brown', 'Tremblay', 'Martin', 'Roy', 'Wilson', 'MacDonald', 'Johnson', 'Thompson', 'Anderson'],
            'Chinois': ['Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Zhao', 'Huang', 'Zhou', 'Wu', 'Xu', 'Sun'],
            'Coréen': ['Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Jang', 'Lim', 'Han', 'Oh'],
            'Croate': ['Horvat', 'Novak', 'Marić', 'Petrović', 'Jurić', 'Babić', 'Matić', 'Pavić', 'Tomić', 'Kovač'],
            'Danois': ['Nielsen', 'Jensen', 'Hansen', 'Pedersen', 'Andersen', 'Christensen', 'Larsen', 'Sørensen', 'Rasmussen', 'Jørgensen'],
            'Égyptien': ['Mohamed', 'Ahmed', 'Mahmoud', 'Hassan', 'Ali', 'Ibrahim', 'Abdel Rahman', 'Omar', 'Khalil', 'Said'],
            'Espagnol': ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Gómez', 'Martín'],
            'Estonien': ['Tamm', 'Saar', 'Sepp', 'Mägi', 'Kask', 'Kukk', 'Rebane', 'Ilves', 'Pärn', 'Känd'],
            'Finlandais': ['Korhonen', 'Virtanen', 'Mäkinen', 'Nieminen', 'Mäkelä', 'Hämäläinen', 'Laine', 'Heikkinen', 'Koskinen', 'Järvinen'],
            'Français': ['Martin', 'Bernard', 'Thomas', 'Petit', 'Robert', 'Richard', 'Durand', 'Dubois', 'Moreau', 'Laurent', 'Simon', 'Michel'],
            'Grec': ['Papadopoulos', 'Georgiou', 'Dimitriou', 'Nikolaou', 'Ioannou', 'Petrou', 'Andreou', 'Christou', 'Antoniou', 'Stavrou'],
            'Hongrois': ['Nagy', 'Kovács', 'Tóth', 'Szabó', 'Horváth', 'Varga', 'Kiss', 'Molnár', 'Németh', 'Farkas'],
            'Indien': ['Sharma', 'Verma', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Mishra', 'Jain', 'Patel', 'Yadav'],
            'Indonésien': ['Sari', 'Dewi', 'Lestari', 'Wati', 'Indira', 'Putri', 'Anggraini', 'Fitria', 'Ningsih', 'Maharani'],
            'Iranien': ['Hosseini', 'Ahmadi', 'Mohammadi', 'Rezaei', 'Moradi', 'Mousavi', 'Karimi', 'Rahimi', 'Bagheri', 'Hashemi'],
            'Irlandais': ["O'Brien", "O'Sullivan", 'Murphy', "O'Connor", 'Kelly', 'Ryan', "O'Neill", 'Walsh', 'McCarthy', 'Gallagher'],
            'Islandais': ['Jónsson', 'Sigurdsson', 'Guðmundsson', 'Einarsson', 'Gunnarsson', 'Ólafsson', 'Kristjánsson', 'Magnússon', 'Stefánsson', 'Þórsson'],
            'Italien': ['Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco'],
            'Japonais': ['Sato', 'Suzuki', 'Takahashi', 'Tanaka', 'Watanabe', 'Ito', 'Yamamoto', 'Nakamura', 'Kobayashi', 'Kato', 'Yoshida', 'Yamada'],
            'Marocain': ['Alami', 'Bennani', 'El Idrissi', 'Fassi', 'Tazi', 'Benali', 'Berrada', 'Chakir', 'Lamrani', 'Oudghiri'],
            'Mexicain': ['González', 'García', 'Martínez', 'López', 'Hernández', 'Pérez', 'Rodríguez', 'Sánchez', 'Ramírez', 'Cruz'],
            'Néerlandais': ['De Jong', 'Jansen', 'De Vries', 'Van den Berg', 'Van Dijk', 'Bakker', 'Janssen', 'Visser', 'Smit', 'Meijer'],
            'Nigérian': ['Adebayo', 'Okafor', 'Okoro', 'Eze', 'Nwankwo', 'Okonkwo', 'Ogbonna', 'Chukwu', 'Emeka', 'Ikechukwu'],
            'Norvégien': ['Hansen', 'Johansen', 'Olsen', 'Larsen', 'Andersen', 'Pedersen', 'Nilsen', 'Kristiansen', 'Jensen', 'Karlsen'],
            'Polonais': ['Nowak', 'Kowalski', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński', 'Szymański', 'Woźniak'],
            'Portugais': ['Silva', 'Santos', 'Ferreira', 'Pereira', 'Oliveira', 'Costa', 'Rodrigues', 'Martins', 'Jesus', 'Sousa'],
            'Roumain': ['Popescu', 'Ionescu', 'Popa', 'Stoica', 'Stan', 'Dumitrescu', 'Gheorghe', 'Constantinescu', 'Marin', 'Diaconu'],
            'Russe': ['Ivanov', 'Smirnov', 'Kuznetsov', 'Popov', 'Sokolov', 'Lebedev', 'Kozlov', 'Novikov', 'Morozov', 'Petrov'],
            'Suédois': ['Andersson', 'Johansson', 'Karlsson', 'Nilsson', 'Eriksson', 'Larsson', 'Olsson', 'Persson', 'Svensson', 'Gustafsson'],
            'Suisse': ['Müller', 'Meier', 'Schmid', 'Keller', 'Weber', 'Huber', 'Schneider', 'Meyer', 'Steiner', 'Fischer'],
            'Tchèque': ['Novák', 'Svoboda', 'Novotný', 'Dvořák', 'Černý', 'Procházka', 'Krejčí', 'Hájek', 'Kratochvíl', 'Horák'],
            'Thaïlandais': ['Chanthavy', 'Siriporn', 'Somboon', 'Chanpen', 'Kamon', 'Narongsak', 'Prasert', 'Suwan', 'Thawatchai', 'Wichai'],
            'Turc': ['Yılmaz', 'Kaya', 'Demir', 'Şahin', 'Çelik', 'Yıldız', 'Yıldırım', 'Öztürk', 'Aydin', 'Özkan'],
            'Américain': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez']
        }
        
        nationality_first_names = first_names.get(nationality, first_names['Français'])
        nationality_last_names = last_names.get(nationality, last_names['Français'])
        
        gender_first_names = nationality_first_names[gender]
        first_name = random.choice(gender_first_names)
        last_name = random.choice(nationality_last_names)
        
        return f"{first_name} {last_name}"
    
    @classmethod
    def _generate_unique_name(cls, nationality: str, gender: str, used_names: set) -> str:
        """Génère un nom unique qui n'a pas encore été utilisé dans la partie"""
        max_attempts = 50  # Éviter les boucles infinies si toutes les combinaisons sont épuisées
        
        for attempt in range(max_attempts):
            name = cls._generate_random_name(nationality, gender)
            if name not in used_names:
                used_names.add(name)
                return name
        
        # Si on n'arrive pas à trouver un nom unique après max_attempts,
        # on ajoute un suffixe numérique
        base_name = cls._generate_random_name(nationality, gender)
        counter = 1
        while f"{base_name} {counter}" in used_names:
            counter += 1
        
        final_name = f"{base_name} {counter}"
        used_names.add(final_name)
        return final_name
    
    @classmethod
    def generate_multiple_players(cls, count: int) -> List[Player]:
        """Génère plusieurs joueurs en évitant les noms en double"""
        players = []
        used_names = set()
        
        for i in range(1, count + 1):
            # Sélection du rôle selon les probabilités
            rand = random.random()
            cumulative_probability = 0
            selected_role = PlayerRole.NORMAL
            
            for role, probability in cls.ROLE_PROBABILITIES.items():
                cumulative_probability += probability
                if rand <= cumulative_probability:
                    selected_role = role
                    break
            
            nationality_key = random.choice(list(cls.NATIONALITIES.keys()))
            gender = random.choice(['M', 'F'])
            nationality_display = cls.NATIONALITIES[nationality_key][gender]
            
            # Génération des stats selon le rôle
            stats = cls._generate_stats_by_role(selected_role)
            
            player = Player(
                number=str(i).zfill(3),
                name=cls._generate_unique_name(nationality_key, gender, used_names),
                nationality=nationality_display,
                gender=gender,
                role=selected_role,
                stats=stats,
                portrait=cls._generate_portrait(nationality_key, gender),
                uniform=cls._generate_uniform(),
                alive=True,
                health=100,
                total_score=stats.intelligence + stats.force + stats.agilité
            )
            
            players.append(player)
        
        return players
    
    @classmethod
    def _generate_portrait(cls, nationality: str, gender: str = 'M') -> PlayerPortrait:
        """Génère un portrait cohérent avec la nationalité et sélectionne les calques PNG"""
        skin_color_ranges = {
            # Asie de l'Est
            'Chinois': (2, 10),
            'Coréen': (0, 8),
            'Japonais': (0, 8),
            
            # Europe du Nord
            'Britannique': (0, 5),
            'Danois': (0, 4),
            'Finlandais': (0, 4),
            'Irlandais': (0, 5),
            'Islandais': (0, 3),
            'Norvégien': (0, 4),
            'Suédois': (0, 4),
            
            # Europe de l'Ouest
            'Allemand': (0, 5),
            'Autrichien': (0, 5),
            'Belge': (0, 5),
            'Français': (0, 5),
            'Néerlandais': (0, 5),
            'Suisse': (0, 5),
            
            # Europe du Sud
            'Espagnol': (2, 8),
            'Grec': (3, 9),
            'Italien': (2, 8),
            'Portugais': (2, 8),
            
            # Europe de l'Est
            'Bulgare': (1, 7),
            'Croate': (1, 7),
            'Estonien': (0, 4),
            'Hongrois': (1, 7),
            'Polonais': (0, 6),
            'Roumain': (1, 7),
            'Russe': (0, 6),
            'Tchèque': (0, 6),
            
            # Moyen-Orient
            'Afghan': (6, 16),
            'Iranien': (5, 15),
            'Turc': (4, 12),
            
            # Afrique du Nord
            'Égyptien': (8, 18),
            'Marocain': (6, 16),
            
            # Afrique sub-saharienne
            'Nigérian': (15, 24),
            
            # Asie du Sud et du Sud-Est
            'Indien': (8, 18),
            'Indonésien': (6, 16),
            'Thaïlandais': (4, 14),
            
            # Amériques
            'Américain': (0, 15),
            'Argentin': (2, 10),
            'Australien': (0, 8),
            'Brésilien': (4, 20),
            'Canadien': (0, 12),
            'Mexicain': (6, 16),
        }
        
        skin_range = skin_color_ranges.get(nationality, (0, 15))
        skin_color_index = random.randint(skin_range[0], min(skin_range[1], len(cls.SKIN_COLORS) - 1))
        
        # Sélectionner des calques PNG cohérents avec la nationalité
        portrait_layers = portrait_service.select_random_portrait_layers(
            nationality=nationality,
            gender=gender
        )
        
        return PlayerPortrait(
            face_shape=random.choice(cls.FACE_SHAPES),
            skin_color=cls.SKIN_COLORS[skin_color_index],
            hairstyle=random.choice(cls.HAIRSTYLES),
            hair_color=random.choice(cls.HAIR_COLORS),
            eye_color=random.choice(['#8B4513', '#654321', '#2F4F2F', '#483D8B', '#556B2F', '#000000']),
            eye_shape=random.choice(['Amande', 'Rond', 'Allongé', 'Tombant', 'Relevé', 'Petit', 'Grand']),
            # Ajout des calques PNG
            layer_base=portrait_layers.get('base'),
            layer_eyes=portrait_layers.get('eyes'),
            layer_hair=portrait_layers.get('hair'),
            layer_mouth=portrait_layers.get('mouth'),
            layer_nose=portrait_layers.get('nose')
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
    def simulate_event(cls, players: List[Player], event: GameEvent, groups: Dict[str, Any] = None) -> EventResult:
        """Simule une épreuve et retourne les résultats avec animations de mort - VERSION CORRIGÉE avec support des groupes"""
        alive_players = [p for p in players if p.alive]
        survivors = []
        eliminated = []
        
        if not alive_players:
            return EventResult(
                event_id=event.id,
                event_name=event.name,
                survivors=[],
                eliminated=[],
                total_participants=0
            )
        
        # Traiter les groupes si fournis
        groups_dict = groups or {}
        
        # Logique spéciale pour les épreuves finales
        if event.is_final:
            # Les finales garantissent un seul survivant
            target_survivors = 1
        else:
            # Calculer le nombre exact de survivants selon le taux d'élimination configuré
            target_survivors = int(len(alive_players) * (1 - event.elimination_rate))
            # S'assurer qu'il y a au moins 1 survivant
            target_survivors = max(1, target_survivors)
        
        # Calculer un score de survie pour chaque joueur (stats + rôle + aléatoire + bonus groupe)
        player_scores = []
        for player in alive_players:
            # Bonus de stats selon le type d'épreuve
            stat_bonus = cls._get_stat_bonus_for_event(player, event)
            
            # Bonus de rôle
            role_bonus = cls._get_role_bonus_for_event(player, event)
            
            # Bonus de groupe (coopération)
            group_bonus = 0
            if player.group_id and player.group_id in groups_dict:
                # Compter les alliés vivants dans le groupe
                allies_alive = sum(1 for p in alive_players if p.group_id == player.group_id and p.id != player.id)
                group_bonus = allies_alive * 0.5  # Bonus de coopération
            
            # Malus de difficulté
            difficulty_malus = (event.difficulty - 5) * 0.5
            
            # Score de base + bonus - malus + facteur aléatoire RENFORCÉ (augmenté de 0-15 à 0-25)
            survival_score = stat_bonus + (role_bonus * 10) + group_bonus - difficulty_malus + random.uniform(0, 25)
            
            player_scores.append((player, survival_score))
        
        # Trier par score de survie (les meilleurs en premier)
        player_scores.sort(key=lambda x: x[1], reverse=True)
        
        # AMÉLIORATION MAJEURE: Mélange aléatoire plus agressif des joueurs ayant des scores similaires
        # Augmentation de l'écart de 2 à 4 points pour plus de mélange
        final_scores = []
        i = 0
        while i < len(player_scores):
            # Grouper les joueurs avec des scores similaires (écart augmenté à 4 points)
            similar_group = [player_scores[i]]
            j = i + 1
            while j < len(player_scores) and abs(player_scores[j][1] - player_scores[i][1]) < 4.0:
                similar_group.append(player_scores[j])
                j += 1
            
            # Mélanger aléatoirement ce groupe PLUSIEURS FOIS pour plus de randomness
            for _ in range(3):  # Triple mélange pour plus d'aléatoire
                random.shuffle(similar_group)
            
            final_scores.extend(similar_group)
            i = j
        
        player_scores = final_scores
        
        # NOUVEAU: Mélange final supplémentaire pour briser les patterns restants
        # Diviser en chunks et mélanger chaque chunk
        chunk_size = max(5, len(player_scores) // 10)  # Chunks de 5 minimum ou 10% des joueurs
        final_mixed_scores = []
        
        for chunk_start in range(0, len(player_scores), chunk_size):
            chunk_end = min(chunk_start + chunk_size, len(player_scores))
            chunk = player_scores[chunk_start:chunk_end]
            random.shuffle(chunk)
            final_mixed_scores.extend(chunk)
        
        player_scores = final_mixed_scores
        
        # Sélectionner exactement target_survivors survivants (les meilleurs)
        survivors_selected = player_scores[:target_survivors]
        eliminated_selected = player_scores[target_survivors:]
        
        # Traiter les survivants - CORRECTION: initialiser event_kills à 0, sera calculé plus tard
        for player, score in survivors_selected:
            time_remaining = random.randint(event.survival_time_min // 4, event.survival_time_max // 2)
            
            # Gérer les trahisons selon les groupes
            betrayed = False
            if player.group_id and player.group_id in groups_dict:
                # Trahison possible uniquement si autorisée dans le groupe
                group = groups_dict[player.group_id]
                if hasattr(group, 'allow_betrayals') and group.allow_betrayals:
                    betrayed = random.random() < 0.1
            else:
                # Pas de groupe = pas de trahison possible
                betrayed = False
            
            player.survived_events += 1
            # NOTE: player.kills sera mis à jour plus tard après attribution des éliminations
            if betrayed:
                player.betrayals += 1
            
            # Score temporaire (sera mis à jour après calcul des kills réels)
            temp_score = time_remaining - (5 if betrayed else 0)
            
            survivors.append({
                "player": player,
                "number": player.number,
                "name": player.name,
                "time_remaining": time_remaining,
                "event_kills": 0,  # Sera mis à jour plus tard
                "betrayed": betrayed,
                "score": temp_score,  # Score temporaire
                "kills": player.kills,  # Kills actuels (sera mis à jour)
                "total_score": player.total_score,  # Sera mis à jour
                "survived_events": player.survived_events
            })
        
        # Traiter les éliminés
        for player, score in eliminated_selected:
            player.alive = False
            death_animation = EventsService.get_random_death_animation(event)
            
            eliminated.append({
                "player": player,
                "number": player.number,
                "name": player.name,
                "elimination_time": random.randint(10, event.survival_time_max // 2),
                "cause": death_animation,
                "decor": event.decor,
                "event_name": event.name
            })
        
        # CORRECTION MAJEURE: Attribution cohérente des kills basée sur les éliminations réelles
        if eliminated and survivors:
            # Calculer le nombre maximum de kills possibles par survivant selon le type d'épreuve
            # CORRECTION: Limite plus stricte - maximum 2 kills par événement pour épreuves de force, 1 pour les autres
            max_kills_per_event = 2 if event.type == EventType.FORCE else 1
            total_eliminated = len(eliminated)
            total_survivors = len(survivors)
            
            # Distribuer les éliminations de manière équitable et réaliste
            eliminated_copy = eliminated.copy()
            random.shuffle(eliminated_copy)
            
            # Tracker des kills par survivant pour CET événement seulement
            event_kills_tracker = {s["player"].id: 0 for s in survivors}
            
            # Distribuer chaque élimination à un survivant
            for i, eliminated_player_data in enumerate(eliminated_copy):
                eliminated_player = eliminated_player_data["player"]
                
                # Chercher des survivants disponibles (qui n'ont pas atteint leur limite pour CET événement)
                available_killers = [s for s in survivors if event_kills_tracker[s["player"].id] < max_kills_per_event]
                
                # Filtrer pour éviter les kills entre membres du même groupe (sauf si épreuve 1v1)
                if len(alive_players) > 4:  # Pas une épreuve finale
                    available_killers = [
                        s for s in available_killers 
                        if not (s["player"].group_id and 
                               s["player"].group_id == eliminated_player.group_id and 
                               s["player"].group_id in groups_dict)
                    ]
                
                if available_killers:
                    # Sélectionner un tueur aléatoire parmi les disponibles
                    killer_data = random.choice(available_killers)
                    killer = killer_data["player"]
                    
                    # Attribuer le kill
                    killer.killed_players.append(eliminated_player.id)
                    event_kills_tracker[killer.id] += 1
                else:
                    # Si aucun tueur disponible avec les limites strictes, 
                    # choisir parmi tous les survivants mais limiter à 1 kill supplémentaire
                    if survivors:
                        # Prioriser les survivants avec le moins de kills pour cet événement
                        sorted_survivors = sorted(survivors, key=lambda s: event_kills_tracker[s["player"].id])
                        killer_data = sorted_survivors[0]
                        killer = killer_data["player"]
                        
                        # Ne pas dépasser 2 kills même dans les cas extrêmes
                        if event_kills_tracker[killer.id] < 2:
                            killer.killed_players.append(eliminated_player.id)
                            event_kills_tracker[killer.id] += 1
                        # Si tous les survivants ont déjà 2 kills, l'élimination reste sans tueur spécifique
            
            # Mettre à jour les stats des survivants avec les kills réels
            for survivor_data in survivors:
                player = survivor_data["player"]
                actual_kills = event_kills_tracker[player.id]
                
                # Mettre à jour le compteur de kills du joueur
                player.kills += actual_kills
                
                # Mettre à jour les données du survivant
                survivor_data["event_kills"] = actual_kills
                survivor_data["kills"] = player.kills
                
                # Recalculer le score avec les kills réels
                event_score = survivor_data["time_remaining"] + (actual_kills * 10) - (5 if survivor_data["betrayed"] else 0)
                player.total_score += event_score
                survivor_data["score"] = event_score
                survivor_data["total_score"] = player.total_score
        
        # Trier les survivants par score d'événement
        survivors.sort(key=lambda x: x["score"], reverse=True)
        
        return EventResult(
            event_id=event.id,
            event_name=event.name,
            survivors=survivors,
            eliminated=eliminated,
            total_participants=len(alive_players)
        )
    
    @classmethod
    def _get_stat_bonus_for_event(cls, player: Player, event: GameEvent) -> int:
        """Retourne le bonus de stat pour une épreuve"""
        if event.type == EventType.INTELLIGENCE:
            return player.stats.intelligence
        elif event.type == EventType.FORCE:
            return player.stats.force
        elif event.type == EventType.AGILITÉ:
            return player.stats.agilité
        else:
            return (player.stats.intelligence + player.stats.force + player.stats.agilité) // 3
    
    @classmethod
    def _get_role_bonus_for_event(cls, player: Player, event: GameEvent) -> float:
        """Retourne le bonus de rôle pour une épreuve"""
        if player.role == PlayerRole.INTELLIGENT and event.type == EventType.INTELLIGENCE:
            return 0.2
        elif player.role == PlayerRole.BRUTE and event.type == EventType.FORCE:
            return 0.2
        elif player.role == PlayerRole.SPORTIF and event.type == EventType.AGILITÉ:
            return 0.2
        elif player.role == PlayerRole.ZERO:
            return 0.15  # Bonus universel
        elif player.role == PlayerRole.PEUREUX:
            return -0.1
        else:
            return 0.05 if event.type in [EventType.INTELLIGENCE, EventType.FORCE, EventType.AGILITÉ] else 0
    
    @classmethod
    def generate_celebrities(cls, count: int = 1000) -> List[Celebrity]:
        """Génère une liste de célébrités fictives"""
        celebrities = []
        categories = [
            ("Ancien vainqueur", 5, 35000000, 60000000),      # 35-60 millions pour 5 étoiles
            ("Sportif", 4, 15000000, 35000000),               # 15-35 millions pour 4 étoiles
            ("Scientifique", 4, 15000000, 35000000),          # 15-35 millions pour 4 étoiles
            ("Acteur", 3, 5000000, 15000000),                 # 5-15 millions pour 3 étoiles
            ("Chanteuse", 3, 5000000, 15000000),              # 5-15 millions pour 3 étoiles
            ("Influenceur", 2, 2000000, 5000000),             # 2-5 millions pour 2 étoiles
            ("Chef", 2, 2000000, 5000000),                    # 2-5 millions pour 2 étoiles
            ("Politicien", 3, 5000000, 15000000),             # 5-15 millions pour 3 étoiles
            ("Écrivain", 2, 2000000, 5000000),                # 2-5 millions pour 2 étoiles
            ("Artiste", 3, 5000000, 15000000)                 # 5-15 millions pour 3 étoiles
        ]
        
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn', 
                      'Sage', 'River', 'Phoenix', 'Skyler', 'Rowan', 'Kai', 'Nova', 'Zara',
                      'Luna', 'Atlas', 'Iris', 'Orion', 'Maya', 'Leo', 'Aria', 'Max', 'Zoe']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                     'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 
                     'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
        
        for i in range(count):
            category, stars, min_price, max_price = random.choice(categories)
            # Generate price and round to nearest hundred thousand
            raw_price = random.randint(min_price, max_price)
            price = round(raw_price / 100000) * 100000
            
            # Générer des stats selon la catégorie
            if category == "Ancien vainqueur":
                stats = PlayerStats(
                    intelligence=random.randint(7, 10),
                    force=random.randint(6, 9),
                    agilité=random.randint(7, 10)
                )
                wins = random.randint(1, 3)
            elif category == "Sportif":
                stats = PlayerStats(
                    intelligence=random.randint(4, 7),
                    force=random.randint(8, 10),
                    agilité=random.randint(8, 10)
                )
                wins = 0
            elif category == "Scientifique":
                stats = PlayerStats(
                    intelligence=random.randint(9, 10),
                    force=random.randint(2, 5),
                    agilité=random.randint(3, 6)
                )
                wins = 0
            else:
                stats = PlayerStats(
                    intelligence=random.randint(4, 8),
                    force=random.randint(3, 7),
                    agilité=random.randint(4, 8)
                )
                wins = 0
            
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            nationality_key = random.choice(list(cls.NATIONALITIES.keys()))
            gender = random.choice(['M', 'F'])
            nationality_display = cls.NATIONALITIES[nationality_key][gender]
            
            biography = cls._generate_biography(category, name)
            
            celebrities.append(Celebrity(
                name=name,
                category=category,
                stars=stars,
                price=price,
                nationality=nationality_display,
                wins=wins,
                stats=stats,
                biography=biography
            ))
        
        return celebrities
    
    @classmethod
    def generate_single_celebrity(cls, category: str = None, stars: int = None) -> Celebrity:
        """Génère une seule célébrité avec une catégorie et des étoiles spécifiques"""
        categories = [
            ("Ancien vainqueur", 5, 35000000, 60000000),      # 35-60 millions pour 5 étoiles
            ("Sportif", 4, 15000000, 35000000),               # 15-35 millions pour 4 étoiles
            ("Scientifique", 4, 15000000, 35000000),          # 15-35 millions pour 4 étoiles
            ("Acteur", 3, 5000000, 15000000),                 # 5-15 millions pour 3 étoiles
            ("Chanteuse", 3, 5000000, 15000000),              # 5-15 millions pour 3 étoiles
            ("Influenceur", 2, 2000000, 5000000),             # 2-5 millions pour 2 étoiles
            ("Chef", 2, 2000000, 5000000),                    # 2-5 millions pour 2 étoiles
            ("Politicien", 3, 5000000, 15000000),             # 5-15 millions pour 3 étoiles
            ("Écrivain", 2, 2000000, 5000000),                # 2-5 millions pour 2 étoiles
            ("Artiste", 3, 5000000, 15000000)                 # 5-15 millions pour 3 étoiles
        ]
        
        # Si catégorie et étoiles spécifiées, utiliser ces valeurs
        if category and stars:
            matching_categories = [c for c in categories if c[0] == category and c[1] == stars]
            if matching_categories:
                selected_category, selected_stars, min_price, max_price = matching_categories[0]
            else:
                # Fallback : chercher juste par catégorie
                matching_categories = [c for c in categories if c[0] == category]
                if matching_categories:
                    selected_category, selected_stars, min_price, max_price = matching_categories[0]
                else:
                    # Fallback final : utiliser une catégorie aléatoire
                    selected_category, selected_stars, min_price, max_price = random.choice(categories)
        else:
            # Générer aléatoirement
            selected_category, selected_stars, min_price, max_price = random.choice(categories)
        
        # Generate price and round to nearest hundred thousand
        raw_price = random.randint(min_price, max_price)
        price = round(raw_price / 100000) * 100000
        
        # Générer des stats selon la catégorie
        if selected_category == "Ancien vainqueur":
            stats = PlayerStats(
                intelligence=random.randint(7, 10),
                force=random.randint(6, 9),
                agilité=random.randint(7, 10)
            )
            wins = random.randint(1, 3)
        elif selected_category == "Sportif":
            stats = PlayerStats(
                intelligence=random.randint(4, 7),
                force=random.randint(8, 10),
                agilité=random.randint(8, 10)
            )
            wins = 0
        elif selected_category == "Scientifique":
            stats = PlayerStats(
                intelligence=random.randint(9, 10),
                force=random.randint(2, 5),
                agilité=random.randint(3, 6)
            )
            wins = 0
        else:
            stats = PlayerStats(
                intelligence=random.randint(4, 8),
                force=random.randint(3, 7),
                agilité=random.randint(4, 8)
            )
            wins = 0
        
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn', 
                      'Sage', 'River', 'Phoenix', 'Skyler', 'Rowan', 'Kai', 'Nova', 'Zara',
                      'Luna', 'Atlas', 'Iris', 'Orion', 'Maya', 'Leo', 'Aria', 'Max', 'Zoe']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                     'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 
                     'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        nationality_key = random.choice(list(cls.NATIONALITIES.keys()))
        gender = random.choice(['M', 'F'])
        nationality_display = cls.NATIONALITIES[nationality_key][gender]
        
        biography = cls._generate_biography(selected_category, name)
        
        return Celebrity(
            name=name,
            category=selected_category,
            stars=selected_stars,
            price=price,
            nationality=nationality_display,
            wins=wins,
            stats=stats,
            biography=biography
        )
    
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
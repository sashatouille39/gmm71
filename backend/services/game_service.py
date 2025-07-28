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
        "Afghane", "Allemande", "Argentine", "Australienne", "Autrichienne", "Belge", 
        "Brésilienne", "Britannique", "Bulgare", "Canadienne", "Chinoise", "Coréenne", 
        "Croate", "Danoise", "Égyptienne", "Espagnole", "Estonienne", "Finlandaise", 
        "Française", "Grecque", "Hongroise", "Indienne", "Indonésienne", "Iranienne", 
        "Irlandaise", "Islandaise", "Israélienne", "Italienne", "Japonaise", "Kazakhe", 
        "Lettone", "Lituanienne", "Luxembourgeoise", "Marocaine", "Mexicaine", "Néerlandaise", 
        "Nigériane", "Norvégienne", "Polonaise", "Portugaise", "Roumaine", "Russe", 
        "Suédoise", "Suisse", "Tchèque", "Thaïlandaise", "Turque", "Ukrainienne", "Américaine"
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
        """Génère un nom complet aléatoire selon la nationalité et le genre"""
        first_names = {
            'Afghane': {
                'M': ['Ahmad', 'Mohammed', 'Abdul', 'Hassan', 'Omar', 'Ali', 'Mahmud', 'Rashid'],
                'F': ['Fatima', 'Aisha', 'Zara', 'Maryam', 'Layla', 'Nadia', 'Soraya', 'Jamila']
            },
            'Allemande': {
                'M': ['Hans', 'Klaus', 'Jürgen', 'Wolfgang', 'Dieter', 'Günter', 'Helmut', 'Manfred'],
                'F': ['Ursula', 'Ingrid', 'Gisela', 'Christa', 'Helga', 'Monika', 'Renate', 'Brigitte']
            },
            'Argentine': {
                'M': ['Carlos', 'Juan', 'José', 'Luis', 'Miguel', 'Jorge', 'Roberto', 'Diego'],
                'F': ['María', 'Ana', 'Carmen', 'Rosa', 'Isabel', 'Teresa', 'Cristina', 'Patricia']
            },
            'Australienne': {
                'M': ['Jack', 'William', 'James', 'Benjamin', 'Luke', 'Henry', 'Alexander', 'Mason'],
                'F': ['Charlotte', 'Ruby', 'Lily', 'Sophie', 'Emily', 'Chloe', 'Mia', 'Grace']
            },
            'Autrichienne': {
                'M': ['Johann', 'Franz', 'Karl', 'Josef', 'Georg', 'Anton', 'Heinrich', 'Paul'],
                'F': ['Maria', 'Anna', 'Elisabeth', 'Theresia', 'Johanna', 'Franziska', 'Katharina', 'Barbara']
            },
            'Belge': {
                'M': ['Jean', 'Pierre', 'Marc', 'Philippe', 'Michel', 'Paul', 'Luc', 'André'],
                'F': ['Marie', 'Anne', 'Catherine', 'Martine', 'Françoise', 'Monique', 'Christine', 'Isabelle']
            },
            'Brésilienne': {
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
            'Canadienne': {
                'M': ['Liam', 'Noah', 'William', 'James', 'Logan', 'Benjamin', 'Mason', 'Ethan'],
                'F': ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Charlotte', 'Mia', 'Amelia']
            },
            'Chinoise': {
                'M': ['Wei', 'Jun', 'Ming', 'Hao', 'Lei', 'Qiang', 'Yang', 'Bin'],
                'F': ['Li', 'Wang', 'Zhang', 'Liu', 'Chen', 'Yang', 'Zhao', 'Huang']
            },
            'Coréenne': {
                'M': ['Min-jun', 'Seo-jun', 'Do-yoon', 'Si-woo', 'Joon-ho', 'Hyun-woo', 'Jin-woo', 'Sung-min'],
                'F': ['Seo-yeon', 'Min-seo', 'Ji-woo', 'Ha-eun', 'Soo-jin', 'Ye-jin', 'Su-bin', 'Na-eun']
            },
            'Croate': {
                'M': ['Marko', 'Ante', 'Josip', 'Ivan', 'Luka', 'Matej', 'Tomislav', 'Petar'],
                'F': ['Ana', 'Marija', 'Petra', 'Marijana', 'Ivana', 'Katarina', 'Nikolina', 'Sara']
            },
            'Danoise': {
                'M': ['Lars', 'Niels', 'Jens', 'Peter', 'Henrik', 'Thomas', 'Christian', 'Martin'],
                'F': ['Anne', 'Kirsten', 'Mette', 'Hanne', 'Lene', 'Susanne', 'Camilla', 'Maria']
            },
            'Égyptienne': {
                'M': ['Mohamed', 'Ahmed', 'Mahmoud', 'Omar', 'Ali', 'Hassan', 'Khaled', 'Amr'],
                'F': ['Fatima', 'Aisha', 'Maryam', 'Zeinab', 'Nour', 'Salma', 'Yasmin', 'Nadia']
            },
            'Espagnole': {
                'M': ['Antonio', 'José', 'Francisco', 'David', 'Juan', 'Javier', 'Daniel', 'Carlos'],
                'F': ['Carmen', 'María', 'Josefa', 'Isabel', 'Ana', 'Pilar', 'Mercedes', 'Dolores']
            },
            'Estonienne': {
                'M': ['Jaan', 'Toomas', 'Andres', 'Mart', 'Ants', 'Peeter', 'Kalev', 'Rein'],
                'F': ['Kadri', 'Kristiina', 'Liis', 'Mari', 'Karin', 'Helen', 'Piret', 'Anne']
            },
            'Finlandaise': {
                'M': ['Jukka', 'Mikael', 'Juha', 'Matti', 'Pekka', 'Antti', 'Jari', 'Heikki'],
                'F': ['Maria', 'Helena', 'Johanna', 'Anna', 'Kaarina', 'Kristiina', 'Margareta', 'Elisabeth']
            },
            'Française': {
                'M': ['Pierre', 'Jean', 'Michel', 'Alain', 'Philippe', 'Nicolas', 'Antoine', 'Julien'],
                'F': ['Marie', 'Nathalie', 'Isabelle', 'Sylvie', 'Catherine', 'Valérie', 'Christine', 'Sophie']
            },
            'Grecque': {
                'M': ['Georgios', 'Ioannis', 'Konstantinos', 'Dimitrios', 'Nikolaos', 'Panagiotis', 'Vasileios', 'Christos'],
                'F': ['Maria', 'Eleni', 'Aikaterini', 'Vasiliki', 'Sofia', 'Angeliki', 'Georgia', 'Dimitra']
            },
            'Hongroise': {
                'M': ['László', 'József', 'János', 'Zoltán', 'Sándor', 'Gábor', 'Ferenc', 'Attila'],
                'F': ['Mária', 'Erzsébet', 'Katalin', 'Ilona', 'Éva', 'Anna', 'Zsuzsanna', 'Margit']
            },
            'Indienne': {
                'M': ['Rahul', 'Amit', 'Raj', 'Vikash', 'Sunil', 'Ravi', 'Anil', 'Sanjay'],
                'F': ['Priya', 'Sunita', 'Pooja', 'Kavita', 'Neetu', 'Rekha', 'Geeta', 'Seema']
            },
            'Indonésienne': {
                'M': ['Budi', 'Ahmad', 'Agus', 'Andi', 'Bambang', 'Dedi', 'Eko', 'Hadi'],
                'F': ['Sari', 'Sri', 'Indira', 'Dewi', 'Rina', 'Maya', 'Lestari', 'Wati']
            },
            'Iranienne': {
                'M': ['Mohammad', 'Ali', 'Hassan', 'Hossein', 'Reza', 'Ahmad', 'Mehdi', 'Abbas'],
                'F': ['Fatima', 'Zahra', 'Maryam', 'Narges', 'Somayeh', 'Fatemeh', 'Leila', 'Nasrin']
            },
            'Irlandaise': {
                'M': ['Sean', 'Patrick', 'Michael', 'John', 'David', 'Daniel', 'Paul', 'Mark'],
                'F': ['Mary', 'Margaret', 'Catherine', 'Bridget', 'Anne', 'Patricia', 'Helen', 'Elizabeth']
            },
            'Islandaise': {
                'M': ['Jón', 'Sigurdur', 'Guðmundur', 'Gunnar', 'Ólafur', 'Einar', 'Kristján', 'Magnús'],
                'F': ['Guðrún', 'Anna', 'Kristín', 'Margrét', 'Sigríður', 'Helga', 'Ragnhildur', 'Jóhanna']
            },
            'Israélienne': {
                'M': ['Moshe', 'David', 'Yosef', 'Daniel', 'Michael', 'Avi', 'Roi', 'Itai'],
                'F': ['Sarah', 'Miriam', 'Rachel', 'Tamar', 'Yael', 'Noa', 'Maya', 'Chen']
            },
            'Italienne': {
                'M': ['Giuseppe', 'Antonio', 'Giovanni', 'Mario', 'Francesco', 'Luigi', 'Angelo', 'Vincenzo'],
                'F': ['Maria', 'Anna', 'Giuseppina', 'Rosa', 'Angela', 'Giovanna', 'Teresa', 'Lucia']
            },
            'Japonaise': {
                'M': ['Hiroshi', 'Takeshi', 'Akira', 'Yuki', 'Daiki', 'Haruto', 'Sota', 'Ren'],
                'F': ['Sakura', 'Yuki', 'Ai', 'Rei', 'Mana', 'Yui', 'Hina', 'Emi']
            },
            'Kazakhe': {
                'M': ['Askar', 'Nurzhan', 'Dauren', 'Arman', 'Serik', 'Baurzhan', 'Erlan', 'Marat'],
                'F': ['Aida', 'Aigerim', 'Zhanna', 'Madina', 'Gulnara', 'Saule', 'Aliya', 'Nazira']
            },
            'Lettone': {
                'M': ['Jānis', 'Pēteris', 'Andris', 'Juris', 'Māris', 'Aivars', 'Valdis', 'Edgars'],
                'F': ['Anna', 'Marija', 'Ieva', 'Linda', 'Kristīne', 'Inese', 'Ilze', 'Dace']
            },
            'Lituanienne': {
                'M': ['Jonas', 'Antanas', 'Vytautas', 'Petras', 'Algirdas', 'Kęstutis', 'Mindaugas', 'Rimantas'],
                'F': ['Ona', 'Marija', 'Elena', 'Janina', 'Irena', 'Nijolė', 'Danutė', 'Aldona']
            },
            'Luxembourgeoise': {
                'M': ['Jean', 'Pierre', 'Marc', 'Alain', 'Claude', 'Michel', 'André', 'François'],
                'F': ['Marie', 'Anne', 'Monique', 'Josée', 'Christiane', 'Nicole', 'Martine', 'Françoise']
            },
            'Marocaine': {
                'M': ['Mohamed', 'Ahmed', 'Ali', 'Hassan', 'Omar', 'Youssef', 'Khalid', 'Abdelkader'],
                'F': ['Fatima', 'Aisha', 'Khadija', 'Zahra', 'Amina', 'Nadia', 'Malika', 'Samira']
            },
            'Mexicaine': {
                'M': ['José', 'Juan', 'Antonio', 'Jesús', 'Miguel', 'Pedro', 'Alejandro', 'Manuel'],
                'F': ['María', 'Guadalupe', 'Juana', 'Margarita', 'Francisca', 'Rosa', 'Isabel', 'Teresa']
            },
            'Néerlandaise': {
                'M': ['Johannes', 'Gerrit', 'Jan', 'Pieter', 'Cornelis', 'Hendrikus', 'Jacobus', 'Adrianus'],
                'F': ['Maria', 'Anna', 'Johanna', 'Cornelia', 'Elisabeth', 'Catharina', 'Geertruida', 'Margaretha']
            },
            'Nigériane': {
                'M': ['Chukwu', 'Emeka', 'Ikechukwu', 'Nnamdi', 'Obinna', 'Chijioke', 'Kelechi', 'Chidi'],
                'F': ['Ngozi', 'Chioma', 'Ifeoma', 'Adaeze', 'Chinwe', 'Nneka', 'Chiamaka', 'Uchechi']
            },
            'Norvégienne': {
                'M': ['Ole', 'Lars', 'Nils', 'Erik', 'Hans', 'Knut', 'Magnus', 'Bjørn'],
                'F': ['Anna', 'Marie', 'Ingrid', 'Karen', 'Astrid', 'Solveig', 'Kari', 'Liv']
            },
            'Polonaise': {
                'M': ['Jan', 'Andrzej', 'Krzysztof', 'Stanisław', 'Tomasz', 'Paweł', 'Józef', 'Marcin'],
                'F': ['Anna', 'Maria', 'Katarzyna', 'Małgorzata', 'Agnieszka', 'Barbara', 'Ewa', 'Elżbieta']
            },
            'Portugaise': {
                'M': ['José', 'António', 'João', 'Manuel', 'Francisco', 'Carlos', 'Joaquim', 'Luís'],
                'F': ['Maria', 'Ana', 'Manuela', 'Helena', 'Fernanda', 'Isabel', 'Paula', 'Conceição']
            },
            'Roumaine': {
                'M': ['Ion', 'Gheorghe', 'Nicolae', 'Vasile', 'Dumitru', 'Petre', 'Florin', 'Marian'],
                'F': ['Maria', 'Ana', 'Elena', 'Ioana', 'Mihaela', 'Cristina', 'Daniela', 'Andreea']
            },
            'Russe': {
                'M': ['Aleksandr', 'Sergei', 'Vladimir', 'Dmitri', 'Andrei', 'Alexei', 'Nikolai', 'Ivan'],
                'F': ['Elena', 'Olga', 'Irina', 'Tatyana', 'Svetlana', 'Natasha', 'Marina', 'Lyudmila']
            },
            'Suédoise': {
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
            'Thaïlandaise': {
                'M': ['Somchai', 'Surasak', 'Sombat', 'Suwan', 'Prasert', 'Wichai', 'Pornchai', 'Thawatchai'],
                'F': ['Siriporn', 'Sunisa', 'Pranee', 'Suwanna', 'Malee', 'Pimchai', 'Wanna', 'Sirikul']
            },
            'Turque': {
                'M': ['Mehmet', 'Mustafa', 'Ahmed', 'Ali', 'Hasan', 'İbrahim', 'Osman', 'Süleyman'],
                'F': ['Fatma', 'Ayşe', 'Emine', 'Hatice', 'Zeynep', 'Elif', 'Meryem', 'Özlem']
            },
            'Ukrainienne': {
                'M': ['Oleksandr', 'Sergiy', 'Andriy', 'Volodymyr', 'Oleksiy', 'Vitaliy', 'Igor', 'Yuriy'],
                'F': ['Oksana', 'Natalya', 'Olena', 'Iryna', 'Tetyana', 'Lyudmyla', 'Svitlana', 'Mariya']
            },
            'Américaine': {
                'M': ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Christopher', 'Matthew'],
                'F': ['Mary', 'Jennifer', 'Linda', 'Patricia', 'Susan', 'Jessica', 'Sarah', 'Karen']
            }
        }
        
        last_names = {
            'Afghane': ['Ahmad', 'Khan', 'Shah', 'Ali', 'Rahman', 'Hassan', 'Hussain', 'Mahmud', 'Omar', 'Yusuf'],
            'Allemande': ['Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann'],
            'Argentine': ['González', 'Rodríguez', 'Gómez', 'Fernández', 'López', 'Díaz', 'Martínez', 'Pérez', 'García', 'Sánchez'],
            'Australienne': ['Smith', 'Jones', 'Williams', 'Brown', 'Wilson', 'Taylor', 'Johnson', 'White', 'Martin', 'Anderson'],
            'Autrichienne': ['Gruber', 'Huber', 'Bauer', 'Wagner', 'Müller', 'Pichler', 'Steiner', 'Moser', 'Mayer', 'Hofer'],
            'Belge': ['Peeters', 'Janssens', 'Maes', 'Jacobs', 'Mertens', 'Willems', 'Claes', 'Goossens', 'Wouters', 'De Smet'],
            'Brésilienne': ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira', 'Lima', 'Gomes'],
            'Britannique': ['Smith', 'Jones', 'Taylor', 'Williams', 'Brown', 'Davies', 'Evans', 'Wilson', 'Thomas', 'Roberts'],
            'Bulgare': ['Ivanov', 'Petrov', 'Dimitrov', 'Georgiev', 'Nikolov', 'Todorov', 'Hristov', 'Stoyanov', 'Marinov', 'Angelov'],
            'Canadienne': ['Smith', 'Brown', 'Tremblay', 'Martin', 'Roy', 'Wilson', 'MacDonald', 'Johnson', 'Thompson', 'Anderson'],
            'Chinoise': ['Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Zhao', 'Huang', 'Zhou', 'Wu', 'Xu', 'Sun'],
            'Coréenne': ['Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Jang', 'Lim', 'Han', 'Oh'],
            'Croate': ['Horvat', 'Novak', 'Marić', 'Petrović', 'Jurić', 'Babić', 'Matić', 'Pavić', 'Tomić', 'Kovač'],
            'Danoise': ['Nielsen', 'Jensen', 'Hansen', 'Pedersen', 'Andersen', 'Christensen', 'Larsen', 'Sørensen', 'Rasmussen', 'Jørgensen'],
            'Égyptienne': ['Mohamed', 'Ahmed', 'Mahmoud', 'Hassan', 'Ali', 'Ibrahim', 'Abdel Rahman', 'Omar', 'Khalil', 'Said'],
            'Espagnole': ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Gómez', 'Martín'],
            'Estonienne': ['Tamm', 'Saar', 'Sepp', 'Mägi', 'Kask', 'Kukk', 'Rebane', 'Ilves', 'Pärn', 'Känd'],
            'Finlandaise': ['Korhonen', 'Virtanen', 'Mäkinen', 'Nieminen', 'Mäkelä', 'Hämäläinen', 'Laine', 'Heikkinen', 'Koskinen', 'Järvinen'],
            'Française': ['Martin', 'Bernard', 'Thomas', 'Petit', 'Robert', 'Richard', 'Durand', 'Dubois', 'Moreau', 'Laurent', 'Simon', 'Michel'],
            'Grecque': ['Papadopoulos', 'Georgiou', 'Dimitriou', 'Nikolaou', 'Ioannou', 'Petrou', 'Andreou', 'Christou', 'Antoniou', 'Stavrou'],
            'Hongroise': ['Nagy', 'Kovács', 'Tóth', 'Szabó', 'Horváth', 'Varga', 'Kiss', 'Molnár', 'Németh', 'Farkas'],
            'Indienne': ['Sharma', 'Verma', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Mishra', 'Jain', 'Patel', 'Yadav'],
            'Indonésienne': ['Sari', 'Dewi', 'Lestari', 'Wati', 'Indira', 'Putri', 'Anggraini', 'Fitria', 'Ningsih', 'Maharani'],
            'Iranienne': ['Hosseini', 'Ahmadi', 'Mohammadi', 'Rezaei', 'Moradi', 'Mousavi', 'Karimi', 'Rahimi', 'Bagheri', 'Hashemi'],
            'Irlandaise': ["O'Brien", "O'Sullivan", 'Murphy', "O'Connor", 'Kelly', 'Ryan', "O'Neill", 'Walsh', 'McCarthy', 'Gallagher'],
            'Islandaise': ['Jónsson', 'Sigurdsson', 'Guðmundsson', 'Einarsson', 'Gunnarsson', 'Ólafsson', 'Kristjánsson', 'Magnússon', 'Stefánsson', 'Þórsson'],
            'Israélienne': ['Cohen', 'Levy', 'Miller', 'Goldberg', 'Goldstein', 'Rosen', 'Katz', 'Friedman', 'Klein', 'Green'],
            'Italienne': ['Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco'],
            'Japonaise': ['Sato', 'Suzuki', 'Takahashi', 'Tanaka', 'Watanabe', 'Ito', 'Yamamoto', 'Nakamura', 'Kobayashi', 'Kato', 'Yoshida', 'Yamada'],
            'Kazakhe': ['Nazarbayev', 'Suleimenov', 'Akhmetov', 'Zhakenov', 'Kassymov', 'Moldashev', 'Bekmuratov', 'Aubakirov', 'Tuleyev', 'Mukanov'],
            'Lettone': ['Bērziņš', 'Kalniņš', 'Ozols', 'Krūmiņš', 'Liepa', 'Pētersons', 'Jansons', 'Kļaviņš', 'Zariņš', 'Sproģis'],
            'Lituanienne': ['Kazlauskas', 'Petrauskas', 'Jankauskas', 'Stankevicius', 'Vasiliauskas', 'Zukauskas', 'Butkus', 'Paulauskas', 'Urbonas', 'Rimkus'],
            'Luxembourgeoise': ['Muller', 'Weber', 'Wagner', 'Schmit', 'Hansen', 'Becker', 'Hoffmann', 'Klein', 'Fischer', 'Mayer'],
            'Marocaine': ['Alami', 'Bennani', 'El Idrissi', 'Fassi', 'Tazi', 'Benali', 'Berrada', 'Chakir', 'Lamrani', 'Oudghiri'],
            'Mexicaine': ['González', 'García', 'Martínez', 'López', 'Hernández', 'Pérez', 'Rodríguez', 'Sánchez', 'Ramírez', 'Cruz'],
            'Néerlandaise': ['De Jong', 'Jansen', 'De Vries', 'Van den Berg', 'Van Dijk', 'Bakker', 'Janssen', 'Visser', 'Smit', 'Meijer'],
            'Nigériane': ['Adebayo', 'Okafor', 'Okoro', 'Eze', 'Nwankwo', 'Okonkwo', 'Ogbonna', 'Chukwu', 'Emeka', 'Ikechukwu'],
            'Norvégienne': ['Hansen', 'Johansen', 'Olsen', 'Larsen', 'Andersen', 'Pedersen', 'Nilsen', 'Kristiansen', 'Jensen', 'Karlsen'],
            'Polonaise': ['Nowak', 'Kowalski', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński', 'Szymański', 'Woźniak'],
            'Portugaise': ['Silva', 'Santos', 'Ferreira', 'Pereira', 'Oliveira', 'Costa', 'Rodrigues', 'Martins', 'Jesus', 'Sousa'],
            'Roumaine': ['Popescu', 'Ionescu', 'Popa', 'Stoica', 'Stan', 'Dumitrescu', 'Gheorghe', 'Constantinescu', 'Marin', 'Diaconu'],
            'Russe': ['Ivanov', 'Smirnov', 'Kuznetsov', 'Popov', 'Sokolov', 'Lebedev', 'Kozlov', 'Novikov', 'Morozov', 'Petrov'],
            'Suédoise': ['Andersson', 'Johansson', 'Karlsson', 'Nilsson', 'Eriksson', 'Larsson', 'Olsson', 'Persson', 'Svensson', 'Gustafsson'],
            'Suisse': ['Müller', 'Meier', 'Schmid', 'Keller', 'Weber', 'Huber', 'Schneider', 'Meyer', 'Steiner', 'Fischer'],
            'Tchèque': ['Novák', 'Svoboda', 'Novotný', 'Dvořák', 'Černý', 'Procházka', 'Krejčí', 'Hájek', 'Kratochvíl', 'Horák'],
            'Thaïlandaise': ['Chanthavy', 'Siriporn', 'Somboon', 'Chanpen', 'Kamon', 'Narongsak', 'Prasert', 'Suwan', 'Thawatchai', 'Wichai'],
            'Turque': ['Yılmaz', 'Kaya', 'Demir', 'Şahin', 'Çelik', 'Yıldız', 'Yıldırım', 'Öztürk', 'Aydin', 'Özkan'],
            'Ukrainienne': ['Petrenko', 'Kovalenko', 'Bondarenko', 'Tkachenko', 'Kovalchuk', 'Kravchenko', 'Shevchenko', 'Polishchuk', 'Lysenko', 'Savchenko'],
            'Américaine': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez']
        }
        
        nationality_first_names = first_names.get(nationality, first_names['Française'])
        nationality_last_names = last_names.get(nationality, last_names['Française'])
        
        gender_first_names = nationality_first_names[gender]
        first_name = random.choice(gender_first_names)
        last_name = random.choice(nationality_last_names)
        
        return f"{first_name} {last_name}"
    
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
        """Simule une épreuve et retourne les résultats avec animations de mort"""
        alive_players = [p for p in players if p.alive]
        survivors = []
        eliminated = []
        
        for player in alive_players:
            # Calcul des chances de survie selon les stats et le rôle
            stat_bonus = cls._get_stat_bonus_for_event(player, event)
            role_bonus = cls._get_role_bonus_for_event(player, event)
            
            # Calcul base de survie influencé par difficulté et taux d'élimination
            base_survival = 1.0 - event.elimination_rate
            survive_chance = min(0.95, base_survival + (stat_bonus * 0.06) + role_bonus)
            
            # Ajustement selon difficulté
            difficulty_malus = (event.difficulty - 5) * 0.02  # Malus pour épreuves difficiles
            survive_chance = max(0.05, survive_chance - difficulty_malus)
            
            if random.random() < survive_chance:
                # Survie
                time_remaining = random.randint(event.survival_time_min // 4, event.survival_time_max // 2)
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
                    "number": player.number,
                    "name": player.name,
                    "time_remaining": time_remaining,
                    "event_kills": event_kills,
                    "betrayed": betrayed,
                    "score": score,
                    "kills": player.kills,
                    "total_score": player.total_score,
                    "survived_events": player.survived_events
                })
            else:
                # Élimination avec animation de mort spécifique
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
        
        # Trier les survivants par score
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
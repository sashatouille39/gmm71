import random
from typing import List
from models.game_models import GameEvent, EventType, EventCategory

class EventsService:
    """Service gérant les 80+ épreuves du jeu avec décors et animations uniques"""
    
    # 80+ épreuves organisées par catégories
    GAME_EVENTS = [
        # ================================
        # ÉPREUVES CLASSIQUES (5)
        # ================================
        GameEvent(
            id=1, name="Feu rouge, Feu vert", type=EventType.AGILITE, category=EventCategory.CLASSIQUES, difficulty=3,
            description="Avancez quand c'est vert, arrêtez-vous au rouge sinon vous mourrez",
            decor="Grande cour d'école avec poupée géante aux yeux laser",
            death_animations=[
                "Criblé de balles par les snipers",
                "Touché en plein mouvement, chute brutale",
                "Tentative de fuite, abattu dans le dos",
                "Paralysé par la peur, exécuté à bout portant"
            ],
            survival_time_min=120, survival_time_max=300,
            elimination_rate=0.4,
            special_mechanics=["Détection de mouvement laser", "Snipers automatiques"]
        ),
        
        GameEvent(
            id=2, name="Pont de verre", type=EventType.INTELLIGENCE, category=EventCategory.CLASSIQUES, difficulty=8,
            description="Traversez le pont en choisissant les bonnes plaques de verre",
            decor="Pont suspendu au-dessus d'un abîme de 50 mètres",
            death_animations=[
                "Chute mortelle de 50 mètres, impact au sol",
                "Verre brisé, découpage mortel avant la chute",
                "Poussé par un autre joueur, hurlement d'agonie",
                "Glissade, tentative désespérée de s'accrocher"
            ],
            survival_time_min=60, survival_time_max=180,
            elimination_rate=0.6,
            special_mechanics=["Ordre de passage", "Verre trempé vs normal"]
        ),
        
        GameEvent(
            id=3, name="Billes", type=EventType.INTELLIGENCE, category=EventCategory.CLASSIQUES, difficulty=6,
            description="Jeu de stratégie par paires, le perdant meurt",
            decor="Petites arènes individuelles sous surveillance",
            death_animations=[
                "Exécution d'une balle dans la tête",
                "Étranglement par les gardes",
                "Empoisonnement par injection",
                "Électrocution sur place"
            ],
            survival_time_min=180, survival_time_max=600,
            elimination_rate=0.5,
            special_mechanics=["Jeu par paires", "Trahison possible"]
        ),
        
        GameEvent(
            id=4, name="Tir à la corde", type=EventType.FORCE, category=EventCategory.CLASSIQUES, difficulty=7,
            description="Tirez plus fort que l'équipe adverse ou tombez dans le vide",
            decor="Plateforme suspendue avec cordes au-dessus d'un gouffre",
            death_animations=[
                "Chute collective de l'équipe perdante",
                "Glissade de la plateforme, tentative de rattrapage",
                "Écrasement contre les parois rocheuses",
                "Impact final au fond du gouffre"
            ],
            survival_time_min=90, survival_time_max=300,
            elimination_rate=0.5,
            special_mechanics=["Jeu d'équipe", "Stratégie collective"]
        ),
        
        GameEvent(
            id=5, name="Gaufres au sucre", type=EventType.AGILITE, category=EventCategory.CLASSIQUES, difficulty=5,
            description="Découpez la forme sans la casser en 10 minutes",
            decor="Salle de classe sinistre avec bureaux et aiguilles",
            death_animations=[
                "Balle dans la tête pour échec",
                "Aiguille empoisonnée dans le cœur",
                "Étranglement par fil de fer",
                "Brûlure au fer rouge"
            ],
            survival_time_min=300, survival_time_max=600,
            elimination_rate=0.3,
            special_mechanics=["Précision requise", "Limite de temps"]
        ),

        # ================================
        # ÉPREUVES DE COMBAT (15)
        # ================================
        GameEvent(
            id=6, name="Combat de gladiateurs", type=EventType.FORCE, category=EventCategory.COMBAT, difficulty=9,
            description="Battez-vous à mort dans l'arène avec des armes",
            decor="Arène romaine avec gradins remplis de VIP",
            death_animations=[
                "Coup d'épée mortel dans la poitrine",
                "Décapitation à la hache",
                "Étranglement au filet de gladiateur",
                "Transpercé par un trident"
            ],
            survival_time_min=60, survival_time_max=300,
            elimination_rate=0.55,
            special_mechanics=["Armes diverses", "Combat 1vs1"]
        ),
        
        GameEvent(
            id=7, name="Bataille royale", type=EventType.FORCE, category=EventCategory.COMBAT, difficulty=10,
            description="Dernière personne debout remporte l'épreuve",
            decor="Zone de guerre urbaine avec bâtiments en ruine",
            death_animations=[
                "Égorgement au couteau de combat",
                "Explosion de grenade, membres arrachés",
                "Coup de massue, crâne fracassé",
                "Noyade forcée dans une mare de sang"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.65,  # Exception: Battle Royale peut être plus élevé
            special_mechanics=["Libre pour tous", "Armes cachées"]
        ),
        
        GameEvent(
            id=8, name="Ring de boxe mortel", type=EventType.FORCE, difficulty=8,
            description="Boxe jusqu'à la mort, pas de règles",
            decor="Ring de boxe avec cordes électrifiées",
            death_animations=[
                "KO final, hémorragie cérébrale",
                "Coup mortel au foie, agonie lente",
                "Étranglement aux cordes électrifiées",
                "Chute du ring, nuque brisée"
            ],
            survival_time_min=180, survival_time_max=600,
            elimination_rate=0.6,
            special_mechanics=["Combat au corps à corps", "Ring électrifié"]
        ),
        
        GameEvent(
            id=9, name="Arène des fauves", type=EventType.FORCE, difficulty=9,
            description="Survivez aux animaux sauvages lâchés dans l'arène",
            decor="Arène avec cages d'animaux sauvages (lions, tigres)",
            death_animations=[
                "Dévoré vivant par un lion",
                "Griffures mortelles de tigre",
                "Piétiné par un éléphant enragé",
                "Mordu par un serpent venimeux géant"
            ],
            survival_time_min=120, survival_time_max=300,
            elimination_rate=0.58,
            special_mechanics=["Animaux sauvages", "Survie pure"]
        ),
        
        GameEvent(
            id=10, name="Duel au pistolet", type=EventType.FORCE, difficulty=7,
            description="Duel à l'ancienne, un seul survivant",
            decor="Cour d'honneur avec brouillard artificiel",
            death_animations=[
                "Balle en plein cœur, mort instantanée",
                "Touché au ventre, agonie prolongée",
                "Raté le tir, exécuté à bout portant",
                "Balle dans la tête, explosion crânienne"
            ],
            survival_time_min=30, survival_time_max=60,
            elimination_rate=0.5,
            special_mechanics=["Duel 1vs1", "Un seul tir"]
        ),
        
        GameEvent(
            id=11, name="Combat au couteau", type=EventType.FORCE, difficulty=8,
            description="Mêlée générale aux couteaux dans l'obscurité",
            decor="Salle plongée dans le noir avec éclairages stroboscopiques",
            death_animations=[
                "Poignardé dans le dos", 
                "Gorge tranchée d'un geste vif",
                "Éventré, tripes répandues au sol",
                "Coup de couteau dans l'œil"
            ],
            survival_time_min=120, survival_time_max=300,
            elimination_rate=0.6,
            special_mechanics=["Obscurité", "Combat rapproché"]
        ),
        
        GameEvent(
            id=12, name="Fosse aux serpents", type=EventType.FORCE, difficulty=6,
            description="Traversez la fosse remplie de serpents venimeux",
            decor="Grande fosse avec milliers de serpents venimeux",
            death_animations=[
                "Mordu par un cobra, convulsions mortelles",
                "Enlacé par un python, étouffement",
                "Multiples morsures, poison foudroyant",
                "Chute dans la fosse, dévoré vivant"
            ],
            survival_time_min=60, survival_time_max=180,
            elimination_rate=0.4,
            special_mechanics=["Serpents venimeux", "Traversée obligatoire"]
        ),
        
        GameEvent(
            id=13, name="Combat à l'épée", type=EventType.FORCE, difficulty=8,
            description="Escrime mortelle avec épées aiguisées",
            decor="Salle d'armes médiévale avec armures décoratives",
            death_animations=[
                "Transpercé par l'épée adverse",
                "Décapitation d'un coup net",
                "Coup dans le ventre, hémorragie",
                "Chute et empalement sur épée"
            ],
            survival_time_min=120, survival_time_max=360,
            elimination_rate=0.5,
            special_mechanics=["Escrime", "Technique requise"]
        ),
        
        GameEvent(
            id=14, name="Cage de la mort", type=EventType.FORCE, difficulty=9,
            description="Combat en cage, mort du perdant obligatoire",
            decor="Cage métallique suspendue au-dessus du vide",
            death_animations=[
                "Jeté hors de la cage, chute mortelle",
                "Étranglé contre les barreaux",
                "Crâne fracassé contre le sol de métal",
                "Étouffé dans une prise mortelle"
            ],
            survival_time_min=180, survival_time_max=420,
            elimination_rate=0.5,
            special_mechanics=["Cage fermée", "Combat rapproché"]
        ),
        
        GameEvent(
            id=15, name="Roulette russe géante", type=EventType.FORCE, difficulty=5,
            description="Version géante de la roulette russe avec révolver",
            decor="Grande roue de la fortune avec revolvers géants",
            death_animations=[
                "Balle dans la tête, explosion crânienne",
                "Raté, mais torture psychologique avant exécution",
                "Arme qui explose, mutilation faciale",
                "Crise cardiaque avant même de tirer"
            ],
            survival_time_min=30, survival_time_max=60,
            elimination_rate=0.3,
            special_mechanics=["Pur hasard", "Tension psychologique"]
        ),
        
        GameEvent(
            id=16, name="Combat de robots", type=EventType.FORCE, difficulty=8,
            description="Combattez des robots de combat programmés pour tuer",
            decor="Laboratoire futuriste avec robots de guerre",
            death_animations=[
                "Broyé par les pinces hydrauliques",
                "Laser mortel qui perfore le corps",
                "Électrocution par décharge haute tension",
                "Explosion du robot, shrapnels mortels"
            ],
            survival_time_min=120, survival_time_max=300,
            elimination_rate=0.6,
            special_mechanics=["Robots IA", "Technology avancée"]
        ),
        
        GameEvent(
            id=17, name="Arène aquatique", type=EventType.FORCE, difficulty=7,
            description="Combat dans un bassin avec requins affamés",
            decor="Bassin géant avec requins et plateforme centrale",
            death_animations=[
                "Dévoré par les requins",
                "Noyade après épuisement",
                "Mordu et saigné à mort",
                "Traîné sous l'eau par un requin"
            ],
            survival_time_min=180, survival_time_max=420,
            elimination_rate=0.6,
            special_mechanics=["Milieu aquatique", "Requins"]
        ),
        
        GameEvent(
            id=18, name="Combat au lance-flammes", type=EventType.FORCE, difficulty=9,
            description="Éliminez vos adversaires avec des lance-flammes",
            decor="Entrepôt industriel avec bidons d'essence",
            death_animations=[
                "Brûlé vif, hurlements d'agonie",
                "Explosion d'un bidon, carbonisation",
                "Inhalation de fumées toxiques",
                "Peau fondue par les flammes"
            ],
            survival_time_min=90, survival_time_max=240,
            elimination_rate=0.5,
            special_mechanics=["Armes à feu", "Environnement inflammable"]
        ),
        
        GameEvent(
            id=19, name="Bataille de masse", type=EventType.FORCE, difficulty=10,
            description="Guerre totale avec armes médiévales",
            decor="Champ de bataille médiéval avec château en ruine",
            death_animations=[
                "Transpercé par une lance de cavalerie",
                "Tête tranchée par une hache de guerre",
                "Écrasé par un boulet de catapulte",
                "Piétiné par la cavalerie lourde"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.52,
            special_mechanics=["Bataille massive", "Armes médiévales"]
        ),
        
        GameEvent(
            id=20, name="Prison de combat", type=EventType.FORCE, difficulty=8,
            description="Combat de prisonniers dans les cellules",
            decor="Prison avec cellules ouvertes et couloirs sombres",
            death_animations=[
                "Poignardé avec objet artisanal",
                "Étranglé avec drap de lit",
                "Crâne fracassé contre les barreaux",
                "Empoisonné avec produit de nettoyage"
            ],
            survival_time_min=240, survival_time_max=600,
            elimination_rate=0.6,
            special_mechanics=["Environnement carcéral", "Armes improvisées"]
        ),

        # ================================
        # ÉPREUVES D'AGILITÉ (15)
        # ================================
        GameEvent(
            id=21, name="Course d'obstacles mortels", type=EventType.AGILITE, difficulty=7,
            description="Parcours d'obstacles avec pièges mortels",
            decor="Parcours militaire avec lames rotatives et fosses",
            death_animations=[
                "Découpé par lames rotatives",
                "Chute dans fosse à pieux",
                "Écrasé par marteau géant",
                "Électrocuté sur fil barbelé"
            ],
            survival_time_min=180, survival_time_max=420,
            elimination_rate=0.5,
            special_mechanics=["Pièges mécaniques", "Chrono strict"]
        ),
        
        GameEvent(
            id=22, name="Parkour de la mort", type=EventType.AGILITE, difficulty=8,
            description="Parcours urbain avec pièges et snipers",
            decor="Ville en ruine avec bâtiments piégés",
            death_animations=[
                "Chute du toit d'un immeuble",
                "Abattu par sniper en mouvement",
                "Explosion de piège dans bâtiment",
                "Électrocution sur ligne haute tension"
            ],
            survival_time_min=240, survival_time_max=600,
            elimination_rate=0.6,
            special_mechanics=["Environnement urbain", "Snipers"]
        ),
        
        GameEvent(
            id=23, name="Labyrinthe tournant", type=EventType.AGILITE, difficulty=6,
            description="Labyrinthe dont les murs bougent et écrasent",
            decor="Labyrinthe mécanique avec murs mobiles",
            death_animations=[
                "Écrasé par murs qui se referment",
                "Broyé dans mécanisme rotatif",
                "Coupé en deux par mur-lame",
                "Piétiné dans la panique générale"
            ],
            survival_time_min=300, survival_time_max=600,
            elimination_rate=0.4,
            special_mechanics=["Murs mobiles", "Mécanismes d'écrasement"]
        ),
        
        GameEvent(
            id=24, name="Saut de la mort", type=EventType.AGILITE, difficulty=8,
            description="Sautez de plateforme en plateforme au-dessus du vide",
            decor="Série de plateformes suspendues au-dessus d'un abîme",
            death_animations=[
                "Raté le saut, chute dans le vide",
                "Plateforme s'effondre sous le poids",
                "Glissade, tentative de rattrapage échouée",
                "Poussé par un autre concurrent"
            ],
            survival_time_min=120, survival_time_max=300,
            elimination_rate=0.6,
            special_mechanics=["Plateformes instables", "Précision requise"]
        ),
        
        GameEvent(
            id=25, name="Tunnel rampant", type=EventType.AGILITE, difficulty=5,
            description="Ramper dans tunnels avec gaz toxique qui monte",
            decor="Réseau de tunnels étroits avec ventilation toxique",
            death_animations=[
                "Asphyxié par gaz toxique",
                "Coincé dans tunnel, écrasé",
                "Empoisonnement par vapeurs",
                "Panique, crise cardiaque dans tunnel"
            ],
            survival_time_min=180, survival_time_max=360,
            elimination_rate=0.3,
            special_mechanics=["Espaces confinés", "Gaz toxique"]
        ),
        
        GameEvent(
            id=26, name="Escalade mortelle", type=EventType.AGILITE, difficulty=7,
            description="Escaladez la tour pendant qu'elle s'effondre",
            decor="Tour en construction qui s'effondre progressivement",
            death_animations=[
                "Chute du haut de la tour",
                "Écrasé par débris qui tombent",
                "Corde qui lâche, chute libre",
                "Enseveli sous éboulement"
            ],
            survival_time_min=240, survival_time_max=480,
            elimination_rate=0.5,
            special_mechanics=["Escalade", "Effondrement progressif"]
        ),
        
        GameEvent(
            id=27, name="Course de voitures", type=EventType.AGILITE, difficulty=6,
            description="Course-poursuite avec voitures piégées",
            decor="Circuit de course avec véhicules explosifs",
            death_animations=[
                "Explosion de voiture, carbonisation",
                "Accident frontal, impact mortel",
                "Éjection de véhicule, chute mortelle",
                "Écrasement contre barrière de sécurité"
            ],
            survival_time_min=180, survival_time_max=420,
            elimination_rate=0.6,
            special_mechanics=["Véhicules", "Explosifs"]
        ),
        
        GameEvent(
            id=28, name="Tyrolienne de l'enfer", type=EventType.AGILITE, difficulty=7,
            description="Traversez sur tyrolienne avec cordes qui se coupent",
            decor="Canyon profond avec tyroliennes qui se sectionnent",
            death_animations=[
                "Corde qui lâche, chute dans canyon",
                "Collision avec paroi rocheuse",
                "Harnais qui cède, glissade mortelle",
                "Sabotage par autre concurrent"
            ],
            survival_time_min=90, survival_time_max=180,
            elimination_rate=0.5,
            special_mechanics=["Tyrolienne", "Cordes défaillantes"]
        ),
        
        GameEvent(
            id=29, name="Surf sur lave", type=EventType.AGILITE, difficulty=9,
            description="Surfez sur planches au-dessus de lave en fusion",
            decor="Volcan artificiel avec rivières de lave",
            death_animations=[
                "Chute dans lave, carbonisation instantanée",
                "Planche qui fond, immersion mortelle",
                "Brûlures par projections de lave",
                "Inhalation de gaz toxiques volcaniques"
            ],
            survival_time_min=120, survival_time_max=240,
            elimination_rate=0.48,
            special_mechanics=["Lave en fusion", "Équilibre extrême"]
        ),
        
        GameEvent(
            id=30, name="Slalom explosif", type=EventType.AGILITE, difficulty=6,
            description="Slalom entre mines antipersonnel",
            decor="Champ de mines avec parcours balisé",
            death_animations=[
                "Explosion de mine, membres arrachés",
                "Onde de choc, hémorragie interne",
                "Shrapnels dans tout le corps",
                "Déflagration en chaîne, vaporisation"
            ],
            survival_time_min=60, survival_time_max=180,
            elimination_rate=0.4,
            special_mechanics=["Mines explosives", "Parcours précis"]
        ),
        
        GameEvent(
            id=31, name="Swing de la jungle", type=EventType.AGILITE, difficulty=7,
            description="Balancez-vous de liane en liane au-dessus de crocodiles",
            decor="Jungle artificielle avec bassin de crocodiles",
            death_animations=[
                "Liane qui casse, chute chez crocodiles",
                "Dévoré vivant par crocodiles affamés",
                "Glissade des mains, noyade",
                "Coup de queue de crocodile, nuque brisée"
            ],
            survival_time_min=120, survival_time_max=300,
            elimination_rate=0.5,
            special_mechanics=["Lianes", "Crocodiles"]
        ),
        
        GameEvent(
            id=32, name="Fuite dans égouts", type=EventType.AGILITE, difficulty=5,
            description="Fuyez dans égouts avec eau qui monte",
            decor="Réseau d'égouts avec niveau d'eau montant",
            death_animations=[
                "Noyade dans égout bouché",
                "Emporté par courant d'égout",
                "Empoisonnement par eau contaminée",
                "Coincé dans grille, asphyxie"
            ],
            survival_time_min=240, survival_time_max=480,
            elimination_rate=0.3,
            special_mechanics=["Milieu aquatique", "Montée des eaux"]
        ),
        
        GameEvent(
            id=33, name="Trampolines mortels", type=EventType.AGILITE, difficulty=6,
            description="Sautez de trampoline en trampoline avec pièges",
            decor="Parc de trampolines avec lames et fosses",
            death_animations=[
                "Atterrissage sur lames, transpercement",
                "Saut raté, chute dans fosse à pieux",
                "Trampoline piégé, explosion au contact",
                "Collision avec autre concurrent, chute mortelle"
            ],
            survival_time_min=180, survival_time_max=360,
            elimination_rate=0.4,
            special_mechanics=["Trampolines", "Pièges intégrés"]
        ),
        
        GameEvent(
            id=34, name="Course de drones", type=EventType.AGILITE, difficulty=8,
            description="Évitez les drones tueurs en courant",
            decor="Terrain découvert avec essaim de drones armés",
            death_animations=[
                "Criblé par mitraillettes de drones",
                "Explosion de drone kamikaze",
                "Laser mortel de drone de pointe",
                "Électrocution par taser de drone"
            ],
            survival_time_min=120, survival_time_max=300,
            elimination_rate=0.6,
            special_mechanics=["Drones IA", "Armes automatisées"]
        ),
        
        GameEvent(
            id=35, name="Patinage sur glace mortelle", type=EventType.AGILITE, difficulty=7,
            description="Patinez sur glace qui se brise avec requins dessous",
            decor="Patinoire au-dessus d'aquarium à requins",
            death_animations=[
                "Glace qui cède, chute chez requins",
                "Hypothermie dans eau glacée",
                "Dévoré par requins après chute",
                "Glissade, coup mortel contre bord"
            ],
            survival_time_min=180, survival_time_max=360,
            elimination_rate=0.5,
            special_mechanics=["Glace fragile", "Requins en dessous"]
        ),

        # ================================
        # ÉPREUVES D'INTELLIGENCE (15)
        # ================================
        GameEvent(
            id=36, name="Énigme du Sphinx mortel", type=EventType.INTELLIGENCE, difficulty=8,
            description="Résolvez l'énigme ou soyez dévoré par le sphinx mécanique",
            decor="Temple égyptien avec sphinx robotique géant",
            death_animations=[
                "Dévoré par mâchoires mécaniques du sphinx",
                "Écrasé sous pattes du sphinx",
                "Laser mortel des yeux du sphinx",
                "Gaz toxique émis par sphinx pour mauvaise réponse"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.6,
            special_mechanics=["Énigmes complexes", "Sphinx robotique"]
        ),
        
        GameEvent(
            id=37, name="Laboratoire chimique", type=EventType.INTELLIGENCE, difficulty=7,
            description="Créez l'antidote ou mourez empoisonné",
            decor="Laboratoire avec produits chimiques et équipement",
            death_animations=[
                "Empoisonnement par mauvais mélange",
                "Explosion chimique, brûlures acides",
                "Inhalation de gaz toxique mortel",
                "Convulsions par poison neural"
            ],
            survival_time_min=240, survival_time_max=600,
            elimination_rate=0.5,
            special_mechanics=["Chimie", "Formules complexes"]
        ),
        
        GameEvent(
            id=38, name="Salle des miroirs", type=EventType.INTELLIGENCE, difficulty=6,
            description="Trouvez la sortie dans labyrinthe de miroirs avant le gaz",
            decor="Labyrinthe de miroirs avec gaz qui se répand",
            death_animations=[
                "Asphyxie par gaz mortel",
                "Coupure mortelle en brisant miroir",
                "Crise de panique, crise cardiaque",
                "Perdu dans dédale, effondrement"
            ],
            survival_time_min=180, survival_time_max=420,
            elimination_rate=0.4,
            special_mechanics=["Illusions optiques", "Gaz toxique"]
        ),
        
        GameEvent(
            id=39, name="Puzzle temporel", type=EventType.INTELLIGENCE, difficulty=9,
            description="Résolvez puzzle 3D avant l'explosion",
            decor="Salle avec puzzle géant et bombe à retardement",
            death_animations=[
                "Explosion de bombe, vaporisation",
                "Écrasement par pièces de puzzle",
                "Électrocution par mauvaise manipulation",
                "Onde de choc, hémorragie interne"
            ],
            survival_time_min=600, survival_time_max=1200,
            elimination_rate=0.48,
            special_mechanics=["Puzzle 3D", "Bombe à retardement"]
        ),
        
        GameEvent(
            id=40, name="Bataille navale géante", type=EventType.INTELLIGENCE, difficulty=6,
            description="Bataille navale avec vraies explosions sur plateau géant",
            decor="Plateau de bataille navale avec piscines et explosifs",
            death_animations=[
                "Explosion de navire, noyade",
                "Brûlures par napalm naval",
                "Coulé avec navire, asphyxie",
                "Shrapnels d'explosion, hémorragie"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.5,
            special_mechanics=["Stratégie navale", "Explosions réelles"]
        ),
        
        GameEvent(
            id=41, name="Codes secrets", type=EventType.INTELLIGENCE, difficulty=8,
            description="Cassez les codes avant que les lasers vous découpent",
            decor="Salle high-tech avec lasers mortels et ordinateurs",
            death_animations=[
                "Découpé par grille de lasers",
                "Électrocution par sécurité informatique",
                "Gaz neurotoxique pour mauvais code",
                "Incinération par défense thermique"
            ],
            survival_time_min=240, survival_time_max=600,
            elimination_rate=0.6,
            special_mechanics=["Codes informatiques", "Lasers de sécurité"]
        ),
        
        GameEvent(
            id=42, name="Échecs de la mort", type=EventType.INTELLIGENCE, difficulty=7,
            description="Échecs géants, les pièces tuées meurent vraiment",
            decor="Échiquier géant avec joueurs comme pièces vivantes",
            death_animations=[
                "Exécution selon règle d'échecs",
                "Décapitation par pièce adverse",
                "Piétiné par cavalier géant",
                "Écrasé par tour qui bouge"
            ],
            survival_time_min=900, survival_time_max=1800,
            elimination_rate=0.5,
            special_mechanics=["Règles d'échecs", "Pièces vivantes"]
        ),
        
        GameEvent(
            id=43, name="Désamorçage de bombe", type=EventType.INTELLIGENCE, difficulty=9,
            description="Désamorcez bombe complexe ou mourez dans l'explosion",
            decor="Bunker avec bombe atomique miniature",
            death_animations=[
                "Explosion nucléaire, vaporisation",
                "Radiation mortelle par mauvaise manipulation",
                "Déflagration chimique, carbonisation",
                "Onde de choc, pulvérisation"
            ],
            survival_time_min=180, survival_time_max=600,
            elimination_rate=0.52,
            special_mechanics=["Désamorçage", "Bombe complexe"]
        ),
        
        GameEvent(
            id=44, name="Sudoku mortel", type=EventType.INTELLIGENCE, difficulty=6,
            description="Résolvez sudoku géant ou soyez électrocuté",
            decor="Grille de sudoku électrifiée géante au sol",
            death_animations=[
                "Électrocution par mauvais chiffre",
                "Décharge mortelle haute tension",
                "Court-circuit, explosion électrique",
                "Paralysie puis arrêt cardiaque"
            ],
            survival_time_min=600, survival_time_max=1200,
            elimination_rate=0.4,
            special_mechanics=["Sudoku géant", "Électrification"]
        ),
        
        GameEvent(
            id=45, name="Interrogatoire psychologique", type=EventType.INTELLIGENCE, difficulty=5,
            description="Répondez aux questions psychologiques ou soyez éliminé",
            decor="Salle d'interrogatoire avec détecteur de mensonges",
            death_animations=[
                "Injection létale pour mensonge",
                "Décharge électrique de détecteur",
                "Gaz soporifique puis élimination",
                "Poison dans eau pour mauvaise réponse"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.3,
            special_mechanics=["Psychologie", "Détecteur de mensonges"]
        ),
        
        GameEvent(
            id=46, name="Calculs de survie", type=EventType.INTELLIGENCE, difficulty=8,
            description="Calculez trajectoire d'évasion avant impact de missiles",
            decor="Salle de contrôle avec missiles en approche",
            death_animations=[
                "Impact direct de missile, vaporisation",
                "Onde de choc, démembrement",
                "Shrapnels de missile, perforation",
                "Explosion en chaîne, carbonisation"
            ],
            survival_time_min=120, survival_time_max=300,
            elimination_rate=0.52,
            special_mechanics=["Calculs balistiques", "Missiles réels"]
        ),
        
        GameEvent(
            id=47, name="Mémoire photographique", type=EventType.INTELLIGENCE, difficulty=6,
            description="Mémorisez séquence complexe ou soyez gazé",
            decor="Salle avec écrans géants et diffuseurs de gaz",
            death_animations=[
                "Gaz mortel pour mauvaise séquence",
                "Asphyxie par gaz neurotoxique",
                "Convulsions par poison neural",
                "Paralysie respiratoire"
            ],
            survival_time_min=180, survival_time_max=480,
            elimination_rate=0.5,
            special_mechanics=["Mémoire visuelle", "Séquences complexes"]
        ),
        
        GameEvent(
            id=48, name="Logique quantique", type=EventType.INTELLIGENCE, difficulty=10,
            description="Résolvez équations quantiques ou soyez désintégré",
            decor="Laboratoire quantique avec accélérateur de particules",
            death_animations=[
                "Désintégration par faisceau quantique",
                "Annihilation moléculaire",
                "Téléportation ratée, dispersion",
                "Radiation quantique, mutation mortelle"
            ],
            survival_time_min=600, survival_time_max=1800,
            elimination_rate=0.52,
            special_mechanics=["Physique quantique", "Science avancée"]
        ),
        
        GameEvent(
            id=49, name="Stratégie militaire", type=EventType.INTELLIGENCE, difficulty=8,
            description="Dirigez bataille tactique ou mourez avec vos troupes",
            decor="Salle de guerre avec cartes et communications",
            death_animations=[
                "Exécution pour défaite militaire",
                "Explosion d'obus sur QG",
                "Assassinat par sniper ennemi",
                "Poison dans rations militaires"
            ],
            survival_time_min=900, survival_time_max=1800,
            elimination_rate=0.6,
            special_mechanics=["Tactique militaire", "Guerre réelle"]
        ),
        
        GameEvent(
            id=50, name="Diagnostic médical", type=EventType.INTELLIGENCE, difficulty=7,
            description="Diagnostiquez maladie mortelle ou mourez du même mal",
            decor="Hôpital avec patients mourants et équipement médical",
            death_animations=[
                "Contamination par maladie non identifiée",
                "Empoisonnement par mauvais traitement",
                "Infection par manipulation d'organes",
                "Virus mortel par contact patient"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.5,
            special_mechanics=["Médecine", "Diagnostics complexes"]
        ),

        # ================================
        # ÉPREUVES MIXTES ET SPÉCIALES (35)
        # ================================
        GameEvent(
            id=51, name="Jeu de la confiance", type=EventType.INTELLIGENCE, difficulty=5,
            description="Faites confiance ou trahissez, mais choisissez bien",
            decor="Salle avec cabines individuelles et système de vote",
            death_animations=[
                "Empoisonnement par partenaire traître",
                "Strangulation par celui en qui on avait confiance",
                "Poignardé dans le dos par allié",
                "Électrocution par vote majoritaire"
            ],
            survival_time_min=600, survival_time_max=1800,
            elimination_rate=0.4,
            special_mechanics=["Psychologie sociale", "Trahison possible"]
        ),
        
        GameEvent(
            id=52, name="Test de loyauté", type=EventType.INTELLIGENCE, difficulty=4,
            description="Prouvez votre loyauté en sacrifiant un autre",
            decor="Arène avec participants enchaînés",
            death_animations=[
                "Sacrifié par choix d'un autre",
                "Refus de sacrifice, exécution",
                "Torture pour désobéissance",
                "Suicide plutôt que trahir"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.3,
            special_mechanics=["Sacrifice forcé", "Loyauté testée"]
        ),
        
        GameEvent(
            id=53, name="Roulette de torture", type=EventType.FORCE, difficulty=6,
            description="Roulette qui détermine votre méthode de torture",
            decor="Salle de torture médiévale avec roue géante",
            death_animations=[
                "Écartelé par la roue",
                "Brûlé au fer rouge",
                "Noyé dans cuve d'acide",
                "Découpé à la scie électrique"
            ],
            survival_time_min=180, survival_time_max=600,
            elimination_rate=0.5,
            special_mechanics=["Torture aléatoire", "Souffrance prolongée"]
        ),
        
        GameEvent(
            id=54, name="Chambre des horreurs", type=EventType.AGILITE, difficulty=7,
            description="Traversez chambre remplie de pièges sadiques",
            decor="Manoir hanté avec pièges psychologiques",
            death_animations=[
                "Empalé sur pieux cachés",
                "Décapité par lame pendulaire",
                "Écrasé par plafond qui descend",
                "Empoisonné par aiguilles murales"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.6,
            special_mechanics=["Pièges sadiques", "Horreur psychologique"]
        ),
        
        GameEvent(
            id=55, name="Labyrinthe de glace", type=EventType.INTELLIGENCE, difficulty=6,
            description="Trouvez sortie avant hypothermie mortelle",
            decor="Labyrinthe dans chambre froide industrielle",
            death_animations=[
                "Mort par hypothermie",
                "Gelé sur place, statuefié",
                "Glissade mortelle sur glace",
                "Brisé comme statue de glace"
            ],
            survival_time_min=600, survival_time_max=1200,
            elimination_rate=0.4,
            special_mechanics=["Froid extrême", "Hypothermie"]
        ),
        
        GameEvent(
            id=56, name="Salle de pression", type=EventType.FORCE, difficulty=8,
            description="Résistez à pression extrême ou soyez écrasé",
            decor="Chambre de décompression spatiale",
            death_animations=[
                "Écrasement par pression atmosphérique",
                "Explosion interne par décompression",
                "Hémorragie par surpression",
                "Asphyxie dans vide spatial"
            ],
            survival_time_min=120, survival_time_max=360,
            elimination_rate=0.6,
            special_mechanics=["Pression extrême", "Environnement spatial"]
        ),
        
        GameEvent(
            id=57, name="Danse macabre", type=EventType.AGILITE, difficulty=5,
            description="Dansez parfaitement ou soyez exécuté",
            decor="Salle de bal gothique avec orchestred'squelettes",
            death_animations=[
                "Décapitation pour faux pas",
                "Poignardé par danseur squelette",
                "Chute dans trappe du sol",
                "Empoisonnement par parfum mortel"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.3,
            special_mechanics=["Chorégraphie précise", "Rythme mortel"]
        ),
        
        GameEvent(
            id=58, name="Aquarium de la mort", type=EventType.AGILITE, difficulty=7,
            description="Nagez parmi créatures marines mortelles",
            decor="Aquarium géant avec prédateurs marins",
            death_animations=[
                "Dévoré par requin-tigre",
                "Piqûre mortelle de raie",
                "Étreinte mortelle de pieuvre géante",
                "Empoisonnement par méduse"
            ],
            survival_time_min=180, survival_time_max=420,
            elimination_rate=0.6,
            special_mechanics=["Milieu aquatique", "Prédateurs marins"]
        ),
        
        GameEvent(
            id=59, name="Forêt empoisonnée", type=EventType.INTELLIGENCE, difficulty=6,
            description="Traversez forêt sans toucher plantes toxiques",
            decor="Serre tropicale avec plantes carnivores et toxiques",
            death_animations=[
                "Empoisonnement par plante toxique",
                "Dévoré par plante carnivore",
                "Paralysé par pollen mortel",
                "Suffocation par spores toxiques"
            ],
            survival_time_min=240, survival_time_max=600,
            elimination_rate=0.5,
            special_mechanics=["Botanique mortelle", "Toxines naturelles"]
        ),
        
        GameEvent(
            id=60, name="Mine abandonnée", type=EventType.AGILITE, difficulty=7,
            description="Échappez-vous de mine qui s'effondre",
            decor="Mine de charbon avec structure instable",
            death_animations=[
                "Enseveli sous éboulement",
                "Asphyxié par gaz de mine",
                "Noyé dans infiltration d'eau",
                "Explosion de grisou, carbonisation"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.6,
            special_mechanics=["Effondrement", "Gaz toxiques"]
        ),
        
        GameEvent(
            id=61, name="Casino russe", type=EventType.INTELLIGENCE, difficulty=5,
            description="Jeux de casino mortels avec vraies conséquences",
            decor="Casino luxueux avec tables de jeu mortelles",
            death_animations=[
                "Abattu pour dette de jeu",
                "Empoisonné dans cocktail",
                "Étranglé par dealer",
                "Défenestré depuis étage élevé"
            ],
            survival_time_min=600, survival_time_max=1800,
            elimination_rate=0.4,
            special_mechanics=["Jeux de hasard", "Dettes mortelles"]
        ),
        
        GameEvent(
            id=62, name="Usine chimique", type=EventType.AGILITE, difficulty=8,
            description="Fuyez usine en explosion avec produits toxiques",
            decor="Complexe industriel chimique en feu",
            death_animations=[
                "Incinéré dans explosion chimique",
                "Intoxiqué par vapeurs toxiques",
                "Brûlé par acide renversé",
                "Asphyxié par fumées mortelles"
            ],
            survival_time_min=180, survival_time_max=420,
            elimination_rate=0.6,
            special_mechanics=["Explosion industrielle", "Produits chimiques"]
        ),
        
        GameEvent(
            id=63, name="Bibliothèque maudite", type=EventType.INTELLIGENCE, difficulty=6,
            description="Trouvez livre de vie avant que livres vous tuent",
            decor="Bibliothèque gothique avec livres animés",
            death_animations=[
                "Étranglé par pages de livre",
                "Empoisonné par encre mortelle",
                "Papercuts mortelles multiples",
                "Écrasé sous pile de livres"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.5,
            special_mechanics=["Livres animés", "Connaissance mortelle"]
        ),
        
        GameEvent(
            id=64, name="Cirque de l'horreur", type=EventType.AGILITE, difficulty=7,
            description="Spectacle de cirque où vous êtes la performance",
            decor="Chapiteau de cirque avec numéros mortels",
            death_animations=[
                "Raté cascade, chute mortelle",
                "Dévoré par lions de cirque",
                "Accident de trapèze, écrasement",
                "Couteau de lanceur qui trouve sa cible"
            ],
            survival_time_min=240, survival_time_max=600,
            elimination_rate=0.6,
            special_mechanics=["Numéros de cirque", "Performance mortelle"]
        ),
        
        GameEvent(
            id=65, name="Hôpital psychiatrique", type=EventType.INTELLIGENCE, difficulty=8,
            description="Échappez-vous avant de devenir fou et d'être lobotomisé",
            decor="Asile psychiatrique abandonné avec patients fantômes",
            death_animations=[
                "Lobotomie forcée",
                "Suicide par folie induite",
                "Attaque par patient fou",
                "Overdose de médicaments psychiatriques"
            ],
            survival_time_min=600, survival_time_max=1800,
            elimination_rate=0.5,
            special_mechanics=["Santé mentale", "Folie progressive"]
        ),
        
        GameEvent(
            id=66, name="Vaisseau spatial", type=EventType.INTELLIGENCE, difficulty=9,
            description="Réparez vaisseau avant qu'il s'écrase sur planète",
            decor="Vaisseau spatial en perdition au-dessus de planète hostile",
            death_animations=[
                "Crash sur planète, vaporisation",
                "Éjecté dans espace, asphyxie",
                "Radiation cosmique mortelle",
                "Explosion de réacteur nucléaire"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.6,
            special_mechanics=["Technologie spatiale", "Réparations complexes"]
        ),
        
        GameEvent(
            id=67, name="Cimetière hanté", type=EventType.FORCE, difficulty=6,
            description="Survivez aux morts-vivants qui sortent des tombes",
            decor="Cimetière gothique avec tombes ouvertes",
            death_animations=[
                "Dévoré par zombie affamé",
                "Griffé mortellement par squelette",
                "Étranglé par fantôme vengeur",
                "Enterré vivant dans tombe"
            ],
            survival_time_min=240, survival_time_max=720,
            elimination_rate=0.5,
            special_mechanics=["Morts-vivants", "Horreur surnaturelle"]
        ),
        
        GameEvent(
            id=68, name="Bunker nucléaire", type=EventType.INTELLIGENCE, difficulty=8,
            description="Désactivez réacteur avant explosion nucléaire",
            decor="Bunker militaire avec réacteur nucléaire en surchauffe",
            death_animations=[
                "Vaporisation par explosion nucléaire",
                "Radiation mortelle par exposition",
                "Fusion par chaleur du réacteur",
                "Asphyxie par vapeur radioactive"
            ],
            survival_time_min=180, survival_time_max=600,
            elimination_rate=0.52,
            special_mechanics=["Énergie nucléaire", "Radiation mortelle"]
        ),
        
        GameEvent(
            id=69, name="Parc d'attractions", type=EventType.AGILITE, difficulty=6,
            description="Survivez aux attractions mortelles du parc maudit",
            decor="Parc d'attractions abandonné avec manèges mortels",
            death_animations=[
                "Éjecté de montagnes russes mortelles",
                "Noyé dans tunnel de l'amour toxique",
                "Découpé par manège détraqué",
                "Électrocuté dans auto-tamponneuses"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.5,
            special_mechanics=["Attractions mortelles", "Parc abandonné"]
        ),
        
        GameEvent(
            id=70, name="Sous-marin", type=EventType.INTELLIGENCE, difficulty=8,
            description="Réparez sous-marin qui coule avant noyade",
            decor="Sous-marin militaire qui prend l'eau",
            death_animations=[
                "Noyade dans sous-marin coulé",
                "Écrasé par pression des grands fonds",
                "Empoisonné par fuite de combustible",
                "Explosion de torpille, démembrement"
            ],
            survival_time_min=240, survival_time_max=720,
            elimination_rate=0.45,
            special_mechanics=["Milieu sous-marin", "Réparations techniques"]
        ),
        
        GameEvent(
            id=71, name="Désert de sable", type=EventType.FORCE, difficulty=7,
            description="Traversez désert avec tempête de sable et vers géants",
            decor="Désert hostile avec tempête et créatures souterraines",
            death_animations=[
                "Dévoré par ver de sable géant",
                "Mort de soif et déshydratation",
                "Enseveli par tempête de sable",
                "Empoisonné par morsure de scorpion"
            ],
            survival_time_min=600, survival_time_max=1800,
            elimination_rate=0.6,
            special_mechanics=["Environnement désertique", "Créatures hostiles"]
        ),
        
        GameEvent(
            id=72, name="Prison flottante", type=EventType.AGILITE, difficulty=7,
            description="Échappez-vous de prison sur plateforme pétrolière",
            decor="Plateforme pétrolière convertie en prison",
            death_animations=[
                "Noyade en tentant de fuir",
                "Abattu par gardiens sur tours",
                "Explosion de puits de pétrole",
                "Requin qui dévore pendant évasion"
            ],
            survival_time_min=420, survival_time_max=1200,
            elimination_rate=0.6,
            special_mechanics=["Milieu maritime", "Évasion de prison"]
        ),
        
        GameEvent(
            id=73, name="Laboratoire génétique", type=EventType.INTELLIGENCE, difficulty=9,
            description="Survivez aux mutations génétiques expérimentales",
            decor="Laboratoire avec créatures mutantes en liberté",
            death_animations=[
                "Déchiqueté par mutant génétique",
                "Infection par virus mutagène",
                "Dévoré par plante carnivore mutante",
                "Transformation mortelle en monstre"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.48,
            special_mechanics=["Mutations génétiques", "Créatures expérimentales"]
        ),
        
        GameEvent(
            id=74, name="Glacier mortel", type=EventType.AGILITE, difficulty=8,
            description="Escaladez glacier avant avalanche mortelle",
            decor="Glacier en haute montagne avec crevasses",
            death_animations=[
                "Enseveli par avalanche",
                "Chute dans crevasse profonde",
                "Hypothermie en haute altitude",
                "Écrasé par bloc de glace"
            ],
            survival_time_min=240, survival_time_max=720,
            elimination_rate=0.5,
            special_mechanics=["Haute altitude", "Conditions extrêmes"]
        ),
        
        GameEvent(
            id=75, name="Usine robotique", type=EventType.INTELLIGENCE, difficulty=8,
            description="Programmez robots ou soyez éliminé par eux",
            decor="Usine automatisée avec robots industriels",
            death_animations=[
                "Broyé par robot industriel",
                "Soudé par robot automatique",
                "Découpé par laser de robot",
                "Électrocuté par robot défaillant"
            ],
            survival_time_min=300, survival_time_max=900,
            elimination_rate=0.6,
            special_mechanics=["Programmation robotique", "IA hostile"]
        ),
        
        GameEvent(
            id=76, name="Volcan actif", type=EventType.FORCE, difficulty=9,
            description="Échappez-vous du volcan en éruption",
            decor="Cratère volcanique avec lave et gaz toxiques",
            death_animations=[
                "Carbonisé par coulée de lave",
                "Asphyxié par gaz volcanique",
                "Brûlé par projection de magma",
                "Chute dans lac de lave"
            ],
            survival_time_min=180, survival_time_max=480,
            elimination_rate=0.6,
            special_mechanics=["Éruption volcanique", "Lave en fusion"]
        ),
        
        GameEvent(
            id=77, name="Station spatiale", type=EventType.INTELLIGENCE, difficulty=9,
            description="Réparez station avant qu'elle tombe sur Terre",
            decor="Station spatiale internationale en perdition",
            death_animations=[
                "Brûlé lors de rentrée atmosphérique",
                "Asphyxié dans espace",
                "Radiation mortelle du Soleil",
                "Impact au sol, vaporisation"
            ],
            survival_time_min=240, survival_time_max=720,
            elimination_rate=0.6,
            special_mechanics=["Technologie spatiale", "Apesanteur"]
        ),
        
        GameEvent(
            id=78, name="Jungle amazonienne", type=EventType.AGILITE, difficulty=7,
            description="Survivez dans jungle avec prédateurs et tribus",
            decor="Forêt amazonienne dense avec animaux sauvages",
            death_animations=[
                "Dévoré par jaguar affamé",
                "Empoisonné par flèche de tribu",
                "Mordu par serpent venimeux",
                "Noyé dans rivière aux piranhas"
            ],
            survival_time_min=720, survival_time_max=2160,
            elimination_rate=0.6,
            special_mechanics=["Survie en jungle", "Prédateurs naturels"]
        ),
        
        GameEvent(
            id=79, name="Château fort", type=EventType.FORCE, difficulty=8,
            description="Assiégez château défendu par archers et soldats",
            decor="Château médiéval fortifié avec défenseurs",
            death_animations=[
                "Transpercé par flèche d'archer",
                "Ébouillantement par huile bouillante",
                "Écrasé par pierre de catapulte",
                "Empalé sur pieux de défense"
            ],
            survival_time_min=600, survival_time_max=1800,
            elimination_rate=0.48,
            special_mechanics=["Siège médiéval", "Guerre de château"]
        ),
        
        GameEvent(
            id=80, name="Réacteur à fusion", type=EventType.INTELLIGENCE, difficulty=10,
            description="Contrôlez fusion nucléaire avant explosion stellaire",
            decor="Laboratoire de fusion avec réacteur expérimental",
            death_animations=[
                "Désintégration par fusion nucléaire",
                "Vaporisation par plasma solaire",
                "Radiation stellaire mortelle",
                "Mini-supernova, annihilation"
            ],
            survival_time_min=120, survival_time_max=480,
            elimination_rate=0.5,
            special_mechanics=["Fusion nucléaire", "Science extrême"]
        ),
        
        # ================================
        # ÉPREUVE FINALE UNIQUE
        # ================================
        GameEvent(
            id=81, name="Le Jugement Final", type=EventType.INTELLIGENCE, difficulty=10,
            description="Épreuve ultime combinant tous les types de défis",
            decor="Arène multidimensionnelle avec tous les environnements précédents",
            death_animations=[
                "Combinaison de toutes les morts possibles",
                "Désintégration dans vortex dimensionnel",
                "Sacrifice héroïque pour sauver autres",
                "Transcendance mortelle vers autre dimension"
            ],
            survival_time_min=1800, survival_time_max=3600,
            elimination_rate=0.7,  # Exception: Épreuve finale
            special_mechanics=["Tous les défis combinés", "Épreuve ultime"]
        )
    ]
    
    @classmethod
    def get_event_by_id(cls, event_id: int) -> GameEvent:
        """Récupère une épreuve par son ID"""
        for event in cls.GAME_EVENTS:
            if event.id == event_id:
                return event
        raise ValueError(f"Aucune épreuve trouvée avec l'ID {event_id}")
    
    @classmethod
    def get_events_by_type(cls, event_type: EventType) -> List[GameEvent]:
        """Récupère toutes les épreuves d'un type donné"""
        return [event for event in cls.GAME_EVENTS if event.type == event_type]
    
    @classmethod
    def get_events_by_difficulty(cls, min_difficulty: int, max_difficulty: int) -> List[GameEvent]:
        """Récupère les épreuves dans une fourchette de difficulté"""
        return [
            event for event in cls.GAME_EVENTS 
            if min_difficulty <= event.difficulty <= max_difficulty
        ]
    
    @classmethod
    def get_random_death_animation(cls, event: GameEvent) -> str:
        """Retourne une animation de mort aléatoire pour une épreuve"""
        if not event.death_animations:
            return "Élimination standard"
        return random.choice(event.death_animations)
    
    @classmethod
    def get_event_statistics(cls) -> dict:
        """Retourne les statistiques des épreuves"""
        total_events = len(cls.GAME_EVENTS)
        by_type = {}
        by_difficulty = {}
        
        for event in cls.GAME_EVENTS:
            # Par type
            if event.type not in by_type:
                by_type[event.type] = 0
            by_type[event.type] += 1
            
            # Par difficulté
            if event.difficulty not in by_difficulty:
                by_difficulty[event.difficulty] = 0
            by_difficulty[event.difficulty] += 1
        
        return {
            "total_events": total_events,
            "by_type": by_type,
            "by_difficulty": by_difficulty,
            "average_elimination_rate": sum(e.elimination_rate for e in cls.GAME_EVENTS) / total_events
        }
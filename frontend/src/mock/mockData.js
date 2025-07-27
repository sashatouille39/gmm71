// Mock data pour Game Master Manager

// Rôles des joueurs avec probabilités
export const PLAYER_ROLES = {
  normal: { probability: 0.60, name: "Normal", baseStats: "équilibrés", bonus: [] },
  sportif: { probability: 0.11, name: "Sportif", baseStats: "agilité", bonus: ["+2 force"] },
  peureux: { probability: 0.10, name: "Peureux", baseStats: "faibles", bonus: ["-4 répartis"] },
  brute: { probability: 0.11, name: "La Brute", baseStats: "force", bonus: ["+2 agilité", "intimidation"] },
  intelligent: { probability: 0.07, name: "L'Intelligent", baseStats: "intelligence", bonus: ["+2 aléatoire", "manipulation"] },
  zero: { probability: 0.01, name: "Le Zéro", baseStats: "aléatoires 4-10", bonus: ["très manipulateur"] }
};

// Nationalités cohérentes
export const NATIONALITIES = [
  "Coréenne", "Japonaise", "Chinoise", "Américaine", "Française", "Allemande", 
  "Britannique", "Italienne", "Espagnole", "Russe", "Brésilienne", "Indienne",
  "Australienne", "Canadienne", "Mexicaine", "Turque", "Égyptienne", "Nigériane"
];

// Formes de visages (15+)
export const FACE_SHAPES = [
  "Ovale", "Rond", "Carré", "Rectangulaire", "Triangulaire", "Cœur", 
  "Losange", "Oblong", "Poire", "Hexagonal", "Pentagonal", "Allongé",
  "Large", "Étroit", "Angular", "Doux", "Fin", "Robuste", "Délicat"
];

// Formes des yeux
export const EYE_SHAPES = [
  "Amande", "Rond", "Allongé", "Tombant", "Relevé", "Petit", "Grand",
  "Bridé", "Écarté", "Rapproché", "En forme de chat", "Monolide", "Encapuchonné"
];

// Couleurs des yeux
export const EYE_COLORS = [
  "#8B4513", "#654321", "#2F4F2F", "#483D8B", "#556B2F", "#000000",
  "#4169E1", "#006400", "#8B0000", "#2E8B57", "#DAA520", "#9ACD32",
  "#FF8C00", "#DC143C", "#4B0082", "#B22222", "#228B22", "#FF4500"
];

// Couleurs de peau (25+ couleurs du blanc clair au noir foncé)
export const SKIN_COLORS = [
  // Tons très clairs
  "#FDF2E9", "#FAE7D0", "#F8D7C0", "#F6C8A0", "#F4B980", 
  // Tons clairs
  "#E8A456", "#D49156", "#C07D46", "#AC6A36", "#985726", 
  // Tons moyens
  "#844516", "#703306", "#5C2100", "#481000", "#340000", 
  // Tons rosés/beiges
  "#FFEEE6", "#FFE4D6", "#FFDAC6", "#FFD0B6", "#FFC6A6", 
  // Tons dorés
  "#FFBC96", "#FFB286", "#FFA876", "#FF9E66", "#FF9456", 
  // Tons olivâtres
  "#E88A46", "#D18036", "#BA7626", "#A36C16", "#8B5A00",
  // Tons plus foncés
  "#7A4F12", "#6B4423", "#5C3317", "#4D2B1A", "#3E1F0A",
  // Tons très foncés
  "#2F1608", "#251308", "#1B0F05", "#120A03", "#080401"
];

// Coiffures (80+)
export const HAIRSTYLES = [
  // Coupes courtes
  "Cheveux courts", "Pixie", "Buzz cut", "Crew cut", "Undercut", "Fade", 
  "High and tight", "Caesar", "Textured crop", "French crop", "Induction cut",
  "Burr cut", "Butch cut", "Flat top", "High top", "Brush cut",
  
  // Coupes moyennes
  "Bob", "Lob", "Carré plongeant", "Carré court", "Carré long", "Shag",
  "Layered", "Wavy bob", "Asymmetrical bob", "A-line bob", "Inverted bob",
  "Stacked bob", "Graduated bob", "Textured bob", "Blunt bob",
  
  // Coupes longues
  "Cheveux longs", "Cheveux très longs", "Layers", "Beach waves", "Straight long",
  "V-cut", "U-cut", "Feathered", "Side-swept long", "Curtain bangs long",
  "Bohemian long", "Waterfall layers", "Face-framing layers",
  
  // Styles spéciaux
  "Mohawk", "Faux hawk", "Pompadour", "Quiff", "Slicked back", "Comb over",
  "Side part", "Deep side part", "Middle part", "Zigzag part",
  
  // Coiffures attachées
  "Queue de cheval", "Queue haute", "Queue basse", "Queue sur le côté",
  "Chignon", "Chignon bas", "Chignon haut", "Chignon messy", "Top knot", 
  "Man bun", "Space buns", "Double buns", "Half-up half-down",
  
  // Tresses et locks
  "Tresses", "Tresse française", "Tresse hollandaise", "Tresses africaines",
  "Box braids", "Cornrows", "Dreadlocks", "Faux locs", "Twist out",
  "Bantu knots", "Fulani braids", "Dutch braids", "Fishtail braid",
  
  // Textures et styles
  "Afro", "Curly", "Wavy", "Straight", "Spiky", "Messy", "Sleek", "Volume",
  "Textured", "Choppy", "Blunt", "Feathered", "Tousled", "Bedhead",
  
  // Styles avec frange
  "Bangs", "Side swept", "Blunt bangs", "Wispy bangs", "Curtain bangs",
  "Baby bangs", "Long bangs", "Choppy bangs", "Round bangs",
  
  // Styles rétro/vintage
  "Retro", "Vintage", "Pin-up", "Victory rolls", "Beehive", "Bouffant",
  "Finger waves", "Marcel waves", "Gibson tuck", "Pompadour féminin"
];

// Couleurs de cheveux
export const HAIR_COLORS = [
  "#2C1B18", "#3C2414", "#4A2C20", "#5D4037", "#6D4C41", "#8D6E63",
  "#A1887F", "#BCAAA4", "#D7CCC8", "#EFEBE9", "#FFF3E0", "#FFE0B2",
  "#FFCC02", "#FFA000", "#FF8F00", "#FF6F00", "#E65100", "#D84315",
  "#BF360C", "#A0522D", "#8B4513", "#654321", "#800080", "#9932CC",
  "#BA55D3", "#DA70D6", "#EE82EE", "#FF1493", "#FF69B4", "#FFB6C1"
];

// Épreuves du jeu (81 épreuves totales)
export const GAME_EVENTS = [
  // Épreuves classiques Squid Game (5)
  { id: 1, name: "Feu rouge, Feu vert", type: "agilité", difficulty: 3, description: "Avancez quand c'est vert, arrêtez-vous au rouge sinon vous mourrez" },
  { id: 2, name: "Pont de verre", type: "intelligence", difficulty: 8, description: "Traversez le pont en choisissant les bonnes plaques de verre" },
  { id: 3, name: "Billes", type: "intelligence", difficulty: 6, description: "Jeu de stratégie par paires, le perdant meurt" },
  { id: 4, name: "Tir à la corde", type: "force", difficulty: 7, description: "Tirez plus fort que l'équipe adverse ou tombez dans le vide" },
  { id: 5, name: "Gaufres au sucre", type: "agilité", difficulty: 5, description: "Découpez la forme sans la casser en 10 minutes" },
  
  // Épreuves de combat (15)
  { id: 6, name: "Combat de gladiateurs", type: "force", difficulty: 9, description: "Battez-vous à mort dans l'arène avec des armes" },
  { id: 7, name: "Bataille royale", type: "force", difficulty: 10, description: "Dernière personne debout remporte l'épreuve" },
  { id: 8, name: "Ring de boxe mortel", type: "force", difficulty: 8, description: "Boxe jusqu'à la mort, pas de règles" },
  { id: 9, name: "Arène des fauves", type: "force", difficulty: 9, description: "Survivez aux animaux sauvages lâchés dans l'arène" },
  { id: 10, name: "Duel au pistolet", type: "force", difficulty: 7, description: "Duel à l'ancienne, un seul survivant" },
  { id: 11, name: "Combat au couteau", type: "force", difficulty: 8, description: "Mêlée générale aux couteaux dans l'obscurité" },
  { id: 12, name: "Fosse aux serpents", type: "force", difficulty: 6, description: "Traversez la fosse remplie de serpents venimeux" },
  { id: 13, name: "Combat à l'épée", type: "force", difficulty: 8, description: "Escrime mortelle avec épées aiguisées" },
  { id: 14, name: "Cage de la mort", type: "force", difficulty: 9, description: "Combat en cage, mort du perdant obligatoire" },
  { id: 15, name: "Roulette russe géante", type: "force", difficulty: 5, description: "Version géante de la roulette russe avec révolver" },
  { id: 16, name: "Combat de robots", type: "force", difficulty: 8, description: "Combattez des robots de combat programmés pour tuer" },
  { id: 17, name: "Arène aquatique", type: "force", difficulty: 7, description: "Combat dans un bassin avec requins affamés" },
  { id: 18, name: "Combat au lance-flammes", type: "force", difficulty: 9, description: "Éliminez vos adversaires avec des lance-flammes" },
  { id: 19, name: "Bataille de masse", type: "force", difficulty: 10, description: "Guerre totale avec armes médiévales" },
  { id: 20, name: "Prison de combat", type: "force", difficulty: 8, description: "Combat de prisonniers dans les cellules" },
  
  // Épreuves d'agilité (15)
  { id: 21, name: "Course d'obstacles mortels", type: "agilité", difficulty: 7, description: "Parcours d'obstacles avec pièges mortels" },
  { id: 22, name: "Parkour de la mort", type: "agilité", difficulty: 8, description: "Parcours urbain avec pièges et snipers" },
  { id: 23, name: "Labyrinthe tournant", type: "agilité", difficulty: 6, description: "Labyrinthe dont les murs bougent et écrasent" },
  { id: 24, name: "Saut de la mort", type: "agilité", difficulty: 8, description: "Sautez de plateforme en plateforme au-dessus du vide" },
  { id: 25, name: "Tunnel rampant", type: "agilité", difficulty: 5, description: "Ramper dans tunnels avec gaz toxique qui monte" },
  { id: 26, name: "Escalade mortelle", type: "agilité", difficulty: 7, description: "Escaladez la tour pendant qu'elle s'effondre" },
  { id: 27, name: "Course de voitures", type: "agilité", difficulty: 6, description: "Course-poursuite avec voitures piégées" },
  { id: 28, name: "Tyrolienne de l'enfer", type: "agilité", difficulty: 7, description: "Traversez sur tyrolienne avec cordes qui se coupent" },
  { id: 29, name: "Surf sur lave", type: "agilité", difficulty: 9, description: "Surfez sur planches au-dessus de lave en fusion" },
  { id: 30, name: "Slalom explosif", type: "agilité", difficulty: 6, description: "Slalom entre mines antipersonnel" },
  { id: 31, name: "Swing de la jungle", type: "agilité", difficulty: 7, description: "Balancez-vous de liane en liane au-dessus de crocodiles" },
  { id: 32, name: "Fuite dans égouts", type: "agilité", difficulty: 5, description: "Fuyez dans égouts avec eau qui monte" },
  { id: 33, name: "Trampolines mortels", type: "agilité", difficulty: 6, description: "Sautez de trampoline en trampoline avec pièges" },
  { id: 34, name: "Course de drones", type: "agilité", difficulty: 8, description: "Évitez les drones tueurs en courant" },
  { id: 35, name: "Patinage sur glace mortelle", type: "agilité", difficulty: 7, description: "Patinez sur glace qui se brise avec requins dessous" },
  
  // Épreuves d'intelligence (15)
  { id: 36, name: "Énigme du Sphinx mortel", type: "intelligence", difficulty: 8, description: "Résolvez l'énigme ou soyez dévoré par le sphinx mécanique" },
  { id: 37, name: "Laboratoire chimique", type: "intelligence", difficulty: 7, description: "Créez l'antidote ou mourez empoisonné" },
  { id: 38, name: "Salle des miroirs", type: "intelligence", difficulty: 6, description: "Trouvez la sortie dans labyrinthe de miroirs avant le gaz" },
  { id: 39, name: "Puzzle temporel", type: "intelligence", difficulty: 9, description: "Résolvez puzzle 3D avant l'explosion" },
  { id: 40, name: "Bataille navale géante", type: "intelligence", difficulty: 6, description: "Bataille navale avec vraies explosions sur plateau géant" },
  { id: 41, name: "Codes secrets", type: "intelligence", difficulty: 8, description: "Cassez les codes avant que les lasers vous découpent" },
  { id: 42, name: "Échecs de la mort", type: "intelligence", difficulty: 7, description: "Échecs géants, les pièces tuées meurent vraiment" },
  { id: 43, name: "Désamorçage de bombe", type: "intelligence", difficulty: 9, description: "Désamorcez bombe complexe ou mourez dans l'explosion" },
  { id: 44, name: "Sudoku mortel", type: "intelligence", difficulty: 6, description: "Résolvez sudoku géant ou soyez électrocuté" },
  { id: 45, name: "Interrogatoire psychologique", type: "intelligence", difficulty: 5, description: "Répondez aux questions psychologiques ou soyez éliminé" },
  { id: 46, name: "Calculs de survie", type: "intelligence", difficulty: 8, description: "Calculez trajectoire d'évasion avant impact de missiles" },
  { id: 47, name: "Mémoire photographique", type: "intelligence", difficulty: 6, description: "Mémorisez séquence complexe ou soyez gazé" },
  { id: 48, name: "Logique quantique", type: "intelligence", difficulty: 10, description: "Résolvez équations quantiques ou soyez désintégré" },
  { id: 49, name: "Stratégie militaire", type: "intelligence", difficulty: 8, description: "Dirigez bataille tactique ou mourez avec vos troupes" },
  { id: 50, name: "Diagnostic médical", type: "intelligence", difficulty: 7, description: "Diagnostiquez maladie mortelle ou mourez du même mal" },
  
  // Épreuves mixtes et spéciales (31)
  { id: 51, name: "Jeu de la confiance", type: "intelligence", difficulty: 5, description: "Faites confiance ou trahissez, mais choisissez bien" },
  { id: 52, name: "Test de loyauté", type: "intelligence", difficulty: 4, description: "Prouvez votre loyauté en sacrifiant un autre" },
  { id: 53, name: "Roulette de torture", type: "force", difficulty: 6, description: "Roulette qui détermine votre méthode de torture" },
  { id: 54, name: "Chambre des horreurs", type: "agilité", difficulty: 7, description: "Traversez chambre remplie de pièges sadiques" },
  { id: 55, name: "Labyrinthe de glace", type: "intelligence", difficulty: 6, description: "Trouvez sortie avant hypothermie mortelle" },
  { id: 56, name: "Salle de pression", type: "force", difficulty: 8, description: "Résistez à pression extrême ou soyez écrasé" },
  { id: 57, name: "Danse macabre", type: "agilité", difficulty: 5, description: "Dansez parfaitement ou soyez exécuté" },
  { id: 58, name: "Aquarium de la mort", type: "agilité", difficulty: 7, description: "Nagez parmi créatures marines mortelles" },
  { id: 59, name: "Forêt empoisonnée", type: "intelligence", difficulty: 6, description: "Traversez forêt sans toucher plantes toxiques" },
  { id: 60, name: "Mine abandonnée", type: "agilité", difficulty: 7, description: "Échappez-vous de mine qui s'effondre" },
  { id: 61, name: "Casino russe", type: "intelligence", difficulty: 5, description: "Jeux de casino mortels avec vraies conséquences" },
  { id: 62, name: "Usine chimique", type: "agilité", difficulty: 8, description: "Fuyez usine en explosion avec produits toxiques" },
  { id: 63, name: "Bibliothèque maudite", type: "intelligence", difficulty: 6, description: "Trouvez livre de vie avant que livres vous tuent" },
  { id: 64, name: "Cirque de l'horreur", type: "agilité", difficulty: 7, description: "Spectacle de cirque où vous êtes la performance" },
  { id: 65, name: "Hôpital psychiatrique", type: "intelligence", difficulty: 8, description: "Échappez-vous avant de devenir fou et d'être lobotomisé" },
  { id: 66, name: "Vaisseau spatial", type: "intelligence", difficulty: 9, description: "Réparez vaisseau avant qu'il s'écrase sur planète" },
  { id: 67, name: "Cimetière hanté", type: "force", difficulty: 6, description: "Survivez aux morts-vivants qui sortent des tombes" },
  { id: 68, name: "Bunker nucléaire", type: "intelligence", difficulty: 8, description: "Désactivez réacteur avant explosion nucléaire" },
  { id: 69, name: "Parc d'attractions", type: "agilité", difficulty: 6, description: "Survivez aux attractions mortelles du parc maudit" },
  { id: 70, name: "Sous-marin", type: "intelligence", difficulty: 8, description: "Réparez sous-marin qui coule avant noyade" },
  { id: 71, name: "Désert de sable", type: "force", difficulty: 7, description: "Traversez désert avec tempête de sable et vers géants" },
  { id: 72, name: "Prison flottante", type: "agilité", difficulty: 7, description: "Échappez-vous de prison sur plateforme pétrolière" },
  { id: 73, name: "Laboratoire génétique", type: "intelligence", difficulty: 9, description: "Survivez aux mutations génétiques expérimentales" },
  { id: 74, name: "Glacier mortel", type: "agilité", difficulty: 8, description: "Escaladez glacier avant avalanche mortelle" },
  { id: 75, name: "Usine robotique", type: "intelligence", difficulty: 8, description: "Programmez robots ou soyez éliminé par eux" },
  { id: 76, name: "Volcan actif", type: "force", difficulty: 9, description: "Échappez-vous du volcan en éruption" },
  { id: 77, name: "Station spatiale", type: "intelligence", difficulty: 9, description: "Réparez station avant qu'elle tombe sur Terre" },
  { id: 78, name: "Jungle amazonienne", type: "agilité", difficulty: 7, description: "Survivez dans jungle avec prédateurs et tribus" },
  { id: 79, name: "Château fort", type: "force", difficulty: 8, description: "Assiégez château défendu par archers et soldats" },
  { id: 80, name: "Réacteur à fusion", type: "intelligence", difficulty: 10, description: "Contrôlez fusion nucléaire avant explosion stellaire" },
  { id: 81, name: "Le Jugement Final", type: "intelligence", difficulty: 10, description: "Épreuve ultime combinant tous les types de défis" }
];

// VIP avec personnalités
export const VIP_CHARACTERS = [
  {
    id: 1,
    name: "Le Cochon Sale",
    mask: "cochon-sale",
    personality: "absurde",
    dialogues: [
      "Ah ! Comme dirait mon grand-père... euh... il est mort !",
      "Cette épreuve me rappelle quand j'ai mangé un sandwich... au thon !",
      "MAGNIFIQUE ! Comme la fois où j'ai perdu mes clés dans un aquarium !",
      "Ho ho ho ! Exactement comme dans Titanic... ou était-ce Bambi ?",
      "Mes chers amis, ceci me rappelle ma première pizza... elle était carrée !"
    ],
    bets: 0,
    favoritePlayer: null
  },
  {
    id: 2,
    name: "Le Porc Propre", 
    mask: "cochon-propre",
    personality: "raffiné",
    dialogues: [
      "Quelle élégance dans cette brutalité, très cher !",
      "L'art de mourir avec classe, tout à fait remarquable.",
      "Ces jeux me rappellent les soirées à l'opéra... en plus sanglant.",
      "Magnifique chorégraphie de la mort, mes compliments !",
      "Un spectacle digne des plus grands maîtres !"
    ],
    bets: 0,
    favoritePlayer: null
  },
  {
    id: 3,
    name: "Le Triangle",
    mask: "triangle",
    personality: "calculateur",
    dialogues: [
      "Les probabilités de survie sont... intéressantes.",
      "Analyse statistique : 73.4% de chances d'élimination.",
      "Variables imprévues détectées dans le comportement.",
      "Calculs recalculés. Nouveau pronostic en cours.",
      "Données insuffisantes. Observation requise."
    ],
    bets: 0,
    favoritePlayer: null
  }
];

// Célébrités fictives
export const MOCK_CELEBRITIES = [
  // Célébrités 5 étoiles (Anciens vainqueurs)
  {
    id: 1,
    name: "Viktor Kozlov",
    category: "Ancien vainqueur",
    stars: 5,
    price: 50000,
    nationality: "Russe",
    wins: 3,
    stats: { intelligence: 9, force: 8, agilité: 10 },
    biography: "Triple vainqueur légendaire, maître de tous les jeux."
  },
  {
    id: 2,
    name: "Luna Hartwell",
    category: "Ancienne vainqueur",
    stars: 5,
    price: 45000,
    nationality: "Britannique",
    wins: 2,
    stats: { intelligence: 10, force: 6, agilité: 9 },
    biography: "Stratège exceptionnelle, gagnante de deux éditions consécutives."
  },
  
  // Célébrités 4 étoiles
  {
    id: 3,
    name: "Marco Rossini",
    category: "Sportif",
    stars: 4,
    price: 25000,
    nationality: "Italienne",
    stats: { intelligence: 6, force: 9, agilité: 10 },
    biography: "Champion olympique de décathlon."
  },
  {
    id: 4,
    name: "Dr. Sarah Chen",
    category: "Scientifique",
    stars: 4,
    price: 22000,
    nationality: "Chinoise",
    stats: { intelligence: 10, force: 4, agilité: 6 },
    biography: "Prix Nobel de physique, génie reconnu mondialement."
  },
  
  // Célébrités 3 étoiles
  {
    id: 5,
    name: "Jake Morrison",
    category: "Acteur",
    stars: 3,
    price: 15000,
    nationality: "Américaine",
    stats: { intelligence: 7, force: 6, agilité: 7 },
    biography: "Star de cinéma action, cascadeur expérimenté."
  },
  {
    id: 6,
    name: "Isabella Santos",
    category: "Chanteuse",
    stars: 3,
    price: 12000,
    nationality: "Brésilienne",
    stats: { intelligence: 8, force: 5, agilité: 8 },
    biography: "Diva internationale, voix d'or du Brésil."
  },
  
  // Célébrités 2 étoiles
  {
    id: 7,
    name: "Tommy Fletcher",
    category: "Influenceur",
    stars: 2,
    price: 8000,
    nationality: "Australienne",
    stats: { intelligence: 6, force: 5, agilité: 6 },
    biography: "Influenceur populaire, 50M de followers."
  },
  {
    id: 8,
    name: "Marie Dubois",
    category: "Chef",
    stars: 2,
    price: 6000,
    nationality: "Française",
    stats: { intelligence: 7, force: 4, agilité: 5 },
    biography: "Chef étoilée, reine de la gastronomie française."
  }
];

// Uniformes et personnalisation
export const UNIFORM_STYLES = ["Classic", "Moderne", "Vintage", "Sport", "Élégant"];
export const UNIFORM_PATTERNS = ["Uni", "Rayures", "Carreaux", "Points", "Floral", "Géométrique"];
export const UNIFORM_COLORS = ["Rouge", "Bleu", "Vert", "Jaune", "Rose", "Violet", "Orange", "Noir", "Blanc"];

// Générateur de joueurs aléatoires
export const generateRandomPlayer = (id) => {
  // Sélection du rôle selon les probabilités
  const rand = Math.random();
  let cumulativeProbability = 0;
  let selectedRole = 'normal';
  
  for (const [role, data] of Object.entries(PLAYER_ROLES)) {
    cumulativeProbability += data.probability;
    if (rand <= cumulativeProbability) {
      selectedRole = role;
      break;
    }
  }
  
  const roleData = PLAYER_ROLES[selectedRole];
  const nationality = NATIONALITIES[Math.floor(Math.random() * NATIONALITIES.length)];
  const gender = Math.random() > 0.5 ? 'M' : 'F';
  
  // Génération des stats selon le rôle
  let stats = { intelligence: 0, force: 0, agilité: 0 };
  let totalPoints = 12;
  
  // Distribution selon le rôle
  switch (selectedRole) {
    case 'sportif':
      stats.agilité = Math.min(10, 4 + Math.floor(Math.random() * 4));
      stats.force = Math.min(10, stats.agilité - 2 + Math.floor(Math.random() * 3));
      stats.intelligence = Math.max(0, totalPoints - stats.agilité - stats.force);
      break;
    case 'brute':
      stats.force = Math.min(10, 4 + Math.floor(Math.random() * 4));
      stats.agilité = Math.min(10, stats.force - 2 + Math.floor(Math.random() * 3));
      stats.intelligence = Math.max(0, totalPoints - stats.force - stats.agilité);
      break;
    case 'intelligent':
      stats.intelligence = Math.min(10, 4 + Math.floor(Math.random() * 4));
      const bonus = Math.floor(Math.random() * 3);
      if (bonus === 0) stats.force += 2;
      else if (bonus === 1) stats.agilité += 2;
      else stats.intelligence += 2;
      totalPoints = 14; // +2 bonus
      break;
    case 'peureux':
      totalPoints = 8; // -4 malus
      break;
    case 'zero':
      stats.intelligence = 4 + Math.floor(Math.random() * 7);
      stats.force = 4 + Math.floor(Math.random() * 7);
      stats.agilité = 4 + Math.floor(Math.random() * 7);
      break;
    default: // normal
      break;
  }
  
  // Distribution équilibrée pour les normaux et ajustements
  if (selectedRole === 'normal' || selectedRole === 'peureux') {
    const remaining = totalPoints;
    stats.intelligence = Math.floor(Math.random() * (remaining / 3)) + 1;
    stats.force = Math.floor(Math.random() * ((remaining - stats.intelligence) / 2)) + 1;
    stats.agilité = Math.max(0, remaining - stats.intelligence - stats.force);
  }
  
  return {
    id,
    number: String(id).padStart(3, '0'),
    name: generateRandomName(nationality, gender),
    nationality,
    gender,
    role: selectedRole,
    stats,
    portrait: generatePortraitData(nationality),
    uniform: {
      style: UNIFORM_STYLES[Math.floor(Math.random() * UNIFORM_STYLES.length)],
      color: UNIFORM_COLORS[Math.floor(Math.random() * UNIFORM_COLORS.length)],
      pattern: UNIFORM_PATTERNS[Math.floor(Math.random() * UNIFORM_PATTERNS.length)]
    },
    alive: true,
    kills: 0,
    betrayals: 0,
    survivedEvents: 0,
    totalScore: 0
  };
};

const generateRandomName = (nationality, gender) => {
  const names = {
    'Coréenne': {
      M: ['Min-jun', 'Seo-jun', 'Do-yoon', 'Si-woo', 'Joon-ho'],
      F: ['Seo-yeon', 'Min-seo', 'Ji-woo', 'Ha-eun', 'Soo-jin']
    },
    'Japonaise': {
      M: ['Hiroshi', 'Takeshi', 'Akira', 'Yuki', 'Daiki'],
      F: ['Sakura', 'Yuki', 'Ai', 'Rei', 'Mana']
    },
    'Française': {
      M: ['Pierre', 'Jean', 'Michel', 'Alain', 'Philippe'],
      F: ['Marie', 'Nathalie', 'Isabelle', 'Sylvie', 'Catherine']
    },
    // Ajouter plus de noms par nationalité...
  };
  
  const nationalityNames = names[nationality] || names['Française'];
  const genderNames = nationalityNames[gender];
  return genderNames[Math.floor(Math.random() * genderNames.length)];
};

const generatePortraitData = (nationality) => {
  // Génération cohérente selon la nationalité
  const skinColorIndex = getSkinColorByNationality(nationality);
  
  return {
    faceShape: FACE_SHAPES[Math.floor(Math.random() * FACE_SHAPES.length)],
    skinColor: SKIN_COLORS[skinColorIndex],
    hairstyle: HAIRSTYLES[Math.floor(Math.random() * HAIRSTYLES.length)],
    hairColor: HAIR_COLORS[Math.floor(Math.random() * HAIR_COLORS.length)],
    eyeColor: generateEyeColor(),
    eyeShape: generateEyeShape()
  };
};

const getSkinColorByNationality = (nationality) => {
  const ranges = {
    'Coréenne': [0, 8],
    'Japonaise': [0, 8],
    'Chinoise': [2, 10],
    'Européenne': [0, 5],
    'Africaine': [15, 24],
    'Indienne': [8, 18],
    // etc...
  };
  
  const range = ranges[nationality] || [0, 15];
  return range[0] + Math.floor(Math.random() * (range[1] - range[0]));
};

const generateEyeColor = () => {
  const colors = ['#8B4513', '#654321', '#2F4F2F', '#483D8B', '#556B2F', '#000000'];
  return colors[Math.floor(Math.random() * colors.length)];
};

const generateEyeShape = () => {
  const shapes = ['Amande', 'Rond', 'Allongé', 'Tombant', 'Relevé', 'Petit', 'Grand'];
  return shapes[Math.floor(Math.random() * shapes.length)];
};

// État initial du jeu
export const INITIAL_GAME_STATE = {
  money: 50000,
  vipSalonLevel: 1,
  unlockedUniforms: [],
  unlockedPatterns: [],
  gameStats: {
    totalGamesPlayed: 0,
    totalKills: 0,
    totalBetrayals: 0,
    favoriteCelebrity: null
  }
};
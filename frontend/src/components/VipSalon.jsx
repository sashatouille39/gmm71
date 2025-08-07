import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Progress } from './ui/progress';
import { 
  ArrowLeft, 
  Crown, 
  Users, 
  Star, 
  ShoppingCart,
  Trophy,
  DollarSign,
  Skull,
  Zap,
  MessageCircle,
  TrendingUp,
  RefreshCw
} from 'lucide-react';
// Retrait des mocks: les célébrités sont désormais chargées depuis le backend
import { vipService } from '../services/vipService';

// Fonction pour obtenir l'emoji correspondant au masque animal
const getAnimalEmoji = (mask) => {
  const emojiMap = {
    'loup': '🐺', 'renard': '🦊', 'ours': '🐻', 'chat': '🐱', 'elephant': '🐘',
    'lion': '🦁', 'tigre': '🐅', 'singe': '🐵', 'aigle': '🦅', 'corbeau': '🐦‍⬛',
    'chouette': '🦉', 'vautour': '🦅', 'paon': '🦚', 'flamant': '🦩', 'serpent': '🐍',
    'crocodile': '🐊', 'iguane': '🦎', 'tortue': '🐢', 'mante': '🦗', 'scorpion': '🦂',
    'araignee': '🕷️', 'scarabee': '🪲', 'libellule': '🦋', 'papillon': '🦋', 'requin': '🦈',
    'pieuvre': '🐙', 'homard': '🦞', 'hippocampe': '🦄', 'dragon': '🐉', 'phenix': '🔥',
    'chauve-souris': '🦇', 'pangolin': '🦔', 'cameleon': '🦎', 'pingouin': '🐧', 'ours-polaire': '🐻‍❄️',
    'narval': '🦄', 'toucan': '🦜', 'jaguar': '🐆', 'capibara': '🐹', 'raie-manta': '🐠',
    'poisson-lune': '🐟', 'anguille': '🐍', 'trilobite': '🦀', 'ammonite': '🐚',
    'kraken': '🐙', 'licorne': '🦄', 'griffon': '🦅', 'sphinx': '🐱'
  };
  return emojiMap[mask] || '🎭';
};

// Fonction pour obtenir la couleur selon la personnalité
const getPersonalityColor = (personality) => {
  const colorMap = {
    'dominateur': 'text-red-400 border-red-400',
    'manipulateur': 'text-purple-400 border-purple-400',
    'violent': 'text-red-600 border-red-600',
    'énigmatique': 'text-indigo-400 border-indigo-400',
    'philosophe': 'text-blue-400 border-blue-400',
    'royal': 'text-yellow-400 border-yellow-400',
    'chasseur': 'text-orange-400 border-orange-400',
    'fou': 'text-pink-400 border-pink-400',
    'observateur': 'text-cyan-400 border-cyan-400',
    'oracle': 'text-purple-600 border-purple-600',
    'mystique': 'text-indigo-600 border-indigo-600',
    'nécrophage': 'text-gray-400 border-gray-400',
    'narcissique': 'text-pink-600 border-pink-600',
    'excentrique': 'text-magenta-400 border-magenta-400',
    'traître': 'text-green-600 border-green-600',
    'primitif': 'text-brown-400 border-brown-400',
    'méditatif': 'text-green-400 border-green-400',
    'sage': 'text-blue-600 border-blue-600',
    'predateur': 'text-red-500 border-red-500',
    'vengeur': 'text-orange-600 border-orange-600',
    'envoûteur': 'text-violet-400 border-violet-400',
    'mélancolique': 'text-gray-500 border-gray-500',
    'brutal': 'text-red-700 border-red-700',
    'impérial': 'text-gold-400 border-gold-400',
    'cyclique': 'text-teal-400 border-teal-400',
    'vampirique': 'text-red-800 border-red-800',
    'défensif': 'text-gray-600 border-gray-600',
    'snob': 'text-blue-300 border-blue-300',
    'survivant': 'text-white border-white',
    'licorne': 'text-rainbow border-rainbow',
    'gracieux': 'text-cyan-300 border-cyan-300',
    'bizarre': 'text-lime-400 border-lime-400',
    'énergique': 'text-yellow-500 border-yellow-500',
    'ancien': 'text-brown-600 border-brown-600',
    'léviathan': 'text-blue-800 border-blue-800',
    'corrompu': 'text-black border-black',
    'devinettes': 'text-amber-400 border-amber-400'
  };
  return colorMap[personality] || 'text-gray-400 border-gray-400';
};

const VipSalon = ({ gameState, updateGameState }) => {
  const navigate = useNavigate();
  const [selectedTab, setSelectedTab] = useState('salon');
  const [selectedCelebrity, setSelectedCelebrity] = useState(null);
  const [currentVips, setCurrentVips] = useState([]);
  const [loadingVips, setLoadingVips] = useState(false);
  const [allVips, setAllVips] = useState([]);
  const [pastWinners, setPastWinners] = useState([]);
  const [loadingWinners, setLoadingWinners] = useState(false);
  const [purchasingCelebrity, setPurchasingCelebrity] = useState(null);
  const [shopCelebrities, setShopCelebrities] = useState([]);
  const [loadingCelebs, setLoadingCelebs] = useState(false);

  // Charger les VIPs, célébrités et les gagnants lors du montage du composant
  useEffect(() => {
    loadSalonVips();
    loadAllVips();
    loadPastWinners();
    loadShopCelebrities();
  }, [gameState.vipSalonLevel]);

  const loadPastWinners = async () => {
    try {
      setLoadingWinners(true);
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/statistics/winners`);
      if (response.ok) {
        const winners = await response.json();
        setPastWinners(winners);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des gagnants:', error);
    } finally {
      setLoadingWinners(false);
    }
  };

  const loadShopCelebrities = async () => {
    try {
      setLoadingCelebs(true);
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/celebrities/?limit=60`);
      if (response.ok) {
        const celebs = await response.json();
        setShopCelebrities(celebs);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des célébrités:', error);
    } finally {
      setLoadingCelebs(false);
    }
  };

  const loadSalonVips = async () => {
    try {
      setLoadingVips(true);
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/vips/salon/${gameState.vipSalonLevel}`);
      if (response.ok) {
        const vips = await response.json();
        setCurrentVips(vips);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des VIPs:', error);
    } finally {
      setLoadingVips(false);
    }
  };

  const loadAllVips = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/vips/all`);
      if (response.ok) {
        const vips = await response.json();
        setAllVips(vips);
      }
    } catch (error) {
      console.error('Erreur lors du chargement de tous les VIPs:', error);
    }
  };

  const ownedCelebrities = gameState.ownedCelebrities || [];

  // Niveaux de salon disponibles avec les détails
  const salonUpgrades = [
    { 
      level: 1, 
      name: 'Salon Standard', 
      capacity: 3, 
      cost: 0, 
      description: 'Salon de base, 3 places VIP',
      unlocked: true 
    },
    { 
      level: 2, 
      name: 'Salon Premium', 
      capacity: 5, 
      cost: 500000, // 500k
      description: 'Plus de places VIP, 5 places',
      unlocked: gameState.money >= 500000 && gameState.vipSalonLevel >= 1 
    },
    { 
      level: 3, 
      name: 'Salon Royal', 
      capacity: 8, 
      cost: 2000000, // 2M
      description: 'Salon royal, 8 places VIP',
      unlocked: gameState.money >= 2000000 && gameState.vipSalonLevel >= 2 
    },
    { 
      level: 4, 
      name: 'Salon Impérial', 
      capacity: 10, 
      cost: 5000000, // 5M
      description: 'Prestige impérial, 10 places VIP',
      unlocked: gameState.money >= 5000000 && gameState.vipSalonLevel >= 3 
    },
    { 
      level: 5, 
      name: 'Salon Divin', 
      capacity: 12, 
      cost: 10000000, // 10M
      description: 'Salon divin ultime, 12 places VIP',
      unlocked: gameState.money >= 10000000 && gameState.vipSalonLevel >= 4 
    },
    { 
      level: 6, 
      name: 'Salon Mythique', 
      capacity: 15, 
      cost: 20000000, // 20M
      description: 'Prestige mythique, 15 places VIP',
      unlocked: gameState.money >= 20000000 && gameState.vipSalonLevel >= 5 
    },
    { 
      level: 7, 
      name: 'Salon Cosmique', 
      capacity: 17, 
      cost: 40000000, // 40M
      description: 'Influence cosmique, 17 places VIP',
      unlocked: gameState.money >= 40000000 && gameState.vipSalonLevel >= 6 
    },
    { 
      level: 8, 
      name: 'Salon Transcendant', 
      capacity: 18, 
      cost: 75000000, // 75M
      description: 'Pouvoir transcendant, 18 places VIP',
      unlocked: gameState.money >= 75000000 && gameState.vipSalonLevel >= 7 
    },
    { 
      level: 9, 
      name: 'Salon Légendaire', 
      capacity: 20, 
      cost: 100000000, // 100M
      description: 'Prestige maximum légendaire, 20 places VIP',
      unlocked: gameState.money >= 100000000 && gameState.vipSalonLevel >= 8 
    }
  ];

  const purchaseCelebrity = async (celebrity) => {
    if (gameState.money >= celebrity.price && !purchasingCelebrity) {
      try {
        setPurchasingCelebrity(celebrity.id);
        const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
        
        // Utiliser l'API gamestate/purchase pour gérer l'argent + possession atomiquement
        const response = await fetch(`${backendUrl}/api/gamestate/purchase`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            item_type: 'celebrity',
            item_id: celebrity.id,
            price: celebrity.price
          })
        });

        if (response.ok) {
          const updatedState = await response.json();
          // Adapter le format backend -> frontend
          updateGameState({
            money: updatedState.money,
            ownedCelebrities: updatedState.owned_celebrities || []
          });
          console.log(`Célébrité ${celebrity.name} achetée avec succès !`);
        } else {
          console.error('Erreur lors de l\'achat de la célébrité');
        }
      } catch (error) {
        console.error('Erreur de connexion lors de l\'achat:', error);
      } finally {
        setPurchasingCelebrity(null);
      }
    }
  };

  const upgradeSalon = (level) => {
    const upgrade = salonUpgrades.find(s => s.level === level);
    if (upgrade && gameState.money >= upgrade.cost) {
      updateGameState({
        money: gameState.money - upgrade.cost,
        vipSalonLevel: level
      });
    }
  };

  const currentSalon = salonUpgrades.find(s => s.level === gameState.vipSalonLevel);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-4">
            <Button
              onClick={() => navigate('/')}
              variant="ghost"
              className="text-gray-400 hover:text-white"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Retour au menu
            </Button>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-yellow-400 to-red-500 bg-clip-text text-transparent">
                Salon VIP
              </h1>
              <p className="text-gray-400">Gérez vos VIP et achetez des célébrités</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-green-400">
              ${gameState.money.toLocaleString()}
            </div>
            <div className="text-gray-400 text-sm">
              Salon niveau {gameState.vipSalonLevel}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <Tabs value={selectedTab} onValueChange={setSelectedTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 bg-gray-800/50">
            <TabsTrigger value="salon" className="text-white data-[state=active]:bg-purple-600">
              <Crown className="w-4 h-4 mr-2" />
              Salon VIP
            </TabsTrigger>
            <TabsTrigger value="celebrities" className="text-white data-[state=active]:bg-red-600">
              <Star className="w-4 h-4 mr-2" />
              Boutique célébrités
            </TabsTrigger>
            <TabsTrigger value="museum" className="text-white data-[state=active]:bg-gray-600">
              <Skull className="w-4 h-4 mr-2" />
              Musée des morts
            </TabsTrigger>
          </TabsList>

          {/* Salon VIP */}
          <TabsContent value="salon" className="space-y-6">
            {/* Status actuel */}
            <Card className="bg-black/50 border-purple-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Crown className="w-5 h-5" />
                    {currentSalon?.name}
                  </div>
                  <Badge variant="outline" className="text-purple-400 border-purple-400">
                    Niveau {gameState.vipSalonLevel}
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-400">{currentVips.length}</div>
                    <div className="text-gray-400">VIPs présents</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-400">{currentSalon?.capacity || 0}</div>
                    <div className="text-gray-400">Capacité maximale</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-400">
                      ${currentVips.reduce((sum, vip) => sum + vip.viewing_fee, 0).toLocaleString()}
                    </div>
                    <div className="text-gray-400">Revenus potentiels</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* VIPs actuels */}
            <Card className="bg-black/50 border-purple-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  VIPs du salon actuel
                </CardTitle>
              </CardHeader>
              <CardContent>
                {loadingVips ? (
                  <div className="text-center py-8 text-gray-400">
                    <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p>Chargement des VIPs...</p>
                  </div>
                ) : currentVips.length === 0 ? (
                  <div className="text-center py-8 text-gray-400">
                    <Crown className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <p>Aucun VIP dans le salon</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {currentVips.map((vip) => (
                      <div
                        key={vip.id}
                        className={`p-4 rounded-lg border transition-all bg-gray-800/50 border-gray-600 ${getPersonalityColor(vip.personality)}`}
                      >
                        <div className="flex items-center gap-3 mb-3">
                          <div className="text-2xl">{getAnimalEmoji(vip.mask)}</div>
                          <div className="flex-1">
                            <h3 className="text-white font-medium">{vip.name}</h3>
                            <p className="text-gray-400 text-sm capitalize">{vip.personality}</p>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Frais de visionnage:</span>
                            <span className="text-green-400">${vip.viewing_fee.toLocaleString()}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Paris totaux:</span>
                            <span className="text-yellow-400">${vip.bets.toLocaleString()}</span>
                          </div>
                        </div>

                        {vip.favorite_player && (
                          <div className="mt-2 text-xs text-purple-400">
                            Favorise: {vip.favorite_player}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Améliorations du salon */}
            <Card className="bg-black/50 border-purple-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  Améliorations du salon
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {salonUpgrades.map((upgrade) => (
                    <div
                      key={upgrade.level}
                      className={`p-4 rounded-lg border transition-all ${
                        upgrade.level === gameState.vipSalonLevel
                          ? 'bg-purple-600/20 border-purple-500'
                          : upgrade.unlocked
                          ? 'bg-gray-800/50 border-gray-600 hover:bg-gray-700/50'
                          : 'bg-gray-900/50 border-gray-700 opacity-50'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-3">
                        <h3 className={`font-medium ${
                          upgrade.level === gameState.vipSalonLevel ? 'text-purple-400' : 'text-white'
                        }`}>
                          {upgrade.name}
                        </h3>
                        {upgrade.level === gameState.vipSalonLevel && (
                          <Badge className="bg-purple-600 text-white text-xs">ACTUEL</Badge>
                        )}
                      </div>

                      <p className="text-gray-400 text-sm mb-3">{upgrade.description}</p>

                      <div className="space-y-2 mb-4">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">Capacité:</span>
                          <span className="text-white">{upgrade.capacity} VIPs</span>
                        </div>
                        {upgrade.cost > 0 && (
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Coût:</span>
                            <span className="text-yellow-400">${upgrade.cost.toLocaleString()}</span>
                          </div>
                        )}
                      </div>

                      {upgrade.level > gameState.vipSalonLevel && (
                        <Button
                          onClick={() => upgradeSalon(upgrade.level)}
                          disabled={!upgrade.unlocked || gameState.money < upgrade.cost}
                          className={`w-full text-xs ${
                            upgrade.unlocked && gameState.money >= upgrade.cost
                              ? 'bg-purple-600 hover:bg-purple-700'
                              : 'bg-gray-600 cursor-not-allowed'
                          }`}
                        >
                          {upgrade.unlocked ? 'Améliorer' : 'Verrouillé'}
                        </Button>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Boutique de célébrités */}
          <TabsContent value="celebrities" className="space-y-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white">Boutique de célébrités</h2>
              <div className="flex gap-2">
                <Badge variant="outline" className="text-blue-400 border-blue-400">
                  {ownedCelebrities.length} possédées
                </Badge>
                <Badge variant="outline" className="text-gray-400">
                  {/* Calculer le total : célébrités normales + vrais gagnants */}
                  {shopCelebrities.filter(c => c.category !== "Ancien vainqueur" && c.category !== "Ancienne vainqueur").length + pastWinners.length} disponibles
                </Badge>
                {pastWinners.length > 0 && (
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    {pastWinners.length} anciens gagnants
                  </Badge>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Afficher les célébrités normales (filtrer les faux anciens gagnants) */}
              {shopCelebrities
                .filter(celebrity => celebrity.category !== "Ancien vainqueur" && celebrity.category !== "Ancienne vainqueur")
                .map((celebrity) => {
                  const isOwned = gameState.ownedCelebrities?.includes(celebrity.id);
                  const isPurchasing = purchasingCelebrity === celebrity.id;
                  
                  return (
                    <Card 
                      key={celebrity.id} 
                      className={`transition-all cursor-pointer ${
                        isOwned 
                          ? 'bg-green-900/20 border-green-500/30' 
                          : 'bg-gray-800/50 border-gray-600/30 hover:bg-gray-700/50'
                      }`}
                      onClick={() => setSelectedCelebrity(celebrity)}
                    >
                      <CardContent className="p-6">
                        <div className="text-center mb-4">
                          <div className="w-16 h-16 bg-gray-600 rounded-full mx-auto mb-3 flex items-center justify-center">
                            <Star className="w-8 h-8 text-yellow-400" />
                          </div>
                          <h3 className="text-white font-bold">{celebrity.name}</h3>
                          <p className="text-gray-400 text-sm">{celebrity.category}</p>
                        </div>

                        <div className="space-y-2 mb-4">
                          {/* Étoiles */}
                          <div className="flex justify-center">
                            {[...Array(5)].map((_, i) => (
                              <Star 
                                key={i} 
                                className={`w-4 h-4 ${
                                  i < celebrity.stars ? 'text-yellow-400 fill-current' : 'text-gray-600'
                                }`} 
                              />
                            ))}
                          </div>

                          {/* Stats */}
                          <div className="text-xs space-y-1">
                            <div className="flex justify-between">
                              <span className="text-gray-400">Intel:</span>
                              <span className="text-white">{celebrity.stats.intelligence}/10</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-400">Force:</span>
                              <span className="text-white">{celebrity.stats.force}/10</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-400">Agilité:</span>
                              <span className="text-white">{celebrity.stats.agilité}/10</span>
                            </div>
                          </div>

                          {celebrity.wins && (
                            <div className="flex justify-center">
                              <Badge variant="outline" className="text-purple-400 border-purple-400 text-xs">
                                {celebrity.wins} victoires
                              </Badge>
                            </div>
                          )}
                        </div>

                        <div className="text-center">
                          {isOwned ? (
                            <Badge variant="outline" className="text-green-400 border-green-400">
                              Possédée
                            </Badge>
                          ) : (
                            <div className="space-y-2">
                              <div className="text-yellow-400 font-bold">
                                ${celebrity.price.toLocaleString()}
                              </div>
                              <Button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  purchaseCelebrity(celebrity);
                                }}
                                disabled={gameState.money < celebrity.price || isPurchasing}
                                className={`w-full text-xs ${
                                  gameState.money >= celebrity.price && !isPurchasing
                                    ? 'bg-red-600 hover:bg-red-700'
                                    : 'bg-gray-600 cursor-not-allowed'
                                }`}
                              >
                                {isPurchasing ? (
                                  <RefreshCw className="w-3 h-3 mr-1 animate-spin" />
                                ) : (
                                  <ShoppingCart className="w-3 h-3 mr-1" />
                                )}
                                {isPurchasing ? 'Achat...' : 'Acheter'}
                              </Button>
                            </div>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}

              {/* Afficher les vrais anciens gagnants */}
              {pastWinners.map((winner) => {
                const isOwned = gameState.ownedCelebrities?.includes(winner.id);
                const isPurchasing = purchasingCelebrity === winner.id;
                
                return (
                  <Card 
                    key={winner.id} 
                    className={`transition-all cursor-pointer border-2 ${
                      isOwned 
                        ? 'bg-green-900/20 border-green-500/30' 
                        : 'bg-gradient-to-br from-yellow-900/30 to-red-900/30 border-yellow-400/50 hover:border-yellow-400/70'
                    }`}
                    onClick={() => setSelectedCelebrity(winner)}
                  >
                    <CardContent className="p-6">
                      <div className="text-center mb-4">
                        <div className="w-16 h-16 bg-gradient-to-br from-yellow-600 to-red-600 rounded-full mx-auto mb-3 flex items-center justify-center">
                          <Crown className="w-8 h-8 text-yellow-200" />
                        </div>
                        <h3 className="text-white font-bold">{winner.name}</h3>
                        <p className="text-yellow-400 text-sm font-medium">{winner.category}</p>
                        <p className="text-gray-400 text-xs">{winner.nationality}</p>
                      </div>

                      <div className="space-y-2 mb-4">
                        {/* Étoiles */}
                        <div className="flex justify-center">
                          {[...Array(5)].map((_, i) => (
                            <Star 
                              key={i} 
                              className={`w-4 h-4 ${
                                i < winner.stars ? 'text-yellow-400 fill-current' : 'text-gray-600'
                              }`} 
                            />
                          ))}
                        </div>

                        {/* Stats améliorées */}
                        <div className="text-xs space-y-1">
                          <div className="flex justify-between">
                            <span className="text-gray-400">Intel:</span>
                            <span className="text-blue-400 font-bold">{winner.stats.intelligence}/10</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Force:</span>
                            <span className="text-red-400 font-bold">{winner.stats.force}/10</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Agilité:</span>
                            <span className="text-green-400 font-bold">{winner.stats.agilité}/10</span>
                          </div>
                        </div>

                        <div className="flex justify-center">
                          <Badge variant="outline" className="text-yellow-400 border-yellow-400 text-xs">
                            👑 Vainqueur
                          </Badge>
                        </div>
                      </div>

                      <div className="text-center">
                        {isOwned ? (
                          <Badge variant="outline" className="text-green-400 border-green-400">
                            Possédée
                          </Badge>
                        ) : (
                          <div className="space-y-2">
                            <div className="text-yellow-400 font-bold">
                              ${winner.price.toLocaleString()}
                            </div>
                            <Button
                              onClick={(e) => {
                                e.stopPropagation();
                                purchaseCelebrity(winner);
                              }}
                              disabled={gameState.money < winner.price || isPurchasing}
                              className={`w-full text-xs ${
                                gameState.money >= winner.price && !isPurchasing
                                  ? 'bg-yellow-600 hover:bg-yellow-700 text-black font-bold'
                                  : 'bg-gray-600 cursor-not-allowed'
                              }`}
                            >
                              {isPurchasing ? (
                                <RefreshCw className="w-3 h-3 mr-1 animate-spin" />
                              ) : (
                                <Crown className="w-3 h-3 mr-1" />
                              )}
                              {isPurchasing ? 'Achat...' : 'Acheter'}
                            </Button>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}

              {/* Message si pas de gagnants */}
              {pastWinners.length === 0 && !loadingWinners && (
                <Card className="bg-gray-800/30 border-gray-600/30 col-span-full">
                  <CardContent className="p-8 text-center">
                    <Crown className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <h3 className="text-white font-bold mb-2">Aucun ancien gagnant</h3>
                    <p className="text-gray-400 text-sm">
                      Terminez vos premières parties pour voir apparaître vos gagnants dans la boutique !
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          {/* Musée des morts */}
          <TabsContent value="museum" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Skull className="w-5 h-5" />
                  Musée des morts
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12 text-gray-400">
                  <Skull className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <h3 className="text-xl font-medium mb-2">Bientôt disponible</h3>
                  <p>Les portraits des joueurs éliminés seront exposés ici</p>
                  <p className="text-sm mt-2">Organisez votre premier jeu pour commencer la collection</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Modal détails célébrité */}
        {selectedCelebrity && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <Card className="bg-gray-900 border-red-500/30 max-w-md w-full">
              <CardHeader>
                <CardTitle className="text-white flex items-center justify-between">
                  {selectedCelebrity.name}
                  <Button
                    variant="ghost"
                    onClick={() => setSelectedCelebrity(null)}
                    className="text-gray-400 hover:text-white p-1"
                  >
                    ✕
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="w-20 h-20 bg-gray-600 rounded-full mx-auto mb-3 flex items-center justify-center">
                    {selectedCelebrity.category === "Ancien gagnant" ? (
                      <Crown className="w-10 h-10 text-yellow-400" />
                    ) : (
                      <Star className="w-10 h-10 text-yellow-400" />
                    )}
                  </div>
                  <Badge variant="outline" className="text-gray-300">
                    {selectedCelebrity.nationality}
                  </Badge>
                </div>

                <div className="bg-gray-800/50 p-4 rounded-lg">
                  <h4 className="text-white font-medium mb-2">Biographie</h4>
                  <p className="text-gray-300 text-sm">{selectedCelebrity.biography}</p>
                </div>

                <div className="grid grid-cols-3 gap-4 text-center">
                  <div className="bg-gray-800/30 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-blue-400">{selectedCelebrity.stats.intelligence}</div>
                    <div className="text-xs text-gray-400">Intelligence</div>
                  </div>
                  <div className="bg-gray-800/30 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-red-400">{selectedCelebrity.stats.force}</div>
                    <div className="text-xs text-gray-400">Force</div>
                  </div>
                  <div className="bg-gray-800/30 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-green-400">{selectedCelebrity.stats.agilité}</div>
                    <div className="text-xs text-gray-400">Agilité</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default VipSalon;
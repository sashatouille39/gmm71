import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Separator } from './ui/separator';
import { 
  Users, 
  Zap, 
  ArrowLeft, 
  Play, 
  Shuffle, 
  UserPlus,
  Settings2,
  Target,
  DollarSign
} from 'lucide-react';
import { generateRandomPlayer, GAME_EVENTS } from '../mock/mockData';
import CustomPlayersList from './CustomPlayersList';

const GameSetup = ({ gameState, onStartGame }) => {
  const navigate = useNavigate();
  const [players, setPlayers] = useState([]);
  const [playerCount, setPlayerCount] = useState(100);
  const [selectedEvents, setSelectedEvents] = useState([]);
  const [gameMode, setGameMode] = useState('standard');
  const [isGenerating, setIsGenerating] = useState(false);

  const gameModes = {
    standard: { name: 'Standard', cost: 1000, description: 'Jeu classique avec épreuves variées' },
    hardcore: { name: 'Hardcore', cost: 2500, description: 'Épreuves plus difficiles, moins de survivants' },
    custom: { name: 'Personnalisé', cost: 1500, description: 'Choisissez vos propres épreuves' }
  };

  const generatePlayers = async () => {
    setIsGenerating(true);
    const newPlayers = [];
    
    // Simulation du temps de génération pour l'effet visuel
    for (let i = 1; i <= playerCount; i++) {
      newPlayers.push(generateRandomPlayer(i));
      
      // Mise à jour progressive pour l'animation
      if (i % 20 === 0) {
        setPlayers([...newPlayers]);
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
    
    setPlayers(newPlayers);
    setIsGenerating(false);
  };

  const selectRandomEvents = () => {
    const shuffled = [...GAME_EVENTS].sort(() => 0.5 - Math.random());
    const eventCount = Math.min(8, shuffled.length);
    setSelectedEvents(shuffled.slice(0, eventCount));
  };

  const toggleEvent = (eventId) => {
    setSelectedEvents(prev => 
      prev.includes(eventId) 
        ? prev.filter(id => id !== eventId)
        : [...prev, eventId]
    );
  };

  const calculateTotalCost = () => {
    const baseCost = gameModes[gameMode].cost;
    const playerCost = Math.floor(playerCount * 10);
    const eventCost = selectedEvents.length * 500;
    return baseCost + playerCost + eventCost;
  };

  const canAfford = () => {
    return gameState.money >= calculateTotalCost();
  };

  const startGame = () => {
    if (!canAfford()) return;
    if (players.length === 0 || selectedEvents.length === 0) return;
    
    const eventsData = GAME_EVENTS.filter(event => selectedEvents.includes(event.id));
    onStartGame(players, eventsData);
    navigate('/game-arena');
  };

  useEffect(() => {
    selectRandomEvents();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/')}
              className="text-gray-400 hover:text-white"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Retour
            </Button>
            <div>
              <h1 className="text-4xl font-black text-white">Configuration de partie</h1>
              <p className="text-gray-400">Préparez votre propre Squid Game</p>
            </div>
          </div>
          
          <div className="text-right">
            <div className="text-2xl font-bold text-green-400">${gameState.money.toLocaleString()}</div>
            <div className="text-sm text-gray-400">Budget disponible</div>
          </div>
        </div>

        <Tabs defaultValue="players" className="space-y-6">
          <TabsList className="bg-black/50 border border-red-500/30">
            <TabsTrigger value="players" className="data-[state=active]:bg-red-600">
              <Users className="w-4 h-4 mr-2" />
              Joueurs
            </TabsTrigger>
            <TabsTrigger value="custom" className="data-[state=active]:bg-red-600">
              <UserPlus className="w-4 h-4 mr-2" />
              Personnalisés
            </TabsTrigger>
            <TabsTrigger value="events" className="data-[state=active]:bg-red-600">
              <Target className="w-4 h-4 mr-2" />
              Épreuves
            </TabsTrigger>
            <TabsTrigger value="launch" className="data-[state=active]:bg-red-600">
              <Play className="w-4 h-4 mr-2" />
              Lancement
            </TabsTrigger>
          </TabsList>

          {/* Configuration des joueurs */}
          <TabsContent value="players" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="bg-black/50 border-red-500/30 lg:col-span-1">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Settings2 className="w-5 h-5" />
                    Configuration
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div>
                    <Label className="text-gray-300">Nombre de joueurs</Label>
                    <Input
                      type="number"
                      min="20"
                      max="1000"
                      value={playerCount}
                      onChange={(e) => setPlayerCount(Math.max(20, Math.min(1000, parseInt(e.target.value) || 20)))}
                      className="bg-gray-800 border-gray-600 text-white mt-2"
                    />
                    <div className="text-sm text-gray-400 mt-1">
                      Entre 20 et 1000 joueurs
                    </div>
                  </div>

                  <div>
                    <Label className="text-gray-300">Mode de jeu</Label>
                    <div className="mt-2 space-y-2">
                      {Object.entries(gameModes).map(([mode, data]) => (
                        <div
                          key={mode}
                          className={`p-3 rounded-lg cursor-pointer transition-all border ${
                            gameMode === mode
                              ? 'bg-red-600/20 border-red-500'
                              : 'bg-gray-800/50 border-gray-600 hover:bg-gray-700/50'
                          }`}
                          onClick={() => setGameMode(mode)}
                        >
                          <div className="flex justify-between items-center">
                            <span className="text-white font-medium">{data.name}</span>
                            <Badge variant="outline" className="text-green-400 border-green-400">
                              ${data.cost}
                            </Badge>
                          </div>
                          <div className="text-sm text-gray-400 mt-1">{data.description}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <Separator className="bg-gray-600" />

                  <div className="space-y-3">
                    <Button
                      onClick={generatePlayers}
                      disabled={isGenerating}
                      className="w-full bg-red-600 hover:bg-red-700"
                    >
                      <Shuffle className="w-4 h-4 mr-2" />
                      {isGenerating ? 'Génération...' : 'Générer les joueurs'}
                    </Button>

                    <Button
                      variant="outline"
                      onClick={() => navigate('/player-creator')}
                      className="w-full border-red-500 text-red-400 hover:bg-red-500/10"
                    >
                      <UserPlus className="w-4 h-4 mr-2" />
                      Créer manuellement
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-black/50 border-red-500/30 lg:col-span-2">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span className="flex items-center gap-2">
                      <Users className="w-5 h-5" />
                      Joueurs générés ({players.length})
                    </span>
                    {isGenerating && (
                      <div className="flex items-center gap-2 text-sm">
                        <div className="w-4 h-4 border-2 border-red-500 border-t-transparent rounded-full animate-spin"></div>
                        Génération en cours...
                      </div>
                    )}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {players.length === 0 ? (
                    <div className="text-center py-12 text-gray-400">
                      <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
                      <p>Aucun joueur généré</p>
                      <p className="text-sm">Cliquez sur "Générer les joueurs" pour commencer</p>
                    </div>
                  ) : (
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 max-h-96 overflow-y-auto">
                      {players.map((player) => (
                        <div
                          key={player.id}
                          className="bg-gray-800/50 border border-gray-600 rounded-lg p-3 text-center hover:bg-gray-700/50 transition-colors"
                        >
                          <div className="w-12 h-12 bg-red-600 rounded-full mx-auto mb-2 flex items-center justify-center text-white font-bold">
                            {player.number}
                          </div>
                          <div className="text-white text-sm font-medium truncate">{player.name}</div>
                          <div className="text-xs text-gray-400">{player.nationality}</div>
                          <Badge
                            variant="outline"
                            className="text-xs mt-1 border-red-400 text-red-400"
                          >
                            {player.role}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Configuration des épreuves */}
          <TabsContent value="events" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <Target className="w-5 h-5" />
                    Sélection des épreuves
                  </span>
                  <Button
                    variant="outline"
                    onClick={selectRandomEvents}
                    className="border-red-500 text-red-400 hover:bg-red-500/10"
                  >
                    <Shuffle className="w-4 h-4 mr-2" />
                    Sélection aléatoire
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {GAME_EVENTS.map((event) => (
                    <div
                      key={event.id}
                      className={`p-4 rounded-lg cursor-pointer transition-all border ${
                        selectedEvents.includes(event.id)
                          ? 'bg-red-600/20 border-red-500'
                          : 'bg-gray-800/50 border-gray-600 hover:bg-gray-700/50'
                      }`}
                      onClick={() => toggleEvent(event.id)}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-white font-medium text-sm">{event.name}</h3>
                        <Badge
                          variant={event.type === 'force' ? 'destructive' : event.type === 'agilité' ? 'default' : 'secondary'}
                          className="text-xs"
                        >
                          {event.type}
                        </Badge>
                      </div>
                      <p className="text-gray-400 text-xs">{event.description}</p>
                      <div className="flex justify-between items-center mt-2">
                        <div className="flex text-yellow-400">
                          {[...Array(5)].map((_, i) => (
                            <span key={i} className={i < event.difficulty ? '★' : '☆'}></span>
                          ))}
                        </div>
                        <div className="text-xs text-green-400">+$500</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Lancement */}
          <TabsContent value="launch" className="space-y-6">
            <Card className="bg-black/50 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Play className="w-5 h-5" />
                  Récapitulatif et lancement
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {/* Résumé des joueurs */}
                  <div className="bg-gray-800/30 rounded-lg p-4">
                    <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                      <Users className="w-4 h-4" />
                      Joueurs
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Total:</span>
                        <span className="text-white">{players.length}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Coût par joueur:</span>
                        <span className="text-green-400">$10</span>
                      </div>
                      <Separator className="bg-gray-600" />
                      <div className="flex justify-between font-medium">
                        <span className="text-gray-300">Sous-total:</span>
                        <span className="text-green-400">${(players.length * 10).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>

                  {/* Résumé des épreuves */}
                  <div className="bg-gray-800/30 rounded-lg p-4">
                    <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                      <Target className="w-4 h-4" />
                      Épreuves
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Sélectionnées:</span>
                        <span className="text-white">{selectedEvents.length}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Coût par épreuve:</span>
                        <span className="text-green-400">$500</span>
                      </div>
                      <Separator className="bg-gray-600" />
                      <div className="flex justify-between font-medium">
                        <span className="text-gray-300">Sous-total:</span>
                        <span className="text-green-400">${(selectedEvents.length * 500).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>

                  {/* Coût total */}
                  <div className="bg-gray-800/30 rounded-lg p-4">
                    <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                      <DollarSign className="w-4 h-4" />
                      Coût total
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Mode {gameModes[gameMode].name}:</span>
                        <span className="text-green-400">${gameModes[gameMode].cost}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Joueurs:</span>
                        <span className="text-green-400">${(players.length * 10).toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Épreuves:</span>
                        <span className="text-green-400">${(selectedEvents.length * 500).toLocaleString()}</span>
                      </div>
                      <Separator className="bg-gray-600" />
                      <div className="flex justify-between text-lg font-bold">
                        <span className="text-white">Total:</span>
                        <span className={canAfford() ? "text-green-400" : "text-red-400"}>
                          ${calculateTotalCost().toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Bouton de lancement */}
                <div className="text-center">
                  <Button
                    onClick={startGame}
                    disabled={!canAfford() || players.length === 0 || selectedEvents.length === 0}
                    className={`px-12 py-6 text-lg font-bold ${
                      canAfford() && players.length > 0 && selectedEvents.length > 0
                        ? 'bg-red-600 hover:bg-red-700'
                        : 'bg-gray-600 cursor-not-allowed'
                    }`}
                  >
                    <Play className="w-6 h-6 mr-3" />
                    {!canAfford() ? 'Budget insuffisant' : 
                     players.length === 0 ? 'Aucun joueur' :
                     selectedEvents.length === 0 ? 'Aucune épreuve' :
                     'LANCER LA PARTIE'}
                  </Button>
                  
                  {(!canAfford() || players.length === 0 || selectedEvents.length === 0) && (
                    <p className="text-red-400 text-sm mt-3">
                      {!canAfford() && `Il vous manque $${(calculateTotalCost() - gameState.money).toLocaleString()}`}
                      {players.length === 0 && 'Générez d\'abord des joueurs'}
                      {selectedEvents.length === 0 && 'Sélectionnez au moins une épreuve'}
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default GameSetup;
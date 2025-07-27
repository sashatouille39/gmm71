import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { 
  Play, 
  Pause, 
  SkipForward, 
  ArrowLeft, 
  Users, 
  Skull, 
  Trophy,
  Eye,
  Clock,
  Target,
  AlertTriangle
} from 'lucide-react';

const GameArena = ({ currentGame, setCurrentGame, gameState, updateGameState }) => {
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentEvent, setCurrentEvent] = useState(null);
  const [eventResults, setEventResults] = useState([]);
  const [spectatorMode, setSpectatorMode] = useState(false);
  const [eventProgress, setEventProgress] = useState(0);

  useEffect(() => {
    if (currentGame && currentGame.events.length > 0) {
      setCurrentEvent(currentGame.events[currentGame.currentEventIndex]);
    }
  }, [currentGame]);

  const simulateEvent = () => {
    if (!currentEvent || !currentGame) return;

    setIsPlaying(true);
    setEventProgress(0);

    // Simulation progressive de l'épreuve
    const interval = setInterval(() => {
      setEventProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          completeEvent();
          return 100;
        }
        return prev + 2;
      });
    }, 100);
  };

  const completeEvent = () => {
    const survivors = [];
    const eliminated = [];
    const kills = {};
    const betrayals = {};

    // Simulation des résultats basés sur les stats et le hasard
    currentGame.players.forEach(player => {
      if (!player.alive) return;

      const statBonus = getStatBonusForEvent(player, currentEvent);
      const roleBonus = getRoleBonusForEvent(player, currentEvent);
      const surviveChance = Math.min(0.9, 0.3 + (statBonus * 0.06) + roleBonus);
      
      if (Math.random() < surviveChance) {
        // Survie
        const timeRemaining = Math.floor(120 * Math.random()); // Temps restant fictif
        const eventKills = Math.floor(Math.random() * 3);
        const betrayed = Math.random() < 0.1;

        player.survivedEvents += 1;
        player.kills += eventKills;
        if (betrayed) player.betrayals += 1;

        const score = timeRemaining + (eventKills * 10) - (betrayed ? 5 : 0);
        player.totalScore += score;

        survivors.push({
          ...player,
          timeRemaining,
          eventKills,
          betrayed,
          score
        });
      } else {
        // Élimination
        player.alive = false;
        eliminated.push({
          ...player,
          eliminationTime: Math.floor(Math.random() * 120),
          cause: getRandomDeathCause(currentEvent)
        });
      }
    });

    // Mise à jour du jeu
    const newResults = {
      eventId: currentEvent.id,
      eventName: currentEvent.name,
      survivors: survivors.sort((a, b) => b.score - a.score),
      eliminated,
      totalParticipants: survivors.length + eliminated.length
    };

    setEventResults(prev => [...prev, newResults]);
    
    // Préparer le prochain événement
    const nextEventIndex = currentGame.currentEventIndex + 1;
    if (nextEventIndex < currentGame.events.length) {
      setCurrentGame(prev => ({
        ...prev,
        currentEventIndex: nextEventIndex,
        players: [...survivors, ...eliminated]
      }));
    } else {
      // Fin de la partie
      setCurrentGame(prev => ({ ...prev, completed: true }));
      updateGameState({
        money: gameState.money + calculateWinnings(survivors.length),
        gameStats: {
          ...gameState.gameStats,
          totalGamesPlayed: gameState.gameStats.totalGamesPlayed + 1,
          totalKills: gameState.gameStats.totalKills + survivors.reduce((acc, p) => acc + p.kills, 0)
        }
      });
    }

    setIsPlaying(false);
  };

  const getStatBonusForEvent = (player, event) => {
    switch (event.type) {
      case 'intelligence': return player.stats.intelligence;
      case 'force': return player.stats.force;
      case 'agilité': return player.stats.agilité;
      default: return (player.stats.intelligence + player.stats.force + player.stats.agilité) / 3;
    }
  };

  const getRoleBonusForEvent = (player, event) => {
    switch (player.role) {
      case 'intelligent': return event.type === 'intelligence' ? 0.2 : 0.1;
      case 'brute': return event.type === 'force' ? 0.2 : 0.1;
      case 'sportif': return event.type === 'agilité' ? 0.2 : 0.1;
      case 'zero': return 0.15; // Bonus universel
      case 'peureux': return -0.1;
      default: return 0;
    }
  };

  const getRandomDeathCause = (event) => {
    const causes = {
      'Feu rouge, Feu vert': ['Abattu en mouvement', 'Panique collective', 'Tentative de fuite'],
      'Pont de verre': ['Chute mortelle', 'Verre brisé', 'Poussé par un autre joueur'],
      'Combat de gladiateurs': ['Coup fatal', 'Hémorragie', 'Épuisement'],
      default: ['Élimination standard', 'Erreur fatale', 'Mauvaise décision']
    };
    
    const eventCauses = causes[event.name] || causes.default;
    return eventCauses[Math.floor(Math.random() * eventCauses.length)];
  };

  const calculateWinnings = (survivorCount) => {
    const basePayout = 10000;
    const participantBonus = (currentGame.players.length - survivorCount) * 100;
    return basePayout + participantBonus;
  };

  if (!currentGame) {
    navigate('/');
    return null;
  }

  const alivePlayers = currentGame.players.filter(p => p.alive);
  const deadPlayers = currentGame.players.filter(p => !p.alive);

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
              Arrêter la partie
            </Button>
            <div>
              <h1 className="text-4xl font-black text-white">Arène de jeu</h1>
              <p className="text-gray-400">Partie en cours - {currentGame.events.length} épreuves</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              onClick={() => setSpectatorMode(!spectatorMode)}
              className={spectatorMode ? "border-red-500 text-red-400" : "border-gray-600 text-gray-400"}
            >
              <Eye className="w-4 h-4 mr-2" />
              Mode spectateur
            </Button>
          </div>
        </div>

        {/* Statistiques en temps réel */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <Card className="bg-black/50 border-green-500/30">
            <CardContent className="p-4 text-center">
              <Users className="w-6 h-6 text-green-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{alivePlayers.length}</div>
              <div className="text-sm text-gray-400">Survivants</div>
            </CardContent>
          </Card>
          
          <Card className="bg-black/50 border-red-500/30">
            <CardContent className="p-4 text-center">
              <Skull className="w-6 h-6 text-red-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{deadPlayers.length}</div>
              <div className="text-sm text-gray-400">Éliminés</div>
            </CardContent>
          </Card>
          
          <Card className="bg-black/50 border-yellow-500/30">
            <CardContent className="p-4 text-center">
              <Target className="w-6 h-6 text-yellow-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{currentGame.currentEventIndex + 1}</div>
              <div className="text-sm text-gray-400">Épreuve actuelle</div>
            </CardContent>
          </Card>
          
          <Card className="bg-black/50 border-blue-500/30">
            <CardContent className="p-4 text-center">
              <Trophy className="w-6 h-6 text-blue-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{Math.floor((deadPlayers.length / currentGame.players.length) * 100)}%</div>
              <div className="text-sm text-gray-400">Taux d'élimination</div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Épreuve actuelle */}
          <Card className="bg-black/50 border-red-500/30 lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-white flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Target className="w-5 h-5" />
                  {currentEvent?.name || 'Aucune épreuve'}
                </span>
                {currentEvent && (
                  <Badge variant="outline" className="text-red-400 border-red-400">
                    {currentEvent.type}
                  </Badge>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {currentEvent ? (
                <>
                  <div className="bg-gray-800/30 p-4 rounded-lg">
                    <p className="text-gray-300 mb-4">{currentEvent.description}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-gray-400">Difficulté:</span>
                        <div className="flex text-yellow-400">
                          {[...Array(5)].map((_, i) => (
                            <span key={i} className={i < currentEvent.difficulty ? '★' : '☆'}></span>
                          ))}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-gray-400" />
                        <span className="text-gray-400">2 minutes</span>
                      </div>
                    </div>
                  </div>

                  {/* Barre de progression de l'événement */}
                  {isPlaying && (
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-white font-medium">Épreuve en cours...</span>
                        <span className="text-gray-400">{eventProgress}%</span>
                      </div>
                      <Progress value={eventProgress} className="h-2" />
                    </div>
                  )}

                  {/* Contrôles */}
                  <div className="flex gap-4">
                    <Button
                      onClick={simulateEvent}
                      disabled={isPlaying || currentGame.completed}
                      className="bg-red-600 hover:bg-red-700 flex-1"
                    >
                      {isPlaying ? (
                        <>
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                          En cours...
                        </>
                      ) : (
                        <>
                          <Play className="w-4 h-4 mr-2" />
                          Lancer l'épreuve
                        </>
                      )}
                    </Button>
                    
                    {!isPlaying && (
                      <Button
                        variant="outline"
                        onClick={() => {
                          // Passer à l'épreuve suivante
                          if (currentGame.currentEventIndex < currentGame.events.length - 1) {
                            setCurrentGame(prev => ({
                              ...prev,
                              currentEventIndex: prev.currentEventIndex + 1
                            }));
                          }
                        }}
                        disabled={currentGame.currentEventIndex >= currentGame.events.length - 1}
                        className="border-gray-600 text-gray-400"
                      >
                        <SkipForward className="w-4 h-4 mr-2" />
                        Passer
                      </Button>
                    )}
                  </div>

                  {/* Mode spectateur */}
                  {spectatorMode && (
                    <div className="bg-gray-800/30 p-4 rounded-lg">
                      <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                        <Eye className="w-4 h-4" />
                        Vue spectateur
                      </h3>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center">
                          <div className="w-full h-24 bg-gray-700 rounded-lg flex items-center justify-center mb-2">
                            <span className="text-gray-400">Caméra 1</span>
                          </div>
                          <span className="text-xs text-gray-400">Vue d'ensemble</span>
                        </div>
                        <div className="text-center">
                          <div className="w-full h-24 bg-gray-700 rounded-lg flex items-center justify-center mb-2">
                            <span className="text-gray-400">Caméra 2</span>
                          </div>
                          <span className="text-xs text-gray-400">Focus joueur</span>
                        </div>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center py-12 text-gray-400">
                  <AlertTriangle className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>Partie terminée</p>
                  <Button
                    onClick={() => navigate('/statistics')}
                    className="mt-4 bg-red-600 hover:bg-red-700"
                  >
                    Voir les statistiques
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Liste des joueurs */}
          <Card className="bg-black/50 border-red-500/30">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Users className="w-5 h-5" />
                Joueurs ({alivePlayers.length} vivants)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="max-h-96 overflow-y-auto space-y-2">
                {currentGame.players
                  .sort((a, b) => b.alive - a.alive || b.totalScore - a.totalScore)
                  .map((player) => (
                  <div
                    key={player.id}
                    className={`p-3 rounded-lg border transition-all ${
                      player.alive 
                        ? 'bg-gray-800/50 border-green-500/30 hover:bg-gray-700/50' 
                        : 'bg-red-900/20 border-red-500/30 opacity-60'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                          player.alive ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                        }`}>
                          {player.number}
                        </div>
                        <div>
                          <div className="text-white text-sm font-medium">{player.name}</div>
                          <div className="text-xs text-gray-400">{player.nationality}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        {player.alive ? (
                          <div className="text-green-400 text-sm">{player.totalScore} pts</div>
                        ) : (
                          <Skull className="w-4 h-4 text-red-400" />
                        )}
                        <div className="text-xs text-gray-400">{player.survivedEvents} épreuves</div>
                      </div>
                    </div>
                    
                    {/* Stats mini */}
                    <div className="mt-2 flex gap-2">
                      <div className="text-xs text-gray-400">
                        I:{player.stats.intelligence} F:{player.stats.force} A:{player.stats.agilité}
                      </div>
                      {player.kills > 0 && (
                        <Badge variant="outline" className="text-xs text-red-400 border-red-400">
                          {player.kills} kills
                        </Badge>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Résultats des épreuves précédentes */}
        {eventResults.length > 0 && (
          <Card className="bg-black/50 border-red-500/30 mt-8">
            <CardHeader>
              <CardTitle className="text-white">Historique des épreuves</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {eventResults.map((result, index) => (
                  <div key={index} className="bg-gray-800/30 p-4 rounded-lg">
                    <div className="flex justify-between items-center mb-3">
                      <h3 className="text-white font-medium">{result.eventName}</h3>
                      <div className="flex gap-2">
                        <Badge variant="outline" className="text-green-400 border-green-400">
                          {result.survivors.length} survivants
                        </Badge>
                        <Badge variant="outline" className="text-red-400 border-red-400">
                          {result.eliminated.length} éliminés
                        </Badge>
                      </div>
                    </div>
                    
                    {/* Top 3 des survivants */}
                    {result.survivors.length > 0 && (
                      <div>
                        <h4 className="text-gray-400 text-sm mb-2">Meilleurs performances:</h4>
                        <div className="grid grid-cols-3 gap-2">
                          {result.survivors.slice(0, 3).map((survivor, i) => (
                            <div key={survivor.id} className="text-xs">
                              <span className={`${i === 0 ? 'text-yellow-400' : i === 1 ? 'text-gray-300' : 'text-orange-400'}`}>
                                #{i + 1} {survivor.name}
                              </span>
                              <div className="text-gray-400">
                                {survivor.score} pts ({survivor.timeRemaining}s restant)
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default GameArena;
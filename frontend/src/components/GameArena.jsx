import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import EliminatedPlayersModal from './EliminatedPlayersModal';
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

const GameArena = ({ currentGame, setCurrentGame, gameState, updateGameState, onRefreshGameState }) => {
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentEvent, setCurrentEvent] = useState(null);
  const [eventResults, setEventResults] = useState([]);
  const [spectatorMode, setSpectatorMode] = useState(false);
  const [showEliminatedModal, setShowEliminatedModal] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [eventProgress, setEventProgress] = useState(0);
  const [animationPhase, setAnimationPhase] = useState('idle');

  useEffect(() => {
    if (currentGame && currentGame.events.length > 0) {
      // Si le jeu est terminé, ne pas définir d'événement courant pour afficher l'écran de fin
      if (currentGame.completed) {
        setCurrentEvent(null);
      } else {
        setCurrentEvent(currentGame.events[currentGame.currentEventIndex]);
      }
    }
  }, [currentGame]);

  // Fonction pour collecter automatiquement les gains VIP quand le jeu se termine
  const collectVipEarningsAutomatically = async (gameId) => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      // Vérifier d'abord le statut des gains VIP
      const statusResponse = await fetch(`${backendUrl}/api/games/${gameId}/vip-earnings-status`);
      if (!statusResponse.ok) {
        console.error('Erreur lors de la vérification du statut VIP');
        return;
      }
      
      const statusData = await statusResponse.json();
      console.log('Statut des gains VIP:', statusData);
      
      // Si le jeu est terminé et qu'il y a des gains à collecter
      if (statusData.completed && statusData.can_collect && statusData.earnings_available > 0) {
        const collectResponse = await fetch(`${backendUrl}/api/games/${gameId}/collect-vip-earnings`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
        
        if (collectResponse.ok) {
          const collectData = await collectResponse.json();
          console.log('Gains VIP collectés automatiquement:', collectData);
          
          // Afficher une notification à l'utilisateur
          const notification = document.createElement('div');
          notification.innerHTML = `
            <div class="fixed top-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-3 animate-fade-in">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <div>
                <div class="font-bold">💰 Gains VIP collectés !</div>
                <div class="text-sm">+$${collectData.earnings_collected.toLocaleString()}</div>
              </div>
            </div>
          `;
          document.body.appendChild(notification.firstElementChild);
          
          // Supprimer la notification après 5 secondes
          setTimeout(() => {
            const notif = document.querySelector('.fixed.top-4.right-4');
            if (notif) notif.remove();
          }, 5000);
          
          // Recharger le gameState depuis le backend pour synchroniser le nouveau solde
          if (onRefreshGameState) {
            await onRefreshGameState();
          }
        } else {
          console.error('Erreur lors de la collecte des gains VIP');
        }
      } else {
        console.log('Pas de gains VIP à collecter ou jeu non terminé');
      }
      
    } catch (error) {
      console.error('Erreur lors de la collecte automatique des gains VIP:', error);
    }
  };

  const simulateEvent = async () => {
    setIsPlaying(true);
    setAnimationPhase('preparation');
    
    try {
      // Animation de préparation
      await new Promise(resolve => setTimeout(resolve, 2000));
      setAnimationPhase('action');
      
      // Animation d'action
      await new Promise(resolve => setTimeout(resolve, 1500));
      setAnimationPhase('results');
      
      // Appeler l'API backend pour simuler l'événement
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/games/${currentGame.id}/simulate-event`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status}`);
      }
      
      const { result, game } = await response.json();
      
      // Fonction pour adapter un joueur du format backend vers frontend
      const adaptPlayer = (player) => ({
        ...player,
        totalScore: player.total_score || 0, // Convertir snake_case vers camelCase
        survivedEvents: player.survived_events || 0 // Convertir snake_case vers camelCase
      });
      
      // Adapter le format de jeu pour le frontend avec conversion complète des champs
      const adaptedGame = {
        id: game.id,
        players: game.players.map(adaptPlayer), // CRITIQUE: adapter tous les joueurs
        events: game.events,
        currentEventIndex: game.current_event_index || 0, // CORRECTION: convertir snake_case vers camelCase
        completed: game.completed || false, // CRITIQUE: s'assurer que completed est préservé
        start_time: game.start_time,
        end_time: game.end_time,
        winner: game.winner ? adaptPlayer(game.winner) : null, // CRITIQUE: adapter le gagnant aussi
        total_cost: game.total_cost || 0,
        earnings: game.earnings || 0,
        event_results: game.event_results || []
      };
      
      // Mettre à jour l'état du jeu avec les résultats du backend
      setCurrentGame(adaptedGame);
      
      // NOUVEAU: Si le jeu est terminé, collecter automatiquement les gains VIP
      if (adaptedGame.completed) {
        console.log('🎉 Jeu terminé ! Collecte automatique des gains VIP...');
        await collectVipEarningsAutomatically(currentGame.id);
      }
      
      // Mettre à jour les stats des célébrités si nécessaire
      if (result.survivors) {
        for (const survivorData of result.survivors) {
          if (survivorData.player && survivorData.player.isCelebrity) {
            await updateCelebrityStats(survivorData.player.celebrityId, {
              survived_events: survivorData.player.survived_events || 0,
              total_score: survivorData.player.total_score || 0
            });
          }
        }
      }
      
      // Traiter les victoires si le jeu est terminé
      if (game.completed && game.winner && game.winner.isCelebrity) {
        await updateCelebrityVictory(game.winner.celebrityId);
      }
      
      console.log('Événement simulé avec succès:', {
        survivors: result.survivors?.length || 0,
        eliminated: result.eliminated?.length || 0,
        totalParticipants: result.total_participants || 0
      });
      
    } catch (error) {
      console.error('Erreur lors de la simulation:', error);
      alert('Erreur lors de la simulation de l\'événement. Vérifiez votre connexion.');
    } finally {
      setIsPlaying(false);
    }
  };

  // Fonction pour mettre à jour les stats des célébrités après un jeu
  const updateCelebrityStats = async (celebrityIdOrPlayers, stats) => {
    // Si appelé avec un seul celebrityId et des stats
    if (typeof celebrityIdOrPlayers === 'string' && stats) {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      try {
        await fetch(`${backendUrl}/api/celebrities/${celebrityIdOrPlayers}/participation`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(stats)
        });
      } catch (error) {
        console.error('Erreur lors de la mise à jour des stats de célébrité:', error);
      }
      return;
    }

    // Si appelé avec une liste de joueurs (comportement original)
    const finalPlayers = celebrityIdOrPlayers;
    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
    
    for (const player of finalPlayers) {
      if (player.isCelebrity && player.celebrityId) {
        try {
          // Si la célébrité a survécu et a gagné, enregistrer une victoire
          if (player.alive && player === currentGame.winner) {
            await fetch(`${backendUrl}/api/celebrities/${player.celebrityId}/victory`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
              }
            });
          }
          
          // Enregistrer la participation générale de la célébrité
          await fetch(`${backendUrl}/api/celebrities/${player.celebrityId}/participation`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              survived_events: player.survivedEvents || 0,
              total_score: player.totalScore || 0,
              alive: player.alive || false
            })
          });
          
        } catch (error) {
          console.error('Erreur lors de la mise à jour des stats de célébrité:', error);
        }
      }
    }
  };

  // Fonction pour enregistrer une victoire de célébrité
  const updateCelebrityVictory = async (celebrityId) => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
    
    try {
      await fetch(`${backendUrl}/api/celebrities/${celebrityId}/victory`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        }
      });
    } catch (error) {
      console.error('Erreur lors de l\'enregistrement de la victoire:', error);
    }
  };

  const completeEvent = () => {
    const survivors = [];
    const eliminated = [];
    const kills = {};
    const betrayals = {};

    // Calcul plus équilibré du taux de survie global selon la difficulté de l'épreuve
    const baseSurvivalRate = Math.max(0.3, 1 - (currentEvent.difficulty * 0.08)); // 30% minimum, diminue avec difficulté
    const alivePlayersCount = currentGame.players.filter(p => p.alive).length;
    
    // Garantir qu'au moins 20% des joueurs survivent (minimum 5 joueurs)
    const minSurvivors = Math.max(5, Math.floor(alivePlayersCount * 0.2));
    let actualSurvivors = 0;

    // Première passe : calcul des chances de survie pour chaque joueur
    const playersWithChances = currentGame.players
      .filter(p => p.alive)
      .map(player => {
        const statBonus = getStatBonusForEvent(player, currentEvent);
        const roleBonus = getRoleBonusForEvent(player, currentEvent);
        
        // Formule améliorée : base plus élevée, bonus plus significatifs
        let surviveChance = baseSurvivalRate + (statBonus * 0.04) + roleBonus + (Math.random() * 0.1);
        surviveChance = Math.min(0.95, Math.max(0.15, surviveChance)); // Entre 15% et 95%
        
        return {
          player,
          surviveChance
        };
      })
      .sort((a, b) => b.surviveChance - a.surviveChance); // Trier par chance de survie décroissante

    // Simulation des résultats avec garantie de survivants minimum
    playersWithChances.forEach(({ player, surviveChance }, index) => {
      let survives = Math.random() < surviveChance;
      
      // Forcer la survie si on n'a pas assez de survivants et qu'on est dans le top
      if (!survives && actualSurvivors < minSurvivors && index < minSurvivors) {
        survives = true;
      }
      
      // Empêcher trop de survivants (maximum 80%)
      const maxSurvivors = Math.floor(alivePlayersCount * 0.8);
      if (survives && actualSurvivors >= maxSurvivors) {
        survives = false;
      }

      if (survives) {
        actualSurvivors++;
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

    console.log(`🎯 Épreuve ${currentEvent.name}:`, {
      participants: alivePlayersCount,
      survivors: actualSurvivors,
      eliminated: eliminated.length,
      survivalRate: `${((actualSurvivors / alivePlayersCount) * 100).toFixed(1)}%`,
      difficulty: currentEvent.difficulty
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
    const alivePlayers = survivors.filter(s => s.alive !== false);
    
    // Condition d'arrêt : 1 survivant OU tous les événements terminés
    if (alivePlayers.length <= 1 || nextEventIndex >= currentGame.events.length) {
      // Déterminer le gagnant
      let winner = null;
      if (alivePlayers.length === 1) {
        winner = alivePlayers[0];
      } else if (alivePlayers.length > 1) {
        winner = alivePlayers.reduce((prev, current) => 
          prev.totalScore > current.totalScore ? prev : current
        );
      }

      // Fin de la partie
      const finalPlayers = [...survivors, ...eliminated];
      setCurrentGame(prev => ({ 
        ...prev, 
        completed: true,
        winner: winner,
        players: finalPlayers
      }));

      // Mettre à jour les stats des célébrités
      updateCelebrityStats(finalPlayers);

      updateGameState({
        money: gameState.money + calculateWinnings(survivors.length),
        gameStats: {
          ...gameState.gameStats,
          totalGamesPlayed: gameState.gameStats.totalGamesPlayed + 1,
          totalKills: gameState.gameStats.totalKills + survivors.reduce((acc, p) => acc + p.kills, 0)
        }
      });
    } else {
      // Continuer au prochain événement
      setCurrentGame(prev => ({
        ...prev,
        currentEventIndex: nextEventIndex,
        players: [...survivors, ...eliminated]
      }));
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
      case 'intelligent': return event.type === 'intelligence' ? 0.15 : 0.05;
      case 'brute': return event.type === 'force' ? 0.15 : 0.05;
      case 'sportif': return event.type === 'agilité' ? 0.15 : 0.05;
      case 'zero': return 0.20; // Bonus universel - Le Zéro est exceptionnel
      case 'peureux': return -0.05; // Moins de pénalité
      case 'celebrity': return 0.08; // Bonus modéré pour les célébrités
      default: return 0.02; // Petit bonus pour les joueurs normaux
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

  // Fonction pour quitter la partie avec remboursement automatique si non terminée
  const handleQuitGame = async () => {
    if (!currentGame) {
      navigate('/');
      return;
    }
    
    const shouldQuit = window.confirm(
      currentGame.completed 
        ? 'Voulez-vous retourner au menu principal ?' 
        : 'Attention : La partie n\'est pas terminée. Si vous quittez maintenant, vous serez automatiquement remboursé. Continuer ?'
    );
    
    if (!shouldQuit) return;
    
    try {
      // Si la partie n'est pas terminée, la supprimer pour déclencher le remboursement
      if (!currentGame.completed) {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
        const response = await fetch(`${backendUrl}/api/games/${currentGame.id}`, {
          method: 'DELETE',
        });
        
        if (response.ok) {
          const result = await response.json();
          console.log('Partie supprimée:', result);
          
          // Afficher notification de remboursement si applicable
          if (result.refund_amount > 0) {
            const notification = document.createElement('div');
            notification.innerHTML = `
              <div class="fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-3 animate-fade-in">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
                </svg>
                <div>
                  <div class="font-bold">💸 Remboursement automatique</div>
                  <div class="text-sm">+$${result.refund_amount.toLocaleString()} remboursé</div>
                </div>
              </div>
            `;
            document.body.appendChild(notification.firstElementChild);
            
            setTimeout(() => {
              const notif = document.querySelector('.fixed.top-4.right-4');
              if (notif) notif.remove();
            }, 5000);
          }
          
          // Recharger le gameState depuis le backend pour synchroniser le nouveau solde
          if (onRefreshGameState) {
            await onRefreshGameState();
          }
        }
      }
    } catch (error) {
      console.error('Erreur lors de la suppression de la partie:', error);
    }
    
    // Retourner au menu principal
    navigate('/');
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
              onClick={handleQuitGame}
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
                  <Trophy className="w-16 h-16 mx-auto mb-4 text-yellow-400" />
                  
                  {/* Message de fin de jeu */}
                  {alivePlayers.length === 1 ? (
                    <div className="mb-6">
                      <p className="text-xl text-white mb-2">Nous avons un gagnant !</p>
                      <div className="text-lg text-yellow-400 font-bold flex items-center justify-center gap-2">
                        {alivePlayers[0].isCelebrity && (
                          <span className="text-yellow-500">👑</span>
                        )}
                        🏆 {alivePlayers[0].name} (#{alivePlayers[0].number})
                        {alivePlayers[0].isCelebrity && (
                          <span className="text-xs bg-yellow-600 px-2 py-1 rounded-full">CÉLÉBRITÉ</span>
                        )}
                      </div>
                      <p className="text-sm text-gray-400 mt-2">
                        Score final: {alivePlayers[0].totalScore} points
                      </p>
                      {alivePlayers[0].isCelebrity && (
                        <p className="text-sm text-yellow-400 mt-1">
                          Une victoire supplémentaire ajoutée à cette célébrité !
                        </p>
                      )}
                    </div>
                  ) : alivePlayers.length === 0 ? (
                    <div className="mb-6">
                      <p className="text-xl text-red-400 mb-2">Aucun survivant</p>
                      <p className="text-sm text-gray-400">Tous les joueurs ont été éliminés</p>
                    </div>
                  ) : (
                    <div className="mb-6">
                      <p className="text-xl text-white mb-2">Partie terminée</p>
                      <p className="text-sm text-gray-400">{alivePlayers.length} survivants restants</p>
                      {/* Afficher les célébrités survivantes */}
                      {alivePlayers.filter(p => p.isCelebrity).length > 0 && (
                        <div className="mt-3 p-3 bg-yellow-900/20 rounded-lg border border-yellow-500/30">
                          <p className="text-yellow-400 text-sm font-medium mb-2">Célébrités survivantes :</p>
                          <div className="space-y-1">
                            {alivePlayers.filter(p => p.isCelebrity).map(celeb => (
                              <div key={celeb.id} className="text-xs text-yellow-300 flex items-center gap-2">
                                👑 {celeb.name} - {celeb.totalScore} points
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {/* Boutons d'action */}
                  <div className="flex flex-col sm:flex-row gap-3 justify-center">
                    <Button
                      onClick={handleQuitGame}
                      variant="outline"
                      className="border-gray-600 text-gray-300 hover:bg-gray-700"
                    >
                      <ArrowLeft className="w-4 h-4 mr-2" />
                      Retour au menu
                    </Button>
                    <Button
                      onClick={() => navigate(`/final-ranking/${currentGame.id}`)}
                      className="bg-yellow-600 hover:bg-yellow-700"
                    >
                      <Trophy className="w-4 h-4 mr-2" />
                      Classement complet
                    </Button>
                    <Button
                      onClick={() => navigate('/statistics')}
                      className="bg-red-600 hover:bg-red-700"
                    >
                      <Target className="w-4 h-4 mr-2" />
                      Statistiques
                    </Button>
                  </div>
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
                          <div className="text-white text-sm font-medium flex items-center gap-2">
                            {player.name}
                            {player.isCelebrity && (
                              <span className="text-yellow-400 text-xs">👑</span>
                            )}
                          </div>
                          <div className="text-xs text-gray-400 flex items-center gap-1">
                            {player.nationality}
                            {player.isCelebrity && (
                              <span className="text-yellow-500 bg-yellow-900/30 px-1 rounded text-xs">STAR</span>
                            )}
                          </div>
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
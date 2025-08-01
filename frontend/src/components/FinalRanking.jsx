import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import EliminatedPlayersModal from './EliminatedPlayersModal';
import { 
  Trophy, 
  Medal, 
  Award, 
  ArrowLeft, 
  Crown,
  Skull,
  Target,
  Calendar
} from 'lucide-react';

const FinalRanking = ({ gameState }) => {
  const navigate = useNavigate();
  const { gameId } = useParams();
  const [rankingData, setRankingData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showEliminatedModal, setShowEliminatedModal] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  useEffect(() => {
    if (gameId) {
      loadFinalRanking();
    }
  }, [gameId]);

  // Nouvel effet pour vérifier et collecter automatiquement les gains VIP
  useEffect(() => {
    if (rankingData && rankingData.completed && rankingData.vip_earnings > 0) {
      // Vérifier si les gains VIP peuvent encore être collectés
      checkAndCollectVipEarnings();
    }
  }, [rankingData]);

  const checkAndCollectVipEarnings = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      // Vérifier le statut des gains VIP
      const statusResponse = await fetch(`${backendUrl}/api/games/${gameId}/vip-earnings-status`);
      if (statusResponse.ok) {
        const statusData = await statusResponse.json();
        
        // Si les gains peuvent encore être collectés, les collecter automatiquement
        if (statusData.completed && statusData.can_collect && statusData.earnings_available > 0) {
          console.log('🎭 Collecte automatique des gains VIP depuis FinalRanking...');
          
          const collectResponse = await fetch(`${backendUrl}/api/games/${gameId}/collect-vip-earnings`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            }
          });
          
          if (collectResponse.ok) {
            const collectData = await collectResponse.json();
            console.log('✅ Gains VIP collectés depuis FinalRanking:', collectData);
            
            // Optionnel: Afficher une notification de succès
            // toast ou autre notification système peut être ajoutée ici
          }
        }
      }
    } catch (error) {
      console.error('Erreur lors de la vérification des gains VIP:', error);
    }
  };

  const loadFinalRanking = async () => {
    try {
      setIsLoading(true);
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/games/${gameId}/final-ranking`);
      
      if (!response.ok) {
        throw new Error('Erreur lors du chargement du classement');
      }
      
      const data = await response.json();
      setRankingData(data);
    } catch (error) {
      console.error('Erreur lors du chargement du classement:', error);
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKillsClick = (player, kills) => {
    if (kills > 0) {
      setSelectedPlayer(player);
      setShowEliminatedModal(true);
    }
  };

  const getRankingIcon = (position) => {
    switch (position) {
      case 1: return <Trophy className="w-6 h-6 text-yellow-500" />;
      case 2: return <Medal className="w-6 h-6 text-gray-400" />;
      case 3: return <Award className="w-6 h-6 text-amber-600" />;
      default: return <span className="w-6 h-6 flex items-center justify-center text-gray-400 font-bold text-lg">#{position}</span>;
    }
  };

  const getRankingStyle = (position, isAlive) => {
    if (!isAlive) {
      return 'bg-red-900/20 border-red-500/30 opacity-70';
    }
    
    switch (position) {
      case 1: return 'bg-yellow-900/30 border-yellow-500 shadow-lg shadow-yellow-500/20';
      case 2: return 'bg-gray-700/50 border-gray-400';
      case 3: return 'bg-amber-900/30 border-amber-500';
      default: return 'bg-gray-800/50 border-gray-600';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black p-6 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-red-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-white">Chargement du classement...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black p-6 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">Erreur: {error}</p>
          <Button onClick={() => navigate('/')} className="bg-red-600 hover:bg-red-700">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour au menu
          </Button>
        </div>
      </div>
    );
  }

  if (!rankingData) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/')}
              className="text-gray-400 hover:text-white"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Retour au menu
            </Button>
            <div>
              <h1 className="text-4xl font-black text-white">Classement Final</h1>
              <p className="text-gray-400">Résultats complets de la partie</p>
            </div>
          </div>
          
          <div className="text-right">
            <div className="text-2xl font-bold text-yellow-400">
              {rankingData.winner ? `🏆 ${rankingData.winner.name}` : 'Aucun gagnant'}
            </div>
            <div className="text-sm text-gray-400">Gagnant de la partie</div>
          </div>
        </div>

        {/* Statistiques de la partie */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <Card className="bg-black/50 border-blue-500/30">
            <CardContent className="p-4 text-center">
              <Target className="w-6 h-6 text-blue-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{rankingData.total_players}</div>
              <div className="text-sm text-gray-400">Joueurs total</div>
            </CardContent>
          </Card>
          
          <Card className="bg-black/50 border-green-500/30">
            <CardContent className="p-4 text-center">
              <Trophy className="w-6 h-6 text-green-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{rankingData.events_completed}</div>
              <div className="text-sm text-gray-400">Épreuves complétées</div>
            </CardContent>
          </Card>

          <Card className="bg-black/50 border-red-500/30">
            <CardContent className="p-4 text-center">
              <Skull className="w-6 h-6 text-red-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">
                {rankingData.ranking.filter(p => !p.player.alive).length}
              </div>
              <div className="text-sm text-gray-400">Éliminés</div>
            </CardContent>
          </Card>

          <Card className="bg-black/50 border-yellow-500/30">
            <CardContent className="p-4 text-center">
              <Calendar className="w-6 h-6 text-yellow-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">
                ${rankingData.vip_earnings?.toLocaleString() || '0'}
              </div>
              <div className="text-sm text-gray-400">Gains VIP</div>
            </CardContent>
          </Card>
        </div>

        {/* Gains VIP - Section dédiée */}
        {rankingData.vip_earnings > 0 && (
          <Card className="bg-gradient-to-r from-green-900/30 to-yellow-900/30 border-green-500/50 mb-8">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Trophy className="w-5 h-5 text-yellow-400" />
                💰 Revenus VIP de cette partie
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-400 mb-2">
                  ${rankingData.vip_earnings.toLocaleString()}
                </div>
                <p className="text-gray-300 mb-4">
                  Les VIPs ont payé leurs frais de visionnage pour cette partie spectaculaire !
                </p>
                <div className="flex justify-center items-center gap-4 text-sm text-gray-400">
                  <span>🎭 Frais de visionnage VIP</span>
                  <span>•</span>
                  <span>💰 Collecté automatiquement</span>
                  <span>•</span>
                  <span>💵 Ajouté à votre solde</span>
                </div>
                <div className="mt-3 p-2 bg-green-900/20 rounded-lg border border-green-600/30">
                  <p className="text-green-200 text-xs">
                    ✅ Ces gains ont été automatiquement ajoutés à votre argent
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Podium des 3 premiers */}
        <Card className="bg-black/50 border-red-500/30 mb-8">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Trophy className="w-5 h-5" />
              Podium
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              {rankingData.ranking.slice(0, 3).map((entry, index) => (
                <div
                  key={entry.player.id}
                  className={`p-6 rounded-lg border text-center ${getRankingStyle(entry.position, entry.player.alive)}`}
                >
                  <div className="flex justify-center mb-4">
                    {getRankingIcon(entry.position)}
                  </div>
                  <div className="mb-4">
                    <div className="text-white text-xl font-bold flex items-center justify-center gap-2">
                      {entry.player.is_celebrity && <Crown className="w-5 h-5 text-yellow-400" />}
                      {entry.player.name}
                      {!entry.player.alive && <Skull className="w-5 h-5 text-red-400" />}
                    </div>
                    <div className="text-gray-400 text-sm">#{entry.player.number} • {entry.player.nationality}</div>
                    {entry.player.is_celebrity && (
                      <Badge className="bg-yellow-600 text-white text-xs mt-2">
                        CÉLÉBRITÉ
                      </Badge>
                    )}
                  </div>
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-green-400">
                      {entry.game_stats.total_score} pts
                    </div>
                    <div className="text-sm text-gray-400">
                      {entry.game_stats.survived_events} épreuves survécues
                    </div>
                    <div className="text-sm text-gray-400">
                      <span 
                        className={`${entry.game_stats.kills > 0 ? 'cursor-pointer hover:text-red-300 hover:underline' : ''}`}
                        onClick={() => handleKillsClick(entry.player, entry.game_stats.kills)}
                      >
                        {entry.game_stats.kills} éliminations
                      </span>
                      {' • '}
                      {entry.game_stats.betrayals} trahisons
                    </div>
                    <div className="text-xs text-gray-500">
                      Int: {entry.player_stats.intelligence} | For: {entry.player_stats.force} | Agi: {entry.player_stats.agilité}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Classement complet */}
        <Card className="bg-black/50 border-red-500/30">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Target className="w-5 h-5" />
              Classement complet ({rankingData.ranking.length} joueurs)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {rankingData.ranking.map((entry) => (
                <div
                  key={entry.player.id}
                  className={`p-3 rounded-lg border transition-all ${getRankingStyle(entry.position, entry.player.alive)}`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {getRankingIcon(entry.position)}
                      <div>
                        <div className="text-white text-sm font-medium flex items-center gap-2">
                          {entry.player.is_celebrity && <Crown className="w-4 h-4 text-yellow-400" />}
                          {entry.player.name}
                          {!entry.player.alive && <Skull className="w-4 h-4 text-red-400" />}
                        </div>
                        <div className="text-xs text-gray-400 flex items-center gap-2">
                          #{entry.player.number} • {entry.player.nationality} • {entry.player.role}
                          {entry.player.is_celebrity && (
                            <Badge className="bg-yellow-600/20 text-yellow-400 text-xs">STAR</Badge>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="text-green-400 text-sm font-bold">
                        {entry.game_stats.total_score} pts
                      </div>
                      <div className="text-xs text-gray-400">
                        <span 
                          className={`${entry.game_stats.kills > 0 ? 'cursor-pointer hover:text-red-300' : ''}`}
                          onClick={() => handleKillsClick(entry.player, entry.game_stats.kills)}
                        >
                          {entry.game_stats.survived_events} épreuves • {entry.game_stats.kills} K
                        </span>
                        {' • '}
                        {entry.game_stats.betrayals} T
                      </div>
                    </div>
                  </div>
                  
                  {/* Barre de progression du score */}
                  <div className="mt-2">
                    <div className="w-full bg-gray-700 rounded-full h-1">
                      <div 
                        className="bg-gradient-to-r from-green-500 to-blue-500 h-1 rounded-full transition-all"
                        style={{ 
                          width: `${Math.min(100, (entry.game_stats.total_score / Math.max(...rankingData.ranking.map(r => r.game_stats.total_score))) * 100)}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex justify-center gap-4 mt-8">
          <Button
            onClick={() => navigate('/')}
            variant="outline"
            className="border-gray-600 text-gray-300 hover:bg-gray-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour au menu
          </Button>
          <Button
            onClick={() => navigate('/statistics')}
            className="bg-red-600 hover:bg-red-700"
          >
            <Trophy className="w-4 h-4 mr-2" />
            Voir les statistiques
          </Button>
        </div>

        {/* Modal pour afficher les joueurs éliminés */}
        <EliminatedPlayersModal
          isOpen={showEliminatedModal}
          onClose={() => setShowEliminatedModal(false)}
          gameId={gameId}
          playerId={selectedPlayer?.id}
          playerName={selectedPlayer?.name}
        />
      </div>
    </div>
  );
};

export default FinalRanking;
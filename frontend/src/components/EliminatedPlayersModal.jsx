import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  X, 
  Skull, 
  Target,
  Crown
} from 'lucide-react';

const EliminatedPlayersModal = ({ isOpen, onClose, gameId, playerId, playerName }) => {
  const [eliminatedData, setEliminatedData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen && gameId && playerId) {
      loadEliminatedPlayers();
    }
  }, [isOpen, gameId, playerId]);

  const loadEliminatedPlayers = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/games/${gameId}/player/${playerId}/eliminated-players`);
      
      if (!response.ok) {
        throw new Error('Erreur lors du chargement des éliminations');
      }
      
      const data = await response.json();
      setEliminatedData(data);
    } catch (error) {
      console.error('Erreur lors du chargement des éliminations:', error);
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <Card className="bg-gray-900 border-red-500/30 w-full max-w-2xl max-h-[80vh] overflow-hidden">
        <CardHeader className="border-b border-red-500/30">
          <div className="flex items-center justify-between">
            <CardTitle className="text-white flex items-center gap-2">
              <Target className="w-5 h-5 text-red-400" />
              Joueurs éliminés par {playerName}
            </CardTitle>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="text-gray-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
        </CardHeader>
        
        <CardContent className="p-0 overflow-y-auto max-h-[60vh]">
          {isLoading && (
            <div className="flex items-center justify-center p-8">
              <div className="w-8 h-8 border-4 border-red-500 border-t-transparent rounded-full animate-spin"></div>
              <span className="ml-3 text-gray-400">Chargement...</span>
            </div>
          )}

          {error && (
            <div className="p-6 text-center">
              <p className="text-red-400 mb-4">Erreur: {error}</p>
              <Button 
                onClick={loadEliminatedPlayers}
                className="bg-red-600 hover:bg-red-700"
              >
                Réessayer
              </Button>
            </div>
          )}

          {eliminatedData && !isLoading && !error && (
            <div className="p-6">
              {eliminatedData.eliminated_players.length === 0 ? (
                <div className="text-center py-8">
                  <Skull className="w-12 h-12 text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-400">
                    {eliminatedData.killer.name} n'a éliminé aucun joueur.
                  </p>
                </div>
              ) : (
                <div>
                  <div className="mb-6 text-center">
                    <div className="text-xl font-bold text-white mb-2">
                      {eliminatedData.killer.name}
                    </div>
                    <Badge className="bg-red-600 text-white">
                      {eliminatedData.killer.total_kills} éliminations totales
                    </Badge>
                  </div>

                  <div className="space-y-3">
                    {eliminatedData.eliminated_players.map((player, index) => (
                      <div
                        key={player.id}
                        className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 transition-all hover:bg-red-900/30"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                              {player.number}
                            </div>
                            <div>
                              <div className="text-white font-medium flex items-center gap-2">
                                {player.name}
                                <Skull className="w-4 h-4 text-red-400" />
                              </div>
                              <div className="text-xs text-gray-400 flex items-center gap-2">
                                {player.nationality} • {player.role}
                              </div>
                            </div>
                          </div>
                          
                          <div className="text-right">
                            <div className="text-xs text-gray-400 space-y-1">
                              <div>Int: {player.stats.intelligence}</div>
                              <div>For: {player.stats.force}</div>
                              <div>Agi: {player.stats.agilité}</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </CardContent>
        
        <div className="border-t border-red-500/30 p-4">
          <div className="flex justify-end">
            <Button
              onClick={onClose}
              variant="outline"
              className="border-gray-600 text-gray-300 hover:bg-gray-700"
            >
              Fermer
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default EliminatedPlayersModal;
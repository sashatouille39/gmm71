import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import MainMenu from './components/MainMenu';
import GameSetup from './components/GameSetup';
import GameArena from './components/GameArena';
import Statistics from './components/Statistics';
import UniformCustomization from './components/UniformCustomization';
import VipSalon from './components/VipSalon';
import Settings from './components/Settings';
import PlayerCreator from './components/PlayerCreator';
import FinalRanking from './components/FinalRanking';
import { INITIAL_GAME_STATE } from './mock/mockData';

function App() {
  const [gameState, setGameState] = useState(INITIAL_GAME_STATE);
  const [currentGame, setCurrentGame] = useState(null);
  const [isLoadingGameState, setIsLoadingGameState] = useState(true);

  // Charger le gameState depuis le backend au démarrage
  useEffect(() => {
    loadGameStateFromBackend();
  }, []);

  const loadGameStateFromBackend = async () => {
    setIsLoadingGameState(true);
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/gamestate/`);
      
      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status}`);
      }
      
      const backendGameState = await response.json();
      
      // Adapter le format backend vers frontend
      const adaptedGameState = {
        money: backendGameState.money,
        vipSalonLevel: backendGameState.vip_salon_level,
        unlockedUniforms: backendGameState.unlocked_uniforms || [],
        unlockedPatterns: backendGameState.unlocked_patterns || [],
        ownedCelebrities: backendGameState.owned_celebrities || [],
        gameStats: {
          totalGamesPlayed: backendGameState.game_stats.total_games_played || 0,
          totalKills: backendGameState.game_stats.total_kills || 0,
          totalBetrayals: backendGameState.game_stats.total_betrayals || 0,
          totalEarnings: backendGameState.game_stats.total_earnings || 0,
          zeroAppearances: backendGameState.game_stats.zero_appearances || 0,
          favoriteCelebrity: backendGameState.game_stats.favorite_celebrity || null
        }
      };
      
      setGameState(adaptedGameState);
      console.log('GameState chargé depuis le backend:', adaptedGameState);
      
    } catch (error) {
      console.error('Erreur lors du chargement du gameState:', error);
      // Fallback vers état initial si erreur backend
      setGameState(INITIAL_GAME_STATE);
    }
    setIsLoadingGameState(false);
  };

  const updateGameState = async (updates) => {
    // Mettre à jour localement d'abord pour la réactivité
    setGameState(prev => ({ ...prev, ...updates }));
    
    // Puis synchroniser avec le backend
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      // Adapter les updates pour le format backend
      const backendUpdates = {};
      if (updates.money !== undefined) backendUpdates.money = updates.money;
      if (updates.vipSalonLevel !== undefined) backendUpdates.vip_salon_level = updates.vipSalonLevel;
      if (updates.unlockedUniforms !== undefined) backendUpdates.unlocked_uniforms = updates.unlockedUniforms;
      if (updates.unlockedPatterns !== undefined) backendUpdates.unlocked_patterns = updates.unlockedPatterns;
      if (updates.ownedCelebrities !== undefined) backendUpdates.owned_celebrities = updates.ownedCelebrities;
      if (updates.gameStats !== undefined) {
        backendUpdates.game_stats = {
          total_games_played: updates.gameStats.totalGamesPlayed,
          total_kills: updates.gameStats.totalKills,
          total_betrayals: updates.gameStats.totalBetrayals,
          total_earnings: updates.gameStats.totalEarnings,
          zero_appearances: updates.gameStats.zeroAppearances,
          favorite_celebrity: updates.gameStats.favoriteCelebrity
        };
      }
      
      await fetch(`${backendUrl}/api/gamestate/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(backendUpdates)
      });
      
      console.log('GameState synchronisé avec le backend:', backendUpdates);
      
    } catch (error) {
      console.error('Erreur lors de la synchronisation du gameState:', error);
      // En cas d'erreur, on garde les changements locaux mais on alerte
      alert('Erreur de synchronisation avec le serveur. Vos changements sont temporaires.');
    }
  };

  const startNewGame = async (players, selectedEvents, gameOptions = {}) => {
    try {
      // Créer la partie via l'API backend
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      // Séparer les joueurs manuels des autres
      const manualPlayers = players.filter(p => p.isCustom || p.isCelebrity);
      const playerCount = players.length;
      
      // Préparer les données pour l'API backend
      const gameRequest = {
        player_count: playerCount,
        manual_players: manualPlayers.map(player => ({
          name: player.name,
          nationality: player.nationality,
          gender: player.gender,
          role: player.role,
          stats: player.stats,
          portrait: player.portrait,
          uniform: player.uniform || {
            style: 'Standard',
            color: '#FF0000',
            pattern: 'Uni'
          }
        })),
        selected_events: gameOptions.selectedEventIds || selectedEvents.map(event => event.id),
        game_mode: gameOptions.gameMode || 'standard',
        preserve_event_order: gameOptions.preserveEventOrder !== undefined ? gameOptions.preserveEventOrder : true
      };

      const response = await fetch(`${backendUrl}/api/games/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(gameRequest)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Erreur API: ${response.status}`);
      }

      const game = await response.json();
      
      // Adapter le format de jeu pour le frontend
      setCurrentGame({
        id: game.id,
        players: game.players,
        events: game.events,
        currentEventIndex: game.current_event_index || 0,
        start_time: game.start_time,
        completed: game.completed || false,
        winner: game.winner || null,
        earnings: game.earnings || 0,
        total_cost: game.total_cost || 0,
        event_results: game.event_results || []
      });
      
      // IMPORTANT: Recharger le gameState depuis le backend après création
      // car le backend a automatiquement déduit l'argent
      await loadGameStateFromBackend();
      
      console.log('Partie créée avec succès:', {
        id: game.id,
        playersCount: game.players.length,
        eventsCount: game.events.length,
        totalCost: game.total_cost,
        preserveOrder: gameRequest.preserve_event_order
      });
      
    } catch (error) {
      console.error('Erreur lors de la création de la partie:', error);
      alert(`Erreur lors de la création de la partie: ${error.message}`);
      
      // Fallback vers création locale en cas d'erreur
      setCurrentGame({
        id: `local_${Date.now()}`,
        players,
        events: selectedEvents,
        currentEventIndex: 0,
        start_time: new Date(),
        completed: false,
        total_cost: 0,
        earnings: 0
      });
    }
  };

  return (
    <div className="App min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black">
      {isLoadingGameState ? (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 border-4 border-red-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-white text-lg">Chargement du Game Master Manager...</p>
            <p className="text-gray-400 text-sm mt-2">Synchronisation avec le serveur</p>
          </div>
        </div>
      ) : (
        <BrowserRouter>
          <Routes>
            <Route path="/" element={
              <MainMenu 
                gameState={gameState}
                hasActiveGame={!!currentGame}
                onRefreshGameState={loadGameStateFromBackend}
              />
            } />
            <Route path="/game-setup" element={
              <GameSetup 
                gameState={gameState}
                onStartGame={startNewGame}
                onRefreshGameState={loadGameStateFromBackend}
              />
            } />
            <Route path="/player-creator" element={
              <PlayerCreator 
                gameState={gameState}
                updateGameState={updateGameState}
              />
            } />
            <Route path="/game-arena" element={
              <GameArena 
                currentGame={currentGame}
                setCurrentGame={setCurrentGame}
                gameState={gameState}
                updateGameState={updateGameState}
                onRefreshGameState={loadGameStateFromBackend}
              />
            } />
            <Route path="/statistics" element={
              <Statistics 
                gameState={gameState}
              />
            } />
            <Route path="/uniform-customization" element={
              <UniformCustomization 
                gameState={gameState}
                updateGameState={updateGameState}
              />
            } />
            <Route path="/vip-salon" element={
              <VipSalon 
                gameState={gameState}
                updateGameState={updateGameState}
              />
            } />
            <Route path="/settings" element={
              <Settings 
                gameState={gameState}
                updateGameState={updateGameState}
              />
            } />
            <Route path="/final-ranking/:gameId" element={
              <FinalRanking />
            } />
          </Routes>
        </BrowserRouter>
      )}
    </div>
  );
}

export default App;
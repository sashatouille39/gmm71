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
import { INITIAL_GAME_STATE } from './mock/mockData';

function App() {
  const [gameState, setGameState] = useState(() => {
    const saved = localStorage.getItem('gamemaster-state');
    return saved ? JSON.parse(saved) : INITIAL_GAME_STATE;
  });

  const [currentGame, setCurrentGame] = useState(null);

  // Sauvegarde automatique
  useEffect(() => {
    localStorage.setItem('gamemaster-state', JSON.stringify(gameState));
  }, [gameState]);

  const updateGameState = (updates) => {
    setGameState(prev => ({ ...prev, ...updates }));
  };

  const startNewGame = async (players, selectedEvents) => {
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
        selected_events: selectedEvents.map(event => event.id),
        game_mode: 'standard'
      };

      const response = await fetch(`${backendUrl}/api/games/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(gameRequest)
      });

      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status}`);
      }

      const game = await response.json();
      
      // Adapter le format de jeu pour le frontend
      setCurrentGame({
        id: game.id,
        players: game.players,
        events: game.events,
        currentEventIndex: game.current_event_index || 0, // CORRECTION: utiliser camelCase pour cohérence frontend
        start_time: game.start_time,
        completed: game.completed || false,
        winner: game.winner || null,
        earnings: game.earnings || 0,
        event_results: game.event_results || []
      });
      
      console.log('Partie créée avec succès:', {
        id: game.id,
        playersCount: game.players.length,
        eventsCount: game.events.length
      });
      
    } catch (error) {
      console.error('Erreur lors de la création de la partie:', error);
      alert(`Erreur lors de la création de la partie: ${error.message}`);
      
      // Fallback vers création locale en cas d'erreur
      setCurrentGame({
        id: `local_${Date.now()}`,
        players,
        events: selectedEvents,
        currentEventIndex: 0, // CORRECTION: utiliser camelCase pour cohérence
        start_time: new Date(),
        completed: false
      });
    }
  };

  return (
    <div className="App min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-black">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={
            <MainMenu 
              gameState={gameState}
              hasActiveGame={!!currentGame}
            />
          } />
          <Route path="/game-setup" element={
            <GameSetup 
              gameState={gameState}
              onStartGame={startNewGame}
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
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
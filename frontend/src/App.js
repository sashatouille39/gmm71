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

  const startNewGame = (players, selectedEvents) => {
    setCurrentGame({
      id: Date.now(),
      players,
      events: selectedEvents,
      currentEventIndex: 0,
      startTime: new Date(),
      completed: false
    });
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
import { useState, useEffect } from 'react';

export const useCustomPlayers = () => {
  const [customPlayers, setCustomPlayers] = useState([]);

  // Charger les joueurs depuis le localStorage
  useEffect(() => {
    const saved = localStorage.getItem('gamemaster-custom-players');
    if (saved) {
      try {
        setCustomPlayers(JSON.parse(saved));
      } catch (error) {
        console.error('Error loading custom players:', error);
        setCustomPlayers([]);
      }
    }
  }, []);

  // Sauvegarder automatiquement
  useEffect(() => {
    localStorage.setItem('gamemaster-custom-players', JSON.stringify(customPlayers));
  }, [customPlayers]);

  const addPlayer = (player) => {
    console.log('🔍 DEBUG: Adding player:', player);
    const newPlayer = {
      ...player,
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
      isCustom: true
    };
    console.log('🔍 DEBUG: New player with ID:', newPlayer);
    setCustomPlayers(prev => {
      const updated = [...prev, newPlayer];
      console.log('🔍 DEBUG: Updated customPlayers list:', updated);
      return updated;
    });
    return newPlayer;
  };

  const removePlayer = (playerId) => {
    setCustomPlayers(prev => prev.filter(p => p.id !== playerId));
  };

  const updatePlayer = (playerId, updates) => {
    setCustomPlayers(prev => 
      prev.map(p => p.id === playerId ? { ...p, ...updates } : p)
    );
  };

  const getPlayerById = (playerId) => {
    return customPlayers.find(p => p.id === playerId);
  };

  const duplicatePlayer = (playerId) => {
    const player = getPlayerById(playerId);
    if (player) {
      const duplicated = {
        ...player,
        id: Date.now().toString(),
        name: `${player.name} (Copie)`,
        createdAt: new Date().toISOString()
      };
      setCustomPlayers(prev => [...prev, duplicated]);
      return duplicated;
    }
    return null;
  };

  return {
    customPlayers,
    addPlayer,
    removePlayer,
    updatePlayer,
    getPlayerById,
    duplicatePlayer
  };
};
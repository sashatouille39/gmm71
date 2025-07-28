import { useState, useEffect, useCallback } from 'react';

export const useCustomPlayers = () => {
  const [customPlayers, setCustomPlayers] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);

  // Fonction pour charger les données depuis localStorage
  const loadFromStorage = useCallback(() => {
    const saved = localStorage.getItem('gamemaster-custom-players');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setCustomPlayers(parsed);
      } catch (error) {
        console.error('Error loading custom players:', error);
        setCustomPlayers([]);
      }
    } else {
      setCustomPlayers([]);
    }
  }, []);

  // Charger les joueurs depuis le localStorage au montage
  useEffect(() => {
    loadFromStorage();
    setIsLoaded(true);
  }, [loadFromStorage]);

  // Écouter les changements d'autres instances du hook
  useEffect(() => {
    const handleCustomPlayersChanged = (event) => {
      console.log('🔍 DEBUG: Received customPlayersChanged event:', event.detail);
      setCustomPlayers(event.detail);
    };

    window.addEventListener('customPlayersChanged', handleCustomPlayersChanged);
    
    return () => {
      window.removeEventListener('customPlayersChanged', handleCustomPlayersChanged);
    };
  }, []);

  // Sauvegarder automatiquement (seulement après le chargement initial)
  useEffect(() => {
    if (!isLoaded) return; // Ne pas sauvegarder pendant le chargement initial
    
    console.log('🔍 DEBUG: Saving to localStorage:', customPlayers);
    localStorage.setItem('gamemaster-custom-players', JSON.stringify(customPlayers));
    
    // Dispatch un événement custom pour notifier les autres composants
    window.dispatchEvent(new CustomEvent('customPlayersChanged', { 
      detail: customPlayers 
    }));
  }, [customPlayers, isLoaded]);

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
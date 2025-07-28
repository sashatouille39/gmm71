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
    
    localStorage.setItem('gamemaster-custom-players', JSON.stringify(customPlayers));
    
    // NE PAS dispatch d'événement automatiquement pour éviter race conditions
    // Les événements seront dispatché seulement lors d'opérations explicites
  }, [customPlayers, isLoaded]);

  const addPlayer = (player) => {
    const newPlayer = {
      ...player,
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
      isCustom: true
    };
    setCustomPlayers(prev => {
      const updated = [...prev, newPlayer];
      // Dispatch l'événement seulement lors d'ajout explicite
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('customPlayersChanged', { 
          detail: updated 
        }));
      }, 0);
      return updated;
    });
    return newPlayer;
  };

  const removePlayer = (playerId) => {
    setCustomPlayers(prev => {
      const updated = prev.filter(p => p.id !== playerId);
      // Dispatch l'événement lors de suppression explicite
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('customPlayersChanged', { 
          detail: updated 
        }));
      }, 0);
      return updated;
    });
  };

  const updatePlayer = (playerId, updates) => {
    setCustomPlayers(prev => {
      const updated = prev.map(p => p.id === playerId ? { ...p, ...updates } : p);
      // Dispatch l'événement lors de mise à jour explicite
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('customPlayersChanged', { 
          detail: updated 
        }));
      }, 0);
      return updated;
    });
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
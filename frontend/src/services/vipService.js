// Service pour gérer les VIPs
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

export const vipService = {
  // Récupère les VIPs pour un niveau de salon donné
  async getSalonVips(salonLevel) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/vips/salon/${salonLevel}`);
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la récupération des VIPs du salon:', error);
      throw error;
    }
  },

  // Récupère les VIPs pour une partie spécifique
  async getGameVips(gameId, salonLevel = 1) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/vips/game/${gameId}?salon_level=${salonLevel}`);
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la récupération des VIPs de la partie:', error);
      throw error;
    }
  },

  // Rafraîchit les VIPs pour une nouvelle partie
  async refreshGameVips(gameId, salonLevel = 1) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/vips/game/${gameId}/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ salon_level: salonLevel })
      });
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Erreur lors du rafraîchissement des VIPs:', error);
      throw error;
    }
  },

  // Récupère tous les VIPs disponibles
  async getAllVips() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/vips/all`);
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la récupération de tous les VIPs:', error);
      throw error;
    }
  },

  // Crée un pari VIP
  async createVipBet(vipId, gameId, playerId, amount, eventId = null) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/vips/bet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vip_id: vipId,
          game_id: gameId,
          player_id: playerId,
          amount: amount,
          event_id: eventId
        })
      });
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la création du pari VIP:', error);
      throw error;
    }
  },

  // Récupère les gains VIP pour une partie
  async getVipEarnings(gameId) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/vips/earnings/${gameId}`);
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la récupération des gains VIP:', error);
      throw error;
    }
  }
};

export default vipService;
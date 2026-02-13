import random
from enum import Enum
from typing import List, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


# Dépendances supposées
class Action(Enum):
    TAKE = 0
    STOP = 1


# --- Réseau de neurones simple (Approximateur de fonctions) ---
class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 24)
        self.fc2 = nn.Linear(24, 24)
        self.fc3 = nn.Linear(24, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


# --- Classe QTable adaptée pour le Deep Learning ---
class QTable:
    def __init__(
        self, state_dim: int, actions: List[Action], learning_rate: float = 0.001
    ):
        self.actions = actions
        self.action_dim = len(actions)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Le réseau de neurones
        self.network = QNetwork(state_dim, self.action_dim).to(self.device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()

    def _state_to_tensor(self, state: Tuple[int, ...]) -> torch.Tensor:
        # Convertit le tuple d'état en tenseur PyTorch pour le réseau
        # On peut avoir besoin de normaliser ici si les valeurs sont grandes
        return torch.FloatTensor(state).unsqueeze(0).to(self.device)

    def get_q_values(self, state: Tuple[int, ...]) -> torch.Tensor:
        """Retourne toutes les valeurs Q pour un état donné."""
        state_tensor = self._state_to_tensor(state)
        with torch.no_grad():
            return self.network(state_tensor)

    def get_q_value(self, state: Tuple[int, ...], action: Action) -> float:
        q_values = self.get_q_values(state)
        return q_values[0][action.value].item()

    def get_max_q(self, state: Tuple[int, ...]) -> float:
        q_values = self.get_q_values(state)
        return torch.max(q_values).item()

    def get_best_action(self, state: Tuple[int, ...]) -> Action:
        q_values = self.get_q_values(state)
        action_idx = torch.argmax(q_values).item()
        return self.actions[action_idx]

    def set_q_value(self, state: Tuple[int, ...], action: Action, target_q: float):
        """Met à jour le réseau de neurones (apprentissage)."""
        state_tensor = self._state_to_tensor(state)

        # Prédiction actuelle
        current_q = self.network(state_tensor)[0][action.value]

        # Calcul de la perte et rétropropagation
        target_q_tensor = torch.tensor([target_q], device=self.device)
        loss = self.criterion(current_q, target_q_tensor)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

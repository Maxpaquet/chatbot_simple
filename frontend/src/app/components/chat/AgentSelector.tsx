// frontend/src/app/components/chat/AgentSelector.tsx
"use client";

import React from 'react';

interface AgentSelectorProps {
    agents: string[];
    selectedAgent: string | null;
    onSelectAgent: (agent: string) => void;
}

const AgentSelector: React.FC<AgentSelectorProps> = ({ agents, selectedAgent, onSelectAgent }) => {
    return (
        <div className="flex items-center space-x-2">
            <label htmlFor="agent-select" className="text-sm font-medium text-gray-700">Agent:</label>
            <select
                id="agent-select"
                value={selectedAgent || ''}
                onChange={(e) => onSelectAgent(e.target.value)}
                className="p-2 rounded-md border border-gray-300 bg-gray-50 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                {agents.map((agent) => (
                    <option key={agent} value={agent}>
                        {agent}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default AgentSelector;

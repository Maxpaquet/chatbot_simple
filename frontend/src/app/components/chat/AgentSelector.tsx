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
        <div className="flex items-center gap-2">
            <label 
                htmlFor="agent-select" 
                className="text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap flex items-center gap-1.5"
            >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
                </svg>
                <span className="hidden sm:inline">Agent:</span>
            </label>
            <div className="relative">
                <select
                    id="agent-select"
                    value={selectedAgent || ''}
                    onChange={(e) => onSelectAgent(e.target.value)}
                    className="appearance-none pl-3 pr-10 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-sm hover:shadow cursor-pointer"
                    aria-label="Sélectionner un agent"
                >
                    {agents.map((agent) => (
                        <option key={agent} value={agent}>
                            {agent}
                        </option>
                    ))}
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500 dark:text-gray-400">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                </div>
            </div>
        </div>
    );
};

export default AgentSelector;

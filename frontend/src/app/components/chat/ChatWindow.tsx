// frontend/src/app/components/chat/ChatWindow.tsx
"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Message, getThreadMessages, postMessage, getAgents } from '../../lib/api';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import AgentSelector from './AgentSelector';
import TypingIndicator from './TypingIndicator';

const ChatWindow: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [threadId, setThreadId] = useState<string>('default-thread'); // Static thread ID for now
    const [agents, setAgents] = useState<string[]>([]);
    const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isInitializing, setIsInitializing] = useState(true);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const messagesContainerRef = useRef<HTMLDivElement>(null);
    const userScrolledRef = useRef(false);

    const scrollToBottom = (force = false) => {
        if (force || !userScrolledRef.current) {
            messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
        }
    };

    const handleScroll = () => {
        if (!messagesContainerRef.current) return;
        const { scrollTop, scrollHeight, clientHeight } = messagesContainerRef.current;
        const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;
        userScrolledRef.current = !isNearBottom;
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        const fetchInitialData = async () => {
            setIsInitializing(true);
            setError(null);
            try {
                const agentData = await getAgents();
                setAgents(agentData.names);
                if (agentData.names.length > 0) {
                    setSelectedAgent(agentData.names[0]);
                }

                const threadData = await getThreadMessages(threadId);
                setMessages(threadData.conversation);
            } catch (error) {
                console.error("Initialization failed:", error);
                setError('Impossible de charger la conversation. Veuillez rafraîchir la page.');
            } finally {
                setIsInitializing(false);
            }
        };
        fetchInitialData();
    }, [threadId]);

    const handleSendMessage = async (content: string) => {
        const userMessage: Message = {
            id: `user-${Date.now()}`,
            author: 'user',
            content: content,
        };
        
        // Optimistic UI update
        setMessages(prevMessages => [...prevMessages, userMessage]);
        setIsLoading(true);
        setError(null);
        userScrolledRef.current = false; // Force scroll on new message

        try {
            await postMessage(threadId, userMessage, selectedAgent);
            const threadData = await getThreadMessages(threadId);
            setMessages(threadData.conversation);
        } catch (error) {
            console.error('Failed to send message:', error);
            const errorMsg = error instanceof Error ? error.message : 'Erreur inconnue';
            setError(`Échec de l'envoi du message: ${errorMsg}`);
            
            // Remove the optimistic message on error
            setMessages(prevMessages => 
                prevMessages.filter(msg => msg.id !== userMessage.id)
            );
        } finally {
            setIsLoading(false);
        }
    };

    if (isInitializing) {
        return (
            <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900 items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-gray-600 dark:text-gray-400">Chargement...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900 transition-colors">
            <div className="flex-1 flex flex-col items-center justify-center p-2 sm:p-4 overflow-hidden">
                <div className="w-full max-w-5xl flex flex-col h-full bg-white dark:bg-gray-800 rounded-xl shadow-2xl transition-colors">
                    {/* Header */}
                    <header className="bg-gradient-to-r from-blue-600 to-blue-700 dark:from-blue-700 dark:to-blue-800 text-white p-4 sm:p-6 flex justify-between items-center rounded-t-xl shadow-md">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                                </svg>
                            </div>
                            <div>
                                <h1 className="text-xl sm:text-2xl font-bold">Assistant Chatbot</h1>
                                <p className="text-xs sm:text-sm text-blue-100">Toujours là pour vous aider</p>
                            </div>
                        </div>
                        {selectedAgent && (
                            <div className="hidden sm:flex items-center gap-2 bg-white/10 px-3 py-1.5 rounded-full text-sm">
                                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                                <span>{selectedAgent}</span>
                            </div>
                        )}
                    </header>

                    {/* Error Banner */}
                    {error && (
                        <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 m-4 rounded-r-lg flex items-start gap-3 animate-in slide-in-from-top">
                            <svg className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                            <div className="flex-1">
                                <p className="text-red-800 dark:text-red-200 text-sm font-medium">{error}</p>
                            </div>
                            <button
                                onClick={() => setError(null)}
                                className="text-red-500 hover:text-red-700 transition-colors"
                                aria-label="Fermer l'erreur"
                            >
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                                </svg>
                            </button>
                        </div>
                    )}

                    {/* Messages Area */}
                    <main 
                        ref={messagesContainerRef}
                        onScroll={handleScroll}
                        className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 scroll-smooth"
                    >
                        {messages.length === 0 && !isLoading ? (
                            <div className="flex flex-col items-center justify-center h-full text-center p-8">
                                <div className="w-20 h-20 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mb-4">
                                    <svg className="w-10 h-10 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                                    </svg>
                                </div>
                                <h2 className="text-xl sm:text-2xl font-semibold text-gray-800 dark:text-gray-200 mb-2">
                                    Commencez une conversation
                                </h2>
                                <p className="text-gray-500 dark:text-gray-400 max-w-md">
                                    Posez-moi n'importe quelle question et je ferai de mon mieux pour vous aider !
                                </p>
                            </div>
                        ) : (
                            <>
                                <MessageList messages={messages} />
                                {isLoading && <TypingIndicator />}
                            </>
                        )}
                        <div ref={messagesEndRef} />
                    </main>

                    {/* Footer / Input Area */}
                    <footer className="p-3 sm:p-4 bg-gray-50 dark:bg-gray-900/50 border-t border-gray-200 dark:border-gray-700 rounded-b-xl">
                        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                            <AgentSelector 
                                agents={agents} 
                                selectedAgent={selectedAgent} 
                                onSelectAgent={setSelectedAgent} 
                            />
                            <MessageInput 
                                onSendMessage={handleSendMessage} 
                                isLoading={isLoading} 
                                className="flex-1" 
                            />
                        </div>
                    </footer>
                </div>
            </div>
        </div>
    );
};

export default ChatWindow;


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
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        const fetchInitialData = async () => {
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
        setMessages(prevMessages => [...prevMessages, userMessage]);
        setIsLoading(true);

        try {
            await postMessage(threadId, userMessage, selectedAgent);
            const threadData = await getThreadMessages(threadId);
            setMessages(threadData.conversation);

        } catch (error) {
            console.error('Failed to send message:', error);
            const errorMessage: Message = {
                id: `error-${Date.now()}`,
                author: 'system',
                content: 'Error sending message. Please try again.',
            };
            setMessages(prevMessages => [...prevMessages, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-200">
            <div className="flex-1 flex flex-col items-center justify-center p-4 overflow-hidden">
                <div className="w-full max-w-4xl flex flex-col h-full bg-white rounded-xl shadow-lg">
                    <header className="bg-blue-600 text-white p-4 flex justify-between items-center rounded-t-xl">
                        <h1 className="text-2xl font-bold">Chatbot</h1>
                    </header>
                    <main className="flex-1 overflow-y-auto p-6 space-y-6">
                        <MessageList messages={messages} />
                        {isLoading && <TypingIndicator />}
                        <div ref={messagesEndRef} />
                    </main>
                    <footer className="p-4 bg-gray-50 border-t rounded-b-xl flex items-center gap-4">
                        <AgentSelector agents={agents} selectedAgent={selectedAgent} onSelectAgent={setSelectedAgent} />
                        <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} className="flex-1" />
                    </footer>
                </div>
            </div>
        </div>
    );
};

export default ChatWindow;


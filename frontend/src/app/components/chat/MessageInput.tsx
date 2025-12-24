// frontend/src/app/components/chat/MessageInput.tsx
"use client";

import React, { useState } from 'react';

interface MessageInputProps {
    onSendMessage: (content: string) => void;
    isLoading: boolean;
    className?: string;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, isLoading, className }) => {
    const [content, setContent] = useState('');

    const handleSendMessage = () => {
        if (content.trim() && !isLoading) {
            onSendMessage(content);
            setContent('');
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        handleSendMessage();
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <form onSubmit={handleSubmit} className={`flex items-center gap-2 ${className || ''}`}>
            <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message... (Shift+Enter for new line)"
                className="flex-1 p-3 bg-gray-100 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 text-black transition-shadow"
                disabled={isLoading}
                rows={1}
                style={{ maxHeight: '150px' }}
            />
            <button
                type="submit"
                className="p-3 bg-blue-600 text-white rounded-full disabled:bg-blue-300 hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                disabled={isLoading || !content.trim()}
            >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
                </svg>
            </button>
        </form>
    );
};

export default MessageInput;

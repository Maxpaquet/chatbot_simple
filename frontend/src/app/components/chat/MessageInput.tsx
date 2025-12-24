// frontend/src/app/components/chat/MessageInput.tsx
"use client";

import React, { useState, useRef, useEffect } from 'react';

interface MessageInputProps {
    onSendMessage: (content: string) => void;
    isLoading: boolean;
    className?: string;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, isLoading, className }) => {
    const [content, setContent] = useState('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    // Auto-resize textarea
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
        }
    }, [content]);

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

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setContent(e.target.value);
    };

    return (
        <form onSubmit={handleSubmit} className={`flex items-end gap-2 ${className || ''}`}>
            <div className="flex-1 relative">
                <textarea
                    ref={textareaRef}
                    value={content}
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
                    placeholder="Tapez votre message... (Shift+Enter pour nouvelle ligne)"
                    className="w-full p-3 pr-12 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 transition-all shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={isLoading}
                    rows={1}
                    style={{ 
                        minHeight: '48px',
                        maxHeight: '150px',
                        overflowY: 'auto'
                    }}
                    aria-label="Message input"
                />
                {/* Character count indicator for long messages */}
                {content.length > 200 && (
                    <div className="absolute bottom-2 right-2 text-xs text-gray-400 dark:text-gray-500">
                        {content.length}
                    </div>
                )}
            </div>
            <button
                type="submit"
                className="p-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-full disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed hover:from-blue-700 hover:to-blue-800 active:scale-95 transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-lg hover:shadow-xl disabled:shadow-none group"
                disabled={isLoading || !content.trim()}
                aria-label="Envoyer le message"
            >
                {isLoading ? (
                    <svg className="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 transform group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                )}
            </button>
        </form>
    );
};

export default MessageInput;

// frontend/src/app/components/chat/MessageList.tsx
import React from 'react';
import { Message } from '../../lib/api';
import ReactMarkdown from 'react-markdown';

interface MessageListProps {
    messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
    const getAuthorIcon = (author: string) => {
        if (author === 'user') {
            return (
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white flex-shrink-0">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                </div>
            );
        } else if (author === 'agent') {
            return (
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center text-white flex-shrink-0">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
                        <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
                    </svg>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="space-y-4">
            {messages.map((msg, index) => (
                <div
                    key={msg.id}
                    className={`flex items-end gap-2 sm:gap-3 animate-in slide-in-from-bottom duration-300 ${
                        msg.author === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                    style={{ animationDelay: `${index * 50}ms` }}
                >
                    {/* Avatar for agent messages */}
                    {msg.author !== 'user' && getAuthorIcon(msg.author)}
                    
                    <div className="flex flex-col max-w-[85%] sm:max-w-xl md:max-w-2xl">
                        {/* Author label for non-user messages */}
                        {msg.author !== 'user' && (
                            <span className="text-xs text-gray-500 dark:text-gray-400 mb-1 ml-1 font-medium capitalize">
                                {msg.author}
                            </span>
                        )}
                        
                        <div
                            className={`group relative px-4 py-3 rounded-2xl shadow-sm hover:shadow-md transition-all ${
                                msg.author === 'user'
                                    ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-br-sm'
                                    : msg.author === 'system'
                                    ? 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-900 dark:text-yellow-200 border border-yellow-200 dark:border-yellow-800 rounded-bl-sm'
                                    : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-sm'
                            }`}
                        >
                            <div className={`text-sm leading-relaxed prose prose-sm max-w-none ${
                                msg.author === 'user' 
                                    ? 'prose-invert' 
                                    : 'dark:prose-invert'
                            }`}>
                                <ReactMarkdown
                                    components={{
                                        p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                                        code: ({node, inline, ...props}) => 
                                            inline ? (
                                                <code className="px-1.5 py-0.5 rounded bg-black/10 dark:bg-white/10" {...props} />
                                            ) : (
                                                <code className="block p-2 rounded bg-black/10 dark:bg-white/10 overflow-x-auto" {...props} />
                                            )
                                    }}
                                >
                                    {msg.content}
                                </ReactMarkdown>
                            </div>
                            
                            {/* Timestamp */}
                            {msg.timestamp && (
                                <p className={`text-xs mt-1.5 flex items-center gap-1 ${
                                    msg.author === 'user' 
                                        ? 'text-blue-100 justify-end' 
                                        : 'text-gray-500 dark:text-gray-400 justify-start'
                                }`}>
                                    <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                                    </svg>
                                    {new Date(msg.timestamp).toLocaleTimeString('fr-FR', { 
                                        hour: '2-digit', 
                                        minute: '2-digit' 
                                    })}
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Avatar for user messages */}
                    {msg.author === 'user' && getAuthorIcon(msg.author)}
                </div>
            ))}
        </div>
    );
};

export default MessageList;

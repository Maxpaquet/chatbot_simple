// frontend/src/app/components/chat/MessageList.tsx
import React from 'react';
import { Message } from '../../lib/api';
import ReactMarkdown from 'react-markdown';

interface MessageListProps {
    messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
    return (
        <div className="space-y-5">
            {messages.map((msg) => (
                <div
                    key={msg.id}
                    className={`flex items-end gap-3 ${msg.author === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                    {/* Optional: Avatar can be added here */}
                    {/* <div className="w-8 h-8 rounded-full bg-gray-300"></div> */}
                    <div
                        className={`max-w-lg px-4 py-3 rounded-2xl shadow-md ${
                            msg.author === 'user'
                                ? 'bg-blue-500 text-white rounded-br-none'
                                : 'bg-gray-200 text-gray-800 rounded-bl-none'
                        }`}
                    >
                        <div className="text-sm whitespace-pre-wrap">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                        {msg.timestamp && (
                            <p className={`text-xs text-right mt-1 ${msg.author === 'user' ? 'text-blue-200' : 'text-gray-500'}`}>
                                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </p>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default MessageList;

// frontend/src/app/components/chat/TypingIndicator.tsx
import React from 'react';

const TypingIndicator: React.FC = () => {
    return (
        <div className="flex justify-start">
            <div className="bg-gray-300 text-black p-2 rounded-lg flex items-center space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
            </div>
        </div>
    );
};

export default TypingIndicator;

// frontend/src/app/lib/api.ts

export interface Message {
  id: string;
  author: 'user' | 'agent' | 'tool' | 'system';
  content: string;
  timestamp?: string;
}

export interface Thread {
  thread_id: string;
  conversation: Message[];
}

export interface AgentNames {
  names: string[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function getAgents(): Promise<AgentNames> {
  const response = await fetch(`${API_BASE_URL}/agent/list/agents`);
  if (!response.ok) {
    throw new Error('Failed to fetch agents');
  }
  return response.json();
}

export async function getThreadMessages(thread_id: string): Promise<Thread> {
  const response = await fetch(`${API_BASE_URL}/agent/chat/thread/${thread_id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch thread messages');
  }
  return response.json();
}

export interface StreamCallbacks {
  onStart?: () => void;
  onToken?: (token: string) => void;
  onComplete?: () => void;
  onError?: (error: Error) => void;
}

export async function postMessage(
  thread_id: string,
  message: Omit<Message, 'timestamp'>,
  agent_id: string | null,
  callbacks?: StreamCallbacks
): Promise<any> {
    try {
        callbacks?.onStart?.();
        
        const response = await fetch(`${API_BASE_URL}/agent/chat/${thread_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                thread_id: thread_id,
                input: message,
                agent_id: agent_id,
            }),
        });

        if (!response.ok) {
            const error = new Error(`Failed to post message: ${response.statusText}`);
            callbacks?.onError?.(error);
            throw error;
        }

        const reader = response.body?.getReader();
        if (!reader) {
            const error = new Error('Failed to read response stream');
            callbacks?.onError?.(error);
            throw error;
        }

        let result = '';
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                break;
            }
            const chunk = decoder.decode(value, { stream: true });
            result += chunk;
            callbacks?.onToken?.(chunk);
        }

        // Parse the final result
        try {
            const lastDataIndex = result.lastIndexOf('data:');
            if (lastDataIndex !== -1) {
                const jsonString = result.substring(lastDataIndex + 5).trim();
                if (jsonString === '[DONE]') {
                    callbacks?.onComplete?.();
                    return null;
                }
                const eventData = JSON.parse(jsonString);
                if (eventData.event === 'on_chat_model_end') {
                    callbacks?.onComplete?.();
                    return eventData.data;
                }
            }
            callbacks?.onComplete?.();
            return null;
        } catch (error) {
            console.error('Error parsing streaming response:', error);
            const err = error instanceof Error ? error : new Error('Unknown error parsing response');
            callbacks?.onError?.(err);
            return null;
        }
    } catch (error) {
        const err = error instanceof Error ? error : new Error('Unknown error');
        callbacks?.onError?.(err);
        throw err;
    }
}


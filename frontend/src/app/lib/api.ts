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

export async function postMessage(thread_id: string, message: Omit<Message, 'timestamp'>, agent_id: string | null): Promise<any> {
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
        throw new Error('Failed to post message');
    }

    // The response is a stream of events. For now, we'll just read the stream until it's done.
    // A more robust implementation would handle each event as it arrives.
    const reader = response.body?.getReader();
    if (!reader) {
        throw new Error('Failed to read response stream');
    }

    let result = '';
    while (true) {
        const { done, value } = await reader.read();
        if (done) {
            break;
        }
        result += new TextDecoder().decode(value);
    }

    // Attempt to parse the concatenated JSON objects.
    // This is a simplification. In a real app, you'd parse the stream of JSON objects correctly.
    try {
        // Find the last 'data:' event which should contain the final message
        const lastDataIndex = result.lastIndexOf('data:');
        if (lastDataIndex !== -1) {
            const jsonString = result.substring(lastDataIndex + 5).trim();
            if (jsonString === '[DONE]') {
                return null;
            }
            const eventData = JSON.parse(jsonString);
            if (eventData.event === 'on_chat_model_end') {
                 return eventData.data;
            }
        }
        return null;
    } catch (error) {
        console.error('Error parsing streaming response:', error);
        return null;
    }
}


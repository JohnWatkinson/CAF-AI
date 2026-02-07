import { useState, useEffect, useCallback } from 'react';
import { sendMessage, getErrorMessage } from '@/lib/api';

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  isError?: boolean;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasStarted, setHasStarted] = useState(false);

  const addMessage = useCallback((content: string, role: 'user' | 'assistant', isError = false) => {
    const newMessage: Message = {
      id: crypto.randomUUID(),
      content,
      role,
      timestamp: new Date(),
      isError,
    };
    setMessages((prev) => [...prev, newMessage]);
    return newMessage;
  }, []);

  const send = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return;

    addMessage(content, 'user');
    setIsLoading(true);

    try {
      const response = await sendMessage(content, sessionId);
      setSessionId(response.session_id);
      addMessage(response.reply, 'assistant');
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      addMessage(errorMessage, 'assistant', true);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, isLoading, addMessage]);

  const reset = useCallback(() => {
    setMessages([]);
    setSessionId(null);
    setHasStarted(false);
  }, []);

  // Auto-start conversation on mount
  useEffect(() => {
    if (!hasStarted) {
      setHasStarted(true);
      send('Ciao');
    }
  }, [hasStarted, send]);

  return {
    messages,
    isLoading,
    send,
    reset,
  };
}

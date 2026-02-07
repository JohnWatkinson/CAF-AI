const API_URL = import.meta.env.VITE_API_URL || '';

export interface ChatRequest {
  message: string;
  session_id: string | null;
}

export interface ChatResponse {
  reply: string;
  session_id: string;
}

export async function sendMessage(message: string, sessionId: string | null): Promise<ChatResponse> {
  const url = `${API_URL}/chat`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
    } as ChatRequest),
  });

  if (!response.ok) {
    if (response.status >= 500) {
      throw new Error('SERVER_ERROR');
    }
    if (response.status >= 400) {
      throw new Error('CLIENT_ERROR');
    }
    throw new Error('UNKNOWN_ERROR');
  }

  return response.json();
}

export function getErrorMessage(error: unknown): string {
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return 'Connessione non riuscita. Verifica la tua connessione internet e riprova.';
  }
  
  if (error instanceof Error) {
    switch (error.message) {
      case 'SERVER_ERROR':
        return 'Si è verificato un problema con il servizio. Riprova tra qualche minuto.';
      case 'CLIENT_ERROR':
        return 'Richiesta non valida. Riprova con un messaggio diverso.';
      default:
        return 'Si è verificato un errore imprevisto. Riprova.';
    }
  }
  
  return 'Si è verificato un errore imprevisto. Riprova.';
}

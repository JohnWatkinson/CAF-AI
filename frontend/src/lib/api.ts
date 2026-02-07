const API_URL = import.meta.env.VITE_API_URL || '';

export interface ChatRequest {
  message: string;
  session_id: string | null;
}

export interface ChatResponse {
  reply: string;
  session_id: string;
}

const MAX_RETRIES = 2;
const RETRY_DELAYS = [2000, 5000]; // ms

export async function sendMessage(message: string, sessionId: string | null): Promise<ChatResponse> {
  const url = `${API_URL}/chat`;
  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
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
        if (response.status >= 500 && attempt < MAX_RETRIES) {
          lastError = new Error('SERVER_ERROR');
          await new Promise(r => setTimeout(r, RETRY_DELAYS[attempt]));
          continue;
        }
        if (response.status >= 500) throw new Error('SERVER_ERROR');
        if (response.status >= 400) throw new Error('CLIENT_ERROR');
        throw new Error('UNKNOWN_ERROR');
      }

      return response.json();
    } catch (error) {
      // Network error (fetch failed) — retry
      if (error instanceof TypeError && attempt < MAX_RETRIES) {
        lastError = error;
        await new Promise(r => setTimeout(r, RETRY_DELAYS[attempt]));
        continue;
      }
      throw error;
    }
  }

  throw lastError || new Error('UNKNOWN_ERROR');
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

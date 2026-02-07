import ReactMarkdown from 'react-markdown';
import { cn } from '@/lib/utils';
import { AlertCircle } from 'lucide-react';
import type { Message } from '@/hooks/useChat';

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const isError = message.isError;

  return (
    <div
      className={cn(
        'flex w-full',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          'max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 shadow-sm',
          isUser 
            ? 'bg-user-message text-user-message-foreground rounded-br-md' 
            : 'bg-assistant-message text-assistant-message-foreground rounded-bl-md',
          isError && 'border-2 border-destructive/30 bg-destructive/5'
        )}
      >
        {isError && (
          <div className="flex items-center gap-2 mb-2 text-destructive">
            <AlertCircle className="h-5 w-5" />
            <span className="font-medium">Errore</span>
          </div>
        )}
        <div className="prose prose-sm max-w-none dark:prose-invert">
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>,
              strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
              ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-1">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-1">{children}</ol>,
              li: ({ children }) => <li className="leading-relaxed">{children}</li>,
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}

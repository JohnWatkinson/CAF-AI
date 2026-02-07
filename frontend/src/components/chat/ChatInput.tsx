import { useState, FormEvent, KeyboardEvent } from 'react';
import { Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="border-t bg-background px-4 py-4">
      <form 
        onSubmit={handleSubmit} 
        className="max-w-3xl mx-auto flex gap-3"
      >
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Scrivi la tua domanda sull'IMU..."
          disabled={isLoading}
          className="min-h-[56px] max-h-32 resize-none text-base focus-ring"
          rows={1}
        />
        <Button 
          type="submit" 
          size="lg"
          disabled={!input.trim() || isLoading}
          className="h-14 w-14 shrink-0"
        >
          <Send className="h-5 w-5" />
          <span className="sr-only">Invia</span>
        </Button>
      </form>
    </div>
  );
}

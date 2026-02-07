import { Building2, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ChatHeaderProps {
  onReset: () => void;
}

export function ChatHeader({ onReset }: ChatHeaderProps) {
  return (
    <header className="bg-primary text-primary-foreground px-4 py-4 shadow-md">
      <div className="max-w-3xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-primary-foreground/10 p-2 rounded-lg">
            <Building2 className="h-7 w-7" />
          </div>
          <div>
            <h1 className="text-xl font-semibold tracking-tight">Assistente IMU</h1>
            <p className="text-sm text-primary-foreground/80">Calcolo Imposta Municipale — beta</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="lg"
          onClick={onReset}
          className="text-primary-foreground hover:bg-primary-foreground/10 h-12 px-4 gap-2"
        >
          <RefreshCw className="h-5 w-5" />
          <span className="hidden sm:inline">Nuova conversazione</span>
        </Button>
      </div>
    </header>
  );
}

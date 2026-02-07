export function LoadingIndicator() {
  return (
    <div className="flex items-center gap-2 text-muted-foreground px-4 py-3">
      <span className="text-base">Sto pensando</span>
      <span className="flex gap-1">
        <span className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse-dot" style={{ animationDelay: '0ms' }} />
        <span className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse-dot" style={{ animationDelay: '200ms' }} />
        <span className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse-dot" style={{ animationDelay: '400ms' }} />
      </span>
    </div>
  );
}

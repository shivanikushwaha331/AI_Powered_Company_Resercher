import React from "react";

export function TypingIndicator() {
  return (
    <div className="flex items-center gap-3 p-4 rounded-2xl bg-card/80 border border-border/60 shadow-sm max-w-md my-2 animate-fade-in">
      <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-xs shrink-0">
        AI
      </div>
      <div className="flex items-center gap-1.5">
        <span className="text-xs text-muted-foreground font-medium mr-1">
          Synthesizing response
        </span>
        <div className="w-2 h-2 rounded-full bg-primary animate-bounce [animation-delay:-0.3s]" />
        <div className="w-2 h-2 rounded-full bg-primary animate-bounce [animation-delay:-0.15s]" />
        <div className="w-2 h-2 rounded-full bg-primary animate-bounce" />
      </div>
    </div>
  );
}

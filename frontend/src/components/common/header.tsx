import React from "react";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  onToggleMobileSidebar: () => void;
}

export function Header({ onToggleMobileSidebar }: HeaderProps) {
  return (
    <header className="h-14 border-b border-border bg-card/80 backdrop-blur px-4 md:px-6 flex items-center justify-between shrink-0">
      <div className="flex items-center gap-3">
        {/* Mobile menu toggle */}
        <Button
          variant="ghost"
          size="sm"
          onClick={onToggleMobileSidebar}
          className="md:hidden p-1.5 h-8 w-8"
        >
          ☰
        </Button>

        <div className="flex items-center gap-2">
          <span className="text-xl">🏢</span>
          <h1 className="font-bold text-sm sm:text-base tracking-tight text-foreground">
            AI Company Research Assistant
          </h1>
          <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Gemini 2.5 Flash
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <span className="text-xs text-muted-foreground hidden sm:inline-block">
          🌙 Dark Mode Active
        </span>
      </div>
    </header>
  );
}

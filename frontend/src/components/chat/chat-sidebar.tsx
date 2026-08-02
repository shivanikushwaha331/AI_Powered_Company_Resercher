import React from "react";
import { Button } from "@/components/ui/button";

export interface ChatHistoryItem {
  id: string;
  title: string;
  timestamp: string;
}

interface ChatSidebarProps {
  historyItems: ChatHistoryItem[];
  activeId?: string | null;
  onSelectHistory: (id: string) => void;
  onDeleteHistory?: (id: string) => void;
  onNewChat: () => void;
  isOpenMobile?: boolean;
  onCloseMobile?: () => void;
}

export function ChatSidebar({
  historyItems,
  activeId,
  onSelectHistory,
  onDeleteHistory,
  onNewChat,
  isOpenMobile,
  onCloseMobile,
}: ChatSidebarProps) {
  return (
    <aside
      className={`fixed inset-y-0 left-0 z-40 w-64 bg-card border-r border-border flex flex-col transition-transform duration-300 md:static md:translate-x-0 ${
        isOpenMobile ? "translate-x-0" : "-translate-x-full"
      }`}
    >
      {/* Header & New Chat Button */}
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-primary flex items-center justify-center text-primary-foreground font-bold text-xs">
            AI
          </div>
          <span className="font-bold text-sm text-foreground tracking-tight">Research Assistant</span>
        </div>

        {isOpenMobile && (
          <button
            onClick={onCloseMobile}
            className="md:hidden text-muted-foreground hover:text-foreground text-sm font-bold p-1"
          >
            ✕
          </button>
        )}
      </div>

      <div className="p-3">
        <Button
          onClick={() => {
            onNewChat();
            if (onCloseMobile) onCloseMobile();
          }}
          className="w-full justify-start gap-2 bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20 rounded-xl text-xs font-semibold py-2.5"
        >
          <span>+</span>
          <span>New Research Chat</span>
        </Button>
      </div>

      {/* Conversation Sessions List */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
        <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground px-2 block mb-2">
          Recent Sessions ({historyItems.length})
        </span>

        {historyItems.length === 0 ? (
          <div className="p-4 text-center text-xs text-muted-foreground border border-dashed border-border/60 rounded-xl">
            No research history yet. Start a new chat!
          </div>
        ) : (
          historyItems.map((item) => {
            const isActive = item.id === activeId;
            return (
              <div
                key={item.id}
                className={`group flex items-center justify-between px-3 py-2 rounded-xl text-xs transition-all cursor-pointer ${
                  isActive
                    ? "bg-secondary text-secondary-foreground font-semibold border border-border/80 shadow-sm"
                    : "text-muted-foreground hover:bg-secondary/50 hover:text-foreground"
                }`}
                onClick={() => {
                  onSelectHistory(item.id);
                  if (onCloseMobile) onCloseMobile();
                }}
              >
                <div className="flex items-center gap-2 overflow-hidden">
                  <span>💬</span>
                  <span className="truncate max-w-[130px]">{item.title}</span>
                </div>

                <div className="flex items-center gap-1">
                  <span className="text-[10px] opacity-60">{item.timestamp}</span>
                  {onDeleteHistory && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteHistory(item.id);
                      }}
                      className="opacity-0 group-hover:opacity-100 hover:text-destructive text-xs p-0.5 transition-opacity"
                      title="Delete Session"
                    >
                      🗑️
                    </button>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Footer System Info */}
      <div className="p-3 border-t border-border bg-muted/20 text-[11px] text-muted-foreground flex items-center justify-between">
        <span>AI Engine v1.0</span>
        <span className="inline-flex items-center gap-1 text-emerald-400 font-medium">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Ready
        </span>
      </div>
    </aside>
  );
}

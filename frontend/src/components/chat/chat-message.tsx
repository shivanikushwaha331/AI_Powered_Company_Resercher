import React from "react";
import { ChatMessage } from "@/types/chat";
import { ResearchCard } from "@/components/chat/research-card";
import { MarkdownRenderer } from "@/components/chat/markdown-renderer";
import { MessageActions } from "@/components/chat/message-actions";

interface ChatMessageCardProps {
  message: ChatMessage;
  onRegenerate?: () => void;
}

export function ChatMessageCard({ message, onRegenerate }: ChatMessageCardProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex gap-3 my-3 max-w-4xl mx-auto ${
        isUser ? "justify-end" : "justify-start"
      } animate-fade-in`}
    >
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-primary/20 text-primary font-bold text-xs flex items-center justify-center shrink-0 mt-1 shadow-sm">
          AI
        </div>
      )}

      <div
        className={`rounded-2xl p-4 shadow-sm transition-all ${
          isUser
            ? "bg-primary text-primary-foreground max-w-[85%] rounded-tr-none"
            : "bg-card border border-border/80 text-foreground w-full rounded-tl-none"
        }`}
      >
        <div className="flex items-center justify-between gap-2 mb-1.5 text-[11px] opacity-70">
          <span className="font-semibold">{isUser ? "You" : "AI Research Assistant"}</span>
          <span>{message.timestamp}</span>
        </div>

        {/* Content Body */}
        {isUser ? (
          <p className="text-sm leading-relaxed font-medium whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="space-y-4">
            <MarkdownRenderer content={message.content} />

            {/* Structured Research Card Payload */}
            {message.researchData && <ResearchCard researchData={message.researchData} />}

            {/* Action Bar: Copy & Regenerate */}
            <MessageActions content={message.content} onRegenerate={onRegenerate} />
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-secondary text-secondary-foreground font-bold text-xs flex items-center justify-center shrink-0 mt-1 shadow-sm">
          U
        </div>
      )}
    </div>
  );
}

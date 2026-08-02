import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { ResearchDepth } from "@/types/research";

interface ChatInputProps {
  onSendMessage: (query: string, depth: ResearchDepth, model: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [query, setQuery] = useState("");
  const [depth, setDepth] = useState<ResearchDepth>("standard");
  const [selectedModel, setSelectedModel] = useState<string>("google/gemini-2.5-flash");

  const models = [
    { id: "google/gemini-2.5-flash", name: "Gemini 2.5 Flash" },
    { id: "anthropic/claude-3.5-sonnet", name: "Claude 3.5 Sonnet" },
    { id: "openai/gpt-4o-mini", name: "GPT-4o Mini" },
    { id: "deepseek/deepseek-r1", name: "DeepSeek R1" },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || disabled) return;
    onSendMessage(query, depth, selectedModel);
    setQuery("");
  };

  return (
    <div className="p-4 border-t border-border bg-card/60 backdrop-blur">
      <form onSubmit={handleSubmit} className="max-w-3xl mx-auto space-y-2.5">
        {/* Controls Row: Model Selector & Depth Selector */}
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
          {/* OpenRouter Model Selector Dropdown */}
          <div className="flex items-center gap-1.5">
            <span className="font-semibold text-[11px] uppercase tracking-wider text-muted-foreground">
              🤖 LLM Model:
            </span>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              disabled={disabled}
              className="bg-secondary text-secondary-foreground text-xs font-medium rounded-lg px-2.5 py-1 border border-border/80 focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50 cursor-pointer"
            >
              {models.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name}
                </option>
              ))}
            </select>
          </div>

          {/* Research Depth Selector Pills */}
          <div className="flex items-center gap-1.5">
            <span className="font-semibold text-[11px] uppercase tracking-wider text-muted-foreground">
              Depth:
            </span>
            {(["quick", "standard", "deep"] as ResearchDepth[]).map((d) => (
              <button
                key={d}
                type="button"
                onClick={() => setDepth(d)}
                className={`px-2.5 py-0.5 rounded-full capitalize text-xs font-medium transition-all ${
                  depth === d
                    ? "bg-primary text-primary-foreground font-semibold shadow-sm"
                    : "bg-secondary/60 text-secondary-foreground hover:bg-secondary"
                }`}
              >
                {d}
              </button>
            ))}
          </div>
        </div>

        {/* Floating Input Pill */}
        <div className="relative flex items-center bg-background border border-border/80 focus-within:border-primary/60 rounded-2xl p-1.5 shadow-md transition-all">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type any company name or domain (e.g. Stripe, Nvidia, Tesla)..."
            disabled={disabled}
            className="w-full bg-transparent px-4 py-2 text-sm focus:outline-none placeholder:text-muted-foreground text-foreground disabled:opacity-50"
          />

          <Button
            type="submit"
            disabled={disabled || !query.trim()}
            size="sm"
            className="rounded-xl px-4 font-semibold shadow transition-all flex items-center gap-1 shrink-0"
          >
            {disabled ? (
              <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <span>Research</span>
                <span className="text-xs">➔</span>
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  );
}

import React from "react";

interface PromptSuggestionsProps {
  onSelectPrompt: (query: string) => void;
}

export function PromptSuggestions({ onSelectPrompt }: PromptSuggestionsProps) {
  const suggestions = [
    {
      title: "Research Stripe",
      subtitle: "Payment infrastructure, developer APIs, & financials",
      query: "Research Stripe",
      icon: "💳",
    },
    {
      title: "Analyze Nvidia AI Stack",
      subtitle: "CUDA ecosystem, Blackwell GPUs, & data center growth",
      query: "Research Nvidia",
      icon: "⚡",
    },
    {
      title: "Deep Dive into OpenAI",
      subtitle: "LLM revenue, Microsoft partnership, & compute infrastructure",
      query: "Research OpenAI",
      icon: "🤖",
    },
    {
      title: "Company Technology Audit",
      subtitle: "Detect frontend, backend, & database tech stack signals",
      query: "Research Vercel",
      icon: "🌐",
    },
  ];

  return (
    <div className="h-full flex flex-col items-center justify-center p-6 text-center max-w-2xl mx-auto my-auto space-y-6 animate-fadeIn">
      <div className="space-y-2">
        <div className="w-12 h-12 rounded-2xl bg-primary/20 text-primary flex items-center justify-center text-2xl mx-auto shadow-inner">
          ✨
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground">
          What company would you like to research today?
        </h2>
        <p className="text-sm text-muted-foreground max-w-md mx-auto">
          Enter any company name or web domain to generate real-time market intelligence, technology stack analysis, and financial profiles.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full">
        {suggestions.map((item, idx) => (
          <button
            key={idx}
            onClick={() => onSelectPrompt(item.query)}
            className="p-4 rounded-xl border border-border/70 bg-card/60 hover:bg-secondary/60 hover:border-primary/40 transition-all text-left group shadow-sm flex flex-col justify-between"
          >
            <div className="flex items-center gap-2 mb-1">
              <span className="text-base">{item.icon}</span>
              <span className="font-semibold text-sm text-foreground group-hover:text-primary transition-colors">
                {item.title}
              </span>
            </div>
            <p className="text-xs text-muted-foreground line-clamp-2">{item.subtitle}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

import React from "react";
import { ProgressStep } from "@/hooks/use-mock-chat";

interface ProgressIndicatorProps {
  steps: ProgressStep[];
}

export function ProgressIndicator({ steps }: ProgressIndicatorProps) {
  return (
    <div className="w-full max-w-xl my-4 p-4 rounded-xl border border-primary/20 bg-card/80 backdrop-blur shadow-lg transition-all animate-pulse">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-2.5 h-2.5 rounded-full bg-primary animate-ping" />
        <span className="text-xs font-semibold uppercase tracking-wider text-primary">
          AI Research Pipeline Running
        </span>
      </div>

      <div className="space-y-2">
        {steps.map((s) => (
          <div key={s.step} className="flex items-center gap-3 text-xs">
            <div
              className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-[10px] ${
                s.isComplete
                  ? "bg-emerald-500 text-black"
                  : s.isActive
                  ? "bg-primary text-primary-foreground ring-2 ring-primary/40 animate-bounce"
                  : "bg-muted text-muted-foreground"
              }`}
            >
              {s.isComplete ? "✓" : s.step}
            </div>
            <span
              className={`${
                s.isComplete
                  ? "text-foreground font-medium"
                  : s.isActive
                  ? "text-primary font-semibold"
                  : "text-muted-foreground opacity-60"
              }`}
            >
              {s.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

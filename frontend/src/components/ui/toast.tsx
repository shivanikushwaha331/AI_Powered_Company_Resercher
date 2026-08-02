"use client";

import React from "react";
import { useToast } from "@/hooks/use-toast";

export function ToastContainer() {
  const { toasts, removeToast } = useToast();

  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`pointer-events-auto p-4 rounded-xl border shadow-xl backdrop-blur flex items-start justify-between gap-3 transition-all animate-in slide-in-from-bottom-2 ${
            t.type === "success"
              ? "bg-emerald-950/90 border-emerald-500/40 text-emerald-100"
              : t.type === "error"
              ? "bg-destructive/90 border-destructive-foreground/40 text-destructive-foreground"
              : "bg-card/95 border-border text-card-foreground"
          }`}
        >
          <div className="flex-1 text-xs">
            <div className="font-bold text-sm mb-0.5">{t.title}</div>
            <div className="opacity-90 leading-tight">{t.message}</div>
          </div>
          <button
            onClick={() => removeToast(t.id)}
            className="text-xs opacity-60 hover:opacity-100 transition-opacity p-1"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}

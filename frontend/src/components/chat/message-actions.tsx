import React, { useState } from "react";
import { showToast } from "@/hooks/use-toast";

interface MessageActionsProps {
  content: string;
  onRegenerate?: () => void;
}

export function MessageActions({ content, onRegenerate }: MessageActionsProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    showToast("Copied to Clipboard", "AI response text copied to system clipboard.", "info");
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex items-center gap-2 pt-2 border-t border-border/40 text-xs text-muted-foreground">
      <button
        onClick={handleCopy}
        className="px-2.5 py-1 rounded-md bg-secondary/40 hover:bg-secondary text-secondary-foreground font-medium transition-colors flex items-center gap-1"
      >
        {copied ? (
          <>
            <span className="text-emerald-400">✓</span>
            <span>Copied</span>
          </>
        ) : (
          <>
            <span>📋</span>
            <span>Copy Response</span>
          </>
        )}
      </button>

      {onRegenerate && (
        <button
          onClick={onRegenerate}
          className="px-2.5 py-1 rounded-md bg-secondary/40 hover:bg-secondary text-secondary-foreground font-medium transition-colors flex items-center gap-1"
        >
          <span>🔄</span>
          <span>Regenerate Response</span>
        </button>
      )}
    </div>
  );
}

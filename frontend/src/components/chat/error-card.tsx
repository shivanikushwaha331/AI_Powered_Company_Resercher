import React from "react";
import { Button } from "@/components/ui/button";

interface ErrorCardProps {
  errorMessage: string;
  onRetry: () => void;
}

export function ErrorCard({ errorMessage, onRetry }: ErrorCardProps) {
  return (
    <div className="w-full max-w-2xl my-3 p-4 rounded-xl border border-destructive/40 bg-destructive/10 text-foreground shadow-md">
      <div className="flex items-start gap-3">
        <div className="text-xl shrink-0">⚠️</div>
        <div className="flex-1 space-y-2">
          <div>
            <h4 className="font-semibold text-sm text-destructive-foreground">
              Research Backend Request Failed
            </h4>
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
              {errorMessage}
            </p>
          </div>

          <div className="pt-2 flex items-center gap-3">
            <Button
              onClick={onRetry}
              size="sm"
              variant="outline"
              className="border-destructive/40 hover:bg-destructive/20 text-xs font-semibold flex items-center gap-1.5"
            >
              <span>🔄</span> Retry Request
            </Button>
            <span className="text-[11px] text-muted-foreground">
              Ensure backend server is running on http://localhost:8000
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

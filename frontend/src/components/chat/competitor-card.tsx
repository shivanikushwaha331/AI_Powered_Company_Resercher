import React from "react";
import { CompetitorDetail } from "@/types/research";

interface CompetitorCardProps {
  competitors: CompetitorDetail[];
}

export function CompetitorCardList({ competitors }: CompetitorCardProps) {
  if (!competitors || competitors.length === 0) return null;

  return (
    <div className="space-y-3">
      <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
        Identified Market Competitors ({competitors.length})
      </h4>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {competitors.map((comp, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl border border-border/80 bg-card/80 hover:bg-secondary/40 hover:border-primary/40 transition-all flex flex-col justify-between space-y-3 shadow-sm"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <h5 className="font-bold text-sm text-foreground truncate">{comp.company_name}</h5>
                <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-muted text-muted-foreground shrink-0">
                  {comp.country}
                </span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {comp.reason_for_competition}
              </p>
            </div>

            {/* Visit Website Action Button */}
            <div className="pt-2 border-t border-border/40 flex items-center justify-between">
              <span className="text-[11px] text-muted-foreground truncate max-w-[160px]">
                {comp.website.replace("https://", "").replace("http://", "").replace("www.", "")}
              </span>
              <a
                href={comp.website.startsWith("http") ? comp.website : `https://${comp.website}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:text-primary/80 hover:underline transition-all"
              >
                <span>Visit Website</span>
                <span className="text-[10px]">↗</span>
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

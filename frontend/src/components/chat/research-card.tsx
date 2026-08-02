import React, { useState } from "react";
import { CompanyProfile, ResearchResult, AIStructuredReport } from "@/types/research";
import { Button } from "@/components/ui/button";
import { CompetitorCardList } from "@/components/chat/competitor-card";
import { apiService } from "@/services/api-service";
import { showToast } from "@/hooks/use-toast";

interface ResearchCardProps {
  researchData?: ResearchResult;
}

export function ResearchCard({ researchData }: ResearchCardProps) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [isDiscordSending, setIsDiscordSending] = useState(false);

  if (!researchData || !researchData.profile) return null;
  const profile: CompanyProfile = researchData.profile;
  const aiReport: AIStructuredReport | undefined = researchData.ai_report;

  const handleDownloadPDF = async () => {
    setIsDownloading(true);
    try {
      // 1. Call backend POST /generate-pdf endpoint
      const pdfResult = await apiService.generatePDF({
        title: `${profile.name} Corporate Intelligence Report`,
        content: researchData.summary,
      });

      showToast(
        "PDF Generated Successfully",
        `ReportLab PDF '${pdfResult.file_name}' compiled. Downloading...`,
        "success"
      );

      // 2. Fetch binary PDF blob from backend download_url
      const response = await fetch(pdfResult.download_url);
      if (!response.ok) {
        throw new Error(`Failed to download PDF file (${response.statusText})`);
      }
      const blob = await response.blob();

      // 3. Trigger direct browser download as .pdf file
      const element = document.createElement("a");
      element.href = URL.createObjectURL(blob);
      element.download = pdfResult.file_name;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    } catch (err: any) {
      showToast("PDF Export Failed", err.message || "Could not generate PDF document", "error");
    } finally {
      setIsDownloading(false);
    }
  };

  const handleSendDiscord = async () => {
    setIsDiscordSending(true);
    try {
      const result = await apiService.sendDiscordNotification({
        title: `Research Completed: ${profile.name}`,
        summary: researchData.summary,
        company_name: profile.name,
      });

      showToast(
        "Discord Alert Dispatched",
        `Sent to #${result.channel_name} (Msg ID: ${result.message_id})`,
        "success"
      );
    } catch (err: any) {
      showToast("Discord Dispatch Failed", err.message || "Failed to dispatch webhook", "error");
    } finally {
      setIsDiscordSending(false);
    }
  };

  return (
    <div className="w-full my-4 rounded-xl border border-border bg-card/90 shadow-xl overflow-hidden transition-all hover:border-primary/40">
      {/* Header Banner */}
      <div className="p-5 border-b border-border bg-gradient-to-r from-secondary/50 via-card to-secondary/30 flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-xl font-bold tracking-tight text-foreground">{profile.name}</h3>
            <span className="px-2 py-0.5 rounded-full bg-primary/20 text-primary text-xs font-semibold">
              {profile.industry}
            </span>
            {aiReport?.selected_model && (
              <span className="px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 text-[10px] font-mono border border-purple-500/30">
                🤖 {aiReport.selected_model}
              </span>
            )}
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            📍 {profile.headquarters} • Founded {profile.founded_year} • Domain: {profile.domain}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          <Button
            onClick={handleSendDiscord}
            disabled={isDiscordSending}
            size="sm"
            variant="outline"
            className="border-indigo-500/40 text-indigo-300 hover:bg-indigo-950/50 text-xs font-semibold flex items-center gap-1.5"
          >
            {isDiscordSending ? (
              <div className="w-3 h-3 border-2 border-indigo-300 border-t-transparent rounded-full animate-spin" />
            ) : (
              <span>💬 Share to Discord</span>
            )}
          </Button>

          <Button
            onClick={handleDownloadPDF}
            disabled={isDownloading}
            size="sm"
            className="bg-primary hover:bg-primary/90 text-primary-foreground font-semibold shadow-md transition-all flex items-center gap-1.5"
          >
            {isDownloading ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                Compiling PDF...
              </>
            ) : (
              <>
                <span>📄</span> Download PDF Report
              </>
            )}
          </Button>
        </div>
      </div>

      <div className="p-5 space-y-6">
        {/* Financial Metrics Grid */}
        {profile.financials && (
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-3">
              Financial & Operations Overview
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3 rounded-lg border border-border/60 bg-muted/30">
                <span className="text-[10px] text-muted-foreground block">Estimated Revenue</span>
                <span className="text-sm font-semibold text-foreground">{profile.financials.revenue || "N/A"}</span>
              </div>
              <div className="p-3 rounded-lg border border-border/60 bg-muted/30">
                <span className="text-[10px] text-muted-foreground block">Valuation</span>
                <span className="text-sm font-semibold text-emerald-400">{profile.financials.valuation || "N/A"}</span>
              </div>
              <div className="p-3 rounded-lg border border-border/60 bg-muted/30">
                <span className="text-[10px] text-muted-foreground block">Total Funding</span>
                <span className="text-sm font-semibold text-foreground">{profile.financials.funding_total || "N/A"}</span>
              </div>
              <div className="p-3 rounded-lg border border-border/60 bg-muted/30">
                <span className="text-[10px] text-muted-foreground block">Headcount</span>
                <span className="text-sm font-semibold text-foreground">
                  {profile.financials.headcount ? `${profile.financials.headcount.toLocaleString()}+ employees` : "N/A"}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Business Model & Pain Points Cards */}
        {aiReport && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl border border-primary/20 bg-card/60">
              <h4 className="text-xs font-bold uppercase tracking-wider text-primary mb-2 flex items-center gap-1.5">
                <span>💰</span> Business & Revenue Model
              </h4>
              <p className="text-xs text-foreground leading-relaxed">{aiReport.business_model}</p>
            </div>

            <div className="p-4 rounded-xl border border-amber-500/20 bg-card/60">
              <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-2 flex items-center gap-1.5">
                <span>🎯</span> Target Customers
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {aiReport.target_customers.map((tc) => (
                  <span key={tc} className="px-2 py-0.5 bg-amber-500/10 text-amber-300 text-xs rounded border border-amber-500/20">
                    {tc}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Customer Pain Points Solved */}
        {aiReport?.pain_points && aiReport.pain_points.length > 0 && (
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-2">
              Customer Pain Points Solved
            </h4>
            <div className="space-y-1.5">
              {aiReport.pain_points.map((pp, idx) => (
                <div key={idx} className="p-2 rounded-lg bg-secondary/40 text-xs text-foreground flex items-center gap-2 border border-border/40">
                  <span className="text-destructive font-bold text-sm">💡</span>
                  <span>{pp}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 4-Quadrant SWOT Analysis Grid */}
        {aiReport?.swot_analysis && (
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-3">
              SWOT Analysis Matrix
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {/* Strengths */}
              <div className="p-3 rounded-lg border border-emerald-500/30 bg-emerald-950/20">
                <h5 className="text-xs font-bold text-emerald-400 mb-2 flex items-center gap-1">
                  <span>💪</span> Strengths
                </h5>
                <ul className="space-y-1 text-xs text-emerald-100/90 list-disc list-inside">
                  {aiReport.swot_analysis.strengths.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </div>

              {/* Weaknesses */}
              <div className="p-3 rounded-lg border border-rose-500/30 bg-rose-950/20">
                <h5 className="text-xs font-bold text-rose-400 mb-2 flex items-center gap-1">
                  <span>⚠️</span> Weaknesses
                </h5>
                <ul className="space-y-1 text-xs text-rose-100/90 list-disc list-inside">
                  {aiReport.swot_analysis.weaknesses.map((w, i) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </div>

              {/* Opportunities */}
              <div className="p-3 rounded-lg border border-blue-500/30 bg-blue-950/20">
                <h5 className="text-xs font-bold text-blue-400 mb-2 flex items-center gap-1">
                  <span>🚀</span> Opportunities
                </h5>
                <ul className="space-y-1 text-xs text-blue-100/90 list-disc list-inside">
                  {aiReport.swot_analysis.opportunities.map((o, i) => (
                    <li key={i}>{o}</li>
                  ))}
                </ul>
              </div>

              {/* Threats */}
              <div className="p-3 rounded-lg border border-amber-500/30 bg-amber-950/20">
                <h5 className="text-xs font-bold text-amber-400 mb-2 flex items-center gap-1">
                  <span>🛡️</span> Threats
                </h5>
                <ul className="space-y-1 text-xs text-amber-100/90 list-disc list-inside">
                  {aiReport.swot_analysis.threats.map((t, i) => (
                    <li key={i}>{t}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Competitor Cards Section */}
        {researchData.competitors_detail && researchData.competitors_detail.length > 0 && (
          <CompetitorCardList competitors={researchData.competitors_detail} />
        )}

        {/* Tech Stack Tags */}
        {profile.tech_stack?.length > 0 && (
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-2">
              Detected Tech Stack
            </h4>
            <div className="flex flex-wrap gap-1.5">
              {profile.tech_stack.map((tech) => (
                <span
                  key={tech}
                  className="px-2.5 py-1 rounded-md bg-secondary/80 text-secondary-foreground text-xs font-medium border border-border/40 hover:border-primary/40 transition-colors"
                >
                  ⚡ {tech}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Sources & Citations */}
        {researchData.sources?.length > 0 && (
          <div className="pt-2 border-t border-border/40">
            <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-2">
              Cited References ({researchData.sources.length})
            </h4>
            <div className="space-y-1.5">
              {researchData.sources.map((src, idx) => (
                <a
                  key={idx}
                  href={src.url}
                  target="_blank"
                  rel="noreferrer"
                  className="block p-2 rounded-md border border-border/40 hover:bg-secondary/40 transition-all text-xs"
                >
                  <span className="font-semibold text-primary block">{src.title}</span>
                  <span className="text-[11px] text-muted-foreground truncate block">{src.snippet}</span>
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

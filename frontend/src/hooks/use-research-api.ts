import { useState } from "react";
import { ChatMessage } from "@/types/chat";
import { ResearchDepth } from "@/types/research";
import { apiService } from "@/services/api-service";
import { showToast } from "@/hooks/use-toast";
import { getSavedSettings } from "@/components/settings/settings-modal";

export interface ProgressStep {
  step: number;
  label: string;
  isComplete: boolean;
  isActive: boolean;
}

export function useResearchApi() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isError, setIsError] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [lastQuery, setLastQuery] = useState<string>("");
  const [lastDepth, setLastDepth] = useState<ResearchDepth>("standard");
  const [lastModel, setLastModel] = useState<string>("google/gemini-2.5-flash");

  const [progressSteps, setProgressSteps] = useState<ProgressStep[]>([
    { step: 1, label: "Executing POST /research & Serper domain search...", isComplete: false, isActive: false },
    { step: 2, label: "Crawling website & tech stack signals (POST /crawl)...", isComplete: false, isActive: false },
    { step: 3, label: "OpenRouter LLM 8-part synthesis & competitor analysis...", isComplete: false, isActive: false },
  ]);

  const [chatHistory, setChatHistory] = useState<
    { id: string; title: string; timestamp: string; messages: ChatMessage[] }[]
  >([]);

  const [activeChatId, setActiveChatId] = useState<string | null>(null);

  const startNewChat = () => {
    setMessages([]);
    setActiveChatId(null);
    setIsLoading(false);
    setIsError(false);
    setErrorMessage(null);
  };

  const selectHistorySession = (id: string) => {
    const found = chatHistory.find((item) => item.id === id);
    if (found) {
      setMessages(found.messages);
      setActiveChatId(id);
      setIsError(false);
      setErrorMessage(null);
    }
  };

  const deleteHistorySession = (id: string) => {
    setChatHistory((prev) => prev.filter((item) => item.id !== id));
    if (activeChatId === id) {
      startNewChat();
    }
    showToast("Session Deleted", "Research history item removed.", "info");
  };

  const submitResearchQuery = async (
    query: string,
    depth: ResearchDepth = "standard",
    model: string = "google/gemini-2.5-flash"
  ) => {
    if (!query.trim() || isLoading) return;

    setLastQuery(query);
    setLastDepth(depth);
    setLastModel(model);

    const userMessage: ChatMessage = {
      id: `user_${Date.now()}`,
      role: "user",
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setIsError(false);
    setErrorMessage(null);

    // Set active progress pipeline
    setProgressSteps([
      { step: 1, label: `Executing POST /research for '${query}'...`, isComplete: false, isActive: true },
      { step: 2, label: "Crawling target website & technology stack...", isComplete: false, isActive: false },
      { step: 3, label: `Synthesizing 8-part report & competitor analysis via [${model}]...`, isComplete: false, isActive: false },
    ]);

    try {
      // Step 1: Execute POST /research via Axios API Service
      const researchData = await apiService.researchCompany({
        company_name: query,
        depth: depth,
        model: model,
      });

      setProgressSteps((prev) =>
        prev.map((s) => (s.step === 1 ? { ...s, isComplete: true, isActive: false } : s.step === 2 ? { ...s, isActive: true } : s))
      );

      // Step 2: Execute POST /crawl
      let crawledText = "";
      if (researchData.profile?.website_url) {
        try {
          const crawlResult = await apiService.crawlWebsite({
            url: researchData.profile.website_url,
            max_pages: 3,
          });
          crawledText = crawlResult.extracted_pages.map((p) => p.clean_text || "").join("\n\n");
        } catch {
          // Crawl fallback
        }
      }

      setProgressSteps((prev) =>
        prev.map((s) => (s.step === 2 ? { ...s, isComplete: true, isActive: false } : s.step === 3 ? { ...s, isActive: true } : s))
      );

      // Step 3: Execute OpenRouter LLM 8-part synthesis & Competitor Analysis
      const aiReportData = await apiService.generateAIReport({
        company_name: query,
        crawled_content: crawledText || researchData.summary,
        model: model,
      });

      // Analyze Competitors (resolving missing websites via Serper)
      let competitorDetails: any[] = [];
      try {
        const compRes = await apiService.analyzeCompetitors(
          query,
          aiReportData.competitor_suggestions || researchData.profile?.competitors
        );
        competitorDetails = compRes.competitors;
      } catch {
        // Competitor fallback
      }

      // Generate PDF Document
      let pdfDownloadUrl = "";
      try {
        const pdfRes = await apiService.generatePDF({
          title: `${query} Corporate Research Report`,
          content: researchData.summary,
        });
        pdfDownloadUrl = pdfRes.download_url;
      } catch {
        // PDF fallback
      }

      setProgressSteps((prev) => prev.map((s) => ({ ...s, isComplete: true, isActive: false })));

      // Automated Discord Dispatch using Saved User Settings
      const savedSettings = getSavedSettings();
      try {
        const discordRes = await apiService.sendDiscordNotification({
          applicant_name: savedSettings.applicantName || "John Doe",
          applicant_email: savedSettings.applicantEmail || "john@example.com",
          company_name: researchData.profile?.name || query,
          company_website: researchData.profile?.website_url || researchData.profile?.domain || "N/A",
          summary: researchData.summary,
          pdf_url: pdfDownloadUrl,
          bot_token: savedSettings.discordBotToken || undefined,
          channel_id: savedSettings.discordChannelId || undefined,
        });

        showToast(
          "Discord Notification Dispatched",
          `Report sent for ${query} (Msg ID: ${discordRes.message_id})`,
          "success"
        );
      } catch (err: any) {
        showToast("Discord Dispatch Warning", err.message || "Failed to post Discord alert.", "error");
      }

      // Attach AI structured report & competitor details to research payload
      const combinedResearchData = {
        ...researchData,
        ai_report: aiReportData,
        competitors_detail: competitorDetails,
      };

      const aiMessage: ChatMessage = {
        id: `ai_${Date.now()}`,
        role: "assistant",
        content: aiReportData.company_summary || researchData.summary,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        researchData: combinedResearchData,
      };

      setMessages((prev) => [...prev, aiMessage]);

      // Add to history
      const newHistId = `hist_${Date.now()}`;
      setChatHistory((prev) => [
        { id: newHistId, title: query, timestamp: "Just now", messages: [userMessage, aiMessage] },
        ...prev,
      ]);
      setActiveChatId(newHistId);

      showToast("Research Complete", `Synthesized report & competitor analysis for ${query}`, "success");
    } catch (err: any) {
      const errText = err.message || "Failed to communicate with research backend.";
      setIsError(true);
      setErrorMessage(errText);
      showToast("API Connection Error", errText, "error");
    } finally {
      setIsLoading(false);
    }
  };

  const retryLastQuery = () => {
    if (lastQuery) {
      showToast("Regenerating Response", `Re-submitting research request for '${lastQuery}' using [${lastModel}]...`, "info");
      submitResearchQuery(lastQuery, lastDepth, lastModel);
    }
  };

  return {
    messages,
    isLoading,
    isError,
    errorMessage,
    progressSteps,
    chatHistory,
    activeChatId,
    startNewChat,
    selectHistorySession,
    deleteHistorySession,
    submitResearchQuery,
    retryLastQuery,
  };
}

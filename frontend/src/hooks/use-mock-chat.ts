import { useState } from "react";
import { ChatMessage } from "@/types/chat";
import { ResearchResult, ResearchDepth } from "@/types/research";
import { getMockResearchData } from "@/lib/mock-data";

export interface ProgressStep {
  step: number;
  label: string;
  isComplete: boolean;
  isActive: boolean;
}

export function useMockChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [progressSteps, setProgressSteps] = useState<ProgressStep[]>([
    { step: 1, label: "Searching web sources & domain metadata...", isComplete: false, isActive: false },
    { step: 2, label: "Crawling technology stack & engineering blogs...", isComplete: false, isActive: false },
    { step: 3, label: "Synthesizing executive report & key takeaways...", isComplete: false, isActive: false },
  ]);

  const [chatHistory, setChatHistory] = useState<
    { id: string; title: string; timestamp: string; messages: ChatMessage[] }[]
  >([
    { id: "hist_1", title: "Stripe Payment Infrastructure", timestamp: "2 hours ago", messages: [] },
    { id: "hist_2", title: "Nvidia AI Chip Dominance", timestamp: "Yesterday", messages: [] },
  ]);

  const [activeChatId, setActiveChatId] = useState<string | null>(null);

  const startNewChat = () => {
    setMessages([]);
    setActiveChatId(null);
    setIsLoading(false);
    setCurrentStep(0);
  };

  const loadHistoryItem = (id: string) => {
    const item = chatHistory.find((h) => h.id === id);
    if (!item) return;

    setActiveChatId(id);
    const mockData = getMockResearchData(item.title);
    setMessages([
      {
        id: `user_${id}`,
        role: "user",
        content: `Research ${item.title}`,
        timestamp: "Recently",
      },
      {
        id: `ai_${id}`,
        role: "assistant",
        content: mockData.summary,
        timestamp: "Recently",
        researchData: mockData,
      },
    ]);
  };

  const submitResearchQuery = async (query: string, depth: ResearchDepth = "standard") => {
    if (!query.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: `user_${Date.now()}`,
      role: "user",
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Reset Progress Steps
    setProgressSteps([
      { step: 1, label: `Searching web sources for '${query}'...`, isComplete: false, isActive: true },
      { step: 2, label: "Crawling technology stack & corporate blogs...", isComplete: false, isActive: false },
      { step: 3, label: "Synthesizing AI research report & financial insights...", isComplete: false, isActive: false },
    ]);
    setCurrentStep(1);

    // Simulate Step 1 -> Step 2
    await new Promise((resolve) => setTimeout(resolve, 1200));
    setProgressSteps((prev) =>
      prev.map((s) => (s.step === 1 ? { ...s, isComplete: true, isActive: false } : s.step === 2 ? { ...s, isActive: true } : s))
    );
    setCurrentStep(2);

    // Simulate Step 2 -> Step 3
    await new Promise((resolve) => setTimeout(resolve, 1400));
    setProgressSteps((prev) =>
      prev.map((s) => (s.step === 2 ? { ...s, isComplete: true, isActive: false } : s.step === 3 ? { ...s, isActive: true } : s))
    );
    setCurrentStep(3);

    // Finalize Synthesis
    await new Promise((resolve) => setTimeout(resolve, 1200));
    setProgressSteps((prev) => prev.map((s) => ({ ...s, isComplete: true, isActive: false })));

    // Generate Mock Response Payload
    const researchResult = getMockResearchData(query);

    const aiMessage: ChatMessage = {
      id: `ai_${Date.now()}`,
      role: "assistant",
      content: researchResult.summary,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      researchData: researchResult,
    };

    setMessages((prev) => [...prev, aiMessage]);

    // Add to history
    const newHistId = `hist_${Date.now()}`;
    setChatHistory((prev) => [
      { id: newHistId, title: query, timestamp: "Just now", messages: [userMessage, aiMessage] },
      ...prev,
    ]);
    setActiveChatId(newHistId);

    setIsLoading(false);
    setCurrentStep(0);
  };

  return {
    messages,
    isLoading,
    currentStep,
    progressSteps,
    chatHistory,
    activeChatId,
    startNewChat,
    loadHistoryItem,
    submitResearchQuery,
  };
}

"use client";

import React, { useState, useEffect, useRef } from "react";
import { useResearchApi } from "@/hooks/use-research-api";
import { ChatSidebar } from "@/components/chat/chat-sidebar";
import { ChatMessageCard } from "@/components/chat/chat-message";
import { ChatInput } from "@/components/chat/chat-input";
import { ProgressIndicator } from "@/components/chat/progress-indicator";
import { ErrorCard } from "@/components/chat/error-card";
import { TypingIndicator } from "@/components/chat/typing-indicator";
import { SettingsModal } from "@/components/settings/settings-modal";
import { ToastContainer } from "@/components/ui/toast";

export default function Home() {
  const {
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
  } = useResearchApi();

  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive or during loading
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden font-sans">
      <ToastContainer />

      {/* Settings Dialog Modal */}
      <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />

      {/* Left Sidebar */}
      <ChatSidebar
        historyItems={chatHistory}
        activeId={activeChatId}
        onSelectHistory={selectHistorySession}
        onDeleteHistory={deleteHistorySession}
        onNewChat={startNewChat}
        isOpenMobile={isMobileSidebarOpen}
        onCloseMobile={() => setIsMobileSidebarOpen(false)}
      />

      {/* Main Workspace */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Desktop & Mobile Navbar Header */}
        <header className="p-3 border-b border-border bg-card/80 backdrop-blur flex items-center justify-between z-30">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsMobileSidebarOpen(true)}
              className="p-1.5 rounded-lg bg-secondary text-secondary-foreground text-xs font-semibold md:hidden"
            >
              ☰ History
            </button>
            <span className="font-bold text-sm text-foreground tracking-tight hidden sm:inline">
              AI Company Research Assistant
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsSettingsOpen(true)}
              className="px-3 py-1.5 rounded-xl bg-secondary/80 hover:bg-secondary text-secondary-foreground text-xs font-semibold flex items-center gap-1.5 border border-border/60 shadow-sm transition-all"
            >
              <span>⚙️</span>
              <span>Discord Settings</span>
            </button>

            <button
              onClick={startNewChat}
              className="px-3 py-1.5 rounded-xl bg-primary text-primary-foreground text-xs font-semibold md:hidden"
            >
              + New
            </button>
          </div>
        </header>

        {/* Chat Window */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 max-w-4xl mx-auto w-full">
          {/* Empty Workspace State */}
          {messages.length === 0 && !isLoading && (
            <div className="flex flex-col items-center justify-center min-h-[70vh] text-center space-y-5 my-auto">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-primary/30 via-primary/10 to-purple-500/20 border border-primary/30 flex items-center justify-center text-primary text-3xl shadow-xl">
                🤖
              </div>
              <div className="space-y-1.5 max-w-md">
                <h2 className="text-2xl font-bold tracking-tight text-foreground">
                  AI Company Research Assistant
                </h2>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Enter any company name or domain to generate multi-model OpenRouter LLM reports, tech stack signals, 4-quadrant SWOT matrices, and competitor analysis with automatic Discord notifications.
                </p>
              </div>

              {/* Suggestion Chips */}
              <div className="flex flex-wrap justify-center gap-2 pt-2">
                {["Research Stripe", "Analyze Nvidia AI Stack", "Tesla Competitors", "Microsoft Azure Overview"].map(
                  (chip) => (
                    <button
                      key={chip}
                      onClick={() => submitResearchQuery(chip)}
                      className="px-3 py-1.5 rounded-xl bg-card border border-border/80 hover:border-primary/50 text-xs font-medium text-muted-foreground hover:text-foreground transition-all shadow-sm"
                    >
                      💡 {chip}
                    </button>
                  )
                )}
              </div>
            </div>
          )}

          {/* Active Messages List */}
          {messages.map((msg) => (
            <ChatMessageCard
              key={msg.id}
              message={msg}
              onRegenerate={msg.role === "assistant" ? retryLastQuery : undefined}
            />
          ))}

          {/* Progress Timeline Indicator */}
          {isLoading && (
            <div className="space-y-3">
              <ProgressIndicator steps={progressSteps} />
              <TypingIndicator />
            </div>
          )}

          {/* Error Banner with Retry */}
          {isError && (
            <ErrorCard
              errorMessage={errorMessage || "Failed to communicate with backend API."}
              onRetry={retryLastQuery}
            />
          )}

          <div ref={messagesEndRef} />
        </main>

        {/* Input Bar */}
        <ChatInput onSendMessage={submitResearchQuery} disabled={isLoading} />
      </div>
    </div>
  );
}

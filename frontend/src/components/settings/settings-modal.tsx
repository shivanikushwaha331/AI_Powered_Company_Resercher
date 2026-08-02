import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { showToast } from "@/hooks/use-toast";

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export interface UserSettings {
  applicantName: string;
  applicantEmail: string;
  discordBotToken: string;
  discordChannelId: string;
}

export const SETTINGS_STORAGE_KEY = "ai_company_researcher_settings";

export function getSavedSettings(): UserSettings {
  if (typeof window === "undefined") {
    return { applicantName: "", applicantEmail: "", discordBotToken: "", discordChannelId: "" };
  }
  try {
    const raw = localStorage.getItem(SETTINGS_STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    // Ignore parse error
  }
  return {
    applicantName: "John Doe",
    applicantEmail: "john@example.com",
    discordBotToken: "",
    discordChannelId: "",
  };
}

export function SettingsModal({ isOpen, onClose }: SettingsModalProps) {
  const [applicantName, setApplicantName] = useState("");
  const [applicantEmail, setApplicantEmail] = useState("");
  const [discordBotToken, setDiscordBotToken] = useState("");
  const [discordChannelId, setDiscordChannelId] = useState("");

  useEffect(() => {
    if (isOpen) {
      const saved = getSavedSettings();
      setApplicantName(saved.applicantName);
      setApplicantEmail(saved.applicantEmail);
      setDiscordBotToken(saved.discordBotToken);
      setDiscordChannelId(saved.discordChannelId);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const settings: UserSettings = {
      applicantName,
      applicantEmail,
      discordBotToken,
      discordChannelId,
    };
    try {
      localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settings));
      showToast("Configuration Saved", "Discord integration & applicant settings saved successfully.", "success");
      onClose();
    } catch {
      showToast("Storage Error", "Could not save configuration to localStorage.", "error");
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
      <div className="bg-card border border-border rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
        {/* Modal Header */}
        <div className="p-5 border-b border-border bg-muted/30 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-xl">⚙️</span>
            <h3 className="font-bold text-base text-foreground tracking-tight">Discord Integration Settings</h3>
          </div>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground text-sm p-1 font-bold">
            ✕
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSave} className="p-5 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
              Applicant Name
            </label>
            <input
              type="text"
              value={applicantName}
              onChange={(e) => setApplicantName(e.target.value)}
              placeholder="e.g. John Doe"
              className="w-full px-3 py-2 text-xs rounded-xl bg-background border border-border/80 focus:outline-none focus:border-primary text-foreground"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
              Applicant Email
            </label>
            <input
              type="email"
              value={applicantEmail}
              onChange={(e) => setApplicantEmail(e.target.value)}
              placeholder="e.g. john@example.com"
              className="w-full px-3 py-2 text-xs rounded-xl bg-background border border-border/80 focus:outline-none focus:border-primary text-foreground"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
              Discord Bot Token
            </label>
            <input
              type="password"
              value={discordBotToken}
              onChange={(e) => setDiscordBotToken(e.target.value)}
              placeholder="Bot MTExMjM..."
              className="w-full px-3 py-2 text-xs font-mono rounded-xl bg-background border border-border/80 focus:outline-none focus:border-primary text-foreground"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
              Discord Channel ID
            </label>
            <input
              type="text"
              value={discordChannelId}
              onChange={(e) => setDiscordChannelId(e.target.value)}
              placeholder="e.g. 123456789012345678"
              className="w-full px-3 py-2 text-xs font-mono rounded-xl bg-background border border-border/80 focus:outline-none focus:border-primary text-foreground"
            />
          </div>

          {/* Action Buttons */}
          <div className="pt-3 border-t border-border flex items-center justify-end gap-2">
            <Button type="button" onClick={onClose} variant="outline" size="sm" className="rounded-xl text-xs font-semibold">
              Cancel
            </Button>
            <Button type="submit" size="sm" className="rounded-xl text-xs font-semibold bg-primary hover:bg-primary/90 text-primary-foreground shadow">
              Save Configuration
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

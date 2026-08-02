import { useState } from "react";
import { ChatMessage } from "@/types/chat";

/**
 * Custom hook for managing ChatGPT-style conversation state and streaming messages.
 */
export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const sendMessage = async (content: string) => {
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    // Placeholder stream sender interface logic to be implemented
    setIsLoading(false);
  };

  return {
    messages,
    isLoading,
    sendMessage,
  };
}

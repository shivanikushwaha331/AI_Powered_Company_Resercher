import { useState } from "react";
import { ResearchRequestPayload, ResearchResult } from "@/types/research";
import { fetchApi } from "@/lib/api-client";

/**
 * Custom hook for triggering and polling company research operations.
 */
export function useResearch() {
  const [researchData, setResearchData] = useState<ResearchResult | null>(null);
  const [isResearching, setIsResearching] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const startResearch = async (payload: ResearchRequestPayload) => {
    setIsResearching(true);
    setError(null);
    try {
      const response = await fetchApi<{ data: ResearchResult }>(
        "/research",
        {
          method: "POST",
          body: JSON.stringify(payload),
        }
      );
      setResearchData(response.data);
    } catch (err: any) {
      setError(err.message || "Failed to execute research task");
    } finally {
      setIsResearching(false);
    }
  };

  return {
    researchData,
    isResearching,
    error,
    startResearch,
  };
}

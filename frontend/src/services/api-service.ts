import { axiosClient } from "@/lib/axios-client";
import {
  AIStructuredReport,
  CompanyProfile,
  CompetitorDetail,
  ResearchDepth,
  ResearchRequestPayload,
  ResearchResult,
} from "@/types/research";

export interface APIResponseWrapper<T> {
  success: boolean;
  message: string;
  data: T;
}

export interface CrawlRequestPayload {
  url: string;
  max_pages?: number;
  extract_technologies?: boolean;
}

export interface CrawlResult {
  crawl_id: string;
  target_url: string;
  pages_crawled: number;
  extracted_pages: {
    url: string;
    title: string;
    status_code: number;
    content_length: number;
    headings: string[];
    clean_text?: string;
  }[];
  detected_technologies: string[];
  completed_at: string;
}

export interface ReportRequestPayload {
  company_name: string;
  research_id?: string;
  output_format?: "markdown" | "html" | "json";
}

export interface ReportResult {
  report_id: string;
  company_name: string;
  format: string;
  title: string;
  content: string;
  word_count: number;
  generated_at: string;
}

export interface PDFRequestPayload {
  report_id?: string;
  content?: string;
  title: string;
}

export interface PDFResult {
  pdf_id: string;
  file_name: string;
  file_size_bytes: number;
  download_url: string;
  expires_at: string;
  created_at: string;
}

export interface DiscordRequestPayload {
  applicant_name?: string;
  applicant_email?: string;
  company_name: string;
  company_website?: string;
  summary?: string;
  title?: string;
  pdf_url?: string;
  webhook_url?: string;
  bot_token?: string;
  channel_id?: string;
}

export interface DiscordResult {
  dispatch_id: string;
  status: string;
  message_id: string;
  channel_name: string;
  dispatched_at: string;
}

export interface HealthResult {
  status: string;
  app_name: string;
  environment: string;
  version: string;
  timestamp: string;
}

export interface AIGenerateRequestPayload {
  company_name: string;
  crawled_content: string;
  model?: string;
}

class APIService {
  /**
   * GET /health - Check backend system health
   */
  async getHealth(): Promise<HealthResult> {
    const response = await axiosClient.get<HealthResult>("/health");
    return response.data;
  }

  /**
   * GET /ai/models - Get list of supported OpenRouter models
   */
  async getAvailableModels(): Promise<string[]> {
    try {
      const response = await axiosClient.get<APIResponseWrapper<string[]>>("/ai/models");
      return response.data.data;
    } catch {
      return [
        "google/gemini-2.5-flash",
        "anthropic/claude-3.5-sonnet",
        "openai/gpt-4o-mini",
        "deepseek/deepseek-r1",
      ];
    }
  }

  /**
   * POST /ai/generate - Synthesize 8-part structured AI report using OpenRouter
   */
  async generateAIReport(payload: AIGenerateRequestPayload): Promise<AIStructuredReport> {
    const response = await axiosClient.post<APIResponseWrapper<AIStructuredReport>>(
      "/ai/generate",
      payload
    );
    return response.data.data;
  }

  /**
   * POST /competitors - Analyze direct competitors and resolve missing URLs via Serper
   */
  async analyzeCompetitors(company_name: string, competitor_names?: string[]): Promise<{ target_company: string; competitors: CompetitorDetail[] }> {
    const response = await axiosClient.post<APIResponseWrapper<{ target_company: string; competitors: CompetitorDetail[] }>>(
      "/competitors",
      { company_name, competitor_names }
    );
    return response.data.data;
  }

  /**
   * POST /research - Execute company research task
   */
  async researchCompany(payload: ResearchRequestPayload): Promise<ResearchResult> {
    const response = await axiosClient.post<APIResponseWrapper<ResearchResult>>(
      "/research",
      payload
    );
    return response.data.data;
  }

  /**
   * POST /crawl - Crawl target website
   */
  async crawlWebsite(payload: CrawlRequestPayload): Promise<CrawlResult> {
    const response = await axiosClient.post<APIResponseWrapper<CrawlResult>>(
      "/crawl",
      payload
    );
    return response.data.data;
  }

  /**
   * POST /generate-report - Generate formatted research report
   */
  async generateReport(payload: ReportRequestPayload): Promise<ReportResult> {
    const response = await axiosClient.post<APIResponseWrapper<ReportResult>>(
      "/generate-report",
      payload
    );
    return response.data.data;
  }

  /**
   * POST /generate-pdf - Export research report to PDF metadata
   */
  async generatePDF(payload: PDFRequestPayload): Promise<PDFResult> {
    const response = await axiosClient.post<APIResponseWrapper<PDFResult>>(
      "/generate-pdf",
      payload
    );
    return response.data.data;
  }

  /**
   * POST /discord - Dispatch research notification to Discord
   */
  async sendDiscordNotification(payload: DiscordRequestPayload): Promise<DiscordResult> {
    const response = await axiosClient.post<APIResponseWrapper<DiscordResult>>(
      "/discord",
      payload
    );
    return response.data.data;
  }
}

export const apiService = new APIService();

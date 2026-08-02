/**
 * Company Research Data Models matching Backend Pydantic Schemas.
 */

export type ResearchDepth = "quick" | "standard" | "deep";

export interface ResearchRequestPayload {
  company_name: string;
  depth: ResearchDepth;
  specific_focus?: string[];
  model?: string;
}

export interface FinancialMetrics {
  revenue?: string;
  funding_total?: string;
  valuation?: string;
  headcount?: number;
}

export interface CompanyProfile {
  name: string;
  domain?: string;
  website_url?: string;
  industry?: string;
  description?: string;
  headquarters?: string;
  founded_year?: number;
  financials?: FinancialMetrics;
  key_executives: string[];
  tech_stack: string[];
  competitors: string[];
}

export interface CompetitorDetail {
  company_name: string;
  website: string;
  country: string;
  reason_for_competition: string;
}

export interface SearchSource {
  title: string;
  url: string;
  snippet?: string;
}

export interface SWOTAnalysis {
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
}

export interface AIStructuredReport {
  company_summary: string;
  products: string[];
  services: string[];
  pain_points: string[];
  business_model: string;
  target_customers: string[];
  swot_analysis: SWOTAnalysis;
  competitor_suggestions: string[];
  selected_model?: string;
}

export interface ResearchResult {
  task_id: string;
  company_name: string;
  profile?: CompanyProfile;
  summary: string;
  ai_report?: AIStructuredReport;
  competitors_detail?: CompetitorDetail[];
  key_takeaways: string[];
  sources: SearchSource[];
  created_at: string;
}

import { ResearchResult } from "@/types/research";

export const MOCK_RESEARCH_DATABASE: Record<string, ResearchResult> = {
  stripe: {
    task_id: "res_stripe_101",
    company_name: "Stripe, Inc.",
    profile: {
      name: "Stripe",
      domain: "stripe.com",
      website_url: "https://stripe.com",
      industry: "Financial Infrastructure & Payment Processing",
      description:
        "Stripe is a financial infrastructure platform for businesses. Millions of companies—from the world's largest enterprises to the most ambitious startups—use Stripe to accept payments, grow their revenue, and accelerate new business opportunities.",
      headquarters: "San Francisco, CA & Dublin, Ireland",
      founded_year: 2010,
      financials: {
        revenue: "$14.3 Billion (2023)",
        funding_total: "$8.7 Billion",
        valuation: "$65 Billion",
        headcount: 7000,
      },
      key_executives: ["Patrick Collison (CEO)", "John Collison (President)", "Stefany Goradia (CFO)"],
      tech_stack: ["React", "TypeScript", "Ruby", "Go", "PostgreSQL", "AWS", "Redis", "Kafka", "Sorbet"],
      competitors: ["Adyen", "PayPal", "Square (Block)", "Checkout.com"],
    },
    summary: `### Executive Overview
Stripe is the leading payment processor for internet businesses. Known for its developer-first API integration model, Stripe has expanded from simple credit card processing into a full suite of financial operations tools including subscription billing, corporate cards, identity verification, and banking-as-a-service.

### Key Competitive Highlights
- **Developer Adoption:** Industry standard SDKs and documentation.
- **Global Reach:** Supports 135+ currencies and local payment methods worldwide.
- **AI & Fraud Prevention:** Radar AI processes billions of signals daily to minimize payment fraud.`,
    key_takeaways: [
      "Processes $1+ Trillion in annual payment volume.",
      "Expanded enterprise penetration with customers like Amazon, Salesforce, and BMW.",
      "High growth in AI agent monetization API integrations.",
    ],
    sources: [
      {
        title: "Stripe Official Press & Annual Letter",
        url: "https://stripe.com/newsroom",
        snippet: "Stripe reports record transaction volume growth and expanding global merchant footprint.",
      },
      {
        title: "TechCrunch: Stripe Valuation & Growth Analysis",
        url: "https://techcrunch.com/stripe-analysis",
        snippet: "In-depth breakdown of Stripe's enterprise billing expansion and financial infrastructure tech stack.",
      },
    ],
    created_at: new Date().toISOString(),
  },
  nvidia: {
    task_id: "res_nvidia_102",
    company_name: "NVIDIA Corporation",
    profile: {
      name: "NVIDIA",
      domain: "nvidia.com",
      website_url: "https://nvidia.com",
      industry: "Semiconductors & Artificial Intelligence Hardware",
      description:
        "NVIDIA is the global leader in accelerated computing and graphics processing units (GPUs). Its chips power the vast majority of modern AI model training and inference workloads globally.",
      headquarters: "Santa Clara, CA, USA",
      founded_year: 1993,
      financials: {
        revenue: "$60.9 Billion (FY2024)",
        funding_total: "Public (NASDAQ: NVDA)",
        valuation: "$3.1 Trillion",
        headcount: 29600,
      },
      key_executives: ["Jensen Huang (Founder & CEO)", "Colette Kress (CFO)", "Ian Buck (VP Accelerating Computing)"],
      tech_stack: ["CUDA", "C++", "Python", "TensorRT", "PyTorch", "NeMo", "Linux", "Verilog"],
      competitors: ["AMD", "Intel", "Google TPU", "Amazon Inferentia"],
    },
    summary: `### Executive Overview
NVIDIA has established a near-monopolistic ecosystem in AI accelerated hardware thanks to its proprietary CUDA software moat alongside cutting-edge GPU architectures (Hopper H100/H200, Blackwell B200).

### Key Competitive Highlights
- **Software Moat:** 15+ years of CUDA developer optimizations create extreme lock-in.
- **Data Center Growth:** Over 80% of revenue driven by cloud provider AI compute demand.
- **Full-Stack AI Solutions:** Hardware, networking (InfiniBand/Spectrum-X), and AI software stacks.`,
    key_takeaways: [
      "Controls an estimated 85-90% market share in generative AI training chips.",
      "Blackwell architecture promises 30x performance improvement for LLM inference workloads.",
      "Expanding into sovereign AI data centers worldwide.",
    ],
    sources: [
      {
        title: "NVIDIA Quarterly Financial Results & GTC Keynote",
        url: "https://nvidia.com/investors",
        snippet: "NVIDIA announces Blackwell GPU platform architecture and record data center revenue.",
      },
    ],
    created_at: new Date().toISOString(),
  },
};

export function getMockResearchData(query: string): ResearchResult {
  const normalized = query.toLowerCase().trim();
  if (normalized.includes("stripe")) return MOCK_RESEARCH_DATABASE.stripe;
  if (normalized.includes("nvidia") || normalized.includes("nvda")) return MOCK_RESEARCH_DATABASE.nvidia;

  // Generic Mock Generator for any custom input
  const cleanName = query.charAt(0).toUpperCase() + query.slice(1);
  return {
    task_id: `res_${Math.random().toString(36).substring(2, 9)}`,
    company_name: cleanName,
    profile: {
      name: cleanName,
      domain: `${normalized.replace(/[^a-z0-9]/g, "")}.com`,
      website_url: `https://${normalized.replace(/[^a-z0-9]/g, "")}.com`,
      industry: "Technology & Software Solutions",
      description: `${cleanName} is an innovative enterprise software company specializing in cloud technologies, automated workflows, and data intelligence services.`,
      headquarters: "San Francisco, CA",
      founded_year: 2018,
      financials: {
        revenue: "$120 Million (Est.)",
        funding_total: "$45 Million (Series B)",
        valuation: "$400 Million",
        headcount: 350,
      },
      key_executives: ["Alex Mercer (CEO)", "Elena Vance (CTO)"],
      tech_stack: ["Next.js", "TypeScript", "Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
      competitors: ["Competitor Alpha", "Competitor Beta", "Enterprise Corp"],
    },
    summary: `### Executive Overview for ${cleanName}\n\n**${cleanName}** demonstrates strong product-market fit with accelerated year-over-year revenue growth. Their modern technical architecture and customer retention metrics position them as a key player in their industry.\n\n### Strategic Highlights\n- **Market Expansion:** Expanding international channel partnerships.\n- **Product Innovation:** Integrating AI capabilities directly into core customer workflows.`,
    key_takeaways: [
      `${cleanName} achieves 45% annual growth rate in enterprise subscription ARR.`,
      "High customer retention rate with expanding net dollar retention (NDR).",
      "Modern async microservices infrastructure.",
    ],
    sources: [
      {
        title: `${cleanName} Corporate Portal & Industry Insights`,
        url: `https://${normalized.replace(/[^a-z0-9]/g, "")}.com`,
        snippet: `Official website overview and market research summary for ${cleanName}.`,
      },
    ],
    created_at: new Date().toISOString(),
  };
}

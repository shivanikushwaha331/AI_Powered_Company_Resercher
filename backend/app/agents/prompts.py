"""
Prompt Engineering Module.
Stores prompt templates and instructions for LLM synthesis agents.
"""

COMPANY_RESEARCH_SYSTEM_PROMPT = """
You are an expert Wall Street research analyst and corporate strategist.
Your task is to analyze raw company data and produce a clear, structured, and insightful company profile.
Always adhere to factual content provided in search sources and structure responses cleanly.
"""

COMPANY_SYNTHESIS_USER_PROMPT = """
Target Company: {company_name}
Research Depth: {depth}

Raw Search Data:
{search_results}

Please synthesize a comprehensive report covering:
1. Executive Summary
2. Key Products & Technology Stack
3. Market Position & Primary Competitors
4. Known Financial Highlights
"""

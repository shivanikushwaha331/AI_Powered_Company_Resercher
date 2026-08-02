"""
ReportLab PDF Generation Service Module.
Compiles professional, styled corporate research reports into PDF format.
Includes Cover Page, Company Info, Executive Summary, Products, Services, Pain Points, SWOT Matrix, Competitors, and Numbered Canvas Footers.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from backend.schemas.pdf import PDFRequest, PDFResponse
from backend.utils.helpers import generate_task_id, get_current_utc_timestamp
from backend.utils.logger import logger


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render 'Page X of Y' footers and running headers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Skip header/footer decorations on Cover Page (Page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        self.drawString(54, 11 * 72 - 36, "AI Company Research Assistant — Corporate Report")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Running Footer
        date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
        footer_text = f"Generated Date: {date_str} | Confidential Research"
        page_text = f"Page {self._pageNumber} of {page_count}"

        self.line(54, 45, 8.5 * 72 - 54, 45)
        self.drawString(54, 30, footer_text)
        self.drawRightString(8.5 * 72 - 54, 30, page_text)

        self.restoreState()


class PDFService:
    """Compiles corporate research data into professional PDF documents using ReportLab."""

    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "downloads", "pdf")

    def __init__(self):
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

    async def generate_pdf(
        self,
        request: PDFRequest,
        research_data: Optional[Dict[str, Any]] = None,
    ) -> PDFResponse:
        """Compiles ReportLab PDF document and returns file download metadata."""
        pdf_id = generate_task_id("pdf")
        safe_title = "".join(c for c in request.title if c.isalnum() or c in (" ", "_")).strip().replace(" ", "_")
        file_name = f"{safe_title.lower()}_{pdf_id}.pdf"
        file_path = os.path.join(self.OUTPUT_DIR, file_name)

        logger.info(f"Compiling ReportLab PDF report '{file_name}' at {file_path}")

        # Build ReportLab PDF elements
        self._build_pdf_document(file_path, file_name, request, research_data)

        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 102400
        expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()

        return PDFResponse(
            pdf_id=pdf_id,
            file_name=file_name,
            file_size_bytes=file_size,
            download_url=f"http://localhost:8000/api/v1/downloads/pdf/{pdf_id}",
            expires_at=expires_at,
            created_at=get_current_utc_timestamp(),
        )

    def get_pdf_file_path(self, pdf_id: str) -> Optional[str]:
        """Resolves file path for a given PDF ID."""
        for fn in os.listdir(self.OUTPUT_DIR):
            if pdf_id in fn and fn.endswith(".pdf"):
                return os.path.join(self.OUTPUT_DIR, fn)
        return None

    def _build_pdf_document(
        self,
        file_path: str,
        file_name: str,
        request: PDFRequest,
        data: Optional[Dict[str, Any]],
    ):
        """Assembles ReportLab story elements into PDF file."""
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54,
        )

        styles = getSampleStyleSheet()

        # Custom Typography Styles
        title_style = ParagraphStyle(
            "CoverTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#0F172A"),
            alignment=0,
        )

        subtitle_style = ParagraphStyle(
            "CoverSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#2563EB"),
            alignment=0,
        )

        h1_style = ParagraphStyle(
            "SectionH1",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=14,
            spaceAfter=8,
        )

        h2_style = ParagraphStyle(
            "SectionH2",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#2563EB"),
            spaceBefore=10,
            spaceAfter=4,
        )

        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155"),
            spaceAfter=6,
        )

        bullet_style = ParagraphStyle(
            "BulletCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#334155"),
            leftIndent=12,
            spaceAfter=4,
        )

        table_header_style = ParagraphStyle(
            "TableHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=colors.white,
        )

        table_cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#0F172A"),
        )

        story = []

        # Extract values or use structured defaults
        company_name = data.get("company_name", "Stripe, Inc.") if data else "Stripe, Inc."
        domain = data.get("domain", "stripe.com") if data else "stripe.com"
        industry = data.get("industry", "Financial Infrastructure & Payment Processing") if data else "Financial Technology"
        revenue = data.get("revenue", "$14.3 Billion") if data else "$14.3 Billion"
        headcount = data.get("headcount", "7,000+ employees") if data else "7,000+ employees"
        summary_text = data.get("summary", request.content or "Stripe is a financial infrastructure platform powering online payments, subscription billing, and corporate card management for millions of businesses worldwide.") if data else (request.content or "Stripe is a leading financial infrastructure company.")
        products = data.get("products", ["Stripe Payments API", "Stripe Billing & Subscriptions", "Stripe Radar AI Fraud Detection", "Stripe Connect", "Stripe Treasury"]) if data else ["Stripe Payments API", "Stripe Billing", "Stripe Radar AI", "Stripe Connect"]
        services = data.get("services", ["Implementation Engineering Consulting", "24/7 Enterprise Account Support", "Fraud Policy & Risk Auditing"]) if data else ["Implementation Engineering", "Enterprise Account Management"]
        pain_points = data.get("pain_points", ["High complexity of managing global cross-border payments & currency conversions", "Elevated risk of credit card chargebacks and online transaction fraud", "Manual overhead of multi-country tax compliance and recurring billing operations"]) if data else ["Global payment complexity", "Online fraud risks", "Billing overhead"]
        business_model = data.get("business_model", "Per-transaction fee model (2.9% + $0.30 per charge) combined with monthly SaaS subscription tiers for advanced billing.") if data else "Per-transaction fee and SaaS subscription model."
        target_customers = data.get("target_customers", ["Internet Startups & SaaS Platforms", "Global Enterprise Retailers (Amazon, Salesforce)", "Marketplace Creators & On-Demand Networks"]) if data else ["SaaS Companies", "E-commerce Retailers", "Marketplaces"]

        swot_strengths = data.get("swot_strengths", ["Industry-leading developer adoption & API documentation", "Robust international currency & local payment support", "Advanced Radar AI fraud detection engine"]) if data else ["Developer adoption", "Global payment support", "Radar AI fraud engine"]
        swot_weaknesses = data.get("swot_weaknesses", ["Higher processing fees compared to legacy interchange-plus providers", "Strict automated risk suspension rules"]) if data else ["Higher transaction fees", "Automated risk suspensions"]
        swot_opportunities = data.get("swot_opportunities", ["Rapid expansion into embedded Banking-as-a-Service (BaaS)", "Monetization of AI agent payment autonomous APIs"]) if data else ["Embedded banking (BaaS)", "AI agent payment APIs"]
        swot_threats = data.get("swot_threats", ["Intense competition from regional specialists like Adyen & Checkout.com", "Changing interchange fee caps and regulatory pressure"]) if data else ["Competition from Adyen", "Regulatory pressure"]

        competitors = data.get("competitors", [
            {"name": "Adyen N.V.", "website": "https://www.adyen.com", "country": "Netherlands", "reason": "Direct global competitor in enterprise merchant acquiring and POS infrastructure."},
            {"name": "PayPal / Braintree", "website": "https://www.paypal.com", "country": "United States", "reason": "Competes in digital wallets, checkout buttons, and merchant payment processing."},
            {"name": "Block, Inc. (Square)", "website": "https://squareup.com", "country": "United States", "reason": "Competes in point-of-sale hardware and small business payment processing."},
            {"name": "Checkout.com", "website": "https://www.checkout.com", "country": "United Kingdom", "reason": "Enterprise payment processing platform offering global credit card acquiring."},
        ]) if data else [
            {"name": "Adyen", "website": "https://www.adyen.com", "country": "Netherlands", "reason": "Global enterprise payment processor."},
            {"name": "PayPal", "website": "https://www.paypal.com", "country": "United States", "reason": "Digital wallet and checkout processor."},
        ]

        # ----------------------------------------------------
        # 1. COVER PAGE
        # ----------------------------------------------------
        story.append(Spacer(1, 40))
        story.append(Paragraph("AI Company Research Assistant", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Corporate Research Report:<br/><b>{company_name}</b>", title_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor("#2563EB"), spaceBefore=5, spaceAfter=25))

        gen_date = datetime.now(timezone.utc).strftime("%B %d, %Y")
        meta_html = (
            f"<b>Target Domain:</b> {domain}<br/>"
            f"<b>Industry:</b> {industry}<br/>"
            f"<b>Generation Date:</b> {gen_date}<br/>"
            f"<b>Report Document ID:</b> {file_name}"
        )
        story.append(Paragraph(meta_html, body_style))

        story.append(Spacer(1, 200))
        story.append(Paragraph("CONFIDENTIAL CORPORATE INTELLIGENCE • PREPARED BY AI RESEARCH ENGINE", ParagraphStyle("Conf", parent=body_style, fontSize=8, textColor=colors.HexColor("#94A3B8"))))
        story.append(PageBreak())

        # ----------------------------------------------------
        # 2. COMPANY INFORMATION & METRICS
        # ----------------------------------------------------
        story.append(Paragraph("1. Company Information & Metrics", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=10))

        info_data = [
            [Paragraph("Company Name", table_header_style), Paragraph("Official Domain", table_header_style), Paragraph("Estimated Revenue", table_header_style), Paragraph("Headcount", table_header_style)],
            [Paragraph(company_name, table_cell_style), Paragraph(domain, table_cell_style), Paragraph(revenue, table_cell_style), Paragraph(headcount, table_cell_style)],
        ]
        info_table = Table(info_data, colWidths=[130, 130, 120, 124])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 15))

        # ----------------------------------------------------
        # 3. EXECUTIVE SUMMARY
        # ----------------------------------------------------
        story.append(Paragraph("2. Executive Summary", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=10))
        story.append(Paragraph(summary_text, body_style))
        story.append(Spacer(1, 15))

        # ----------------------------------------------------
        # 4. PRODUCTS & SERVICES
        # ----------------------------------------------------
        story.append(Paragraph("3. Key Products & Professional Services", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=10))

        story.append(Paragraph("<b>Primary Products & Software Platforms:</b>", h2_style))
        for p in products:
            story.append(Paragraph(f"• {p}", bullet_style))

        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Professional Services Offered:</b>", h2_style))
        for s in services:
            story.append(Paragraph(f"• {s}", bullet_style))

        story.append(Spacer(1, 15))

        # ----------------------------------------------------
        # 5. PAIN POINTS & BUSINESS MODEL
        # ----------------------------------------------------
        story.append(Paragraph("4. Customer Pain Points & Business Model", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=10))

        story.append(Paragraph("<b>Customer Pain Points Solved:</b>", h2_style))
        for pp in pain_points:
            story.append(Paragraph(f"💡 {pp}", bullet_style))

        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Monetization & Business Model:</b>", h2_style))
        story.append(Paragraph(business_model, body_style))

        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Target Customer Segments:</b>", h2_style))
        for tc in target_customers:
            story.append(Paragraph(f"🎯 {tc}", bullet_style))

        story.append(Spacer(1, 15))

        # ----------------------------------------------------
        # 6. SWOT ANALYSIS MATRIX
        # ----------------------------------------------------
        story.append(Paragraph("5. 4-Quadrant SWOT Analysis", h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=10))

        str_text = "<br/>".join([f"• {s}" for s in swot_strengths])
        weak_text = "<br/>".join([f"• {w}" for w in swot_weaknesses])
        opp_text = "<br/>".join([f"• {o}" for o in swot_opportunities])
        thr_text = "<br/>".join([f"• {t}" for t in swot_threats])

        swot_data_matrix = [
            [Paragraph("💪 <b>STRENGTHS</b>", table_header_style), Paragraph("⚠️ <b>WEAKNESSES</b>", table_header_style)],
            [Paragraph(str_text, table_cell_style), Paragraph(weak_text, table_cell_style)],
            [Paragraph("🚀 <b>OPPORTUNITIES</b>", table_header_style), Paragraph("🛡️ <b>THREATS</b>", table_header_style)],
            [Paragraph(opp_text, table_cell_style), Paragraph(thr_text, table_cell_style)],
        ]

        swot_table = Table(swot_data_matrix, colWidths=[252, 252])
        swot_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#059669")), # Strengths header (Emerald)
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#DC2626")), # Weaknesses header (Red)
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor("#2563EB")), # Opportunities header (Blue)
            ('BACKGROUND', (1, 2), (1, 2), colors.HexColor("#D97706")), # Threats header (Amber)
            ('BACKGROUND', (0, 1), (1, 1), colors.HexColor("#F8FAFC")),
            ('BACKGROUND', (0, 3), (1, 3), colors.HexColor("#F8FAFC")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(swot_table)
        story.append(Spacer(1, 15))

        # ----------------------------------------------------
        # 7. COMPETITORS TABLE
        # ----------------------------------------------------
        story.append(KeepTogether([
            Paragraph("6. Identified Market Competitors", h1_style),
            HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=10),
        ]))

        comp_rows = [[Paragraph("Company", table_header_style), Paragraph("Website", table_header_style), Paragraph("Country", table_header_style), Paragraph("Reason for Competition", table_header_style)]]
        for c in competitors:
            c_name = c.get("name") or c.get("company_name", "Competitor")
            c_site = c.get("website", "")
            c_country = c.get("country", "Global")
            c_reason = c.get("reason") or c.get("reason_for_competition", "")
            comp_rows.append([
                Paragraph(f"<b>{c_name}</b>", table_cell_style),
                Paragraph(f"<font color='#2563EB'><u>{c_site}</u></font>", table_cell_style),
                Paragraph(c_country, table_cell_style),
                Paragraph(c_reason, table_cell_style),
            ])

        comp_table = Table(comp_rows, colWidths=[100, 110, 84, 210])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ]))
        story.append(comp_table)

        # Build document with NumberedCanvas
        doc.build(story, canvasmaker=NumberedCanvas)


def get_pdf_service() -> PDFService:
    """FastAPI Dependency Provider for PDFService."""
    return PDFService()

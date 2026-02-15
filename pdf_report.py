from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from datetime import datetime
import html


def save_pdf_report(host, open_ports, scan_time):
    filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    safe_host = html.escape(host)

    elements.append(Paragraph("PORT SCAN REPORT", title_style))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"<b>Target:</b> {safe_host}", normal_style))
    elements.append(Paragraph(f"<b>Scan completed:</b> {datetime.now()}", normal_style))
    elements.append(Paragraph(f"<b>Scan duration:</b> {scan_time} seconds", normal_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 0.3 * inch))

    if open_ports:
        elements.append(Paragraph("<b>Open Ports:</b>", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        for port in sorted(open_ports):
            elements.append(Paragraph(f"Port {port} — OPEN", normal_style))
            elements.append(Spacer(1, 0.1 * inch))
    else:
        elements.append(Paragraph("No open ports found.", normal_style))

    doc.build(elements)
    return filename

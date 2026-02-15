import os
import html
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

def save_txt_report(host, results):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/port_report_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Port scan report for {host}\n")
        f.write(f"Generated at: {datetime.now()}\n")
        f.write("="*40 + "\n")
        for port, status in results:
            f.write(f"{port}: {status}\n")
    return filename

def save_pdf_report(host, results, scan_time):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/port_report_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    elements.append(Paragraph(f"Port scan report for {host}", title_style))
    elements.append(Paragraph(f"Generated at: {datetime.now()}", normal_style))
    elements.append(Paragraph(f"Scan duration: {scan_time} seconds", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(HRFlowable(width="100%", thickness=1))
    elements.append(Spacer(1, 0.2*inch))

    for port, status in results:
        status_safe = html.escape(status)
        color = "green" if status == "open" else "red" if status == "closed" else "orange"
        elements.append(
            Paragraph(f"{port}: <font color='{color}'>{status_safe}</font>", normal_style)
        )
        elements.append(Spacer(1, 0.05*inch))

    doc.build(elements)
    return filename
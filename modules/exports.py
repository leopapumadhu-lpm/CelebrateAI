from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet

def make_pdf(plan):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("CelebrateAI - Event Plan", styles["Title"]),
        Spacer(1, 16),
        Paragraph(plan["concept"], styles["BodyText"]),
        Spacer(1, 16),
        Paragraph("Personalized Ideas", styles["Heading2"])
    ]
    for idea in plan["ideas"]:
        story.append(Paragraph("• " + idea, styles["BodyText"]))
    story += [
        Spacer(1, 16),
        Paragraph("Budget Breakdown", styles["Heading2"])
    ]
    rows = [["Category", "Amount (INR)"]]
    rows += [[x["Category"], f'{x["Amount (INR)"]:,.0f}'] for x in plan["budget"]]
    story.append(Table(rows))
    story += [
        Spacer(1, 16),
        Paragraph("Event Timeline", styles["Heading2"])
    ]
    rows = [["Task", "Deadline"]]
    rows += [[x["Task"], x["Deadline"]] for x in plan["timeline"]]
    story.append(Table(rows, repeatRows=1))
    doc.build(story)
    return buffer.getvalue()

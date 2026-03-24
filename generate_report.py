from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas
import os

img_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(img_dir, "report.pdf")

# Header auf jeder Seite
class HeaderCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for page in self.pages:
            self.__dict__.update(page)
            self._draw_header()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_header(self):
        width, height = A4
        y = height - 1.5 * cm
        self.setFont("Helvetica", 9)
        # Links: Namen
        self.drawString(2.5 * cm, y, "Adrian Hansen, Marko Misic")
        # Mitte: FHTW, PRP
        self.drawCentredString(width / 2, y, "FHTW, PRP")
        # Rechts: Datum
        self.drawRightString(width - 2.5 * cm, y, "25.03.2026")
        # Linie drunter
        self.setStrokeColor(colors.grey)
        self.line(2.5 * cm, y - 5, width - 2.5 * cm, y - 5)


doc = SimpleDocTemplate(output_path, pagesize=A4,
                        leftMargin=2.5*cm, rightMargin=2.5*cm,
                        topMargin=3*cm, bottomMargin=2.5*cm)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=22, spaceAfter=6)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=13, alignment=TA_CENTER, spaceAfter=30, textColor=colors.grey)
heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading1'], fontSize=15, spaceBefore=20, spaceAfter=10)
body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=11, leading=15, spaceAfter=8)
bold_style = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')

story = []

# Titel
story.append(Paragraph("Parallel Mandelbrot - Report", title_style))
story.append(Paragraph("Exercise 2: Data Parallelism", subtitle_style))

# 1. Approach
story.append(Paragraph("1. Approach", heading_style))

story.append(Paragraph(
    "The Mandelbrot set was implemented in C using OpenMP for parallelization. "
    "The stb_image_write library was used for PNG image output. The project runs "
    "inside a VS Code Dev Container (Ubuntu 22.04) to ensure consistent builds "
    "across macOS, Windows, and Linux.",
    body_style))

story.append(Paragraph("Parallelization Strategy:", bold_style))
story.append(Paragraph(
    "We used data parallelism via OpenMP's <font face='Courier'>#pragma omp parallel for</font> "
    "directive on the outer loop (rows of pixels). Each thread processes a set of rows independently. "
    "Since each pixel's computation is completely independent from every other pixel, "
    "no synchronization or locking is needed — there are no shared variables being written to, "
    "and each thread writes to its own section of the image array.",
    body_style))

story.append(Paragraph("Scheduling Scheme:", bold_style))
story.append(Paragraph(
    "We chose <font face='Courier'>schedule(dynamic)</font> instead of the default static scheduling. "
    "This is important because not all pixels require the same amount of work. "
    "Pixels outside the Mandelbrot set diverge quickly (sometimes after just 2 iterations), "
    "while pixels inside or near the boundary need the full 1000 iterations. "
    "With static scheduling, some threads would finish early and sit idle while others are still "
    "computing the complex boundary regions. Dynamic scheduling distributes rows on-demand, "
    "so threads that finish early immediately pick up new work.",
    body_style))

story.append(Paragraph(
    "The program accepts configurable parameters via command line arguments: "
    "image dimensions (width, height), maximum iterations, thread count (for benchmarking), "
    "and viewport coordinates (min_x, min_y, max_x, max_y) for zooming.",
    body_style))

# 2. Example Image
story.append(PageBreak())
story.append(Paragraph("2. Example Image", heading_style))

story.append(Paragraph(
    "The following image was generated with the command:", body_style))
story.append(Paragraph(
    "<font face='Courier'>./mandelbrot 2048 2048 1000 8</font>", body_style))
story.append(Paragraph(
    "Settings: 2048x2048 pixels, 1000 max iterations, 8 threads, "
    "Viewport: (-2.0, -1.0, 1.0, 1.0)", body_style))
story.append(Spacer(1, 10))

mandelbrot_path = os.path.join(img_dir, "mandelbrot_parallel.png")
if os.path.exists(mandelbrot_path):
    story.append(Image(mandelbrot_path, width=14*cm, height=14*cm))
else:
    story.append(Paragraph("<i>[mandelbrot_parallel.png not found]</i>", body_style))

# 3. Performance Measurements
story.append(PageBreak())
story.append(Paragraph("3. Performance Measurements", heading_style))

story.append(Paragraph(
    "All benchmarks were run on a 2048x2048 image with 1000 max iterations. "
    "Only the pure computation time was measured (excluding disk I/O), "
    "using <font face='Courier'>omp_get_wtime()</font> before and after the parallel loop. "
    "The Docker container had access to 8 CPU cores.",
    body_style))
story.append(Spacer(1, 10))

table_data = [
    ["Threads", "Time (s)", "Speedup (T_s / T_n)"],
    ["1", "3.7314", "1.00x"],
    ["2", "1.8722", "1.99x"],
    ["4", "0.9900", "3.77x"],
    ["8", "0.6810", "5.48x"],
]
t = Table(table_data, colWidths=[4*cm, 4*cm, 5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 15))

story.append(Paragraph(
    "We also ran additional tests beyond the core count to observe the effect of "
    "over-subscribing threads:", body_style))
story.append(Spacer(1, 5))

extra_data = [
    ["Threads", "Time (s)", "Speedup (T_s / T_n)"],
    ["16", "0.6407", "5.83x"],
    ["32", "0.6435", "5.80x"],
    ["64", "0.6493", "5.75x"],
]
t2 = Table(extra_data, colWidths=[4*cm, 4*cm, 5*cm])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(t2)
story.append(Spacer(1, 15))

graph_path = os.path.join(img_dir, "speedup_graph.png")
if os.path.exists(graph_path):
    story.append(Image(graph_path, width=14*cm, height=10*cm))
else:
    story.append(Paragraph("<i>[speedup_graph.png not found]</i>", body_style))

# 4. Analysis
story.append(Spacer(1, 10))
story.append(Paragraph("4. Analysis", heading_style))

story.append(Paragraph(
    "The results show near-linear speedup up to 2 threads (1.99x), with diminishing returns "
    "as thread count increases. At 4 threads we achieved 3.77x speedup (vs. ideal 4.0x), "
    "and at 8 threads we reached 5.48x (vs. ideal 8.0x).",
    body_style))

story.append(Paragraph(
    "Beyond 8 threads (the number of available CPU cores), performance completely plateaus. "
    "Running with 16, 32, or 64 threads gives no improvement because the extra threads "
    "simply queue up waiting for a free core. There is no additional parallelism to exploit, "
    "and the small overhead of managing more threads causes a very slight slowdown.",
    body_style))

story.append(Paragraph(
    "The gap between measured and ideal speedup is expected and can be attributed to:",
    body_style))

reasons = [
    "Thread creation and scheduling overhead",
    "Memory bandwidth becoming a bottleneck as all cores access the image array",
    "Cache contention between cores",
    "The inherent serial portion of the program (Amdahl's Law)",
]
for r in reasons:
    story.append(Paragraph(f"&bull; {r}", ParagraphStyle('Bullet', parent=body_style, leftIndent=20)))

story.append(Spacer(1, 8))
story.append(Paragraph(
    "The choice of <font face='Courier'>schedule(dynamic)</font> was important for load balancing. "
    "Pixels near the boundary of the Mandelbrot set require significantly more iterations than those "
    "far outside the set, so static scheduling would lead to uneven workloads across threads.",
    body_style))

doc.build(story, canvasmaker=HeaderCanvas)
print(f"Report saved as {output_path}")

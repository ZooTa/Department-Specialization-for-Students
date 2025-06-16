import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from textwrap import wrap
import random


class ReportService:
    def __init__(self, preference_service, margin=50):
        self.preference_service = preference_service
        self.margin = margin
        self.width, self.height = A4
        self.line_height = 14

    def _color_ge(self, num):
        color_list = ["#D3D3D3", "#002147", "#FFC107"]
        colors = []
        last_color = None
        for _ in range(num):
            available_colors = [c for c in color_list if c != last_color]
            color = random.choice(available_colors)
            colors.append(color)
            last_color = color
        return colors

    def _generate_summary(self, data: dict) -> str:
        items = [f"{name} got {value:.1f}%" for name, value in data.items()]
        if not items:
            return "No data available to summarize."
        elif len(items) == 1:
            return f"From the chart, we can see that {items[0]}."
        else:
            *all_but_last, last = items
            return f"From the chart, we can see that {', '.join(all_but_last)}, and {last}."

    def _create_chart(self, data, chart_path="chart.png"):
        sns.set(style="whitegrid")
        plt.figure(figsize=(8, 5))
        colors = self._color_ge(len(data))
        bars = plt.bar(data.keys(), data.values(), color=colors)
        for i, val in enumerate(data.values()):
            plt.text(i, val + 1, f"{val:.1f}%", ha='center')
        plt.ylabel("Percentage")
        plt.title("Project Preference Distribution")
        plt.ylim(0, 110)
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    def _add_text_block(self, c, text, font="Helvetica", font_size=12, spacing=10, current_y=None):
        c.setFont(font, font_size)
        max_width = self.width - 2 * self.margin
        line_height = font_size + 2
        approx_char_width = font_size * 0.5
        max_chars_per_line = int(max_width / approx_char_width)
        if current_y is None:
            current_y = self.height - self.margin

        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            wrapped_lines = wrap(paragraph, width=max_chars_per_line)
            for line in wrapped_lines:
                if current_y < self.margin + line_height:
                    c.showPage()
                    current_y = self.height - self.margin
                    c.setFont(font, font_size)
                c.drawString(self.margin, current_y, line)
                current_y -= line_height
            current_y -= spacing
        return current_y

    def _add_image(self, c, image_path, width=400, spacing=20, current_y=None, height=300):
        if current_y is None:
            current_y = self.height - self.margin
        if current_y - height < self.margin:
            c.showPage()
            current_y = self.height - self.margin
        c.drawImage(
            image_path, self.margin, current_y - height,
            width=width, preserveAspectRatio=True, mask='auto'
        )
        current_y -= height + spacing
        return current_y

    def generate_pdf_report(self, filename="final_report.pdf"):
        c = canvas.Canvas(filename, pagesize=A4)
        current_y = self.height - self.margin

        data = self.preference_service.get_first_preference_percentages()  # Expects a dict: { "Student A": 30.0, ... }
        chart_path = self._create_chart(data)
        summary_text = self._generate_summary(data)

        current_y = self._add_text_block(c, "📊 Project Preference Report", font="Helvetica-Bold", font_size=16, current_y=current_y)
        current_y = self._add_text_block(c, "This report summarizes the student preferences for different projects.", current_y=current_y)
        current_y = self._add_image(c, chart_path, width=450, current_y=current_y)
        current_y = self._add_text_block(c, "From the chart above, we can see that the preferences vary among students.", current_y=current_y)
        current_y = self._add_text_block(c, summary_text, current_y=current_y)
        current_y = self._add_text_block(c, "Further insights and analysis will follow in the next pages...", current_y=current_y)

        c.save()
        print("✅ PDF report generated successfully.")

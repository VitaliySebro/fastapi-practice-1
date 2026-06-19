import os

from fpdf import FPDF


def generate_products_report(filename: str, products_list: list[dict]) -> str:
    """
    Генерує PDF-звіт зі списком товарів.
    """
    pdf = FPDF()
    pdf.add_page()

    # Заголовок (використовуємо латиницю Helvetica, щоб уникнути проблем зі шрифтами)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 15, "SYSTEM PRODUCTS REPORT", ln=True, align="C")
    pdf.ln(5)

    # Заголовки таблиці
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(40, 10, "Product ID", border=1, align="C")
    pdf.cell(100, 10, "Product Name", border=1, align="C")
    pdf.cell(50, 10, "Price ($)", border=1, align="C")
    pdf.ln()

    # Наповнення таблиці даними
    pdf.set_font("Helvetica", "", 12)
    for prod in products_list:
        pdf.cell(40, 10, str(prod.get("id")), border=1, align="C")
        pdf.cell(100, 10, str(prod.get("name")), border=1)
        pdf.cell(50, 10, f"{prod.get('price'):.2f}", border=1, align="R")
        pdf.ln()

    # Створення директорії для звітів, якщо її немає
    reports_dir = "generated_reports"
    os.makedirs(reports_dir, exist_ok=True)

    filepath = os.path.join(reports_dir, filename)
    pdf.output(filepath)

    return filepath

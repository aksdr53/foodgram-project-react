import io

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def drawing_shopping_cart(shopping_cart):
    buffer = io.BytesIO()
    pdf_object = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdf_object.setFont('Vera', 14)
    pdf_object.drawCentredString(100, 800, "Список покупок")
    text_height = 700
    for ingredient in shopping_cart:
        pdf_object.drawString(
            100, text_height,
            f'{ingredient["ingredient__name"]} -'
            f'{ingredient["amount"]},'
            f'{ingredient["ingredient__measurement_unit"]}'
        )
        text_height -= 20
        if text_height <= 40:
            text_height = 800
            pdf_object.showPage()
    pdf_object.showPage()
    pdf_object.save()
    buffer.seek(0)
    return buffer

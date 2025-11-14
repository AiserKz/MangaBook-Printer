from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape, A5
from reportlab.lib.utils import ImageReader
import os, webbrowser


class BookBuilder:
    def __init__(self, proggres_callback):
        self.proggres_callback = proggres_callback

    def format_page(self, format_page):
        if format_page == "A4 (210x297mm)":
            return A4
        elif format_page == "A5 (148x210mm)":
            return A5
        else:
            return A4

    def build_pdf(
        self,
        output_path="test/output/book.pdf",
        margin=10,
        padding=10,
        isNumbering=False,
        pages=[],
        isBookMode=True,
        isSavePropety=True,
        format_page="A4 (210x297mm)",
        isAutoOpen=False,
    ):
        page_format = self.format_page(format_page)
        # Используем альбомную ориентацию
        c = canvas.Canvas(output_path, pagesize=landscape(page_format))
        width, height = landscape(page_format)  # width > height в альбомном режиме

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Сохраняем оригинальные страницы для правильной нумерации
        original_pages = pages[:]

        # Если книжный режим, формируем порядок разворотов
        if isBookMode:
            pages = self._prepare_book_order(pages)

        # Правильная нумерация - находим исходные номера страниц
        page_numbers = []
        for p in pages:
            if p == "None":
                page_numbers.append(None)
            else:
                # Находим индекс этой страницы в оригинальном списке
                index = original_pages.index(p)
                page_numbers.append(index + 1)

        total_pages = len(pages)

        # Формируем листы с 2 сканами на страницу
        for i in range(0, len(pages), 2):
            subset = pages[i : i + 2]
            subset_numbers = page_numbers[i : i + 2]
            self._draw_sheet(
                c,
                subset,
                width,
                height,
                margin,
                padding,
                isNumbering,
                subset_numbers,
                isSavePropety,
            )
            c.showPage()

            if self.proggres_callback:
                self.proggres_callback(i + 2, total_pages)
                print(f"Прогресс22: {i + 2}/{total_pages}", end="\r")
            else:
                print(f"Прогресс: {i}/{total_pages}")

        c.save()
        if isAutoOpen:
            self.open_pdf(output_path)

    def _prepare_book_order(self, pages):
        """Формирует порядок страниц для печати книжным стилем"""
        pages = list(pages)  # создаём копию
        n = len(pages)

        # Дополняем до кратного 4 пустыми страницами
        while len(pages) % 4 != 0:
            pages.append("None")

        total_pages = len(pages)
        book_order = []

        # Для каждого блока по 4 страницы формируем разворот
        blocks = total_pages // 4
        for i in range(blocks):
            book_order.append(pages[total_pages - 1 - i * 2])  # внешняя правая
            book_order.append(pages[i * 2])  # внешняя левая
            book_order.append(pages[i * 2 + 1])  # внутренняя левая
            book_order.append(pages[total_pages - 2 - i * 2])  # внутренняя правая

        return book_order

    def _draw_sheet(
        self,
        c: canvas.Canvas,
        images,
        w,
        h,
        margin,
        padding,
        numbering,
        subset_numbers,
        isSavePropety,
    ):
        """Рисует лист с 2 сканами на страницу в альбомном режиме"""
        rows, cols = 1, 2  # 1 ряд, 2 колонки

        # В альбомном режиме ширина больше высоты, поэтому адаптируем расчеты
        img_w = (w - 2 * margin - padding) / cols  # padding только между страницами
        img_h = h - 2 * margin  # используем полную высоту

        for idx, img_path in enumerate(images):
            if img_path == "None" or not os.path.exists(img_path):
                continue

            row = 0
            col = idx % cols

            if col == 0:
                x = margin
            else:
                x = margin + img_w + padding

            y = margin  # рисуем от нижнего края

            if not isSavePropety:
                # Загружаем изображение чтобы получить его размеры
                img = ImageReader(img_path)
                img_width, img_height = img.getSize()

                # Рассчитываем соотношения сторон
                target_ratio = img_w / img_h
                img_ratio = img_width / img_height

                # Поведение cover: масштабируем так чтобы заполнить всю область, обрезая края
                if img_ratio > target_ratio:
                    # Ширина изображения больше - подгоняем по высоте, обрезаем по ширине
                    scale = img_h / img_height
                    scaled_width = img_width * scale
                    # Центрируем по горизонтали
                    x_offset = (scaled_width - img_w) / 2
                    c.drawImage(
                        img,
                        x - x_offset,  # смещаем влево чтобы обрезать
                        y,
                        scaled_width,  # масштабированная ширина
                        img_h,  # полная высота
                    )
                else:
                    # Высота изображения больше - подгоняем по ширине, обрезаем по высоте
                    scale = img_w / img_width
                    scaled_height = img_height * scale
                    # Центрируем по вертикали
                    y_offset = (scaled_height - img_h) / 2
                    c.drawImage(
                        img,
                        x,
                        y - y_offset,  # смещаем вниз чтобы обрезать
                        img_w,
                        scaled_height,  # масштабированная высота
                    )
            else:
                # Просто растягиваем изображение без сохранения пропорций
                c.drawImage(
                    ImageReader(img_path),
                    x,
                    y,
                    img_w,
                    img_h,
                    preserveAspectRatio=True,
                )

            # Нумерация страниц
            if numbering and subset_numbers[idx] is not None:
                page_number = subset_numbers[idx]
                text_x = x + 10 if col == 0 else x + img_w - 25
                text_y = y + 10
                c.setFillColorRGB(1, 1, 1)
                c.rect(text_x - 5, text_y - 3, 20, 12, fill=1, stroke=0)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(text_x, text_y, str(page_number))

    def open_pdf(self, pdf_path):
        abs_path = os.path.abspath(pdf_path)
        if not os.path.exists(abs_path):
            print("Файл не найден:", abs_path)
            return

        webbrowser.open_new(f"file:///{abs_path}")
        print(f"🌐 Открыт PDF в браузере: {abs_path}")

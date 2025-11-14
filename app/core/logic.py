import flet as ft
from typing import List
from .book_builder import BookBuilder
from .Setting import Setting
import zipfile, tempfile, os, shutil, re


class AppLogic:
    def __init__(
        self, page: ft.Page, on_update, update_progress, update_status, testData=None
    ):
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.files_picked)
        self.file_uploader = ft.FilePicker(on_result=self.export_pdf)
        self.page.overlay.append(self.file_picker)
        self.page.overlay.append(self.file_uploader)
        self.pages: List[str] = []
        self.orig_pages: List[str] = []
        self.update = on_update
        self.update_progress = update_progress
        self.update_status = update_status
        self.status = ""
        self.isAutoOpen = False

        self.Setting = Setting()

        self.BookCore = BookBuilder(proggres_callback=self.proggres)

        self.load_setting()

        self.current_progress = 1
        if testData:
            self.pages = testData
            self.orig_pages = testData
        if self.isBookMode:
            self.page_isBook()

        self.cleanup_temp_dirs()

    def proggres(self, value, total):
        percent = int((value / total) * 100)
        print(f"[{value}/{total}] {percent:.1f}% готово")
        self.current_progress = percent
        self.update_progress(self.current_progress)
        if percent == 100:
            self.set_status("Успешно!")
        else:
            self.set_status(f"Загрузка {percent}%")

    def set_status(self, status: str):
        self.status = status or ""
        self.update_status()

    def load_setting(self):
        (
            self.margin,
            self.padding,
            self.format_page,
            self.page_in_page,
            self.isNumbering,
            self.isBookMode,
            self.isSavePropety,
            self.modeView,
            self.isAutoOpen,
        ) = self.Setting.load_setting()

    def save_setting(self):
        self.Setting.save_setting(
            self.margin,
            self.padding,
            self.format_page,
            self.page_in_page,
            self.isNumbering,
            self.isBookMode,
            self.isSavePropety,
            self.modeView,
            self.isAutoOpen,
        )

    def update_ui(self):
        if len(self.pages) > 0:
            self.update()

    def change_isAutoOpen(self, isAutoOpen: bool):
        self.isAutoOpen = isAutoOpen
        self.save_setting()

    def change_mode_view(self, modeView: int):
        self.modeView = modeView
        self.save_setting()
        self.update_ui()

    def change_margin(self, margin: int):
        self.margin = margin
        self.save_setting()
        self.update_ui()

    def change_padding(self, padding: int):
        self.padding = padding
        self.save_setting()
        self.update_ui()

    def change_format_page(self, format_page: str):
        self.format_page = format_page
        self.save_setting()
        self.update_ui()

    def change_page_in_page(self, page_in_page: int):
        self.page_in_page = page_in_page
        self.save_setting()
        self.update_ui()

    def change_isNumbering(self, isNumbering: bool):
        self.isNumbering = isNumbering
        self.save_setting()
        self.update_ui()

    def change_isSavePropety(self, isSavePropety: bool):
        self.isSavePropety = isSavePropety
        self.save_setting()
        self.update_ui()

    def change_isBookMode(self, isBookMode: bool):
        self.isBookMode = isBookMode
        self.save_setting()

        if isBookMode:
            self.page_isBook()
        else:
            self.pages = self.orig_pages

        self.update_ui()

    def page_isBook(self):
        # Лучше лишний раз не трогать тут а то можно все сломать 😁
        pages = self.orig_pages.copy()

        # Дополняем пустыми страницами в конец, чтобы длина кратна 4 пока логика не слишком сложная думаю
        while len(pages) % 4 != 0:
            pages.append("None")

        n = len(pages)
        book_order = []

        for i in range(n // 4):
            # формируем разворот: верхняя правая, верхняя левая, нижняя левая, нижняя правая
            book_order.append(pages[n - 1 - i * 2])  # верхняя правая
            book_order.append(pages[i * 2])  # верхняя левая
            book_order.append(pages[i * 2 + 1])  # нижняя левая
            book_order.append(pages[n - 2 - i * 2])  # нижняя правая

        self.pages = book_order

    def clear_pages(self):
        self.pages = []
        self.orig_pages = []
        self.cleanup_temp_dirs()
        self.update()

    def open_file_picker(self):
        self.file_picker.pick_files(allow_multiple=True)

    def open_file_uploader(self):
        if len(self.pages) == 0:
            self.set_status("Нет страниц для экспорта")
            return
        self.file_uploader.save_file(file_name="default.pdf")

    def files_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                if f.path.lower().endswith(".jpg") or f.path.lower().endswith(".png"):
                    self.pages.append(f.path)
                elif f.path.lower().endswith(".zip"):
                    self.unzip_file(f.path)
                else:
                    print("Неподдерживаемое расширение", f.path)

            self.orig_pages = self.pages.copy()
            if self.isBookMode:
                self.page_isBook()

            self.page.update()
            self.set_status("")
            self.update()

    def unzip_file(self, path):
        print("Распаковываем", path)

        temp_dir = tempfile.mkdtemp(prefix="aisbook_")

        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            pages = zip_ref.namelist()
            print("Успешно распаковано", pages)

        full_paths = [os.path.join(temp_dir, f) for f in pages]

        image_paths = [
            f for f in full_paths if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ]

        def extract_number(f):
            match = re.search(r"(\d+)", os.path.basename(f))
            return int(match.group(1)) if match else float("inf")

        image_paths.sort(key=extract_number)

        self.pages.extend(image_paths)

    def cleanup_temp_dirs(self):
        temp_dir = tempfile.gettempdir()
        prefix = "aisbook_"

        for name in os.listdir(temp_dir):
            if name.startswith(prefix):
                path = os.path.join(temp_dir, name)
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        os.remove(path)
                    print("Удалено временное каталог", path)
                except Exception as e:
                    print(f"⚠ Не удалось удалить {path}: {e}")

    def remove_page(self, page_name):
        if page_name == "None":
            return

        if page_name in self.pages:
            self.pages.remove(page_name)

        if page_name in self.orig_pages:
            self.orig_pages.remove(page_name)

        if self.isBookMode:
            self.page_isBook()

        self.update()

    def export_pdf(self, e: ft.FilePickerResultEvent):
        output_path = e.path
        if output_path:
            self.BookCore.build_pdf(
                output_path=output_path,
                margin=self.margin,
                padding=self.padding,
                isNumbering=self.isNumbering,
                pages=self.orig_pages,
                isBookMode=self.isBookMode,
                isSavePropety=self.isSavePropety,
                format_page=self.format_page,
                isAutoOpen=self.isAutoOpen,
            )

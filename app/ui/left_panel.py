import flet as ft
from style.appstyle import AppColors
from .button import Button
from .dropdown import dropdown_component
from core.logic import AppLogic


class LeftPanel:
    def __init__(self, page: ft.Page, style: AppColors, logic: AppLogic):
        super().__init__()
        self.page = page
        self.style = style
        self.logic = logic

        self.pages_list = ft.ListView(
            controls=(
                self.page_render()
                if len(self.logic.pages) > 0
                else [
                    ft.Text(
                        "Список страниц пуст...",
                        color=self.style.text_base,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                    ),
                ]
            ),
            spacing=5,
            padding=ft.padding.symmetric(vertical=5, horizontal=5),
            auto_scroll=False,
            expand=False,
            height=self.calc_list_height(),
        )

        self.button_delete = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINED,
            tooltip="Удалить страницы",
            on_click=lambda e: self.logic.clear_pages(),
            hover_color=self.style.error,
        )

        self.container = ft.Container(
            ft.ListView(
                [
                    ft.Text(
                        "Файлы проекта",
                        size=18,
                        color=self.style.text_base,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(height=1, thickness=1),
                    ft.Container(
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.FILE_UPLOAD_OUTLINED,
                                        size=34,
                                        color=self.style.text_base,
                                    ),
                                    padding=ft.padding.all(10),
                                    bgcolor=ft.Colors.with_opacity(
                                        0.2, self.style.primary
                                    ),
                                    border_radius=ft.border_radius.all(24),
                                ),
                                ft.Text(
                                    "Импортировать файлы манги",
                                    color=self.style.text_base,
                                ),
                                ft.Text(
                                    ".zip, .jpg, .png",
                                    color=self.style.text_secondary,
                                ),
                                Button(
                                    self.page,
                                    ft.Icons.ADD,
                                    "Добавить страницу",
                                    on_click=lambda e: self.logic.open_file_picker(),
                                    color=self.style.primary,
                                    hover_color=self.style.hover,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=5, vertical=15),
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(6),
                        bgcolor=ft.Colors.with_opacity(0.1, self.style.primary),
                        border=ft.border.all(
                            1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
                        ),
                        margin=ft.margin.all(5),
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Страницы", size=14, weight=ft.FontWeight.BOLD),
                            self.button_delete,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.pages_list,
                    dropdown_component(
                        self.page,
                        "Формат бумаги",
                        ["A4 (210x297mm)", "A5 (148x210mm)"],
                        str(self.logic.format_page),
                        on_change=lambda e: self.logic.change_format_page(
                            e.control.value
                        ),
                    ),
                    # dropdown_component(
                    #     self.page,
                    #     "Страниц на листе",
                    #     ["1 страница", "2 страницы", "4 страницы"],
                    #     str(self.logic.page_in_page),
                    #     on_change=lambda e: self.logic.change_page_in_page(
                    #         e.control.value
                    #     ),
                    # ),
                ],
                spacing=10,
                expand=True,
            ),
            padding=ft.padding.all(15),
            border_radius=ft.border_radius.all(6),
            bgcolor=self.style.base200,
            border=ft.border.only(
                right=ft.border.BorderSide(
                    1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
                )
            ),
            expand=1,
            adaptive=True,
            alignment=ft.alignment.top_center,
        )

    def page_render(self):
        widgets = []
        for page_name in self.logic.pages:
            title = page_name.split("\\")[-1] if type(page_name) == str else ""
            delete_icon = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINED,
                tooltip="Удалить страницу",
                on_click=lambda e, p=page_name: self.remove_page(p),
                opacity=0,
                animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )

            text_label = ft.Text(title, size=13, color=ft.Colors.WHITE)
            size_label = ft.Text("1.2 Мб", size=10, color=ft.Colors.WHITE, opacity=0.5)
            img_box = ft.Image(
                src=page_name,
                fit=ft.ImageFit.COVER,
                border_radius=ft.border_radius.all(6),
                width=40,
                height=50,
            )
            info_column = ft.Column(
                [text_label, size_label],
                spacing=1,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )

            icon_handle = ft.IconButton(
                icon=ft.Icons.DRAG_INDICATOR_ROUNDED,
                tooltip="Переместить страницу",
                on_click=lambda e, p=page_name: print(p),
                opacity=0.5,
            )
            image_container = ft.Row(
                [
                    icon_handle,
                    img_box,
                ],
                spacing=0,
            )

            container = ft.Container(
                content=ft.Row(
                    [
                        image_container,
                        info_column,
                        delete_icon,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                height=60,
                margin=ft.margin.only(bottom=5),
                expand=True,
                alignment=ft.alignment.center,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                border_radius=ft.border_radius.all(6),
                bgcolor=ft.Colors.TRANSPARENT,
                padding=ft.padding.symmetric(vertical=5),
            )

            def hover_handler(e, icon=delete_icon, cont=container):
                if e.data == "true":
                    cont.bgcolor = ft.Colors.with_opacity(0.15, self.style.hover)
                    icon.opacity = 1
                else:
                    cont.bgcolor = ft.Colors.TRANSPARENT
                    icon.opacity = 0
                self.page.update()

            container.on_hover = hover_handler
            widgets.append(container)

        return widgets

    def remove_page(self, page_name):
        self.logic.remove_page(page_name)

    def render(self):
        return self.container

    def calc_list_height(self):
        return max(min(len(self.logic.pages) * 70, 350), 50)

    def update_pages(self):
        self.pages_list.controls = (
            self.page_render()
            if len(self.logic.pages) > 0
            else [
                ft.Text(
                    "Список страниц пуст...",
                    color=self.style.text_base,
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
            ]
        )

        self.pages_list.height = self.calc_list_height()
        self.pages_list.update()

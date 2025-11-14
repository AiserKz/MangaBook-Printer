import flet as ft
from .button import Button
from style.appstyle import AppColors
from core.logic import AppLogic


class PreviewPanel:
    def __init__(self, page: ft.Page, logic: AppLogic, style: AppColors):
        super().__init__()
        self.page = page
        self.logic = logic
        self.style = style
        self.pages_list = self.logic.pages

        self.button_container = self.render_buttons()

        list_pages = self.render_pages_list()

        self.list_container = list_pages

        self.main_container = ft.AnimatedSwitcher(
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=300,
            reverse_duration=300,
            expand=True,
            content=self.list_container,
        )

        self.container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Предварительный просмотр",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            self.button_container,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.main_container,
                ],
                spacing=10,
            ),
            expand=3,
            margin=ft.margin.symmetric(vertical=20),
            padding=ft.padding.symmetric(horizontal=10),
        )

    def page_preview_Grid(self):
        widgets = []

        for i, page_name in enumerate(self.pages_list, start=1):
            number_page = ft.Text(
                str(i),
                size=32,
                color=ft.Colors.WHITE,
                opacity=0.7,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )

            page_info = ft.Column(
                [
                    number_page,
                    ft.Text(
                        page_name,
                        size=13,
                        color=ft.Colors.WHITE,
                    ),
                ],
                spacing=1,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )

            img_box = (
                ft.Image(
                    src=page_name,
                    width=200,
                    height=250,
                    fit=ft.ImageFit.COVER,
                    border_radius=6,
                    opacity=0.5,
                    animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                ),
            )

            container = ft.Container(
                content=ft.Stack(
                    controls=[
                        *img_box,
                        ft.Container(
                            content=page_info,
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                            border_radius=ft.border_radius.all(4),
                        ),
                    ]
                ),
                width=200,
                height=250,
                border_radius=ft.border_radius.all(6),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )

            def on_hover(
                e,
                page_name=page_name,
                cont=container,
                info=page_info,
                img=img_box[0],
            ):
                if e.data == "true":
                    info.opacity = 0
                    img.opacity = 1
                    img.scale = 1.1

                else:
                    info.opacity = 1
                    img.opacity = 0.6
                    img.scale = 1
                self.page.update()

            container.on_hover = on_hover

            widgets.append(container)

        return ft.Container(
            content=ft.Row(
                controls=widgets,
                wrap=True,
                run_spacing=10,
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            alignment=ft.alignment.top_center,
        )

    def page_preview_book(self):
        widgets = []
        row_widgets = []

        for i, page_name in enumerate(self.pages_list, start=1):
            # Картинка страницы
            img_box = ft.Container(
                content=ft.Image(
                    src=page_name,
                    width=300,
                    height=400,
                    fit=(
                        ft.ImageFit.CONTAIN
                        if self.logic.isSavePropety
                        else ft.ImageFit.COVER
                    ),
                    opacity=1,
                    animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                ),
                padding=ft.padding.only(
                    top=(self.logic.margin - 10),
                    bottom=self.logic.margin - 10,
                ),
            )

            if self.logic.isBookMode:
                real_number = (
                    self.logic.orig_pages.index(page_name) + 1
                    if page_name != "None"
                    else ""
                )
            else:
                real_number = i

            # Номер страницы
            page_number = ft.Text(
                str(real_number),
                size=42,
                color=ft.Colors.BLACK,
                opacity=0.7,
                weight=ft.FontWeight.BOLD,
            )

            if self.logic.isNumbering:
                number_left = ft.Container(
                    content=ft.Text(str(real_number), size=12, color=ft.Colors.BLACK),
                    bgcolor=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=4, vertical=0),
                )
                numeric_page = ft.Container(
                    content=number_left,
                    alignment=(
                        ft.alignment.bottom_right
                        if i % 2 == 0
                        else ft.alignment.bottom_left
                    ),
                    animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    margin=ft.margin.symmetric(horizontal=10, vertical=5),
                )
            else:
                numeric_page = ft.Container()

            # Контейнер для номера поверх картинки
            number_container = ft.Container(
                content=page_number,
                alignment=ft.alignment.center,
                padding=ft.padding.all(5),
                bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                border_radius=ft.border_radius.all(4),
                opacity=0,
                animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )

            # Контейнер страницы с картинкой и номером
            container = ft.Container(
                content=ft.Stack(
                    controls=[
                        img_box,
                        number_container,
                        numeric_page,
                    ],
                ),
                width=300,
                height=400,
                border_radius=ft.border_radius.all(6),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.WHITE,
                padding=ft.padding.only(
                    left=(self.logic.padding if i % 2 == 0 else 10) - 10,
                    right=(self.logic.padding if i % 2 == 1 else 10) - 10,
                ),
            )

            # Hover увеличиваем картинку и скрываем номер
            def on_hover(e, img=img_box, number=number_container):
                if e.data == "false":
                    img.opacity = 1
                    number.opacity = 0
                else:
                    img.opacity = 0.8
                    number.opacity = 1
                self.page.update()

            container.on_hover = on_hover

            row_widgets.append(container)

            # Каждые 2 страницы создаём Row (разворот)
            if i % 2 == 0:
                widgets.append(
                    ft.Row(
                        controls=row_widgets,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                        expand=True,
                    )
                )
                row_widgets = []

        # Если осталась 1 страница
        if row_widgets:
            widgets.append(
                ft.Row(
                    controls=row_widgets,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    expand=True,
                )
            )

        # Оборачиваем всё в ListView для вертикальной прокрутки
        return ft.ListView(
            controls=widgets,
            expand=True,
            spacing=10,
            padding=ft.padding.all(10),
        )

    def on_toggle_view(self, e, value=0):

        self.logic.change_mode_view(value)
        self.button_container.controls.clear()
        self.button_container.controls.extend(self.render_buttons().controls)

        new_list = self.render_pages_list()

        self.main_container.content = new_list

        self.page.update()

    def render_buttons(self):
        return ft.Row(
            controls=[
                Button(
                    self.page,
                    ft.Icons.GRID_4X4_SHARP,
                    "Сетка",
                    on_click=lambda e: self.on_toggle_view(e, 0),
                    active=(self.logic.modeView == 0),
                    active_color=self.style.primary,
                    hover_color=self.style.hover,
                ),
                Button(
                    self.page,
                    ft.Icons.MENU_BOOK_ROUNDED,
                    "Книга",
                    on_click=lambda e: self.on_toggle_view(e, 1),
                    active=(self.logic.modeView == 1),
                    active_color=self.style.primary,
                    hover_color=self.style.hover,
                ),
            ],
            spacing=10,
        )

    def render(self):
        return self.container

    def render_pages_list(self):
        if len(self.pages_list) > 0:
            new_list = (
                self.page_preview_Grid()
                if self.logic.modeView == 0
                else self.page_preview_book()
            )
        else:
            new_list = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            ft.Icons.ERROR_OUTLINED, size=64, color=ft.Colors.WHITE
                        ),
                        ft.Text(
                            "Список страниц пуст...",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
            )

        return new_list

    def update_pages(self):
        self.pages_list = self.logic.pages

        new_list = self.render_pages_list()

        self.main_container.content = new_list

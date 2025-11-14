import flet as ft
from style.appstyle import AppColors
from .button import Button
from core.logic import AppLogic
import asyncio


def Slider(
    page: ft.Page,
    style: AppColors,
    min,
    max,
    label,
    tooltip,
    expand,
    on_change=lambda e: print(f"Выбрано: {e.control.value}"),
    value=0,
):
    value_text = ft.Text(f"{value} мм", size=14, color=style.text_secondary)

    slider = ft.Slider(
        min=min,
        max=max,
        value=value,
        label=str(value),
        tooltip=tooltip,
        expand=expand,
        thumb_color=style.secondary,
        active_color=style.primary,
        inactive_color=style.base200,
        divisions=10,
    )

    def handle_change(e):
        value_text.value = f"{int(e.control.value)} мм"
        slider.label = f"{int(e.control.value)} мм"
        on_change(e)
        page.update()

    slider.on_change = handle_change

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            label,
                            size=16,
                            color=style.text_base,
                            weight=ft.FontWeight.BOLD,
                        ),
                        value_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                slider,
            ],
            spacing=0,
        )
    )


def Toggle(
    page: ft.Page,
    style: AppColors,
    label,
    description,
    value=False,
    on_change=lambda e: print(f"Выбрано: {e.control.value}"),
):
    title = ft.Text(label, size=14, color=style.text_base, weight=ft.FontWeight.BOLD)
    descp = ft.Text(description, size=12, color=style.text_secondary, opacity=0.5)

    info_container = ft.Column([title, descp], spacing=0)
    return ft.Container(
        content=ft.Row(
            [
                info_container,
                ft.Switch(
                    value=value,
                    on_change=on_change,
                    thumb_color=style.base100,
                    active_track_color=style.primary,
                    track_outline_color=style.base200,
                    tooltip=description,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )


class RightPanel:

    def __init__(self, page: ft.Page, style: AppColors, logic: AppLogic):
        super().__init__()
        self.page = page
        self.style = style
        self.logic = logic

        margin_slider = Slider(
            page=self.page,
            style=style,
            min=0,
            max=40,
            label="Поля страницы",
            tooltip="Поля страницы",
            expand=1,
            on_change=self.on_margin_change,
            value=self.logic.margin,
        )

        padding_slider = Slider(
            page=page,
            style=style,
            min=0,
            max=60,
            label="Отступ переплета",
            tooltip="Отступ переплета",
            expand=1,
            on_change=self.on_padding_change,
            value=self.logic.padding,
        )

        option_1 = Toggle(
            page,
            style=style,
            label="Блочная печать",
            description="Печать в формате брошюры",
            value=logic.isBookMode,
            on_change=lambda e: logic.change_isBookMode(e.control.value),
        )

        option_2 = Toggle(
            page,
            style=style,
            label="Нумерация страниц",
            description="Добавить номера страниц",
            value=logic.isNumbering,
            on_change=lambda e: logic.change_isNumbering(e.control.value),
        )

        option_3 = Toggle(
            page,
            style=style,
            label="Сохранить пропорций",
            description="Сохранять пропорции изображений",
            value=logic.isSavePropety,
            on_change=lambda e: logic.change_isSavePropety(e.control.value),
        )

        option_4 = Toggle(
            page,
            style=style,
            label="Открыть после экспорта",
            description="Открыть PDF после экспорта",
            value=logic.isAutoOpen,
            on_change=lambda e: logic.change_isAutoOpen(e.control.value),
        )

        self.proggres_bar = ft.ProgressBar(
            value=0,
            height=6,
            expand=True,
            tooltip="Загрузка",
            bgcolor=style.base200,
            color=style.primary,
            border_radius=3,
            semantics_label="Загрузка",
        )

        self.status_text = ft.Container(
            content=(
                ft.Text(
                    logic.status,
                    size=14,
                    color=style.text_base,
                    weight=ft.FontWeight.BOLD,
                )
                if logic.status != ""
                else None
            ),
            alignment=ft.alignment.center,
        )

        self.container = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Настройки печати",
                        size=18,
                        color=style.text_base,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(),
                    margin_slider,
                    padding_slider,
                    option_1,
                    option_2,
                    option_3,
                    option_4,
                    Button(
                        page,
                        ft.Icons.UPLOAD_FILE_OUTLINED,
                        "Экспортровать в PDF",
                        color=style.primary,
                        active_color=style.primary,
                        hover_color=style.hover,
                        expand=True,
                        on_click=lambda e: logic.open_file_uploader(),
                    ),
                    # Button(
                    #     page,
                    #     ft.Icons.PRINT_OUTLINED,
                    #     "Предпросмотр печати",
                    #     color=style.base100,
                    #     hover_color=style.hover,
                    #     expand=True,
                    # ),
                    self.status_text,
                    self.proggres_bar,
                ],
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True,
                spacing=20,
            ),
            expand=1,
            adaptive=True,
            padding=ft.padding.all(15),
            alignment=ft.alignment.top_left,
            bgcolor=style.base200,
            border=ft.border.only(
                left=ft.border.BorderSide(
                    1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
                )
            ),
        )

    def on_margin_change(self, e):
        self.logic.change_margin(e.control.value)
        self.page.update()

    def on_padding_change(self, e):
        self.logic.change_padding(e.control.value)
        self.page.update()

    def render(self):
        return self.container

    def update_progress(self, progress: int):
        self.proggres_bar.value = progress / 100
        self.page.update()

    def update_status(self):
        self.status_text.content = ft.Text(
            self.logic.status,
            size=14,
            color=self.style.text_base,
            weight=ft.FontWeight.BOLD,
        )
        self.page.update()

    async def animate_progress(self, target_percent: int):
        target = target_percent / 100
        if self.proggres_bar.value is None:
            self.proggres_bar.value = 0

        while self.proggres_bar.value < target:
            self.proggres_bar.value += 0.01
            if self.proggres_bar.value > target:
                self.proggres_bar.value = target
            self.page.update()
            await asyncio.sleep(0.01)

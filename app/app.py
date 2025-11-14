import flet as ft
from ui import Header, LeftPanel, PreviewPanel, RightPanel
from style.appstyle import AppColors
from core.logic import AppLogic


def main(page: ft.Page):
    style = AppColors()
    page.title = "MangaBook Printer"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.icon = "assets/favicon.png"
    page.window.min_width = 1400
    page.window.min_height = 800
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thickness=1,
            track_visibility=False,
            thumb_visibility=True,
            track_color="transparent",
            thumb_color=style.primary,
        )
    )

    def update_ui():
        if preview_container and left_container:
            preview_container.update_pages()
            left_container.update_pages()
            page.update()

    def update_status():
        right_container.update_status()
        page.update()

    def update_progress(progress: int):
        right_container.update_progress(progress)
        page.update()

    logic = AppLogic(
        page=page,
        on_update=update_ui,
        update_progress=update_progress,
        update_status=update_status,
    )

    page.bgcolor = style.base100
    page.padding = 0

    header = Header(page, style)

    left_container = LeftPanel(page, style, logic)
    preview_container = PreviewPanel(page, logic=logic, style=style)
    right_container = RightPanel(page, style, logic)

    def on_close(e):
        print("on_close")
        logic.cleanup_temp_dirs()

    page.on_close = on_close

    page.add(
        ft.Column(
            [
                header.render(),
                ft.Row(
                    [
                        left_container.render(),
                        preview_container.render(),
                        right_container.render(),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                ),
            ],
            expand=True,
            spacing=0,
        )
    )


def startApp():
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP,
        assets_dir="assets",
    )


startApp()

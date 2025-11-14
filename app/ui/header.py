import flet as ft
from style.appstyle import AppColors


class Header:
    def __init__(self, page: ft.Page, style: AppColors):
        super().__init__()
        self.page = page
        self.style = style

        self.about_dialog = ft.AlertDialog(
            title=ft.Text("О приложении"),
            content=ft.Column(
                [
                    ft.Text("Привет! Я Aiser."),
                    ft.Text("Это приложение помогает подготовить вашу мангу к печати."),
                    ft.Divider(),
                    ft.Text(
                        "Если вы это читаете и программа оказалась полезной,\n"
                        "пожалуйста, оставьте звёздочку на GitHub 😋.\n"
                        "Буду очень благодарен!\n\n"
                        "P.S: В приложений могут быть баги и ошибки, для связи пишите \nTelegram: @aisblack",
                        color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                    ),
                    ft.Text("Версия: 1.0.0"),
                ],
                tight=True,
            ),
            actions=[
                ft.ElevatedButton(
                    "Telegram",
                    on_click=self.open_tg,
                    bgcolor=self.style.info,
                ),
                ft.ElevatedButton(
                    "Github",
                    on_click=self.open_github,
                ),
                ft.ElevatedButton(
                    "Закрыть",
                    on_click=lambda e: self.close_dialog(e),
                    bgcolor=self.style.error,
                ),
            ],
            modal=True,
            actions_alignment=ft.MainAxisAlignment.END,
        )

        about_me = ft.Container(
            ft.Row(
                [
                    ft.IconButton(
                        ft.Icons.INFO,
                        on_click=lambda e: self.open_dialog(e),
                        icon_color=ft.Colors.WHITE,
                        tooltip="О приложении",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )

        self.container = ft.Container(
            ft.Row(
                [
                    ft.Container(
                        ft.Icon(
                            ft.Icons.MENU_BOOK,
                            size=28,
                            color=ft.Colors.WHITE,
                        ),
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        alignment=ft.alignment.center,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.center_left,
                            end=ft.alignment.center_right,
                            colors=[
                                self.style.primary,
                                self.style.accent,
                            ],
                        ),
                        border_radius=ft.border_radius.all(6),
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=3,
                            color=ft.Colors.with_opacity(
                                0.3, ft.Colors.DEEP_PURPLE_400
                            ),
                        ),
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                "MangaBook Printer", size=22, weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "Подготовьте вашу мангу для идеальной печати",
                                size=12,
                                opacity=0.7,
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    # ft.IconButton(
                    #     ft.Icons.SUNNY,
                    #     on_click=self.toggle_theme,
                    # ),
                    about_me,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                height=50,
            ),
            alignment=ft.alignment.center_left,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLUE_GREY_900)),
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            bgcolor=self.style.base200,
        )

    def open_dialog(self, e):
        self.page.open(self.about_dialog)

    def close_dialog(self, e):
        self.page.close(self.about_dialog)

    def open_github(self, e):
        self.page.launch_url("https://github.com/AiserKz")

    def open_tg(self, e):
        self.page.launch_url("https://t.me/aisblack")

    def toggle_theme(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT
            if self.page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        self.page.update()

    def render(self):
        return self.container

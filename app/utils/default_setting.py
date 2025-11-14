import flet as ft


def change_theme(page: ft.Page, theme: ft.ThemeMode):
    page.theme_mode = theme
    page.update()

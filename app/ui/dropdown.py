import flet as ft


def dropdown_component(
    page: ft.Page,
    title: str,
    options: list[str],
    value: str,
    on_change=lambda e: print(f"Выбрано: {e.control.value}"),
):
    _options = [ft.dropdown.Option(opt) for opt in options]
    return ft.Container(
        content=ft.Dropdown(
            label=title,
            hint_text=title,
            options=_options,
            value=value,
            border_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
            focused_border_color=ft.Colors.PURPLE_700,
            border_radius=ft.border_radius.all(8),
            border=ft.InputBorder.OUTLINE,
            filled=True,
            fill_color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
            text_style=ft.TextStyle(size=13, color=ft.Colors.WHITE),
            label_style=ft.TextStyle(
                color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE)
            ),
            on_change=on_change,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=5, vertical=5),
        border_radius=ft.border_radius.all(8),
    )

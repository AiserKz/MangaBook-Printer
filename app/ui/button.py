import flet as ft


def Button(
    page: ft.Page,
    icon: ft.Icons,
    text: str,
    on_click=lambda e: print("Click"),
    active=False,
    text_color=ft.Colors.WHITE,
    color=ft.Colors.with_opacity(0.4, ft.Colors.BLUE_GREY_700),
    active_color=ft.Colors.with_opacity(
        1,
        ft.Colors.PURPLE_800,
    ),
    hover_color=ft.Colors.with_opacity(0.15, ft.Colors.PURPLE_800),
    expand=False,
):
    return ft.Container(
        width=float("inf") if expand else None,
        content=ft.Button(
            icon=icon,
            icon_color=ft.Colors.WHITE,
            on_click=on_click,
            text=text,
            color=text_color,
            bgcolor=(color if not active else active_color),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                overlay_color=hover_color,
                padding=ft.padding.all(16),
                alignment=ft.alignment.center,
                shadow_color=color,
            ),
            expand=True,
        ),
        expand=True,
    )

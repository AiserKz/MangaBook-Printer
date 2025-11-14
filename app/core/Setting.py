import os, json, platform


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTING_PATH = os.path.join(BASE_DIR, "setting.json")


class Setting:

    def __init__(self) -> None:
        self.filename = "setting.json"

        local_path = self.filename
        if os.path.exists(local_path):
            self.setting_path = local_path
        else:
            if platform.system() == "Windows":
                base_dir = os.getenv("APPDATA") or os.path.expanduser("~")
            else:
                base_dir = os.path.join(os.path.expanduser("~"), ".config")

            app_folder = os.path.join(base_dir, "AisBook")
            os.makedirs(app_folder, exist_ok=True)
            self.setting_path = os.path.join(app_folder, self.filename)

        print(f"Используется файл настроек: {self.setting_path}")

    def load_setting(self):
        if os.path.exists(self.setting_path):
            with open(self.setting_path, "r") as f:
                setting = json.load(f)

                margin = setting["margin"]
                padding = setting["padding"]
                format_page = setting["format_page"] or "A4 (210x297mm)"
                page_in_page = setting["page_in_page"] or 2
                isNumbering = setting["isNumbering"]
                isBookMode = setting["isBookMode"]
                isSavePropety = setting["isSavePropety"]
                modeView = setting.get("modeView")
                isAuthOpen = setting.get("isAutoOpen")
            return (
                margin,
                padding,
                format_page,
                page_in_page,
                isNumbering,
                isBookMode,
                isSavePropety,
                modeView,
                isAuthOpen,
            )
        else:
            return (10, 10, "A4 (210x297mm)", 2, True, True, True, 1, False)

    def save_setting(
        self,
        margin,
        padding,
        format_page,
        page_in_page,
        isNumbering,
        isBookMode,
        isSavePropety,
        modeView,
        isAutoOpen,
    ):
        folder = os.path.dirname(self.setting_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.setting_path, "w") as f:
            json.dump(
                {
                    "margin": margin,
                    "padding": padding,
                    "format_page": format_page,
                    "page_in_page": page_in_page,
                    "isNumbering": isNumbering,
                    "isBookMode": isBookMode,
                    "isSavePropety": isSavePropety,
                    "modeView": modeView,
                    "isAutoOpen": isAutoOpen,
                },
                f,
                indent=4,
                ensure_ascii=False,
            )

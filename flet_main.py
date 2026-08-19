import flet as ft
import socket
import ssl
import threading
 
HOST = "10.0.2.2"
PORT = 9999
CERT_PATH = "keys/server.crt"
 
MASHOV_GREEN = "#4CA154"
FIELD_BG = "#E0E0E0"
LINK_BLUE = "#0505C6"
DISABLED_GRAY = "#E0E0E0"
TEXT_GRAY = "#808080"
TEXT_DARK = "#202020"
BTN_LIGHT_GREEN = "#E0E0E0"
PAGE_BG = "#F4F5F7"
 
def send_to_server(message: str) -> str:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERT_PATH)
    context.check_hostname = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with context.wrap_socket(s, server_hostname=HOST) as ss:
            ss.connect((HOST, PORT))
            ss.sendall(message.encode("utf-8"))
            return ss.recv(4096).decode("utf-8")
 
def login_view(page: ft.Page):
    page.rtl = True
    page.bgcolor = "#000000"
    page.padding = 0
    page.scroll = ft.ScrollMode.HIDDEN
    page.fonts = {
        "Assistant": "https://raw.githubusercontent.com/google/fonts/main/ofl/assistant/Assistant%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Assistant")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
 
    input_style = dict(
        width=300,
        height=44,
        text_align=ft.TextAlign.RIGHT,
        bgcolor="transparent",
        border=ft.InputBorder.NONE,
        filled=False,
        content_padding=ft.Padding(left=10, top=5, right=10, bottom=0),
        color=TEXT_DARK,
        text_size=12,
    )
 
    def wrap_field(control):
        return ft.Container(
            content=control,
            bgcolor=FIELD_BG,
            border_radius=10,
            width=300,
            height=44,
            alignment=ft.Alignment(0, 0),
        )
 
    school_field = wrap_field(ft.TextField(hint_text='ביה"ס', **input_style,))
 
    year_dropdown = wrap_field(ft.Dropdown(
        hint_text="שנת לימוד",
        options=[
            ft.dropdown.Option('תשפ"ו (2025-2026)'),
            ft.dropdown.Option('תשפ"ה (2024-2025)'),
            ft.dropdown.Option('תשפ"ד (2023-2024)'),
        ],
        elevation=0,
        border=ft.InputBorder.NONE,
        bgcolor="white",
        content_padding=ft.Padding(left=10, top=0, right=10, bottom=14),
        text_size=12,
        width=300,
        height=40,
    ))
 
    username_field = wrap_field(ft.TextField(
        hint_text="שם משתמש / ת.ז.",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        suffix_icon=ft.Icons.VISIBILITY_OFF_OUTLINED,
        **input_style
    ))
 
    password_field = wrap_field(ft.TextField(
        hint_text='סיסמה (משו"ב)',
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        **input_style
    ))
 
    status_text = ft.Text("", color="red", size=11, text_align=ft.TextAlign.CENTER)
 
    login_button = ft.Button(
        content=ft.Text("כניסה", size=13, weight=ft.FontWeight.W_500),
        width=300,
        height=44,
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor={"disabled": DISABLED_GRAY, "": MASHOV_GREEN},
            color={"disabled": "#FFFFFF", "": "#FFFFFF"},
            overlay_color="transparent",
            shadow_color="transparent",
            elevation=0,
            shape=ft.RoundedRectangleBorder(radius=22),
        ),
    )
 
    def create_secondary_button(text):
        return ft.Button(
            content=ft.Text(text, size=12, weight=ft.FontWeight.W_500),
            width=300,
            height=44,
            style=ft.ButtonStyle(
                bgcolor=BTN_LIGHT_GREEN,
                color=TEXT_DARK,
                overlay_color="transparent",
                shadow_color="transparent",
                elevation=0,
                shape=ft.RoundedRectangleBorder(radius=22),
            ),
        )
 
    email_button = create_secondary_button("כניסה באמצעות דואר אלקטרוני (EMAIL)")
    sms_button = create_secondary_button("כניסה באמצעות מסרון (SMS)")
 
    def do_login(e):
        status_text.value = ""
        page.update()
 
        def worker():
            try:
                response = send_to_server("login|test|test")
            except Exception as ex:
                status_text.value = f"שגיאת התחברות לשרת: {ex}"
                page.update()
                return
            page.update()
 
        threading.Thread(target=worker, daemon=True).start()
 
    login_button.on_click = do_login
 
    logo = ft.Image(
        src="mashov_app_logo.png",
        width=99,
        height=99,
        fit=ft.BoxFit.CONTAIN,
    )
 
    header = ft.Column(
        [
            logo,
            ft.Text(
                'משו"ב תלמידים והורים',
                size=22,
                weight=ft.FontWeight.W_900,
                color="#000000",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Row(
                [
                    ft.Text('הזדהות משו"ב', size=12, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Row(
                        [
                            ft.Text("הזדהות משרד החינוך", size=12, weight=ft.FontWeight.BOLD, color=TEXT_GRAY),
                            ft.Text("🦉", size=11)
                        ],
                        spacing=3,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=3,
    )
 
    def link_row(items):
        controls = []
        for i, label in enumerate(items):
            if i > 0:
                controls.append(ft.Text("|", color=TEXT_GRAY, size=10))
            controls.append(
                ft.TextButton(
                    content=ft.Text(label, size=10),
                    style=ft.ButtonStyle(color=LINK_BLUE, overlay_color="transparent", padding=0)
                )
            )
        return ft.Row(controls, alignment=ft.MainAxisAlignment.CENTER, spacing=1)
 
    footer_links_1 = link_row(['אתר משו"ב', "עזרה", "צור קשר"])
    footer_links_2 = link_row(["English", "Українська", "Русский", "العربية", "עברית"])
    footer_links_3 = link_row(["מדיניות פרטיות", "הצהרת נגישות"])
 
    footer_group = ft.Container(
        content=ft.Column(
            [
                footer_links_1,
                footer_links_2,
                footer_links_3,
            ],
            spacing=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(top=0, bottom=0, left=0, right=0),
    )
 
    form = ft.Column(
        [
            school_field,
            year_dropdown,
            username_field,
            password_field,
            ft.Row(
                [
                    ft.TextButton(
                        content=ft.Text("שכחת סיסמה?", size=11),
                        style=ft.ButtonStyle(color=LINK_BLUE, overlay_color="transparent", padding=0)
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Row(
                [
                    ft.Checkbox(
                        label="מכשיר אישי",
                        value=False,
                        label_style=ft.TextStyle(color=TEXT_DARK, size=12)
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            status_text,
            login_button,
            email_button,
            sms_button,
        ],
        width=300,
        spacing=1,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
 
    white_sheet = ft.Container(
        content=ft.Column(
            [
                header,
                form,
                footer_group,
                ft.Column(
                    [
                        ft.Text('משו"ב תלמידים והורים, גרסה: 3.8.70', size=10, color=TEXT_GRAY),
                        ft.Text('© 2026 - משו"ב', size=10, color=TEXT_GRAY),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                ft.Column(
                    [
                        ft.Text("by", size=9, color=TEXT_GRAY),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.APPS, color="#7C4DFF", size=13),
                                ft.Text("Priority", size=12, weight=ft.FontWeight.BOLD, color="#000000"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=3,
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor="#FFFFFF",
        border_radius=16,
        padding=ft.Padding(top=12, bottom=12, left=16, right=16),
        width=340,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )
 
    top_bar = ft.Container(
        bgcolor="#000000",
        height=35,
        width=1000,
        alignment=ft.Alignment(0, 0),
    )
 
    bottom_bar = ft.Container(
        bgcolor="#000000",
        height=25,
        width=1000,
        alignment=ft.Alignment(0, 0),
    )
 
    page.add(
        ft.Column(
            [
                top_bar,
                ft.Container(
                    content=white_sheet,
                    alignment=ft.Alignment(0, 0),
                    bgcolor=PAGE_BG,
                    padding=ft.Padding(top=8, bottom=8, left=10, right=10),
                    expand=True,
                ),
                bottom_bar
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
    )
 
def main(page: ft.Page):
    page.title = "Mashov"
    login_view(page)
 
if __name__ == "__main__":
    ft.run(main, view=ft.AppView.FLET_APP, assets_dir="assets")
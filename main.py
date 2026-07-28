
try: 
    import datetime
    import ssl
    import socket
    import tkinter as tk
    from tkinter import ttk
    import json
    import threading
    import os
    import webbrowser
    import random
    from utils import hashingAlg
    from tkinter import simpledialog
    import customtkinter as ctk
    
    root = tk.Tk()
    root.withdraw() 
    entry_username = None
    entry_password = None

    print("connecting to server...")
    
    print("reciving dataFromServer...")
    print("loading app...")
    print("importing assets...")

    current_toplevel_win = None
    current_username = ""
    current_user_role = ""
    current_user_class = ""
    splash_root = None
    
    import customtkinter as ctk

    def show_custom_message(parent_win=None, title="", message="", icon="⚠️", parent=None):
        active_parent = parent if parent is not None else parent_win

        msg_win = ctk.CTkToplevel(active_parent)
        msg_win.title(title)
        msg_win.overrideredirect(True)
        msg_win.attributes("-topmost", True)

        w, h = 380, 210

        if active_parent and hasattr(active_parent, 'winfo_exists') and active_parent.winfo_exists():
            active_parent.update_idletasks()
            x = active_parent.winfo_x() + (active_parent.winfo_width() // 2) - (w // 2)
            y = active_parent.winfo_y() + (active_parent.winfo_height() // 2) - (h // 2)
        else:
            screen_w = msg_win.winfo_screenwidth()
            screen_h = msg_win.winfo_screenheight()
            x = (screen_w // 2) - (w // 2)
            y = (screen_h // 2) - (h // 2)

        msg_win.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        msg_win.configure(fg_color="#0f172a")

        frame = ctk.CTkFrame(
            msg_win,
            fg_color="#1e293b",
            corner_radius=16,
            border_color="#334155",
            border_width=2
        )
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        ctk.CTkLabel(frame, text=icon, font=("Segoe UI", 34)).pack(pady=(12, 2))
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 16, "bold"), text_color="#ffffff").pack()

        ctk.CTkLabel(
            frame,
            text=message,
            font=("Segoe UI", 12),
            text_color="#cbd5e1",
            wraplength=320,
            justify="center"
        ).pack(pady=(6, 12))

        ctk.CTkButton(
            frame,
            text="אישור",
            font=("Segoe UI", 12, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            height=34,
            width=110,
            corner_radius=8,
            cursor="hand2",
            command=msg_win.destroy
        ).pack(pady=(0, 12))

        msg_win.grab_set()
    
    def verify_server_health(splash_root):
        SERVER_IP = '127.0.0.1'
        PORT = 9999
        
        try:
            with create_secure_socket() as s:
                s.connect((SERVER_IP, PORT))
                s.sendall("ping".encode('utf-8'))
                
                s.settimeout(3.0) 
                response = s.recv(1024).decode('utf-8').strip()
                
                if response == "pong":
                    print("Server health check: OK (Ready for user input)")
                    return 
                
                else:
                    raise Exception("תשובה לא מוכרת מהשרת")     
                    
        except Exception as e:
            splash_root.after(0, lambda: handle_health_failure(splash_root))

    def handle_health_failure(splash_root):
        show_custom_message(splash_root, "שגיאת תקשורת", "לא ניתן להתחבר לשרת המשוב המרכזי.\nאנא וודא שהשרת פועל ושהחיבור לרשת תקין.")
        
        try:
            if splash_root and splash_root.winfo_exists():
                splash_root.destroy()
        except Exception:
            pass

    def proceed_to_app(splash_root):
        try:
            if splash_root and splash_root.winfo_exists():
                splash_root.destroy()
        except Exception:
            pass
            
        open_login_window() 
    
    def create_secure_socket():
        context = ssl.create_default_context(cafile="keys/server.crt")
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_socket = context.wrap_socket(raw_socket, server_hostname="localhost")
        secure_socket.settimeout(5)
        return secure_socket

    def destroy_and_set_new_window(new_win):
        global current_toplevel_win
        if current_toplevel_win is not None and current_toplevel_win.winfo_exists():
            current_toplevel_win.withdraw()
        current_toplevel_win = new_win
        

    ###########################################################
    #               מסך פתיחה                  #
    ###########################################################
    
    def open_splash_screen():
        global splash_root
        
        splash_root = ctk.CTk()
        splash_root.overrideredirect(True)
        
        width, height = 520, 770 
        splash_root.configure(fg_color="#0f172a")

        screen_w = splash_root.winfo_screenwidth()
        screen_h = splash_root.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        splash_root.geometry(f"{width}x{height}+{x}+{y}")

        main_frame = ctk.CTkFrame(
            splash_root,
            fg_color="#1e293b",
            corner_radius=20,
            width=520,
            height=770
        )
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)
        
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#1d4ed8",
            corner_radius=16,
            height=210
        )
        header_frame.pack(fill="x", padx=16, pady=(16, 0))
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="📊",
            font=("Segoe UI", 55),
            text_color="#ffffff"
        ).pack(pady=(25, 0))

        ctk.CTkLabel(
            header_frame,
            text="מערכת משוב",
            font=("Segoe UI", 32, "bold"),
            text_color="#ffffff"
        ).pack()

        ctk.CTkLabel(
            header_frame,
            text="הדרך החכמה לנהל את הלימודים",
            font=("Segoe UI", 12),
            text_color="#93c5fd"
        ).pack(pady=(2, 0))

        # 2. Content Frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=15)

        ctk.CTkLabel(
            content_frame,
            text="ברוכים הבאים",
            font=("Segoe UI", 24, "bold"),
            text_color="#f8fafc"
        ).pack(pady=(20, 10))

        # 3. Features Cards
        features_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        features_frame.pack(pady=20)

        features = [
            ("🕒", "לו\"ז בזמן אמת"),
            ("📝", "מעקב ציונים"),
            ("✅", "ניהול משימות")
        ]

        for icon, txt in features:
            card = ctk.CTkFrame(
                features_frame,
                fg_color="#0f172a",
                corner_radius=12,
                width=110,
                height=90
            )
            card.pack(side="right", padx=6)
            card.pack_propagate(False)

            ctk.CTkLabel(
                card,
                text=icon,
                font=("Segoe UI", 24)
            ).pack(pady=(12, 2))

            ctk.CTkLabel(
                card,
                text=txt,
                font=("Segoe UI", 11, "bold"),
                text_color="#cbd5e1"
            ).pack()

        # 4. Buttons Section
        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))

        login_btn = ctk.CTkButton(
            btn_frame,
            text="כניסה למערכת",
            font=("Segoe UI", 16, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            height=52,
            corner_radius=10,
            cursor="hand2",
            command=open_login_window
        )
        login_btn.pack(fill="x", pady=(0, 12))

        peak_btn = ctk.CTkButton(
            btn_frame,
            text="כניסה כאורח",
            font=("Segoe UI", 15, "bold"),
            fg_color="transparent",
            border_color="#3b82f6",
            border_width=2,
            hover_color="#0f172a",
            text_color="#60a5fa",
            height=50,
            corner_radius=10,
            cursor="hand2",
            command=open_peak
        )
        peak_btn.pack(fill="x")

        footer_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#0f172a",
            corner_radius=12,
            height=50
        )
        footer_frame.pack(side="bottom", fill="x", padx=16, pady=(0, 16))
        footer_frame.pack_propagate(False)

        ctk.CTkLabel(
            footer_frame,
            text="פותח ע\"י אוריה נרקיסי • גרסה 2.0",
            font=("Segoe UI", 11),
            text_color="#64748b"
        ).pack(expand=True)

        threading.Thread(target=lambda: verify_server_health(splash_root), daemon=True).start()
        splash_root.mainloop()

    def open_login_window():
        global splash_root
        if splash_root:
            splash_root.destroy()
        root.deiconify()  

    def open_peak():
        global current_user_role
        show_custom_message(None, "אורח יקר", "בתור אורח אתה לא תוכל להשתמש בכל הפיצרים")
        
        SERVER_IP = '127.0.0.1' 
        PORT = 9999
        
        try:
            with create_secure_socket() as s:
                print(f"Connecting to {SERVER_IP}:{PORT}...")
                s.connect((SERVER_IP, PORT))                                
                
                subject = f"guest"
                s.sendall(subject.encode('utf-8'))
                
                raw_data = s.recv(1024)
                if not raw_data:
                    print("No response from server")
                    return

                dataFromServer = raw_data.decode('utf-8').strip()
                print(f"Received from server: {dataFromServer}")

                if dataFromServer.startswith("200"):
                    current_user_role = "guest"
                    print("successfuly entered as a guest")
                    open_main_page(current_user_role)
                    return
                
                else:
                    show_custom_message(None, "שגיאה", "שגיאת שרת")
                    return
                    

        except ConnectionRefusedError:
            show_custom_message(None, "שגיאה", "לא ניתן להתחבר לשרת. וודא שהוא פועל.")
            
        except Exception as e:
            show_custom_message(None, "שגיאה", f"אירעה שגיאה: {e}")

    def open_main_page(username):
        global current_username, current_user_role

        new_win = ctk.CTkToplevel()
        new_win.overrideredirect(True)
        destroy_and_set_new_window(new_win)
        current_username = username

        new_win.title("עמוד ראשי")

        width, height = 520, 880
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a")  # Dark Background

        # Container ראשי לכל גובה החלון
        main_frame = ctk.CTkFrame(
            new_win,
            fg_color="#1e293b",
            corner_radius=20,
            width=520,
            height=880
        )
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        # 1. Header כחול מודרני
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#1d4ed8",
            corner_radius=16,
            height=170
        )
        header_frame.pack(fill="x", padx=16, pady=(16, 0))
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="🏠",
            font=("Segoe UI", 42),
            text_color="#ffffff"
        ).pack(pady=(16, 0))

        ctk.CTkLabel(
            header_frame,
            text=f"שלום, {username}",
            font=("Segoe UI", 24, "bold"),
            text_color="#ffffff"
        ).pack()

        ctk.CTkLabel(
            header_frame,
            text="מה ברצונך לעשות היום?",
            font=("Segoe UI", 12),
            text_color="#93c5fd"
        ).pack(pady=(2, 0))

        # 2. Grid Frame עבור הכפתורים - מתפרס בצורה שווה במרכז
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # הגדרת משקל שווה לשורות ולעמודות כדי שימלאו את השטח בצורה מאוזנת
        for i in range(4):
            content_frame.rowconfigure(i, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)

        # הגדרת פונקציית עזר ליצירת כפתור אחיד ומעוצב
        def create_menu_button(parent, text, command, icon, row, col, fg_color, hover_color):
            btn = ctk.CTkButton(
                parent,
                text=f"{icon}\n{text}",
                command=command,
                font=("Segoe UI", 14, "bold"),
                fg_color=fg_color,
                hover_color=hover_color,
                corner_radius=14,
                cursor="hand2"
            )
            btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            return btn

        create_menu_button(content_frame, "מערכת שעות", open_marechet, "📅", 0, 1, "#2563eb", "#1d4ed8")
        create_menu_button(content_frame, "דואר נכנס", open_doar, "📨", 0, 0, "#1d4ed8", "#1e40af")

        create_menu_button(content_frame, "ציונים שוטפים", open_grades, "📊", 1, 1, "#0284c7", "#0369a1")
        create_menu_button(content_frame, "צ'אט כיתתי", open_class_chat_room, "💬", 1, 0, "#0369a1", "#075985")

        create_menu_button(content_frame, "משימון", open_todo_list, "📝", 2, 1, "#0f766e", "#115e59")
        create_menu_button(content_frame, "שחרורון", open_freer, "🚀", 2, 0, "#0d9488", "#0f766e")

        create_menu_button(content_frame, "נוכחות בשיעור", open_attendance, "✋", 3, 1, "#4f46e5", "#4338ca")
        create_menu_button(content_frame, "משימות Moodle", open_moodle_tasks, "📚", 3, 0, "#6366f1", "#4f46e5")

        footer_frame = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=12, height=45)
        footer_frame.pack(side="bottom", fill="x", padx=16, pady=(0, 16))
        footer_frame.pack_propagate(False)

        ctk.CTkLabel(
            footer_frame,
            text="Mashov מערכת ניהול לימודים • גרסה 2.0",
            font=("Segoe UI", 11),
            text_color="#64748b"
        ).pack(expand=True)
            
        
    ###########################################################
    #                   פונקציית התחברות                    #
    ###########################################################

    def forgotPass():
        show_custom_message(None, title="?שכחת את הסיסמה", message="שנה/י את סיסמתך במשרד המזכירות בבית הספר")


    def openPrivecyPolicy():
        webbrowser.open("privacy_policy.txt" )
        
    def open_login_window():
        global entry_username, entry_password, root, splash_root
        
        if splash_root is not None: 
            try:
                if splash_root.winfo_exists():
                    splash_root.destroy()
            except Exception:
                pass
            
        login_win = ctk.CTkToplevel(root)
        login_win.title("משוב / התחברות")
        login_win.overrideredirect(True)
        
        destroy_and_set_new_window(login_win)

        width, height = 520, 770 
        screen_width = login_win.winfo_screenwidth()
        screen_height = login_win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        login_win.geometry(f"{width}x{height}+{x}+{y}")
        login_win.configure(fg_color="#0f172a")

        main_frame = ctk.CTkFrame(
            login_win,
            fg_color="#1e293b",
            corner_radius=20,
            width=520,
            height=770
        )
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#1d4ed8",
            corner_radius=16,
            height=180
        )
        header_frame.pack(fill="x", padx=16, pady=(16, 0))
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="🔒",
            font=("Segoe UI", 48),
            text_color="#ffffff"
        ).pack(pady=(22, 0))

        ctk.CTkLabel(
            header_frame,
            text="משוב - מערכת עדכונים",
            font=("Segoe UI", 26, "bold"),
            text_color="#ffffff"
        ).pack()

        card_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#0f172a", 
            corner_radius=16
        )
        card_frame.pack(fill="both", expand=True, padx=20, pady=20)

        form_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=25, pady=20)

        ctk.CTkLabel(
            form_frame,
            text="שם משתמש",
            font=("Segoe UI", 13, "bold"),
            text_color="#cbd5e1"
        ).pack(anchor="e", pady=(10, 6))

        entry_username = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 14),
            height=48,
            corner_radius=10,
            fg_color="#1e293b",
            border_color="#334155",
            text_color="#f8fafc",
            justify="right"
        )
        entry_username.pack(fill="x")

        ctk.CTkLabel(
            form_frame,
            text="סיסמה",
            font=("Segoe UI", 13, "bold"),
            text_color="#cbd5e1"
        ).pack(anchor="e", pady=(18, 6))

        entry_password = ctk.CTkEntry(
            form_frame,
            font=("Segoe UI", 14),
            height=48,
            corner_radius=10,
            fg_color="#1e293b",
            border_color="#334155",
            text_color="#f8fafc",
            show="●",
            justify="right"
        )
        entry_password.pack(fill="x")

        ctk.CTkButton(
            form_frame,
            text="התחברות למערכת",
            font=("Segoe UI", 15, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            height=52,
            corner_radius=10,
            cursor="hand2",
            command=attempt_login
        ).pack(fill="x", pady=(28, 15))

        nav_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        nav_frame.pack(pady=5)
        
        ctk.CTkButton(
            nav_frame, 
            text="שכחת סיסמה",
            font=("Segoe UI", 13, "bold"),
            text_color="#60a5fa",
            fg_color="transparent",
            hover_color="#1e293b",
            height=30,
            corner_radius=6,
            cursor="hand2", 
            command=forgotPass
        ).pack(side="right", padx=4)
        
        ctk.CTkLabel(
            nav_frame,
            text="|",
            text_color="#64748b",
            font=("Segoe UI", 13)
        ).pack(side="right")
        
        ctk.CTkButton(
            nav_frame,
            text="יצירת חשבון חדש",
            font=("Segoe UI", 13, "bold"),
            text_color="#60a5fa",
            fg_color="transparent",
            hover_color="#1e293b",
            height=30,
            corner_radius=6,
            cursor="hand2", 
            command=signUp
        ).pack(side="right", padx=4)

        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=(0, 20)) 
        
        ctk.CTkLabel(
            footer_frame,
            text="בכניסה למערכת הנך מסכים לכל", 
            font=("Segoe UI", 11),
            text_color="#94a3b8"
        ).pack()
        
        ctk.CTkButton(
            footer_frame,
            text="תנאי השימוש ומדיניות הפרטיות שלנו", 
            font=("Segoe UI", 11, "underline"),
            text_color="#60a5fa",
            fg_color="transparent",
            hover_color="#0f172a",
            height=24,
            corner_radius=4,
            cursor="hand2", 
            command=lambda: webbrowser.open("https://www.mashov.info/privacypolicy/")
        ).pack(pady=(2, 8))

        ctk.CTkLabel(
            footer_frame,
            text="📖",
            text_color="#3b82f6",
            font=("Segoe UI", 40)
        ).pack()    
        
        return login_win
    
    def ask_teacher_code(username):
        code_win = tk.Toplevel(root)
        code_win.title("אימות מורה")
        code_win.overrideredirect(True)

        width, height = 400, 250
        x = (code_win.winfo_screenwidth() // 2) - (width // 2)
        y = (code_win.winfo_screenheight() // 2) - (height // 2)

        code_win.geometry(f"{width}x{height}+{x}+{y}")
        code_win.configure(bg="white")
        code_win.resizable(False, False)

        tk.Label(
            code_win,
            text="הכנס קוד כניסה למורים",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1a73e8"
        ).pack(pady=30)

        code_entry = tk.Entry(
            code_win,
            font=("Arial", 16),
            justify="center",
            show="*"
        )
        code_entry.pack(pady=10, ipady=6)
        
    def attempt_login():
        typedUSERNAME = entry_username.get()
        typedPASSWORD = entry_password.get()
        
        SERVER_IP = '127.0.0.1' 
        PORT = 9999
        
        try:
            with create_secure_socket() as s:
                print(f"Connecting to {SERVER_IP}:{PORT}...")
                s.connect((SERVER_IP, PORT))                                
                
                subject = f"login|{typedUSERNAME}|{typedPASSWORD}"
                s.sendall(subject.encode('utf-8'))
                
                raw_data = s.recv(1024)
                if not raw_data:
                    print("No response from server")
                    return

                dataFromServer = raw_data.decode('utf-8').strip()
                print(f"Received from server: {dataFromServer}")

                if dataFromServer.startswith("200 ok"):
                    global current_user_role, current_user_class

                    parts = dataFromServer.split("|")
                    current_user_role = parts[1]
                    current_user_class = parts[2]

                    print(current_user_role, current_user_class)

                    root.withdraw()
                    open_main_page(typedUSERNAME)
                
                elif dataFromServer == "attempt limit reached":
                        show_custom_message(None, "שגיאה", "יותר מידי ניסיונות, במידה ושכחת את הסיסמה שלך אז לחץ על שכחת את הסיסמה")
                        exit()
                
                else:
                    show_custom_message(None, "שגיאה", "שם משתמש או סיסמה שגויים")
                    print("unsuccessful")

        except ConnectionRefusedError:
            show_custom_message(None, "שגיאה", "לא ניתן להתחבר לשרת. וודא שהוא פועל.")
        except Exception as e:
            show_custom_message(None, "שגיאה", f"אירעה שגיאה: {e}")
        
    def signUp():       
        def attemptSignUp():
            all_entries = [firstName, lastName, gmail, newUsername, newPassword]
            role = role_box.get()

            if any(entry.get().strip() == "" for entry in all_entries):
                show_custom_message(None, "שגיאה", "נא למלא את כל השדות")
                return

            if class_box.get().strip() in ["בחר כיתה", ""]:
                show_custom_message(None, "שגיאה", "נא לבחור כיתה")
                return

            if role_box.get().strip() in ["בחר תפקיד", ""]:
                show_custom_message(None, "שגיאה", "נא לבחור תפקיד")
                return

            user_email = gmail.get().strip()
            if "@" not in user_email or user_email.startswith("@") or user_email.endswith("@"):
                show_custom_message(None, "שגיאה", "אימייל לא תקין")
                return

            if firstName.get().isdigit() or lastName.get().isdigit():
                show_custom_message(None, "שגיאה", "שם לא יכול להיות מספר")
                return
            
            if role == "teacher":
                open_teacher_setup(newUsername.get())
            elif role == "student":
                open_student_setup(newUsername.get())

        def open_teacher_setup(username):
            win = ctk.CTkToplevel()
            destroy_and_set_new_window(win)
            win.overrideredirect(True)

            win.title("הגדרת מורה")
            width, height = 480, 520
            screen_width = win.winfo_screenwidth()
            screen_height = win.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            win.geometry(f"{width}x{height}+{x}+{y}")
            win.configure(fg_color="#0f172a")

            frame = ctk.CTkFrame(win, fg_color="#1e293b", corner_radius=20, width=480, height=520)
            frame.place(relx=0.5, rely=0.5, anchor="center")
            frame.pack_propagate(False)

            ctk.CTkLabel(frame, text="🔑", font=("Segoe UI", 42), text_color="#3b82f6").pack(pady=(25, 5))
            ctk.CTkLabel(frame, text="אימות מורה", font=("Segoe UI", 22, "bold"), text_color="#ffffff").pack()

            form_sub = ctk.CTkFrame(frame, fg_color="transparent")
            form_sub.pack(fill="x", padx=40, pady=20)

            ctk.CTkLabel(form_sub, text="קוד מורים", font=("Segoe UI", 12, "bold"), text_color="#cbd5e1").pack(anchor="e", pady=(5, 4))
            teacher_code = ctk.CTkEntry(
                form_sub, font=("Segoe UI", 13), height=42, corner_radius=8,
                fg_color="#334155", border_color="#475569", text_color="#f8fafc", show="*", justify="right"
            )
            teacher_code.pack(fill="x")

            ctk.CTkLabel(form_sub, text="קוד כיתה (לשיתוף)", font=("Segoe UI", 12, "bold"), text_color="#cbd5e1").pack(anchor="e", pady=(15, 4))
            class_code = ctk.CTkEntry(
                form_sub, font=("Segoe UI", 13), height=42, corner_radius=8,
                fg_color="#334155", border_color="#475569", text_color="#f8fafc", justify="right"
            )
            class_code.pack(fill="x")

            def submit():
                teachers_code = teacher_code.get()
                new_class_code = class_code.get()

                if not teachers_code or not new_class_code:
                    show_custom_message(win, "שגיאה", "נא למלא את כל השדות")
                    return

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))

                        subject = (
                            f"signUp|"
                            f"{firstName.get()}|"
                            f"{lastName.get()}|"
                            f"{gmail.get()}|"
                            f"{newUsername.get()}|"
                            f"{newPassword.get()}|"
                            f"{class_box.get()}|"
                            f"{role_box.get()}|"
                            f"{teachers_code}|"
                            f"{new_class_code}"
                        )

                        s.sendall(subject.encode("utf-8"))

                        raw_data = s.recv(1024)
                        if not raw_data:
                            show_custom_message(win, "שגיאה", "אין תגובה מהשרת")
                            return

                        dataFromServer = raw_data.decode("utf-8").strip()

                        if dataFromServer.startswith("200"):
                            show_custom_message(win, "הצלחה", "החשבון נוצר בהצלחה")
                            win.destroy()       
                            open_login_window()
                        elif dataFromServer == "gmail already exists":
                            show_custom_message(win, "שגיאה", "אימייל כבר בשימוש")
                        elif dataFromServer == "username already exists":
                            show_custom_message(win, "שגיאה", "שם משתמש כבר בשימוש")
                        elif dataFromServer == "invalid teacher code":
                            show_custom_message(win, "שגיאה", "קוד מורה שגוי")
                        elif dataFromServer == "invalid student code":
                            show_custom_message(win, "שגיאה", "קוד תלמיד שגוי")
                        elif dataFromServer.startswith("teacher"):
                            show_custom_message(win, "שגיאה", "מורה כבר קיים בכיתה המבוקשת")
                        elif dataFromServer.startswith("error|"):
                            show_custom_message(win, "שגיאת שרת", "שגיאת שרת: 500")
                        elif dataFromServer.startswith("404"):
                            show_custom_message(win, "שגיאה", "הכיתה המבוקשת אינה קיימת")
                        else:
                            show_custom_message(win, "שגיאה", dataFromServer)

                except ConnectionRefusedError:
                    show_custom_message(win, "שגיאה", "לא ניתן להתחבר לשרת")

            ctk.CTkButton(
                frame, text="המשך", font=("Segoe UI", 14, "bold"),
                fg_color="#2563eb", hover_color="#1d4ed8", height=45, corner_radius=8,
                cursor="hand2", command=submit
            ).pack(fill="x", padx=40, pady=20)

        def open_student_setup(username):
            win = ctk.CTkToplevel()
            win.overrideredirect(True)
            destroy_and_set_new_window(win)

            win.title("כניסת תלמיד")
            width, height = 480, 420
            screen_width = win.winfo_screenwidth()  
            screen_height = win.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            win.geometry(f"{width}x{height}+{x}+{y}")
            win.configure(fg_color="#0f172a")

            frame = ctk.CTkFrame(win, fg_color="#1e293b", corner_radius=20, width=480, height=420)
            frame.place(relx=0.5, rely=0.5, anchor="center")
            frame.pack_propagate(False)

            ctk.CTkLabel(frame, text="🎓", font=("Segoe UI", 42), text_color="#3b82f6").pack(pady=(25, 5))
            ctk.CTkLabel(frame, text="הכנס קוד כיתה", font=("Segoe UI", 20, "bold"), text_color="#ffffff").pack()

            form_sub = ctk.CTkFrame(frame, fg_color="transparent")
            form_sub.pack(fill="x", padx=40, pady=20)

            code_entry = ctk.CTkEntry(
                form_sub, font=("Segoe UI", 13), height=45, corner_radius=8,
                fg_color="#334155", border_color="#475569", text_color="#f8fafc", justify="right"
            )
            code_entry.pack(fill="x")

            def submit():
                class_code = code_entry.get()

                if not class_code:
                    show_custom_message(win, "שגיאה", "נא להזין קוד כיתה")
                    return

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))

                        subject = (
                            f"signUp|"
                            f"{firstName.get()}|"
                            f"{lastName.get()}|"
                            f"{gmail.get()}|"
                            f"{newUsername.get()}|"
                            f"{newPassword.get()}|"
                            f"{class_box.get()}|"
                            f"{role_box.get()}|"
                            f"is student|"
                            f"{class_code}"
                        )

                        s.sendall(subject.encode("utf-8"))

                        raw_data = s.recv(1024)
                        if not raw_data:
                            show_custom_message(win, "שגיאה", "אין תגובה מהשרת")
                            return

                        dataFromServer = raw_data.decode("utf-8").strip()

                        if dataFromServer.startswith("200"):
                            show_custom_message(win, "הצלחה", "החשבון נוצר בהצלחה")
                            win.destroy()                  
                            open_login_window()
                        elif dataFromServer == "gmail already exists":
                            show_custom_message(win, "שגיאה", "אימייל כבר בשימוש")
                        elif dataFromServer == "username already exists":
                            show_custom_message(win, "שגיאה", "שם משתמש כבר בשימוש")
                        elif dataFromServer == "invalid student code":
                            show_custom_message(win, "שגיאה", "קוד תלמיד שגוי")
                        elif dataFromServer.startswith("404"):
                            show_custom_message(win, "שגיאה", "הכיתה המבוקשת אינה קיימת")
                        else:
                            show_custom_message(win, "שגיאה", dataFromServer)

                except ConnectionRefusedError:
                    show_custom_message(win, "שגיאה", "לא ניתן להתחבר לשרת")
                except Exception as e:
                    show_custom_message(win, "שגיאה", f"אירעה שגיאה: {e}")

            ctk.CTkButton(
                frame, text="כניסה", font=("Segoe UI", 14, "bold"),
                fg_color="#2563eb", hover_color="#1d4ed8", height=45, corner_radius=8,
                cursor="hand2", command=submit
            ).pack(fill="x", padx=40, pady=10)

        # חלון הרשמה ראשי
        new_win = ctk.CTkToplevel()
        new_win.title("MashovApp / הרשמה")
        new_win.overrideredirect(True)

        width, height = 520, 860
        x = (new_win.winfo_screenwidth() // 2) - (width // 2)
        y = (new_win.winfo_screenheight() // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a")

        main_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=20, width=520, height=860)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        # Header מודרני
        header_frame = ctk.CTkFrame(main_frame, fg_color="#1d4ed8", corner_radius=16, height=140)
        header_frame.pack(fill="x", padx=12, pady=(12, 0))
        header_frame.pack_propagate(False)

        ctk.CTkLabel(header_frame, text="📝", font=("Segoe UI", 40), text_color="#ffffff").pack(pady=(15, 0))
        ctk.CTkLabel(header_frame, text="יצירת חשבון חדש", font=("Segoe UI", 22, "bold"), text_color="#ffffff").pack()

        # Form
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=35, pady=10)

        fields = [
            ("שם פרטי", "firstName", False),
            ("שם משפחה", "lastName", False),
            ("אימייל", "gmail", False),
            ("שם משתמש", "newUsername", False),
            ("סיסמה", "newPassword", True)
        ]

        entries = {}

        for label_text, var_name, is_pass in fields:
            ctk.CTkLabel(form_frame, text=label_text, font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").pack(anchor="e", pady=(6, 2))
            ent = ctk.CTkEntry(
                form_frame, font=("Segoe UI", 13), height=38, corner_radius=8,
                fg_color="#334155", border_color="#475569", text_color="#f8fafc",
                show="●" if is_pass else "", justify="right"
            )
            ent.pack(fill="x")
            entries[var_name] = ent

        firstName, lastName, gmail, newUsername, newPassword = entries.values()
        gmail.configure(placeholder_text="example@gmail.com")

        # כיתה
        ctk.CTkLabel(form_frame, text="כיתה", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").pack(anchor="e", pady=(8, 2))
        classes_list = ["ז1", "ז2", "ז3", "ז4", "ז5", "ז6", "ח1", "ח2", "ח3", "ח4", "ח5", "ח6", "ט1", "ט2", "ט3", "ט4", "ט5", "ט6", "י1", "י2", "י3", "י4", "י5", "י6", "יא1", "יא2", "יא3", "יא4", "יא5", "יא6", "יב1", "יב2", "יב3", "יב4", "יב5", "יב6"]
        
        class_box = ctk.CTkOptionMenu(
            form_frame, values=classes_list, font=("Segoe UI", 12),
            dropdown_font=("Segoe UI", 12), fg_color="#334155", button_color="#475569",
            button_hover_color="#64748b", text_color="#f8fafc", height=38, corner_radius=8
        )
        class_box.set("בחר כיתה")
        class_box.pack(fill="x")

        # תפקיד
        ctk.CTkLabel(form_frame, text="תפקיד", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").pack(anchor="e", pady=(8, 2))
        role_box = ctk.CTkOptionMenu(
            form_frame, values=["student", "teacher"], font=("Segoe UI", 12),
            dropdown_font=("Segoe UI", 12), fg_color="#334155", button_color="#475569",
            button_hover_color="#64748b", text_color="#f8fafc", height=38, corner_radius=8
        )
        role_box.set("בחר תפקיד")
        role_box.pack(fill="x")

        # כפתור יצירת חשבון
        ctk.CTkButton(
            form_frame, text="צור חשבון עכשיו", font=("Segoe UI", 15, "bold"),
            fg_color="#2563eb", hover_color="#1d4ed8", height=46, corner_radius=8,
            cursor="hand2", command=attemptSignUp
        ).pack(fill="x", pady=(20, 5))

        # Footer
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=(0, 15))

        ctk.CTkLabel(footer_frame, text="כבר יש לך חשבון?", font=("Segoe UI", 11), text_color="#94a3b8").pack()
        
        ctk.CTkButton(
            footer_frame, text="חזור למסך ההתחברות", font=("Segoe UI", 11, "underline", "bold"),
            text_color="#60a5fa", fg_color="transparent", hover_color="#334155",
            height=22, corner_radius=4, cursor="hand2", command=lambda: new_win.destroy()
        ).pack(pady=(0, 4))

        ctk.CTkLabel(footer_frame, text="🏫", font=("Segoe UI", 32), text_color="#3b82f6").pack()

        return new_win


    ###########################################################
    #                שערי האפליקציה        #
    ###########################################################
    

    def open_grades():
        if current_user_role not in ["teacher", "student"]:
            show_custom_message(None, "שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
            return

        # --- ממשק מורה (Dark Theme) ---
        if current_user_role == "teacher":
            new_win = ctk.CTkToplevel()
            new_win.overrideredirect(True)

            destroy_and_set_new_window(new_win)
            new_win.title("ניהול ציונים - מורה")

            width, height = 520, 770
            screen_width = new_win.winfo_screenwidth()
            screen_height = new_win.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            new_win.geometry(f"{width}x{height}+{x}+{y}")
            new_win.configure(fg_color="#0f172a")  # Dark Background

            # Container ראשי כהה
            main_frame = ctk.CTkFrame(
                new_win,
                fg_color="#1e293b",
                corner_radius=20,
                width=520,
                height=770
            )
            main_frame.place(relx=0.5, rely=0.5, anchor="center")
            main_frame.pack_propagate(False)

            # Header כחול מודרני
            header_frame = ctk.CTkFrame(
                main_frame,
                fg_color="#1d4ed8",
                corner_radius=16,
                height=190
            )
            header_frame.pack(fill="x", padx=12, pady=(12, 0))
            header_frame.pack_propagate(False)

            ctk.CTkLabel(
                header_frame,
                text="📝",
                font=("Segoe UI", 46),
                text_color="#ffffff"
            ).pack(pady=(20, 0))

            ctk.CTkLabel(
                header_frame,
                text="ניהול והזנת ציונים",
                font=("Segoe UI", 26, "bold"),
                text_color="#ffffff"
            ).pack()

            ctk.CTkLabel(
                header_frame,
                text="ממשק מורה לעדכון והוספת ציוני תלמידים",
                font=("Segoe UI", 12),
                text_color="#93c5fd"
            ).pack(pady=(2, 0))

            # טופס להזנת נתונים בעיצוב כהה
            form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            form_frame.pack(fill="both", expand=True, padx=35, pady=20)

            class_students = []
            SERVER_IP = '127.0.0.1'
            PORT = 9999

            try:
                with create_secure_socket() as s:
                    s.connect((SERVER_IP, PORT))
                    subject = f"get_class_students|{current_user_class}"
                    s.sendall(subject.encode("utf-8"))

                    raw_data = s.recv(1024)
                    if raw_data:
                        dataFromServer = raw_data.decode("utf-8").strip()
                        if dataFromServer.startswith("class_students_response|"):
                            res_parts = dataFromServer.split("|")
                            if res_parts[1]:
                                class_students = res_parts[1].split(",")
            except Exception as e:
                show_custom_message(None, "שגיאה", f"שגיאה בהתחברות לשרת: {e}")
                return

            # שדות הקלט כהים
            ctk.CTkLabel(form_frame, text="שם התלמיד", font=("Segoe UI", 12, "bold"), text_color="#cbd5e1").pack(anchor="e", pady=(8, 4))
            student_entry = ctk.CTkComboBox(
                form_frame,
                font=("Segoe UI", 13),
                values=class_students,
                height=45,
                corner_radius=10,
                fg_color="#334155",
                border_color="#475569",
                button_color="#2563eb",
                dropdown_fg_color="#1e293b",
                text_color="#f8fafc"
            )
            student_entry.pack(fill="x")

            ctk.CTkLabel(form_frame, text="מקצוע", font=("Segoe UI", 12, "bold"), text_color="#cbd5e1").pack(anchor="e", pady=(12, 4))
            subject_entry = ctk.CTkEntry(
                form_frame,
                font=("Segoe UI", 13),
                height=45,
                corner_radius=10,
                fg_color="#334155",
                border_color="#475569",
                text_color="#f8fafc"
            )
            subject_entry.pack(fill="x")

            ctk.CTkLabel(form_frame, text="ציון חדש", font=("Segoe UI", 12, "bold"), text_color="#cbd5e1").pack(anchor="e", pady=(12, 4))
            grade_entry = ctk.CTkEntry(
                form_frame,
                font=("Segoe UI", 13),
                height=45,
                corner_radius=10,
                fg_color="#334155",
                border_color="#475569",
                text_color="#f8fafc"
            )
            grade_entry.pack(fill="x")

            def submit_grade():
                student = student_entry.get().strip()
                sub = subject_entry.get().strip()
                grd = grade_entry.get().strip()

                if not student or not sub or not grd:
                    show_custom_message(None)
                    return

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        subject_data = f"insert_new_grade|{current_user_class}|{grd}|{sub}|{student}"
                        s.sendall(subject_data.encode("utf-8"))

                        raw_data = s.recv(1024)
                        if raw_data:
                            dataFromServer = raw_data.decode("utf-8").strip()
                            if dataFromServer.startswith("insert_grade_response|"):
                                res_parts = dataFromServer.split("|")
                                if res_parts[1] == "success":
                                    show_custom_message(None, "הצלחה", f"הציון {grd} במקצוע {sub} עודכן בהצלחה עבור {student}")
                                else:
                                    show_custom_message(None, "שגיאה", f"{res_parts[2]}")
                except Exception as e:
                    show_custom_message(None, "שגיאה", f"שגיאה בהעברת הנתונים: {e}")

            save_button = ctk.CTkButton(
                form_frame,
                text="עדכן ציון במערכת",
                command=submit_grade,
                font=("Segoe UI", 15, "bold"),
                fg_color="#2563eb",
                hover_color="#1d4ed8",
                height=48,
                corner_radius=10,
                cursor="hand2"
            )
            save_button.pack(fill="x", pady=(22, 0))

            # Footer
            footer_frame = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=12, height=55)
            footer_frame.pack(side="bottom", fill="x", padx=12, pady=12)
            footer_frame.pack_propagate(False)

            ctk.CTkButton(
                footer_frame,
                text="חזרה למסך ראשי",
                command=lambda: open_main_page(current_username),
                font=("Segoe UI", 13, "bold"),
                fg_color="transparent",
                hover_color="#1e293b",
                text_color="#60a5fa",
                height=38,
                corner_radius=8,
                cursor="hand2"
            ).pack(expand=True)

            return

        # --- ממשק תלמיד (Dark Theme) ---
        new_win = ctk.CTkToplevel()
        new_win.overrideredirect(True)

        destroy_and_set_new_window(new_win)
        new_win.title("עמוד ציונים")

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a")

        main_frame = ctk.CTkFrame(
            new_win,
            fg_color="#1e293b",
            corner_radius=20,
            width=520,
            height=770
        )
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        # Header מודרני כהה
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#1d4ed8",
            corner_radius=16,
            height=180
        )
        header_frame.pack(fill="x", padx=12, pady=(12, 0))
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="📊",
            font=("Segoe UI", 46),
            text_color="#ffffff"
        ).pack(pady=(18, 0))

        ctk.CTkLabel(
            header_frame,
            text="ציונים שוטפים",
            font=("Segoe UI", 26, "bold"),
            text_color="#ffffff"
        ).pack()

        ctk.CTkLabel(
            header_frame,
            text="צפייה בכל הציונים והממוצע הכללי",
            font=("Segoe UI", 12),
            text_color="#93c5fd"
        ).pack()

        # טעינת נתונים
        grades = []
        average = 0

        SERVER_IP = '127.0.0.1'
        PORT = 9999
        try:
            with create_secure_socket() as s:
                s.connect((SERVER_IP, PORT))
                subject = f"gradesRequest|{current_user_class}|{current_username}"
                s.sendall(subject.encode('utf-8'))

                raw_data = s.recv(4096)
                if raw_data:
                    res_text = raw_data.decode('utf-8').strip()
                    response_data = json.loads(res_text)

                    if response_data.get("status") == "success":
                        grades = response_data.get("grades", [])
                        average = response_data.get("average", 0)
                    else:
                        show_custom_message(None, "שגיאה", "שגיאה בקבלת הנתונים מהשרת.")
                        new_win.destroy()
                        return
        except Exception as e:
            show_custom_message(None, "שגיאה", "לא ניתן להתחבר לשרת.")
            new_win.destroy()
            return

        # כרטיסיית ממוצע כהה ומובלטת
        avg_card = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=16, height=88)
        avg_card.pack(fill="x", padx=30, pady=15)
        avg_card.pack_propagate(False)

        ctk.CTkLabel(
            avg_card,
            text="ממוצע כללי",
            font=("Segoe UI", 12, "bold"),
            text_color="#94a3b8"
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            avg_card,
            text=str(average),
            font=("Segoe UI", 30, "bold"),
            text_color="#38bdf8"
        ).pack()

        # רשימת ציונים כהה בגלילה
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color="transparent",
            scrollbar_button_color="#334155",
            scrollbar_button_hover_color="#475569"
        )
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        for item_subject, grade_val in grades:
            card = ctk.CTkFrame(
                scroll_frame,
                fg_color="#334155",
                corner_radius=12,
                height=56
            )
            card.pack(fill="x", pady=5)
            card.pack_propagate(False)

            # מקצוע מימין
            ctk.CTkLabel(
                card,
                text=item_subject,
                font=("Segoe UI", 14, "bold"),
                text_color="#f8fafc"
            ).pack(side="right", padx=20)

            # ציון משמאל בתגית כחולה מובלטת
            badge = ctk.CTkFrame(card, fg_color="#1d4ed8", corner_radius=8)
            badge.pack(side="left", padx=15, pady=9)

            ctk.CTkLabel(
                badge,
                text=str(grade_val),
                font=("Segoe UI", 14, "bold"),
                text_color="#ffffff"
            ).pack(padx=12, pady=3)

        # Footer
        footer_frame = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=12, height=55)
        footer_frame.pack(side="bottom", fill="x", padx=12, pady=12)
        footer_frame.pack_propagate(False)

        ctk.CTkButton(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Segoe UI", 13, "bold"),
            fg_color="transparent",
            hover_color="#1e293b",
            text_color="#60a5fa",
            height=38,
            corner_radius=8,
            cursor="hand2"
        ).pack(expand=True)
    
    def open_doar():
        SERVER_IP = '127.0.0.1'
        PORT = 9999
        
        if current_user_role not in ["teacher", "student"]:
            show_custom_message(None, "שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
            return

        # שלב 1: משיכת הנתונים מהשרת
        try:
            with create_secure_socket() as s:
                s.connect((SERVER_IP, PORT))
                subject = f"get_class_doar|{current_user_class}"
                s.sendall(subject.encode('utf-8'))
                
                raw_data = s.recv(4096) 
                if raw_data:
                    res_text = raw_data.decode('utf-8').strip()
                    messages = json.loads(res_text)
                else:
                    messages = []
                    
        except Exception as e:
            print(f"Error loading mail: {e}")
            show_custom_message(None, "שגיאה", "לא ניתן להתחבר לשרת או לטעון את ההודעות.")
            return

        # שלב 2: יצירת חלון הממשק (Dark Theme)
        new_win = ctk.CTkToplevel()
        new_win.overrideredirect(True)

        destroy_and_set_new_window(new_win)
        new_win.title("עמוד דואר")

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a")  # Dark Background

        # Container ראשי כהה
        main_frame = ctk.CTkFrame(
            new_win,
            fg_color="#1e293b",
            corner_radius=20,
            width=520,
            height=770
        )
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        # Header מודרני כחול
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#1d4ed8",
            corner_radius=16,
            height=180
        )
        header_frame.pack(fill="x", padx=12, pady=(12, 0))
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="📨",
            font=("Segoe UI", 46),
            text_color="#ffffff"
        ).pack(pady=(18, 0))

        ctk.CTkLabel(
            header_frame,
            text="דואר נכנס",
            font=("Segoe UI", 26, "bold"),
            text_color="#ffffff"
        ).pack()

        ctk.CTkLabel(
            header_frame,
            text="הודעות ועדכונים מבית הספר",
            font=("Segoe UI", 12),
            text_color="#93c5fd"
        ).pack(pady=(2, 0))

        # רשימת הודעות בגלילה (Scrollable Frame)
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color="transparent",
            scrollbar_button_color="#334155",
            scrollbar_button_hover_color="#475569"
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=15)

        def refresh_messages():
            for widget in scroll_frame.winfo_children():
                widget.destroy()
                
            for sender, msg in messages:
                mail_card = ctk.CTkFrame(
                    scroll_frame,
                    fg_color="#334155",
                    corner_radius=12
                )
                mail_card.pack(fill="x", pady=6, padx=5)

                ctk.CTkLabel(
                    mail_card,
                    text=sender,
                    font=("Segoe UI", 13, "bold"),
                    text_color="#60a5fa"
                ).pack(anchor="e", padx=15, pady=(10, 2))

                ctk.CTkLabel(
                    mail_card,
                    text=msg,
                    font=("Segoe UI", 12),
                    text_color="#f8fafc",
                    wraplength=380,
                    justify="right"
                ).pack(anchor="e", padx=15, pady=(0, 10))

        refresh_messages()

        # חלון כתיבת הודעה חדשה (למורים - Dark Mode)
        def open_teacher_compose_window():
            compose_win = ctk.CTkToplevel(new_win)
            compose_win.overrideredirect(True)

            compose_win.title("פרסום הודעה חדשה")
            compose_win.configure(fg_color="#0f172a")
            
            cx = (screen_width // 2) - 200
            cy = (screen_height // 2) - 225
            compose_win.geometry(f"400x470+{cx}+{cy}")

            card_bg = ctk.CTkFrame(compose_win, fg_color="#1e293b", corner_radius=16)
            card_bg.pack(fill="both", expand=True, padx=10, pady=10)

            ctk.CTkLabel(
                card_bg,
                text="יצירת עדכון חדש",
                font=("Segoe UI", 18, "bold"),
                text_color="#38bdf8"
            ).pack(pady=(15, 5))

            ctk.CTkLabel(
                card_bg,
                text="כותרת ההודעה (למשל: הודעה ממורה למתמטיקה):",
                font=("Segoe UI", 11, "bold"),
                text_color="#cbd5e1"
            ).pack(anchor="e", padx=20, pady=(10, 4))
            
            title_entry = ctk.CTkEntry(
                card_bg,
                font=("Segoe UI", 12),
                height=40,
                corner_radius=8,
                fg_color="#334155",
                border_color="#475569",
                text_color="#f8fafc",
                justify="right"
            )
            title_entry.pack(fill="x", padx=20)

            ctk.CTkLabel(
                card_bg,
                text="תוכן ההודעה:",
                font=("Segoe UI", 11, "bold"),
                text_color="#cbd5e1"
            ).pack(anchor="e", padx=20, pady=(12, 4))

            content_text = ctk.CTkTextbox(
                card_bg,
                font=("Segoe UI", 12),
                height=130,
                corner_radius=8,
                fg_color="#334155",
                border_color="#475569",
                text_color="#f8fafc"
            )
            content_text.pack(fill="x", padx=20)

            def publish_message():
                title = title_entry.get().strip()
                content = content_text.get("1.0", tk.END).strip()
                
                if not title or not content:
                    show_custom_message(None, "שגיאה", "נא למלא את כל השדות", parent=compose_win)
                    return
                    
                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        subject = f"add_class_doar|{current_user_class}|{title}|{content}"
                        s.sendall(subject.encode('utf-8'))
                        
                        server_response = s.recv(1024).decode('utf-8').strip()
                        
                        if server_response == "200 ok":
                            messages.insert(0, (title, content))
                            show_custom_message(None, "הצלחה", "ההודעה פורסמה בהצלחה!", parent=compose_win)
                            compose_win.destroy()
                            refresh_messages()
                        else:
                            show_custom_message(None, "שגיאה", "השרת נכשל בשמירת ההודעה.", parent=compose_win)
                except Exception as e:
                    show_custom_message(None, "שגיאה", f"שגיאת תקשורת עם השרת: {e}", parent=compose_win)

            # כפתור פרסום ירוק מודרני
            ctk.CTkButton(
                card_bg,
                text="פרסום הודעה לכולם",
                command=publish_message,
                font=("Segoe UI", 13, "bold"),
                fg_color="#10b981",
                hover_color="#059669",
                height=42,
                corner_radius=8,
                cursor="hand2"
            ).pack(pady=(20, 10), padx=20, fill="x")

            # כפתור ביטול/סגירה
            ctk.CTkButton(
                card_bg,
                text="ביטול",
                command=compose_win.destroy,
                font=("Segoe UI", 12),
                fg_color="transparent",
                hover_color="#334155",
                text_color="#94a3b8",
                height=30,
                cursor="hand2"
            ).pack()

        # Footer
        footer_frame = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=12, height=58)
        footer_frame.pack(side="bottom", fill="x", padx=12, pady=12)
        footer_frame.pack_propagate(False)

        ctk.CTkButton(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Segoe UI", 12, "bold"),
            fg_color="transparent",
            hover_color="#1e293b",
            text_color="#60a5fa",
            height=38,
            corner_radius=8,
            cursor="hand2"
        ).pack(side="left", padx=15, pady=10)

        if current_user_role == "teacher":
            ctk.CTkButton(
                footer_frame,
                text="➕ כתיבת הודעה חדשה",
                command=open_teacher_compose_window,
                font=("Segoe UI", 12, "bold"),
                fg_color="#10b981",
                hover_color="#059669",
                height=38,
                corner_radius=8,
                cursor="hand2"
            ).pack(side="right", padx=15, pady=10)
        
    def open_class_chat_room():
        global current_username, current_user_class, current_user_role
        
        if current_user_role not in ["student", "teacher"]:
            show_custom_message(None, "שגיאה", "פיצ'ר זה זמין למשתמשים רשומים בלבד")
            return

        hebrew_display_map = {
            "7th1": 'ז\'1', "7th2": 'ז\'2', "7th3": 'ז\'3', "7th4": 'ז\'4', "7th5": 'ז\'5', "7th6": 'ז\'6',
            "8th1": 'ח\'1', "8th2": 'ח\'2', "8th3": 'ח\'3', "8th4": 'ח\'4', "8th5": 'ח\'5', "8th6": 'ח\'6',
            "9th1": 'ט\'1', "9th2": 'ט\'2', "9th3": 'ט\'3', "9th4": 'ט\'4', "9th5": 'ט\'5', "9th6": 'ט\'6',
            "10th1": 'י\'1', "10th2": 'י\'2', "10th3": 'י\'3', "10th4": 'י\'4', "10th5": 'י\'5', "10th6": 'י\'6',
            "11th1": 'י"א1', "11th2": 'י"א2', "11th3": 'י"א3', "11th4": 'י"א4', "11th5": 'י"א5', "11th6": 'י"א6',
            "12th1": 'י"ב1', "12th2": 'י"ב2', "12th3": 'י"ב3', "12th4": 'י"ב4', "12th5": 'י"ב5', "12th6": 'י"ב6',
        }
        
        class_raw = current_user_class
        simplified_class = hebrew_display_map.get(class_raw, class_raw)
        
        # חלון עליון מבית CustomTkinter
        new_win = ctk.CTkToplevel()
        new_win.overrideredirect(True)

        destroy_and_set_new_window(new_win)
        new_win.title("צ'אט כיתתי")
        
        width, height = 480, 720
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a") # רקע כהה ויוקרתי

        # ------------------ כותרת עליונה (Header) ------------------
        header_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=15, height=75)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)

        # כפתור יציאה מודרני ועגול
        btn_back = ctk.CTkButton(
            header_frame, 
            text="✕", 
            width=36,
            height=36,
            corner_radius=18,
            font=("Segoe UI", 14, "bold"), 
            fg_color="#334155", 
            hover_color="#ef4444", # הופך לאדום בריחוף!
            text_color="#f8fafc",
            command=lambda: open_main_page(current_username)
        )
        btn_back.pack(side="left", padx=15, pady=18)

        # פרטי הצ'אט
        title_info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_info_frame.pack(side="right", padx=15, pady=10)

        ctk.CTkLabel(
            title_info_frame, 
            text=f"צ'אט כיתה {simplified_class}", 
            font=("Segoe UI", 16, "bold"), 
            text_color="#f8fafc"
        ).pack(anchor="e")
        
        ctk.CTkLabel(
            title_info_frame, 
            text="🔒 מוצפן מקצה לקצה", 
            font=("Segoe UI", 11), 
            text_color="#38bdf8"
        ).pack(anchor="e")

        # ------------------ אזור הצ'אט (Scrollable Frame מודרני) ------------------
        chat_scroll_frame = ctk.CTkScrollableFrame(
            new_win, 
            fg_color="#0f172a", 
            scrollbar_button_color="#334155",
            scrollbar_button_hover_color="#475569"
        )
        chat_scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # ------------------ סרגל קלט הודעה ------------------
        input_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=20, height=65)
        input_frame.pack(fill="x", padx=10, pady=(5, 10))
        input_frame.pack_propagate(False)

        # כפתור שליחה מעוגל
        btn_send = ctk.CTkButton(
            input_frame, 
            text="שליחה ➔", 
            width=85,
            height=40,
            corner_radius=15,
            font=("Segoe UI", 12, "bold"), 
            fg_color="#2563eb", 
            hover_color="#1d4ed8",
            text_color="white",
            command=lambda: send_message()
        )
        btn_send.pack(side="left", padx=10, pady=12)

        # תיבת טקסט מעוצבת
        msg_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="כתיבת הודעה...",
            font=("Segoe UI", 13), 
            fg_color="#0f172a", 
            border_color="#334155",
            border_width=1,
            corner_radius=15,
            justify="right",
            text_color="#f8fafc",
            placeholder_text_color="#64748b"
        )
        msg_entry.pack(side="right", fill="x", expand=True, padx=(5, 10), pady=12)
        msg_entry.focus_set()

        def send_message(event=None):
            msg_text = msg_entry.get().strip()
            if not msg_text:
                return
            
            msg_text = msg_text.replace("|", " ") 
            
            SERVER_IP = '127.0.0.1'
            PORT = 9999
            try:
                with create_secure_socket() as s:
                    s.connect((SERVER_IP, PORT))
                    subject = f"send_chat_message|{class_raw}|{current_username}|{current_user_role}|{msg_text}"
                    s.sendall(subject.encode('utf-8'))
                    raw_data = s.recv(1024)
                    if raw_data:
                        res = raw_data.decode('utf-8').strip()
                        if res == "200 ok":
                            msg_entry.delete(0, tk.END) 
                            load_chat_history()
            except Exception as e:
                print(f"Error sending message: {e}")

        msg_entry.bind("<Return>", send_message)

        loaded_message_count = 0

        # ------------------ ציור בועת הודעה מעוגלת ------------------
        def render_bubble(msg_data):
            user = msg_data.get("username", "Unknown")
            text = msg_data.get("message", "")
            time_str = msg_data.get("time", "")
            role = msg_data.get("role", "student")
            
            is_me = (user == current_username)
            is_teacher = (role == "teacher")

            row = ctk.CTkFrame(chat_scroll_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)

            # עיצוב הבועה לפי זהות השולח
            if is_teacher:
                bg_color = "#451a03"       # חום-זהב כהה ויוקרתי
                border_color = "#d97706"   # מסגרת זהב
                border_width = 1
                header_text = f"👑 {user} (מורה)"
                header_color = "#fef08a"
                pack_side = "left"
                align_anchor = "w"
            elif is_me:
                bg_color = "#1e3a8a"       # כחול עמוק ומודרני
                border_color = "#3b82f6"
                border_width = 0
                header_text = "אני"
                header_color = "#93c5fd"
                pack_side = "right"
                align_anchor = "e"
            else:
                bg_color = "#1e293b"       # אפור כהה נקי
                border_color = "#334155"
                border_width = 1
                header_text = f"👤 {user}"
                header_color = "#cbd5e1"
                pack_side = "left"
                align_anchor = "w"

            # הבועה המעוגלת!
            bubble = ctk.CTkFrame(
                row, 
                fg_color=bg_color, 
                border_color=border_color, 
                border_width=border_width,
                corner_radius=16
            )
            bubble.pack(side=pack_side, anchor=align_anchor, padx=5)

            # כותרת ההודעה (שם + שעה)
            header_frame_msg = ctk.CTkFrame(bubble, fg_color="transparent")
            header_frame_msg.pack(fill="x", padx=12, pady=(8, 2))

            ctk.CTkLabel(
                header_frame_msg, 
                text=header_text, 
                font=("Segoe UI", 10, "bold"), 
                text_color=header_color
            ).pack(side="right" if is_me else "left")

            ctk.CTkLabel(
                header_frame_msg, 
                text=f"  {time_str}", 
                font=("Segoe UI", 9), 
                text_color="#64748b"
            ).pack(side="right" if is_me else "left")

            # גוף ההודעה
            ctk.CTkLabel(
                bubble, 
                text=text, 
                font=("Segoe UI", 12), 
                text_color="#f8fafc", 
                justify="right", 
                wraplength=290
            ).pack(anchor=align_anchor, padx=12, pady=(0, 8))

        def load_chat_history():
            nonlocal loaded_message_count
            if not new_win.winfo_exists():
                return
                
            SERVER_IP = '127.0.0.1'
            PORT = 9999
            try:
                with create_secure_socket() as s:
                    s.connect((SERVER_IP, PORT))
                    subject = f"get_chat_history|{class_raw}"
                    s.sendall(subject.encode('utf-8'))
                    
                    chunks = []
                    while True:
                        chunk = s.recv(4096)
                        if not chunk:
                            break
                        chunks.append(chunk)
                    
                    raw_res = b"".join(chunks).decode('utf-8').strip()
                    if raw_res.startswith("error") or not raw_res:
                        return
                        
                    history = json.loads(raw_res)
                    
                    if len(history) > loaded_message_count:
                        for msg in history[loaded_message_count:]:
                            render_bubble(msg)
                        
                        loaded_message_count = len(history)
                        
                        # גלילה אוטומטית חלקות למטה
                        chat_scroll_frame._parent_canvas.yview_moveto(1.0)
                        
            except Exception as e:
                print(f"Error loading chat: {e}")

        def auto_refresh():
            if new_win.winfo_exists():
                load_chat_history()
                new_win.after(2000, auto_refresh)
                
        load_chat_history()
        auto_refresh()
        
        
    def open_todo_list():
        global current_username, current_user_class, current_user_role
        SERVER_IP = '127.0.0.1'
        PORT = 9999

        tasks = []

        try:
            with create_secure_socket() as s:
                print(f"Connecting to {SERVER_IP}:{PORT}...")
                s.connect((SERVER_IP, PORT))

                subject = f"tasks|{current_user_class}|{current_username}"
                s.sendall(subject.encode("utf-8"))

                raw_data = s.recv(1024)
                if not raw_data:
                    show_custom_message(None, "שגיאה", "אין תגובה מהשרת")
                    return

                dataFromServer = raw_data.decode("utf-8").strip()
                print(f"Received from server: {dataFromServer}")

                if dataFromServer.startswith("username:"):
                    show_custom_message(None, "שגיאה", "עליך להירשם למערכת כדי להשתמש באופציה זו")
                    open_login_window()
                    return
                else:
                    try:
                        tasks = json.loads(dataFromServer)
                        print(f"Parsed tasks as list: {tasks}")
                    except json.JSONDecodeError:
                        print("Error decoding tasks from server")
                        tasks = []

        except ConnectionRefusedError:
            show_custom_message(None, "שגיאה", "לא ניתן להתחבר לשרת")
            return
        except Exception as e:
            show_custom_message(None, "שגיאה", f"אירעה שגיאה: {e}")
            return

        # ------------------ חלון ראשי ------------------
        new_win = ctk.CTkToplevel()
        new_win.overrideredirect(True)

        destroy_and_set_new_window(new_win)
        new_win.title("To Do List")

        width, height = 550, 750
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a") # רקע כהה

        # התיקון כאן: ה-width וה-height מוגדרים בתוך ה-CTkFrame, ולא ב-place()
        main_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=20, width=510, height=710)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False) # מונע מהפריים להתכווץ לפי התוכן

        # ------------------ כותרת ------------------
        header = ctk.CTkFrame(main_frame, fg_color="#3b82f6", corner_radius=15, height=90)
        header.pack(fill="x", padx=15, pady=(15, 10))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📝 To Do List",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(pady=(15, 2))

        ctk.CTkLabel(
            header,
            text="המשימות שלך להיום",
            font=("Segoe UI", 11),
            text_color="#e0f2fe"
        ).pack()

        # ------------------ אזור המשימות ------------------
        tasks_frame = ctk.CTkScrollableFrame(
            main_frame, 
            fg_color="#0f172a", 
            corner_radius=15,
            scrollbar_button_color="#334155"
        )
        tasks_frame.pack(fill="both", expand=True, padx=15, pady=10)

        def add_task(task_text, done=False):
            row = ctk.CTkFrame(tasks_frame, fg_color="#1e293b", corner_radius=12)
            row.pack(fill="x", pady=5, padx=5)

            var = tk.BooleanVar(value=done)

            def remove_task():
                if var.get(): 
                    if task_text in tasks:
                        tasks.remove(task_text)
                    row.destroy()

            chk = ctk.CTkCheckBox(
                row,
                text="",
                variable=var,
                command=remove_task,
                width=24,
                height=24,
                corner_radius=6,
                checkbox_width=20,
                checkbox_height=20,
                fg_color="#10b981",
                hover_color="#059669"
            )
            chk.pack(side="left", padx=12, pady=12)

            ctk.CTkLabel(
                row,
                text=task_text,
                font=("Segoe UI", 13),
                text_color="#f8fafc",
                anchor="e"
            ).pack(side="right", fill="x", expand=True, padx=15, pady=12)

        def add_task_to_gui():
            if current_user_role in ["teacher", "student"]:
                text_val = task_entry.get().strip()
                add_task(task_text=text_val)
                tasks.append(text_val)
                task_entry.delete(0, tk.END)
            else:
                show_custom_message(None, "שגיאה", "הירשם כדי להשתמש או לראות את פיצ'ר זה")
                return

        for task in tasks:
            add_task(task)

        # ------------------ סרגל הכנסת משימה ------------------
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=10)

        task_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="הקלד משימה חדשה...",
            font=("Segoe UI", 12),
            fg_color="#0f172a",
            border_color="#334155",
            border_width=1,
            corner_radius=12,
            justify="right",
            text_color="#f8fafc",
            placeholder_text_color="#64748b"
        )
        task_entry.pack(side="right", fill="x", expand=True, padx=(8, 0), ipady=4)

        def checkIfValid():
            if current_user_role in ["teacher", "student"]:
                if task_entry.get().strip() == "":
                    show_custom_message(None, "שגיאה", "משימה לא יכולה להיות ריקה")
                    return
                
                if len(tasks) >= 7:
                    show_custom_message(None, "שגיאה", "הגעת למגבלת המשימות (עד 7 משימות)")
                    return
            add_task_to_gui()

        btn_add = ctk.CTkButton(
            input_frame,
            text="הוסף +",
            font=("Segoe UI", 12, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            corner_radius=12,
            width=80,
            height=38,
            command=checkIfValid
        )
        btn_add.pack(side="left")

        footer = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer.pack(fill="x", padx=15, pady=(5, 15))

        def saveTasks():
            if current_user_role in ["teacher", "student"]:
                tasks_json = json.dumps(tasks, ensure_ascii=False)
                update_message = f"update_tasks|{current_user_class}|{current_username}|{tasks_json}"
                
                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        s.sendall(update_message.encode("utf-8"))
                        
                        response = s.recv(1024).decode("utf-8")
                        if response == "200 ok":
                            print("[+] Tasks saved to server successfully")
                        else:
                            print(f"[-] Server error during save: {response}")
                            
                except Exception as e:
                    show_custom_message(None, "שגיאת סנכרון", f"המשימות נשמרו מקומית אך לא בשרת: {e}")
            
            open_main_page(current_username)

        btn_back = ctk.CTkButton(
            footer,
            text="שמור וחזור",
            font=("Segoe UI", 12, "bold"),
            fg_color="#475569",
            hover_color="#334155",
            corner_radius=12,
            height=40,
            command=saveTasks
        )
        btn_back.pack(fill="x")
        
    def open_reminder():
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.overrideredirect(True)

        new_win.title("עמוד תזכורון")
        width = 400
        height = 620
                
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
                    
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
                    
        new_win.geometry(f"{width}x{height}+{x}+{y}")

        def reminder_completed():
                fields = {
                        "כיתה": classt.get(),
                        "לשים לב ל": keep_an_eye.get(),
                        "תזכורת": remind.get(),
                        "מורה": techer.get(),
                        "מה נעשה היום": did_today.get(),
                        "מה לא נעשה": didnt_do.get(),
                        "הכנה לשיעור הבא": preper.get(),
                        "תחילת שיעור": start_leason.get(),
                        "מיקוד": focus.get()
                }
                
                if not current_user_role == "teacher" or not current_user_role == "student":
                    show_custom_message(None, "שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
                    return

                if any(value == "" for value in fields.values()):
                        show_custom_message(None, "שגיאה", "בבקשה תמלא את כל הפרטים בטופס")
                        
                else:
                        try:
                                files = os.listdir(".")
                                for file in files:
                                        if os.path.exists("reminder.json"):
                                                show_custom_message(None, "שגיאה", "תזכורון אחד כבר קיים, מחק אותו כדי ליצור חדש")
                                                break
                                        
                                        else:      
                                                with open("data/reminder.json", "w", encoding="utf-8") as f:
                                                        json.dump(fields, f, indent=4, ensure_ascii=False)
                                                        show_custom_message(None, "תזכורון מוצלח", "טופס התזכורון נשמר בהצלחה!")
                                                        break
                                
                        except Exception as e:
                                show_custom_message(None, "שגיאה", f"ארעה שגיאה בשמירה: {e}")

        def delete_existing():
                files = os.listdir(".")
                for file in files:
                        if os.path.exists("data/reminder.json"):
                                os.remove("data/reminder.json")
                                show_custom_message(None, "הצלחה", "התזכורון הקיים נמחק")
                                break
                        
                else:
                        show_custom_message(None, "שגיאה", "לא נמצא תזכורון קיים")
        
        def see_existing():
                files = os.listdir(".")
                for file in files:
                        if os.path.exists("data/reminder.json"):
                                new_win = tk.Toplevel()
                                destroy_and_set_new_window(new_win)
                                new_win.title("ראיית תזכורון קיים")
                                
                                width = 400
                                height = 620
                                        
                                screen_width = new_win.winfo_screenwidth()
                                screen_height = new_win.winfo_screenheight()
                                            
                                x = (screen_width // 2) - (width // 2)
                                y = (screen_height // 2) - (height // 2)
                                            
                                new_win.geometry(f"{width}x{height}+{x}+{y}")
                                
                                try:
                                        with open("data/reminder.json", "r", encoding="utf-8") as f:
                                                data = json.load(f)
                                                entery_class = data.get("כיתה", "תוכן לא נמצא")
                                                entery_notice = data.get("לשים לב ל", "תוכן לא נמצא")
                                                entery_remind = data.get("תזכורת", "תוכן לא נמצא")
                                                entery_teacher = data.get("מורה", "תוכן לא נמצא")
                                                entery_do_today = data.get("מה נעשה היום", "תוכן לא נמצא")
                                                entery_not_today = data.get("מה לא נעשה", "תוכן לא נמצא")
                                                entery_prepair_next = data.get("הכנה לשיעור הבא", "תוכן לא נמצא")
                                                entery_start = data.get("תחילת שיעור", "תוכן לא נמצא")
                                                entery_focus = data.get("מיקוד", "תוכן לא נמצא")                                
                                
                                except FileNotFoundError as e:
                                        print(f"לא נמצא הקובץ")
                                        
                                tk.Button(new_win, 
                                text="חזרה למסך ראשי",
                                command=lambda: open_main_page(current_username),
                                cursor="hand2",).place(x=10, y=10)

                                tk.Label(new_win, text="התזכורון שלך", font="Arial 21 bold",
                                        fg="blue").place(x=155, y=45)
                                        
                                tk.Label(new_win,
                                        text="אלו הפתקים שכתבת לשיעור הבא שלך",
                                        fg="blue",
                                        font="Arial 14").place(x=75, y=90)

                                tk.Label(new_win,
                                        text="כיתה",
                                        font="Arial 14 bold",
                                        fg="blue").place(x=315,y=145)
                                        
                                classt1 = ttk.Entry(new_win,
                                        width=4,
                                        font="Arial 12")
                                classt1.place(x=250, y=145)
                                
                                classt1.insert(0, entery_class)
                                
                                classt1.config(state="readonly")
                                
                                tk.Label(new_win,
                                        text="מורה",
                                        font="Arial 14 bold",
                                        fg="blue").place(x=185,y=145)
                                        
                                techer1 = ttk.Entry(new_win,
                                        width=9,
                                        font="Arial 12" )
                                techer1.place(x=75, y=145)   
                                
                                techer1.insert(0, entery_teacher)
                                
                                techer1.config(state="readonly")

                                tk.Label(new_win,
                                        text="?מה עשינו היום",
                                        font="Arial 12 bold",
                                        fg="blue",).place(x=288, y=210)

                                did_today1 = ttk.Entry(new_win,
                                        font="Arial 11",
                                        width=20,)
                                did_today1.place(x=114, y=210) 
                                
                                did_today1.insert(0, entery_do_today)
                                
                                did_today1.config(state="readonly")        

                                tk.Label(new_win,
                                        text="?מה צריך להספיק",
                                        font="Arial 12 bold",
                                        fg="blue",).place(x=274, y=250)

                                didnt_do1 = ttk.Entry(new_win,
                                        font="Arial 11",
                                        width=20,)
                                didnt_do1.place(x=100, y=250) 
                                
                                didnt_do1.insert(0, entery_not_today)
                                
                                didnt_do1.config(state="readonly")

                                tk.Label(new_win,
                                        text="?מה צריך להכין לשיעור הבא",
                                        font="Arial 12 bold",
                                        fg="blue",).place(x=209, y=290)

                                preper1 = ttk.Entry(new_win,
                                        font="Arial 11",
                                        width=20,)
                                preper1.place(x=35, y=290) 
                                
                                preper1.insert(0, entery_prepair_next)
                                
                                preper1.config(state="readonly")
                                        
                                tk.Label(new_win,
                                        text="?איך אני אתחיל את השיעור",
                                        font="Arial 12 bold",
                                        fg="blue",).place(x=215, y=330)

                                start_leason1 = ttk.Entry(new_win,
                                        font="Arial 11",
                                        width=20,)
                                start_leason1.place(x=43, y=330) 
                                
                                start_leason1.insert(0, entery_start)
                                
                                start_leason1.config(state="readonly")

                                tk.Label(new_win,
                                        text="?על מה להתפקס בשיעור",
                                        font="Arial 12 bold",
                                        fg="blue",).place(x=228, y=370)

                                focus1 = ttk.Entry(new_win,
                                        font="Arial 11",
                                        width=20,)
                                focus1.place(x=56, y=370) 
                                
                                focus1.insert(0, entery_focus)
                                
                                focus1.config(state="readonly")
                                        
                                tk.Label(new_win,
                                        text="תזכורת לשיעור הבא",
                                        font="Arial 12 bold",
                                        fg="blue",).place(x=259, y=410)

                                remind1 = ttk.Entry(new_win,
                                        font="Arial 11",
                                        width=20,)
                                remind1.place(x=89, y=410) 
                                
                                remind1.insert(0, entery_remind)
                                
                                remind1.config(state="readonly")

                                tk.Label(new_win,
                                        text="?על מי צריך לשים עין",
                                        font="Arial 12 bold",
                                        fg="blue",).place(x=253, y=450)

                                keep_an_eye1 = ttk.Entry(new_win,
                                        font="Arial 11",
                                        width=20,)
                                keep_an_eye1.place(x=82, y=450)
                                
                                keep_an_eye1.insert(0, entery_notice)
                                
                                keep_an_eye1.config(state="readonly")
                                
                        else:
                                show_custom_message(None, "שגיאה", "לא נמצא תזכורון קיים")
                                break
                        
        tk.Button(new_win, 
                text="חזרה למסך ראשי",
                command=lambda: open_main_page(current_username),
                cursor="hand2",).place(x=10, y=10)

        tk.Label(new_win, text="תזכורון", font="Arial 21 bold",
                fg="blue").place(x=155, y=45)
                
        tk.Label(new_win,
                text="פה תכתוב פתקים לשיעור הבא שלך",
                fg="blue",
                font="Arial 14").place(x=75, y=90)

        tk.Label(new_win,
                text="כיתה",
                font="Arial 14 bold",
                fg="blue").place(x=315,y=145)
                
        classt = ttk.Combobox(new_win,
                width=4,
                values=["ט'1", "ט'2", "ט'3", "ט'4", "ט'5", "ט'6"],
                state="readonly",
                font="Arial 12")
        classt.place(x=250, y=145)

        tk.Label(new_win,
                text="מורה",
                font="Arial 14 bold",
                fg="blue").place(x=185,y=145)
                
        techer = ttk.Combobox(new_win,
                width=9,
                values=["הרב שלומי", "אוריה דביר", "יעל אלבז", "המנהל נועם", "נועם שיף", "הרב יעקב"],
                state="readonly",
                font="Arial 12" )
        techer.place(x=75, y=145)   
                

        tk.Label(new_win,
                text="?מה עשינו היום",
                font="Arial 12 bold",
                fg="blue",).place(x=288, y=210)

        did_today = ttk.Entry(new_win,
                font="Arial 11",
                width=20,)
        did_today.place(x=114, y=210)         

        tk.Label(new_win,
                text="?מה צריך להספיק",
                font="Arial 12 bold",
                fg="blue",).place(x=274, y=250)

        didnt_do = ttk.Entry(new_win,
                font="Arial 11",
                width=20,)
        didnt_do.place(x=100, y=250) 

        tk.Label(new_win,
                text="?מה צריך להכין לשיעור הבא",
                font="Arial 12 bold",
                fg="blue",).place(x=209, y=290)

        preper = ttk.Entry(new_win,
                font="Arial 11",
                width=20,)
        preper.place(x=35, y=290) 
                
        tk.Label(new_win,
                text="?איך אני אתחיל את השיעור",
                font="Arial 12 bold",
                fg="blue",).place(x=215, y=330)

        start_leason = ttk.Entry(new_win,
                font="Arial 11",
                width=20,)
        start_leason.place(x=43, y=330) 

        tk.Label(new_win,
                text="?על מה להתפקס בשיעור",
                font="Arial 12 bold",
                fg="blue",).place(x=228, y=370)

        focus = ttk.Entry(new_win,
                font="Arial 11",
                width=20,)
        focus.place(x=56, y=370) 
                
        tk.Label(new_win,
                text="תזכורת לשיעור הבא",
                font="Arial 12 bold",
                fg="blue",).place(x=259, y=410)

        remind = ttk.Entry(new_win,
                font="Arial 11",
                width=20,)
        remind.place(x=89, y=410) 

        tk.Label(new_win,
                text="?על מי צריך לשים עין",
                font="Arial 12 bold",
                fg="blue",).place(x=253, y=450)

        keep_an_eye = ttk.Entry(new_win,
                font="Arial 11",
                width=20,)
        keep_an_eye.place(x=82, y=450)

        tk.Label(new_win, 
                text="בלחיצה על כפתור שמירת הטופס אני מאפשר\n גישה מלאה לקבצים שלי",
                font="Arial 11 bold", 
                fg="blue").place(x=60, y=500) 
                
        tk.Button(new_win,
                text="שמירת הטופס",
                font="Arial 10 bold",
                bg="blue",
                fg="ghostwhite",
                bd=0,
                width=11,
                height=2,
                activebackground="lightblue",
                command=reminder_completed,
                cursor="hand2",).place(x=13, y=560)
        
        tk.Button(new_win,
                text="ניקוי הקיים",
                font="Arial 10 bold",
                bg="blue",
                fg="ghostwhite",
                bd=0,
                width=11,
                height=2,
                activebackground="lightblue",
                command=delete_existing,
                cursor="hand2",).place(x=145, y=560)

        tk.Button(new_win,
                text="ראיית הקיים",
                font="Arial 10 bold",
                bg="blue",
                fg="ghostwhite",
                bd=0,
                width=11,
                height=2,
                activebackground="lightblue",
                command=see_existing,
                cursor="hand2",).place(x=280, y=560)

    def check_my_requests_status(student_id, student_class):
        SERVER_IP = '127.0.0.1'
        PORT = 9999

        try:
            with create_secure_socket() as s:
                s.connect((SERVER_IP, PORT))
                
                request_msg = f"get_student_requests|{student_class}|{student_id}"
                s.sendall(request_msg.encode('utf-8'))

                full_response = ""
                while True:
                    raw_data = s.recv(4096)
                    if not raw_data:
                        break
                    full_response += raw_data.decode('utf-8')
                
                response = full_response.strip()
                
                if response.startswith("student_requests_data|"):
                    json_string = response.split("|", 1)[1]
                    if json_string == "{}" or not json_string:
                        show_custom_message(None, "סטטוס בקשות", "אין לך בקשות שחרור במערכת.")
                        return
                    
                    my_requests = json.loads(json_string)
                    
                    for req_id, req_info in my_requests.items():
                        status = req_info.get("status")
                        day = req_info.get("day")
                        time = req_info.get("time")
                        
                        if status == "approved":
                            status_heb = "אושרה! ✔ (סע לשלום)"
                        elif status == "rejected":
                            status_heb = "נדחתה ❌ (נשארים ללמוד)"
                        else:
                            status_heb = "ממתינה לבדיקת מורה ⏳"
                            
                        show_custom_message(None, "עדכון בקשה", f"הבקשה שלך ל{day} בשעה {time}:\nסטטוס: {status_heb}")
                        
        except Exception as e:
            show_custom_message(None, "שגיאה", f"לא ניתן לבדוק סטטוס: {e}")
    
    def open_freer():            
        global current_user_role, current_username, current_user_class
        
        # =========================================================================
        #                             ממשק מורה (מנהל)
        # =========================================================================
        if current_user_role == "teacher":
            new_win = ctk.CTkToplevel()
            new_win.overrideredirect(True)

            destroy_and_set_new_window(new_win)
            new_win.title("ניהול בקשות שחרור - ממשק מורה")

            width, height = 720, 780 
            screen_width = new_win.winfo_screenwidth()
            screen_height = new_win.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            new_win.geometry(f"{width}x{height}+{x}+{y}")
            new_win.configure(fg_color="#0f172a")

            # פריים ראשי - הגדרת גודל בתוך ה-Constructor
            main_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=20, width=680, height=740)
            main_frame.place(relx=0.5, rely=0.5, anchor="center")
            main_frame.pack_propagate(False)

            # ------------------ כותרת מורה ------------------
            header_frame = ctk.CTkFrame(main_frame, fg_color="#3b82f6", corner_radius=15, height=120)
            header_frame.pack(fill="x", padx=15, pady=(15, 10))
            header_frame.pack_propagate(False)

            ctk.CTkLabel(
                header_frame,
                text="📋 מרכז בקשות שחרור",
                font=("Segoe UI", 20, "bold"),
                text_color="white"
            ).pack(pady=(20, 2))

            ctk.CTkLabel(
                header_frame,
                text="צפייה, אישור ודחייה של בקשות יציאה של תלמידים",
                font=("Segoe UI", 11),
                text_color="#e0f2fe"
            ).pack()

            # ------------------ אזור הטבלה ------------------
            table_container = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=15)
            table_container.pack(fill="both", expand=True, padx=15, pady=10)

            # עיצוב מודרני ל-Treeview המובנה
            style = ttk.Style()
            style.theme_use("clam")
            style.configure(
                "Treeview", 
                font=("Segoe UI", 10), 
                rowheight=32, 
                background="#1e293b", 
                foreground="#f8fafc",
                fieldbackground="#1e293b",
                bordercolor="#334155"
            )
            style.configure(
                "Treeview.Heading", 
                font=("Segoe UI", 10, "bold"), 
                background="#334155", 
                foreground="#f8fafc",
                relief="flat"
            )
            style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "white")])

            columns = ("id_s", "day", "hour", "reason")
            tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")
            
            tree.heading("id_s", text="ת.ז. תלמיד")
            tree.heading("day", text="יום שחרור")
            tree.heading("hour", text="שעה")
            tree.heading("reason", text="סיבה / הערה מההורה")
            
            tree.column("id_s", width=110, anchor="center")
            tree.column("day", width=100, anchor="center")
            tree.column("hour", width=70, anchor="center")
            tree.column("reason", width=280, anchor="e") 

            scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            scrollbar.pack(side="right", fill="y", pady=5)

            # ------------------ לוגיקת מורה ------------------
            def approve_request():
                selected_item = tree.selection()
                if not selected_item:
                    show_custom_message(None, "שימו לב", "אנא בחרו בקשה מהרשימה לאישור")
                    return
                
                req_id = selected_item[0]
                item_details = tree.item(selected_item)['values']
                student_id = item_details[0]

                class_name = current_user_class.get() if hasattr(current_user_class, 'get') else current_user_class
                class_name = str(class_name).strip()

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        update_msg = f"update_request_status|{class_name}|{req_id}|approved"
                        s.sendall(update_msg.encode('utf-8'))

                        raw_data = s.recv(1024)
                        if raw_data:
                            res = raw_data.decode('utf-8').strip()
                            if res == "200 ok":
                                show_custom_message(None, "הצלחה", f"בקשת השחרור עבור תלמיד {student_id} אושרה בהצלחה!")
                                tree.delete(selected_item)
                            else:
                                show_custom_message(None, "שגיאה", f"השרת החזיר תשובה שלילית: {res}")
                except Exception as e:
                    show_custom_message(None, "שגיאה", f"שגיאת תקשורת עם השרת: {e}")

            def reject_request():
                selected_item = tree.selection()
                if not selected_item:
                    show_custom_message(None, "שימו לב", "אנא בחרו בקשה מהרשימה לדחייה")
                    return
                
                req_id = selected_item[0]
                item_details = tree.item(selected_item)['values']
                student_id = item_details[0]

                class_name = current_user_class.get() if hasattr(current_user_class, 'get') else current_user_class
                class_name = str(class_name).strip()

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        update_msg = f"update_request_status|{class_name}|{req_id}|rejected"
                        s.sendall(update_msg.encode('utf-8'))

                        raw_data = s.recv(1024)
                        if raw_data:
                            res = raw_data.decode('utf-8').strip()
                            if res == "200 ok":
                                show_custom_message(None, "סטטוס עודכן", f"בקשת השחרור עבור תלמיד {student_id} נדחתה.")
                                tree.delete(selected_item)
                            else:
                                show_custom_message(None, "שגיאה", f"השרת החזיר תשובה שלילית: {res}")
                except Exception as e:
                    show_custom_message(None, "שגיאה", f"שגיאת תקשורת עם השרת: {e}")

            def load_requests():
                for item in tree.get_children():
                    tree.delete(item)

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        class_name = current_user_class.get() if hasattr(current_user_class, 'get') else current_user_class
                        
                        request_msg = f"get_freer_requests|{class_name}"
                        s.sendall(request_msg.encode('utf-8'))

                        full_response = ""
                        while True:
                            raw_data = s.recv(4096)
                            if not raw_data:
                                break
                            full_response += raw_data.decode('utf-8')
                        
                        response = full_response.strip()

                        if response.startswith("requests_data|"):
                            json_string = response.split("|", 1)[1]
                            if json_string == "{}" or not json_string:
                                return  
                            
                            all_requests = json.loads(json_string)
                            
                            for req_id, req_info in all_requests.items():
                                if req_info.get("status") == "pending":
                                    row = (
                                        req_info.get("student_id"),
                                        req_info.get("day"),
                                        req_info.get("time"),
                                        req_info.get("reason")
                                    )
                                    tree.insert("", "end", iid=req_id, values=row)
                except Exception as e:
                    show_custom_message(None, "שגיאה", f"לא ניתן לטעון את בקשות השחרור: {e}")

            load_requests()

            # ------------------ כפתורי פעולה למורה ------------------
            actions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            actions_frame.pack(fill="x", padx=15, pady=5)

            btn_approve = ctk.CTkButton(
                actions_frame,
                text="אשר בקשה ✔",
                command=approve_request,
                font=("Segoe UI", 12, "bold"),
                fg_color="#10b981", 
                hover_color="#059669",
                corner_radius=10,
                height=40
            )
            btn_approve.pack(side="right", fill="x", expand=True, padx=(5, 0))

            btn_reject = ctk.CTkButton(
                actions_frame,
                text="דחה בקשה ❌",
                command=reject_request,
                font=("Segoe UI", 12, "bold"),
                fg_color="#ef4444", 
                hover_color="#dc2626",
                corner_radius=10,
                height=40
            )
            btn_reject.pack(side="left", fill="x", expand=True, padx=(0, 5))

            footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            footer_frame.pack(fill="x", padx=15, pady=(5, 15))

            ctk.CTkButton(
                footer_frame,
                text="חזרה למסך ראשי",
                command=lambda: open_main_page(current_username),
                font=("Segoe UI", 12, "bold"),
                fg_color="#475569",
                hover_color="#334155",
                corner_radius=10,
                height=38
            ).pack(fill="x")

            return 

        # =========================================================================
        #                        ממשק תלמיד / הורה (טופס)
        # =========================================================================
        new_win = ctk.CTkToplevel()
        new_win.overrideredirect(True)

        destroy_and_set_new_window(new_win)
        new_win.title("עמוד שיחרורון")

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a")

        main_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=20, width=480, height=730)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        student_id_var = tk.StringVar()
        parent_id_var = tk.StringVar()
        day_var = tk.StringVar()
        hour_var = tk.StringVar()
        reason_var = tk.StringVar()

        # ------------------ כותרת תלמיד ------------------
        header_frame = ctk.CTkFrame(main_frame, fg_color="#3b82f6", corner_radius=15, height=130)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)

        # כפתור בדיקת סטטוס בתוך הכותרת
        btn_status = ctk.CTkButton(
            header_frame,
            text="בדוק סטטוס 🔍",
            command=lambda: check_my_requests_status(student_id_var.get(), current_user_class), 
            font=("Segoe UI", 10, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            corner_radius=8,
            width=100,
            height=28
        )
        btn_status.place(relx=0.05, rely=0.15)

        ctk.CTkLabel(
            header_frame,
            text="📄 בקשת שחרור",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(pady=(25, 2))

        ctk.CTkLabel(
            header_frame,
            text="שליחת בקשת יציאה מסודרת למחנך/ת",
            font=("Segoe UI", 11),
            text_color="#e0f2fe"
        ).pack()

        # ------------------ טופס בקשה ------------------
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#0f172a", corner_radius=15)
        form_frame.pack(fill="both", expand=True, padx=15, pady=10)

        def add_label(text):
            ctk.CTkLabel(
                form_frame, 
                text=text, 
                font=("Segoe UI", 11, "bold"), 
                text_color="#cbd5e1",
                anchor="e"
            ).pack(fill="x", pady=(10, 2), padx=5)

        add_label("ת.ז. של התלמיד/ה")
        ctk.CTkEntry(
            form_frame, 
            font=("Segoe UI", 12), 
            textvariable=student_id_var,
            fg_color="#1e293b",
            border_color="#334155",
            text_color="white",
            justify="right"
        ).pack(fill="x", ipady=2, padx=5)

        add_label("ת.ז. שלך (ההורה)")
        ctk.CTkEntry(
            form_frame, 
            font=("Segoe UI", 12), 
            textvariable=parent_id_var,
            fg_color="#1e293b",
            border_color="#334155",
            text_color="white",
            justify="right"
        ).pack(fill="x", ipady=2, padx=5)

        add_label("יום השחרור")
        ctk.CTkComboBox(
            form_frame,
            values=["יום ראשון", "יום שני", "יום שלישי", "יום רביעי", "יום חמישי"],
            font=("Segoe UI", 12),
            dropdown_font=("Segoe UI", 12),
            variable=day_var,
            fg_color="#1e293b",
            border_color="#334155",
            button_color="#3b82f6",
            text_color="white",
            justify="right"
        ).pack(fill="x", padx=5)

        add_label("שעה")
        ctk.CTkComboBox(
            form_frame,
            values=[
                "9:00", "9:30", "10:00", "10:30",
                "11:00", "11:30", "12:00", "12:30",
                "13:00", "13:30", "14:00", "14:30",
                "15:00", "15:30", "16:00"
            ],
            font=("Segoe UI", 12),
            dropdown_font=("Segoe UI", 12),
            variable=hour_var,
            fg_color="#1e293b",
            border_color="#334155",
            button_color="#3b82f6",
            text_color="white",
            justify="right"
        ).pack(fill="x", padx=5)

        add_label("סיבה / הערה")
        ctk.CTkEntry(
            form_frame, 
            font=("Segoe UI", 12), 
            textvariable=reason_var,
            fg_color="#1e293b",
            border_color="#334155",
            text_color="white",
            justify="right"
        ).pack(fill="x", ipady=2, padx=5)

        ctk.CTkLabel(
            form_frame,
            text="בלחיצה על הכפתור הנך מאשר/ת את תנאי השימוש והמדיניות",
            font=("Segoe UI", 9),
            text_color="#64748b",
            wraplength=380,
            justify="center"
        ).pack(pady=15)

        def freer_completed():
            nonlocal student_id_var, parent_id_var, day_var, hour_var, reason_var
            global current_user_role, current_user_class

            if current_user_role not in ["teacher", "student"]:
                show_custom_message(None, "שגיאה", "הירשם כדי להשתמש או לראות את פיצ'ר זה")
                return
            
            s_id = str(student_id_var.get()).strip()
            p_id = str(parent_id_var.get()).strip()
            s_day = str(day_var.get()).strip()
            s_hour = str(hour_var.get()).strip()
            s_reason = str(reason_var.get()).strip()

            if hasattr(current_user_class, 'get'):
                u_class = current_user_class.get()
            else:  
                u_class = str(current_user_class)   

            if not s_id or not p_id or not s_day or not s_hour or not s_reason:
                show_custom_message(None, "שגיאה", "בבקשה תמלא את כל הפרטים בטופס")
                return

            SERVER_IP = '127.0.0.1'
            PORT = 9999

            try:
                with create_secure_socket() as s:
                    s.connect((SERVER_IP, PORT))
                    
                    subject = f"freer premition|{s_id}|{s_hour}|{s_day}|{s_reason}|{u_class}"
                    s.sendall(subject.encode('utf-8'))

                    while True:
                        raw_data = s.recv(1024)
                        if not raw_data:
                            break

                        dataFromServer = raw_data.decode('utf-8').strip()

                        if dataFromServer == "200 ok":
                            show_custom_message(None, "הצלחה!", "בקשת השיחרור נשלחה בהצלחה ומחכה לאישור המחנך")
                            break
                        else:
                            show_custom_message(None, "שגיאה!", "תקלה בשליחת בקשת שיחרור, אנא נסה שוב")
                            break

            except ConnectionRefusedError:
                show_custom_message(None, "שגיאה", "לא ניתן להתחבר לשרת. וודא שהוא פועל.")
            except Exception as e:
                show_custom_message(None, "שגיאה", f"אירעה שגיאה: {e}")

        ctk.CTkButton(
            form_frame,
            text="שלח בקשת שחרור",
            command=freer_completed,
            font=("Segoe UI", 12, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            corner_radius=10,
            height=42
        ).pack(fill="x", padx=5, pady=(0, 10))

        # ------------------ פוטר חזרה ------------------
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(5, 15))

        ctk.CTkButton(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Segoe UI", 12, "bold"),
            fg_color="#475569",
            hover_color="#334155",
            corner_radius=10,
            height=38
        ).pack(fill="x")
        
    def open_marechet():
        global current_username, current_user_class

        new_win = ctk.CTkToplevel()
        new_win.overrideredirect(True)

        destroy_and_set_new_window(new_win)
        new_win.title("מערכת שעות")

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a") # רקע כהה ראשי

        try:
            with open("data/schedules_z_to_yb.json", "r", encoding="utf-8") as f:
                schedule_data = json.load(f)
        except Exception as e:
            show_custom_message(None, "שגיאה", f"שגיאה בטעינת המערכת: {e}")
            return

        # פריים ראשי - הגדרת הגודל מתבצעת בבנאי (Constructor)
        main_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=20, width=480, height=730)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        # ------------------ כותרת ------------------
        header_frame = ctk.CTkFrame(main_frame, fg_color="#3b82f6", corner_radius=15, height=130)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="📅 מערכת שעות",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(pady=(25, 2))

        ctk.CTkLabel(
            header_frame,
            text="צפייה במערכת השבועית לפי יום וכיתה",
            font=("Segoe UI", 11),
            text_color="#e0f2fe"
        ).pack()

        # ------------------ סרגל בחירה ------------------
        selector_frame = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=12)
        selector_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            selector_frame,
            text="בחר יום וכיתה:",
            font=("Segoe UI", 12, "bold"),
            text_color="#f8fafc"
        ).pack(side="right", padx=12, pady=10)

        class_cb = ctk.CTkComboBox(
            selector_frame,
            values=list(schedule_data.keys()),
            font=("Segoe UI", 11),
            dropdown_font=("Segoe UI", 11),
            width=100,
            fg_color="#1e293b",
            border_color="#334155",
            button_color="#3b82f6",
            text_color="white",
            justify="center"
        )
        class_cb.pack(side="right", padx=5, pady=10)

        day_cb = ctk.CTkComboBox(
            selector_frame,
            values=["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"],
            font=("Segoe UI", 11),
            dropdown_font=("Segoe UI", 11),
            width=100,
            fg_color="#1e293b",
            border_color="#334155",
            button_color="#3b82f6",
            text_color="white",
            justify="center"
        )
        day_cb.pack(side="right", padx=5, pady=10)

        # ברירת מחדל: כיתת המשתמש + היום הנוכחי בשבוע
        hebrew_days = {6: "ראשון", 0: "שני", 1: "שלישי", 2: "רביעי", 3: "חמישי", 4: "שישי"}
        today_name = hebrew_days.get(datetime.datetime.now().weekday(), "ראשון")

        user_class_str = current_user_class.get() if hasattr(current_user_class, 'get') else str(current_user_class)

        if user_class_str in schedule_data:
            class_cb.set(user_class_str)
        elif schedule_data:
            class_cb.set(list(schedule_data.keys())[0])

        day_cb.set(today_name)

        # ------------------ רשימת שיעורים נגללת ------------------
        scrollable_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color="#0f172a",
            corner_radius=15,
            scrollbar_button_color="#334155"
        )
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=10)

        def refresh_schedule(choice=None):
            # ניקוי הווידג'טים הקודמים
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            selected_class = class_cb.get()
            selected_day = day_cb.get()

            if not selected_class or not selected_day:
                return

            lessons = schedule_data.get(selected_class, {}).get(selected_day, [])

            if not lessons:
                ctk.CTkLabel(
                    scrollable_frame,
                    text="אין לימודים ביום זה 🎉",
                    font=("Segoe UI", 13),
                    text_color="#94a3b8"
                ).pack(pady=30)
                return

            for lesson in lessons:
                lesson_card = ctk.CTkFrame(
                    scrollable_frame,
                    fg_color="#1e293b",
                    border_color="#334155",
                    border_width=1,
                    corner_radius=10
                )
                lesson_card.pack(fill="x", pady=4, padx=5, ipady=4)

                ctk.CTkLabel(
                    lesson_card,
                    text=lesson,
                    font=("Segoe UI", 12, "bold"),
                    text_color="#f8fafc",
                    anchor="e"
                ).pack(fill="x", padx=15, pady=8)

        # חיבור האירוע של שינוי הבחירה בתיבות הבחירה
        class_cb.configure(command=refresh_schedule)
        day_cb.configure(command=refresh_schedule)

        refresh_schedule()

        # ------------------ פוטר חזרה ------------------
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(5, 15))

        ctk.CTkButton(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Segoe UI", 12, "bold"),
            fg_color="#475569",
            hover_color="#334155",
            corner_radius=10,
            height=38
        ).pack(fill="x")


    def open_moodle_tasks():
        global current_username, current_user_role, current_user_class

        role = current_user_role if 'current_user_role' in globals() else "student"
        username = current_username if 'current_username' in globals() else "תלמיד"
        class_name = current_user_class if 'current_user_class' in globals() else "9th3"

        SERVER_IP = '127.0.0.1'
        PORT = 9999
        fetched_tasks = []

        # ---------------------------------------------------------
        # שלב א': שליפת הנתונים מהשרת
        # ---------------------------------------------------------
        try:
            with create_secure_socket() as s:
                s.connect((SERVER_IP, PORT))
                request_msg = f"get_moodle_tasks|{class_name}|{username}|{role}"
                s.sendall(request_msg.encode('utf-8'))

                raw_data = s.recv(4096)
                if raw_data:
                    dataFromServer = raw_data.decode('utf-8').strip()
                    if dataFromServer.startswith("get_moodle_tasks_response|success|"):
                        json_str = dataFromServer.split("|", 2)[2]
                        fetched_tasks = json.loads(json_str)
        except Exception as e:
            print(f"גילוי שגיאה בטעינת נתונים: {e}")

        # ---------------------------------------------------------
        # שלב ב': בניית ממשק המשתמש (UI)
        # ---------------------------------------------------------
        new_win = ctk.CTkToplevel()
        new_win.title("מרכז משימות ולמידה דיגיטלית")
        destroy_and_set_new_window(new_win)
        new_win.overrideredirect(True)

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a") # רקע כהה ראשי

        main_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=20, width=480, height=730)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        # ---------- כותרת (Header) ----------
        header_frame = ctk.CTkFrame(main_frame, fg_color="#3b82f6", corner_radius=15, height=130)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)

        is_teacher = "teacher" in str(role) or "מורה" in str(role)
        title_text = "🎓 ניהול והעלאת משימות" if is_teacher else "🎓 משימות ומטלות פתוחות"

        ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(pady=(25, 2))

        ctk.CTkLabel(
            header_frame,
            text=f"שלום {username}  •  כיתה {class_name}",
            font=("Segoe UI", 11),
            text_color="#e0f2fe"
        ).pack()

        # ---------- אזור תוכן נגלל (Scrollable Frame) ----------
        scrollable_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color="#0f172a",
            corner_radius=15,
            scrollbar_button_color="#334155"
        )
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # ---------- תצוגת מורה (Teacher View) ----------
        if is_teacher:
            form_card = ctk.CTkFrame(scrollable_frame, fg_color="#1e293b", corner_radius=12, border_color="#334155", border_width=1)
            form_card.pack(fill="x", pady=6, padx=5, ipady=10)

            ctk.CTkLabel(
                form_card,
                text="יצירת משימה חדשה לכיתה",
                font=("Segoe UI", 13, "bold"),
                text_color="#60a5fa"
            ).pack(anchor="e", padx=18, pady=(12, 8))

            ctk.CTkLabel(
                form_card,
                text=":שם המשימה / נושא הלימוד",
                font=("Segoe UI", 10),
                text_color="#94a3b8"
            ).pack(anchor="e", padx=18)

            task_name_entry = ctk.CTkEntry(
                form_card,
                font=("Segoe UI", 12),
                fg_color="#0f172a",
                border_color="#334155",
                text_color="white",
                justify="right"
            )
            task_name_entry.pack(fill="x", padx=18, pady=(2, 10))

            ctk.CTkLabel(
                form_card,
                text=":(Moodle / קישור למטלה (אופק / סרטון",
                font=("Segoe UI", 10),
                text_color="#94a3b8"
            ).pack(anchor="e", padx=18)

            task_url_entry = ctk.CTkEntry(
                form_card,
                font=("Segoe UI", 11),
                fg_color="#0f172a",
                border_color="#334155",
                text_color="white",
                justify="left"
            )
            task_url_entry.insert(0, "https://")
            task_url_entry.pack(fill="x", padx=18, pady=(2, 14))

            def publish_task():
                name = task_name_entry.get().strip()
                url = task_url_entry.get().strip()
                if not name or url == "https://" or not url:
                    show_custom_message(None, "שדה חסר", "אנא מלא שם משימה וקישור תקין")
                    return

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        subject = f"publish_moodle_task|{class_name}|{url}|{name}"
                        s.sendall(subject.encode('utf-8'))

                        while True:
                            raw_data = s.recv(1024)
                            if not raw_data:
                                break
                            dataFromServer = raw_data.decode('utf-8').strip()

                            if dataFromServer.startswith("publish_moodle_task_response|"):
                                parts = dataFromServer.split("|")
                                if len(parts) > 1 and parts[1] == "success":
                                    show_custom_message(None, "משימה פורסמה", f"המשימה '{name}' פורסמה בהצלחה!")
                                    new_win.destroy()
                                    open_moodle_tasks()
                                else:
                                    show_custom_message(None, "שגיאה", "השרת נתקל בשגיאה בעת שמירת המשימה.")
                                break
                except Exception as e:
                    show_custom_message(None, "שגיאה", f"אירעה שגיאה בתקשורת: {e}")

            publish_btn = ctk.CTkButton(
                form_card,
                text="➕  פרסם קישור למשימה",
                font=("Segoe UI", 12, "bold"),
                fg_color="#10b981",
                hover_color="#059669",
                height=36,
                command=publish_task
            )
            publish_btn.pack(fill="x", padx=18, pady=(5, 5))

            ctk.CTkLabel(
                scrollable_frame,
                text=":משימות פעילות כרגע בכיתה",
                font=("Segoe UI", 12, "bold"),
                text_color="#f8fafc"
            ).pack(anchor="e", padx=5, pady=(15, 5))

            if not fetched_tasks:
                ctk.CTkLabel(
                    scrollable_frame,
                    text="אין משימות פעילות כרגע",
                    font=("Segoe UI", 10),
                    text_color="#94a3b8"
                ).pack(anchor="e", padx=5, pady=10)

            for task in fetched_tasks:
                t_name = task.get("name", "משימה ללא שם")
                t_url = task.get("url", "#")

                row = ctk.CTkFrame(scrollable_frame, fg_color="#1e293b", corner_radius=10, border_color="#334155", border_width=1)
                row.pack(fill="x", pady=4, padx=5)

                inner = ctk.CTkFrame(row, fg_color="transparent")
                inner.pack(fill="x", padx=12, pady=8)

                ctk.CTkButton(
                    inner,
                    text="🔗 פתח קישור",
                    font=("Segoe UI", 10, "bold"),
                    fg_color="#2563eb",
                    hover_color="#1d4ed8",
                    width=90,
                    height=28,
                    command=lambda url=t_url: webbrowser.open(url)
                ).pack(side="left")

                ctk.CTkLabel(
                    inner,
                    text=f"• {t_name}",
                    font=("Segoe UI", 11, "bold"),
                    text_color="#f8fafc"
                ).pack(side="right")

        # ---------- תצוגת תלמיד (Student View) ----------
        else:
            total_tasks = len(fetched_tasks)
            completed_tasks = sum(1 for t in fetched_tasks if t.get("status") == "✅ בוצע")
            pct_float = (completed_tasks / total_tasks) if total_tasks > 0 else 1.0
            pct_int = int(pct_float * 100)

            progress_card = ctk.CTkFrame(scrollable_frame, fg_color="#1e293b", corner_radius=12, border_color="#334155", border_width=1)
            progress_card.pack(fill="x", pady=6, padx=5, ipady=8)

            ctk.CTkLabel(
                progress_card,
                text=f"📈 הספק המשימות: {completed_tasks} מתוך {total_tasks} בוצעו ({pct_int}%)",
                font=("Segoe UI", 11, "bold"),
                text_color="#4ade80"
            ).pack(anchor="e", padx=15, pady=(8, 8))

            progress_bar = ctk.CTkProgressBar(
                progress_card,
                fg_color="#0f172a",
                progress_color="#10b981",
                height=10
            )
            progress_bar.pack(fill="x", padx=15, pady=(0, 8))
            progress_bar.set(pct_float)

            ctk.CTkLabel(
                scrollable_frame,
                text=":רשימת קישורים ומטלות לביצוע",
                font=("Segoe UI", 12, "bold"),
                text_color="#f8fafc"
            ).pack(anchor="e", padx=5, pady=(10, 5))

            def toggle_status(btn, task_obj):
                if btn.cget("text") == "❌ לא בוצע":
                    btn.configure(text="✅ בוצע", fg_color="#10b981", hover_color="#059669")
                    task_obj["status"] = "✅ בוצע"
                else:
                    btn.configure(text="❌ לא בוצע", fg_color="#f43f5e", hover_color="#e11d48")
                    task_obj["status"] = "❌ לא בוצע"

            if not fetched_tasks:
                ctk.CTkLabel(
                    scrollable_frame,
                    text="אין משימות כרגע 🎉",
                    font=("Segoe UI", 10),
                    text_color="#94a3b8"
                ).pack(anchor="e", padx=5, pady=10)

            for task in fetched_tasks:
                title = task.get("name", "משימה כללית")
                link_url = task.get("url", "#")
                start_status = task.get("status", "❌ לא בוצע")
                start_color = "#10b981" if start_status == "✅ בוצע" else "#f43f5e"
                hover_color = "#059669" if start_status == "✅ בוצע" else "#e11d48"

                row = ctk.CTkFrame(scrollable_frame, fg_color="#1e293b", corner_radius=10, border_color="#334155", border_width=1)
                row.pack(fill="x", pady=4, padx=5)

                inner = ctk.CTkFrame(row, fg_color="transparent")
                inner.pack(fill="x", padx=12, pady=8)

                btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
                btn_frame.pack(side="left")

                status_btn = ctk.CTkButton(
                    btn_frame,
                    text=start_status,
                    font=("Segoe UI", 9, "bold"),
                    fg_color=start_color,
                    hover_color=hover_color,
                    width=80,
                    height=28
                )
                status_btn.configure(command=lambda b=status_btn, t=task: toggle_status(b, t))
                status_btn.pack(side="left", padx=(0, 5))

                ctk.CTkButton(
                    btn_frame,
                    text="🔗 פתח",
                    font=("Segoe UI", 9, "bold"),
                    fg_color="#2563eb",
                    hover_color="#1d4ed8",
                    width=65,
                    height=28,
                    command=lambda url=link_url: webbrowser.open(url)
                ).pack(side="left")

                ctk.CTkLabel(
                    inner,
                    text=title,
                    font=("Segoe UI", 11, "bold"),
                    text_color="#f8fafc"
                ).pack(side="right", padx=5)

        # ---------- פוטר חזרה (Footer) ----------
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(5, 15))

        ctk.CTkButton(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Segoe UI", 12, "bold"),
            fg_color="#475569",
            hover_color="#334155",
            corner_radius=10,
            height=38
        ).pack(fill="x")
    
    def open_attendance():
        global current_username, current_user_role, current_user_class

        SERVER_IP = '127.0.0.1'
        PORT = 9999
        
        class_students = []
        try:
            with create_secure_socket() as s:
                print(f"Connecting to {SERVER_IP}:{PORT}...")
                s.connect((SERVER_IP, PORT))
                
                subject = f"get_class_students|{current_user_class}"
                s.sendall(subject.encode('utf-8'))

                while True:
                    raw_data = s.recv(1024)
                    if not raw_data:
                        break

                    dataFromServer = raw_data.decode('utf-8').strip()

                    if dataFromServer.startswith("class_students_response|"):
                        parts = dataFromServer.split("|")
                        if len(parts) > 1 and parts[1]:
                            class_students = parts[1].split(",")
                        break
                    else:
                        show_custom_message(None, "שגיאה!", "שגיאת שרת")
                        break

        except ConnectionRefusedError:
            show_custom_message(None, "שגיאה", "לא ניתן להתחבר לשרת. וודא שהוא פועל.")
        except Exception as e:
            show_custom_message(None, "שגיאה", f"אירעה שגיאה: {e}")
        
        role = current_user_role if 'current_user_role' in globals() else "student"
        username = current_username if 'current_username' in globals() else "תלמיד"

        new_win = ctk.CTkToplevel()
        new_win.title("מערכת נוכחות - משוב")
        new_win.overrideredirect(True)

        destroy_and_set_new_window(new_win)

        width, height = 550, 750
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(fg_color="#0f172a") # רקע כהה ראשי

        main_frame = ctk.CTkFrame(new_win, fg_color="#1e293b", corner_radius=20, width=510, height=710)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.pack_propagate(False)

        is_teacher = "teacher" in str(role) or "מורה" in str(role)
        header_color = "#0284c7" if is_teacher else "#0ea5e9"

        # ---------- Header ----------
        header_frame = ctk.CTkFrame(main_frame, fg_color=header_color, corner_radius=15, height=120)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)

        title_text = "📝 ניהול נוכחות כיתתית" if is_teacher else "📝 מצב נוכחות אישי"
        ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(pady=(22, 2))

        ctk.CTkLabel(
            header_frame,
            text=f"משתמש מחובר: {username}",
            font=("Segoe UI", 11),
            text_color="#e0f2fe"
        ).pack()

        subjects_list = [
            "שיעור מתמטיקה", "שיעור נביא", "שיעור גמרא", "שיעור אנגלית", 
            "שיעור עברית", "שיעור לשון", "שיעור היסטוריה", "שיעור מדעים", 
            "שיעור תורה", "שיעור ספורט"
        ]

        # =========================================================
        #                    תצוגת מורה (TEACHER)
        # =========================================================
        if is_teacher:
            class_frame = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=12)
            class_frame.pack(fill="x", padx=15, pady=5)
            
            ctk.CTkLabel(
                class_frame, 
                text=":בחר מקצוע", 
                font=("Segoe UI", 12, "bold"), 
                text_color="#f8fafc"
            ).pack(side="right", padx=(10, 15), pady=8)

            teacher_subject_var = ctk.StringVar(value=subjects_list[0])
            subject_dropdown = ctk.CTkComboBox(
                class_frame, 
                values=subjects_list,
                variable=teacher_subject_var,
                font=("Segoe UI", 11),
                dropdown_font=("Segoe UI", 11),
                width=150,
                fg_color="#1e293b",
                border_color="#334155",
                button_color="#0284c7",
                text_color="white",
                justify="center"
            )
            subject_dropdown.pack(side="right", padx=5, pady=8)

            # אזור גלילה לתלמידים
            scroll_students = ctk.CTkScrollableFrame(
                main_frame,
                fg_color="#0f172a",
                corner_radius=12,
                scrollbar_button_color="#334155"
            )
            scroll_students.pack(fill="both", expand=True, padx=15, pady=10)

            students = class_students if class_students else ["אין תלמידים משוייכים"]
            attendance_vars = {}

            for student_name in students:
                row_card = ctk.CTkFrame(scroll_students, fg_color="#1e293b", corner_radius=10, border_color="#334155", border_width=1)
                row_card.pack(fill="x", pady=4, padx=5)

                ctk.CTkLabel(
                    row_card, 
                    text=student_name, 
                    font=("Segoe UI", 12, "bold"), 
                    text_color="#f8fafc"
                ).pack(side="right", padx=12, pady=8)

                status_var = ctk.StringVar(value="נוכח")
                attendance_vars[student_name] = status_var

                # כפתור סגמנטציוני (Segmented Button) לבחירת סטטוס מהירה
                seg_btn = ctk.CTkSegmentedButton(
                    row_card,
                    values=["חוסר ציוד", "חיסור", "איחור", "נוכח"],
                    variable=status_var,
                    font=("Segoe UI", 9, "bold"),
                    selected_color="#0284c7",
                    selected_hover_color="#0369a1",
                    unselected_color="#0f172a",
                    unselected_hover_color="#334155",
                    text_color="white"
                )
                seg_btn.pack(side="left", padx=8, pady=8)

            def save_attendance_action():
                selected_sub = teacher_subject_var.get()
                
                class_map = {
                    "ז1": "7th1", "ז2": "7th2", "ז3": "7th3", "ז4": "7th4", "ז5": "7th5", "ז6": "7th6",
                    "ח1": "8th1", "ח2": "8th2", "ח3": "8th3", "ח4": "8th4", "ח5": "8th5", "ח6": "8th6",
                    "ט1": "9th1", "ט2": "9th2", "ט3": "9th3", "ט4": "9th4", "ט5": "9th5", "ט6": "9th6",
                    "י1": "10th1", "י2": "10th2", "י3": "10th3", "י4": "10th4", "י5": "10th5", "י6": "10th6",
                    "יא1": "11th1", "יא2": "11th2", "יא3": "11th3", "יא4": "11th4", "יא5": "11th5", "יא6": "11th6",
                    "יב1": "12th1", "יב2": "12th2", "יב3": "12th3", "יב4": "12th4", "יב5": "12th5", "יב6": "12th6"
                }
                server_class_name = class_map.get(current_user_class, current_user_class)
                
                attendance_records = [f"{s_name}:{s_var.get()}" for s_name, s_var in attendance_vars.items()]
                attendance_data_str = ",".join(attendance_records)
                
                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        msg = f"save_attendance|{server_class_name}|{selected_sub}|{attendance_data_str}"
                        s.sendall(msg.encode('utf-8'))
                        
                        raw_response = s.recv(1024)
                        if raw_response:
                            response = raw_response.decode('utf-8').strip()
                            if response == "save_attendance_response|success":
                                show_custom_message(None, "הצלחה", f"יומן הנוכחות עבור שיעור {selected_sub} נשמר בהצלחה בשרת!")
                            else:
                                show_custom_message(None, "שגיאה", "השרת נכשל בשמירת הנתונים בקובץ.")
                        else:
                            show_custom_message(None, "שגיאה", "לא התקבלה תגובה מהשרת.")
                except Exception as e:
                    show_custom_message(None, "שגיאה", f"שגיאת תקשורת עם השרת: {e}")

            # כפתורי תחתית למורה
            footer_btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            footer_btn_frame.pack(fill="x", padx=15, pady=(5, 15))

            ctk.CTkButton(
                footer_btn_frame,
                text="💾 שמור נוכחות ביומן",
                font=("Segoe UI", 12, "bold"),
                fg_color="#0284c7",
                hover_color="#0369a1",
                height=38,
                command=save_attendance_action
            ).pack(fill="x", pady=(0, 6))

            ctk.CTkButton(
                footer_btn_frame,
                text="חזרה למסך ראשי",
                command=lambda: open_main_page(current_username),
                font=("Segoe UI", 12, "bold"),
                fg_color="#475569",
                hover_color="#334155",
                height=36
            ).pack(fill="x")

        # =========================================================
        #                    תצוגת תלמיד (STUDENT)
        # =========================================================
        else:
            # כרטיסיות סטטיסטיקה
            stats_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            stats_frame.pack(fill="x", padx=12, pady=5)
            stats_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="equal")

            cards_data = [
                ("נוכחות", "92%", "#0369a1", "#e0f2fe"),
                ("איחורים", "2", "#b45309", "#fef3c7"),
                ("חיסורים", "1", "#b91c1c", "#fee2e2"),
                ("חוסר ציוד", "3", "#6b21a8", "#f3e8ff"), 
                ("מוצדק", "2", "#334155", "#f1f5f9")
            ]

            for i, (label, val, bg_c, text_c) in enumerate(cards_data):
                card = ctk.CTkFrame(stats_frame, fg_color=bg_c, corner_radius=10, height=65)
                card.grid(row=0, column=i, padx=2)
                card.pack_propagate(False)

                ctk.CTkLabel(card, text=val, font=("Segoe UI", 15, "bold"), text_color=text_c).pack(pady=(8, 0))
                ctk.CTkLabel(card, text=label, font=("Segoe UI", 9, "bold"), text_color=text_c).pack()

            # סרגל סינון
            filter_frame = ctk.CTkFrame(main_frame, fg_color="#0f172a", corner_radius=10)
            filter_frame.pack(fill="x", padx=15, pady=(10, 5))

            ctk.CTkLabel(
                filter_frame, 
                text="היסטוריית אירועים", 
                font=("Segoe UI", 12, "bold"), 
                text_color="#f8fafc"
            ).pack(side="right", padx=12, pady=8)

            student_filter_var = ctk.StringVar(value="הכול")
            filter_dropdown = ctk.CTkComboBox(
                filter_frame, 
                variable=student_filter_var, 
                values=["הכול"] + subjects_list,
                font=("Segoe UI", 10),
                dropdown_font=("Segoe UI", 10),
                width=120,
                fg_color="#1e293b",
                border_color="#334155",
                button_color="#0ea5e9",
                text_color="white",
                justify="center"
            )
            filter_dropdown.pack(side="left", padx=10, pady=8)

            history_scroll = ctk.CTkScrollableFrame(
                main_frame,
                fg_color="#0f172a",
                corner_radius=12,
                scrollbar_button_color="#334155"
            )
            history_scroll.pack(fill="both", expand=True, padx=15, pady=8)

            history_events = []

            try:
                with create_secure_socket() as s:
                    s.connect((SERVER_IP, PORT))
                    msg = f"get_attendance_history|{current_user_class}|{current_username}"
                    s.sendall(msg.encode('utf-8'))
                    
                    raw_response = s.recv(4096) 
                    if raw_response:
                        response = raw_response.decode('utf-8').strip()
                        parts = response.split("|")
                        
                        if len(parts) >= 3 and parts[0] == "get_attendance_response":
                            if parts[1] == "SUCCESS":
                                parts_limited = response.split("|", 2)
                                history_events = json.loads(parts_limited[2])
                            elif parts[1] == "ERROR":
                                show_custom_message(None, "שגיאה", f"שגיאת שרת: {parts[2]}")
                        elif len(parts) >= 2 and parts[0] == "get_attendance_response":
                            parts_limited = response.split("|", 1)
                            history_events = json.loads(parts_limited[1])
                        elif parts[0] == "SUCCESS":
                            parts_limited = response.split("|", 1)
                            history_events = json.loads(parts_limited[1])
                        else:
                            try:
                                history_events = json.loads(response)
                            except json.JSONDecodeError:
                                pass
            except Exception as e:
                print(f"Error fetching attendance history: {e}")

            def update_filtered_history(choice=None):
                for widget in history_scroll.winfo_children():
                    widget.destroy()

                selected_filter = student_filter_var.get()

                if not history_events:
                    ctk.CTkLabel(
                        history_scroll,
                        text="אין נתוני נוכחות להצגה 🎉",
                        font=("Segoe UI", 11),
                        text_color="#94a3b8"
                    ).pack(pady=20)
                    return

                for event_data in history_events:
                    subject = event_data.get("subject", "שיעור כללי")
                    date = event_data.get("date", "")
                    status = event_data.get("status", "")
                    
                    if "חיסור" in status or "חוסר" in status:
                        status_color = "#f43f5e" 
                    elif "איחור" in status:
                        status_color = "#fbbf24" 
                    else:
                        status_color = "#34d399" 

                    if selected_filter == "הכול" or subject == selected_filter:
                        event_row = ctk.CTkFrame(history_scroll, fg_color="#1e293b", corner_radius=8, border_color="#334155", border_width=1)
                        event_row.pack(fill="x", padx=5, pady=3)

                        ctk.CTkLabel(
                            event_row, 
                            text=f"{subject}   •   {date}", 
                            font=("Segoe UI", 11), 
                            text_color="#f8fafc"
                        ).pack(side="right", padx=12, pady=6)

                        ctk.CTkLabel(
                            event_row, 
                            text=status, 
                            font=("Segoe UI", 11, "bold"), 
                            text_color=status_color
                        ).pack(side="left", padx=12, pady=6)

            filter_dropdown.configure(command=update_filtered_history)
            update_filtered_history()

            # פוטר תלמיד
            footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            footer_frame.pack(fill="x", padx=15, pady=(5, 15))

            ctk.CTkButton(
                footer_frame,
                text="חזרה למסך ראשי",
                command=lambda: open_main_page(current_username),
                font=("Segoe UI", 12, "bold"),
                fg_color="#475569",
                hover_color="#334155",
                height=38
            ).pack(fill="x")
        
    
    if __name__ == "__main__":
        open_splash_screen()
        

except KeyboardInterrupt:
    print("Keyboard Interrupt. QUITING!")
except ModuleNotFoundError:
    print(f"module not found")
except ConnectionAbortedError:
    print("connection abborted")
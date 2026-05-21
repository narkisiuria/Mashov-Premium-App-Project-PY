
try: 
    import datetime
    import ssl
    import socket
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk
    import json
    import os
    import webbrowser
    import random
    from utils import hashingAlg
    from tkinter import simpledialog
    
    root = tk.Tk()
    root.withdraw() 
    entry_username = None
    entry_password = None

    print("reciving dataFromServer...")
    print("loading app...")
    print("importing assets...")

    current_toplevel_win = None
    current_username = ""
    current_user_role = ""
    current_user_class = ""
    splash_root = None
    
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
        splash_root = tk.Tk()
        splash_root.overrideredirect(True)
        
        width, height = 520, 770 
        splash_root.geometry(f"{width}x{height}")
        splash_root.configure(bg="#f0f4f8") 

        main_frame = tk.Frame(splash_root,
                              bg="white", bd=0)
        
        main_frame.place(relx=0.5,
                         rely=0.5,
                         anchor="center",
                         width=520,
                         height=770)

        header_frame = tk.Frame(main_frame,
                                bg="#1a73e8",
                                height=220)
        
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="📊",
                 font=("Arial", 55), 
                 fg="white",
                 bg="#1a73e8").pack(pady=(40, 0))
        
        tk.Label(header_frame,
                 text="מערכת משוב",
                 font=("Arial",
                       36,
                       "bold"),
                 fg="white",
                 bg="#1a73e8").pack()
        
        tk.Label(header_frame,
                 text="הדרך החכמה לנהל את הלימודים",
                 font=("Arial", 12),
                 fg="#bbdefb",
                 bg="#1a73e8").pack()

        content_frame = tk.Frame(main_frame,
                                 bg="white")
        
        content_frame.pack(fill="both",
                           expand=True, padx=50)

        tk.Label(content_frame,
                 text="ברוכים הבאים",
                 font=("Arial",
                       22,
                       "bold"),
                 fg="#202124",
                 bg="white").pack(pady=(40, 10))
        
        features_frame = tk.Frame(content_frame,
                                  bg="white")
        
        features_frame.pack(pady=30)

        features = [("🕒", 
                     "לו\"ז בזמן אמת"),
                    ("📝", "מעקב ציונים"),
                    ("✅", "ניהול משימות")]
        
        for icon, txt in features:
            f_row = tk.Frame(features_frame, bg="white")
            f_row.pack(side="left", padx=15)
            tk.Label(f_row, text=icon,
                     font=("Arial", 20),
                     bg="white").pack()
            
            tk.Label(f_row,
                     text=txt,
                     font=("Arial", 10, "bold"),
                     fg="#5f6368",
                     bg="white").pack()

        btn_frame = tk.Frame(content_frame, bg="white")
        btn_frame.pack(fill="x", pady=20)

        login_btn = tk.Button(
            btn_frame,
            text="כניסה למערכת",
            font=("Arial", 16, "bold"),
            bg="#1a73e8",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=open_login_window
        )
        login_btn.pack(fill="x", ipady=15, pady=(0, 15))

        peak_btn = tk.Button(
            btn_frame,
            text="כניסה כאורח ",
            font=("Arial", 14),
            bg="white",
            fg="#1a73e8",
            highlightthickness=2,
            highlightbackground="#1a73e8",
            relief="flat",
            cursor="hand2",
            command=open_peak
        )
        peak_btn.pack(fill="x", ipady=14)

        footer_frame = tk.Frame(main_frame,
                                bg="#f8f9fa",
                                height=80)
        
        footer_frame.pack(side="bottom",
                          fill="x")
        
        footer_frame.pack_propagate(False)

        tk.Label(
            footer_frame, 
            text="פותח ע\"י אוריה נרקיסי • גרסה 1.0", 
            fg="#70757a", 
            bg="#f8f9fa", 
            font=("Arial", 10)
        ).pack(expand=True)

        splash_root.update_idletasks()
        w = splash_root.winfo_screenwidth()
        h = splash_root.winfo_screenheight()
        x = (w/2) - (width/2)
        y = (h/2) - (height/2)
        splash_root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        splash_root.mainloop()
        
    ###########################################################
    #                   מסך לוגין                   #
    ###########################################################

    def open_login_window():
        global splash_root
        if splash_root:
            splash_root.destroy()
        root.deiconify()  

    ###########################################################
    #                      עמוד ראשי               #
    ###########################################################

    def open_peak():
        global current_user_role
        messagebox.showwarning("אורח יקר", "בתור אורח אתה לא תוכל להשתמש בכל הפיצרים")
        
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
                    messagebox.showerror("שגיאה", "שגיאת שרת")
                    return
                    

        except ConnectionRefusedError:
            messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת. וודא שהוא פועל.")
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"אירעה שגיאה: {e}")

    def open_main_page(username):
        global current_username, current_user_role


        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        current_username = username

        new_win.title("עמוד ראשי")

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=730)

        header_frame = tk.Frame(main_frame, bg="#1a73e8", height=170)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🏠",
            font=("Arial", 42),
            fg="white",
            bg="#1a73e8"
        ).pack(pady=(15, 0))

        tk.Label(
            header_frame,
            text=f"שלום {username}",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1a73e8"
        ).pack()

        tk.Label(
            header_frame,
            text="?מה ברצונך לעשות",
            font=("Arial", 12),
            fg="#dbeafe",
            bg="#1a73e8"
        ).pack()

        content_frame = tk.Frame(main_frame, bg="white")
        content_frame.pack(expand=True, pady=40)

        button_style = {
            "fg": "white",
            "font": ("Arial", 14, "bold"),
            "width": 14,
            "height": 4,
            "bd": 0,
            "cursor": "hand2",
            "relief": "flat"
        }

        tk.Button(
            content_frame,
            text="מערכת שעות",
            bg="#1a73e8",
            command=open_marechet,
            **button_style
        ).grid(row=0, column=0, padx=15, pady=15)

        tk.Button(
            content_frame,
            text="דואר נכנס",
            bg="#2563eb",
            command=open_doar,
            **button_style
        ).grid(row=0, column=1, padx=15, pady=15)

        tk.Button(
            content_frame,
            text="ציונים שוטפים",
            bg="#3b82f6",
            command=open_grades,
            **button_style
        ).grid(row=1, column=0, padx=15, pady=15)

        tk.Button(
            content_frame,
            text="צאט כיתתי",
            bg="#60a5fa",
            command=open_class_chat_room,
            **button_style
        ).grid(row=1, column=1, padx=15, pady=15)
        
        tk.Button(
            content_frame,
            text="משימון",
            bg="#1d4ed8",
            command=open_todo_list,
            **button_style
        ).grid(row=2, column=0, padx=15, pady=15)

        tk.Button(
            content_frame,
            text="שיחרורון",
            bg="#0ea5e9",
            command=open_freer,
            **button_style
        ).grid(row=2, column=1, padx=15, pady=15)

        tk.Button(
            content_frame,
            text="🤖 עזרה והדרכה",
            bg="#7c3aed",
            command=open_chatbot_help,   
            fg="white",
            font=("Arial", 14, "bold"),
            width=30,
            height=4,
            bd=0,
            cursor="hand2",
            relief="flat"
        ).grid(row=3, column=0, columnspan=2, padx=0, pady=0)

        footer_frame = tk.Frame(main_frame, bg="#f8fafc", height=10)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        tk.Label(
            footer_frame,
            text="Mashov מערכת ניהול לימודים • גרסה 1.0",
            font=("Arial", 10),
            fg="#64748b",
            bg="#f8fafc"
        ).pack(expand=True)
            
        
    ###########################################################
    #                   פונקציית התחברות                    #
    ###########################################################

    def forgotPass():
        messagebox.showinfo(title="?שכחת את הסיסמה", message="שנה/י את סיסמתך במשרד המזכירות בבית הספר")


    def openPrivecyPolicy():
        webbrowser.open("privacy_policy.txt" )
        
    def open_login_window():
        global entry_username, entry_password, root, splash_root
        
        if splash_root is not None: 
            try:
                if splash_root.winfo_exists():
                    splash_root.destroy()
            except:
                pass
            
        login_win = tk.Toplevel(root)
        login_win.title("משוב / התחברות")
        
        destroy_and_set_new_window(login_win)

        width, height = 520, 770 
        x = (login_win.winfo_screenwidth() // 2) - (width // 2)
        y = (login_win.winfo_screenheight() // 2) - (height // 2)
        login_win.geometry(f"{width}x{height}+{x}+{y}")
        login_win.configure(bg="#f0f4f8")
        login_win.resizable(False, False)

        main_frame = tk.Frame(login_win,
                              bg="white",
                              bd=0)
        main_frame.place(relx=0.5,
                         rely=0.5,
                         anchor="center",
                         width=520, height=755)

        header_frame = tk.Frame(main_frame,
                                bg="#1a73e8",
                                height=160)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame,
                 text="🔒",
                 font=("Arial", 45),
                 fg="white",
                 bg="#1a73e8").pack(pady=(25, 0))
        tk.Label(header_frame,
                 text="משוב - מערכת עדכונים",
                 font=("Arial",
                       28,
                       "bold"),
                 fg="white",
                 bg="#1a73e8").pack()

        form_frame = tk.Frame(main_frame,
                              bg="white")
        form_frame.pack(fill="both",
                        expand=True,
                        padx=45,
                        pady=25)

        tk.Label(form_frame,
                 text="שם משתמש",
                 font=("Arial", 12, "bold"),
                 fg="#333333",
                 bg="white",
                 anchor="e").pack(fill="x",
                                  pady=(10, 5))
                 
        entry_username = tk.Entry(form_frame,
                                  font=("Arial", 16),
                                  bg="#f8f9fa",
                                  relief="solid",
                                  bd=1,
                                  justify="right")
        entry_username.pack(fill="x",
                            ipady=12)

        tk.Label(form_frame,
                 text="סיסמה",
                 font=("Arial", 12, "bold"),
                 fg="#333333",
                 bg="white",
                 anchor="e").pack(fill="x", pady=(20, 5))
        entry_password = tk.Entry(form_frame,
                                  font=("Arial", 16),
                                  bg="#f8f9fa",
                                  relief="solid",
                                  bd=1,
                                  show="●",
                                  justify="right")
        entry_password.pack(fill="x",
                            ipady=12)

        tk.Button(
            form_frame,
            text="התחברות למערכת",
            font=("Arial",
                  16, "bold"), fg="white", bg="#1a73e8",
            activebackground="#1557b0",
            relief="flat",
            cursor="hand2",
            command=attempt_login
        ).pack(fill="x",
               pady=(45, 15),
               ipady=15)

        nav_frame = tk.Frame(form_frame, bg="white")
        nav_frame.pack(pady=10)
        
        tk.Button(nav_frame, 
                  text="שכחת סיסמה",
                  font=("Arial", 14,
                        "bold"),
                  fg="#1a73e8",
                  bg="white",
                  bd=0,
                  cursor="hand2", 
                command=forgotPass).pack(side="right", padx=10)
        
        tk.Label(nav_frame,
                 text="|",
                 fg="#040404",
                 bg="white",
                 font=("Arial", 11)).pack(side="right")
        
        tk.Button(nav_frame,
                  text="יצירת חשבון חדש",
                  font=("Arial",
                        14, "bold"),
                  fg="#1a73e8",
                  bg="white",
                  bd=0,
                  cursor="hand2", 
                command=signUp).pack(side="right", padx=10)

        footer_frame = tk.Frame(main_frame,
                                bg="white")
        footer_frame.pack(side="bottom",
                          pady=2) 
        
        tk.Label(footer_frame,
                 text="בכניסה למערכת הנך מסכים לכל", 
                 font=("Arial", 11),
                 fg="#999999",
                 bg="white").pack()
        
        tk.Button(footer_frame,
                  text="תנאי השימוש ומדיניות הפרטיות שלנו", 
                  font=("Arial", 11, "underline"),
                  fg="#1a73e8", bg="white", 
                  bd=0,
                  cursor="hand2", 
                  command=lambda: webbrowser.open("https://www.mashov.info/privacypolicy/")).pack(pady=(0, 15))

        tk.Label(footer_frame,
                 text="📖",
                 fg="#1a73e8",
                 bg="white", 
                 font=("Arial", 50)).pack()    
        
        return login_win
    
    def ask_teacher_code(username):
        code_win = tk.Toplevel(root)
        code_win.title("אימות מורה")

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
                        messagebox.showerror("שגיאה", "יותר מידי ניסיונות, במידה ושכחת את הסיסמה שלך אז לחץ על שכחת את הסיסמה")
                        exit()
                
                else:
                    messagebox.showerror("שגיאה", "שם משתמש או סיסמה שגויים")
                    print("unsuccessful")

        except ConnectionRefusedError:
            messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת. וודא שהוא פועל.")
        except Exception as e:
            messagebox.showerror("שגיאה", f"אירעה שגיאה: {e}")
        
    def signUp():       
        def attemptSignUp():
            all_entries = [firstName, lastName, gmail, newUsername, newPassword]
            role = role_box.get()

            if any(entry.get().strip() == "" for entry in all_entries):
                messagebox.showerror("שגיאה", "נא למלא את כל השדות")
                return

            if class_box.get().strip() == "":
                messagebox.showerror("שגיאה", "נא לבחור כיתה")
                return

            if role_box.get().strip() == "":
                messagebox.showerror("שגיאה", "נא לבחור תפקיד")
                return

            if "@" not in gmail.get():
                messagebox.showerror("שגיאה", "אימייל לא תקין")
                return

            if gmail.get().startswith("@") or gmail.get().endswith("@"):
                messagebox.showerror("שגיאה", "אימייל לא תקין")
                return

            if firstName.get().isdigit() or lastName.get().isdigit():
                messagebox.showerror("שגיאה", "שם לא יכול להיות מספר")
                return
            
            if role == "teacher":
                open_teacher_setup(newUsername.get())
            
            if role == "student":
                open_student_setup(newUsername.get())


        def open_teacher_setup(username):
            win = tk.Toplevel(root)
            destroy_and_set_new_window(win)

            win.title("הגדרת מורה")
            width, height = 520, 770
            screen_width = win.winfo_screenwidth()
            screen_height = win.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            win.geometry(f"{width}x{height}+{x}+{y}")
            win.configure(bg="#f0f4f8")

            frame = tk.Frame(win, bg="white")
            frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=450)

            tk.Label(frame, text="🔑", font=("Arial", 40), bg="white", fg="#1a73e8").pack(pady=10)

            tk.Label(frame, text="אימות מורה", font=("Arial", 22, "bold"), bg="white").pack()

            tk.Label(frame, text="קוד מורים", bg="white").pack(pady=(20,5))
            teacher_code = tk.Entry(frame, show="*")
            teacher_code.pack(ipady=8, fill="x", padx=40)

            tk.Label(frame, text="קוד כיתה (לשיתוף)", bg="white").pack(pady=(20,5))
            class_code = tk.Entry(frame)
            class_code.pack(ipady=8, fill="x", padx=40)

            def submit():
                teachers_code = teacher_code.get()
                new_class_code = class_code.get()

                if not teacher_code or not class_code:
                    return

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        print(f"Connecting to {SERVER_IP}:{PORT}...")
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
                            f"{class_code.get()}"
                        )

                        s.sendall(subject.encode("utf-8"))

                        raw_data = s.recv(1024)
                        if not raw_data:
                            messagebox.showerror("שגיאה", "אין תגובה מהשרת")
                            return

                        dataFromServer = raw_data.decode("utf-8").strip()
                        print(f"Received from server: {dataFromServer}")

                        if dataFromServer.startswith("200"):
                            parts = dataFromServer.split("|")
                            role = parts[1]
                            class_name = parts[2]
                            
                            messagebox.showinfo("הצלחה", "החשבון נוצר בהצלחה")
                            new_win.destroy()                       
                            open_login_window()

                        elif dataFromServer == "gmail already exists":
                            messagebox.showerror("שגיאה", "אימייל כבר בשימוש")

                        elif dataFromServer == "username already exists":
                            messagebox.showerror("שגיאה", "שם משתמש כבר בשימוש")

                        elif dataFromServer == "invalid teacher code":
                            messagebox.showerror("שגיאה", "קוד מורה שגוי")

                        elif dataFromServer == "invalid student code":
                            messagebox.showerror("שגיאה", "קוד תלמיד שגוי")
                        
                        elif dataFromServer.startswith("teacher"):
                            messagebox.showerror("שגיאה", "מורה כבר קיים בכיתה המבוקשת")
                        
                        elif dataFromServer.startswith("error|"):
                            messagebox.showerror("שגיאת שרת", "שגיאת שרת: 500")
                        
                        elif dataFromServer.startswith("404"):
                            messagebox.showerror("שגיאה", "הכיתה המבוקשת אינה קיימת")
                        
                        else:
                            messagebox.showerror("שגיאה", dataFromServer)

                except ConnectionRefusedError:
                    messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת")
        
            tk.Button(frame, text="המשך", bg="#1a73e8", fg="white",
                    command=submit).pack(pady=30, ipady=10, ipadx=20)

        def open_student_setup(username):
            win = tk.Toplevel(root)
            destroy_and_set_new_window(win)

            win.title("כניסת תלמיד")
            width, height = 520, 770
            screen_width = win.winfo_screenwidth()  
            screen_height = win.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            win.geometry(f"{width}x{height}+{x}+{y}")
            win.configure(bg="#f0f4f8")

            frame = tk.Frame(win, bg="white")
            frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=350)

            tk.Label(frame, text="🎓", font=("Arial", 40), bg="white", fg="#1a73e8").pack(pady=10)

            tk.Label(frame, text="הכנס קוד כיתה", font=("Arial", 20, "bold"), bg="white").pack(pady=10)

            code_entry = tk.Entry(frame)
            code_entry.pack(ipady=10, fill="x", padx=40)

            def submit():
                class_code = code_entry.get()

                if not class_code:
                    return

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        print(f"Connecting to {SERVER_IP}:{PORT}...")
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
                            messagebox.showerror("שגיאה", "אין תגובה מהשרת")
                            return

                        dataFromServer = raw_data.decode("utf-8").strip()
                        print(f"Received from server: {dataFromServer}")

                        if dataFromServer.startswith("200"):
                            parts = dataFromServer.split("|")
                            role = parts[1]
                            class_name = parts[2]
                            
                            messagebox.showinfo("הצלחה", "החשבון נוצר בהצלחה")
                            new_win.destroy()                  
                            open_login_window()

                        elif dataFromServer == "gmail already exists":
                            messagebox.showerror("שגיאה", "אימייל כבר בשימוש")

                        elif dataFromServer == "username already exists":
                            messagebox.showerror("שגיאה", "שם משתמש כבר בשימוש")

                        elif dataFromServer == "invalid teacher code":
                            messagebox.showerror("שגיאה", "קוד מורה שגוי")

                        elif dataFromServer == "invalid student code":
                            messagebox.showerror("שגיאה", "קוד תלמיד שגוי")
                        
                        elif dataFromServer.startswith("teacher"):
                            messagebox.showerror("שגיאה", "מורה כבר קיים בכיתה המבוקשת")
                        
                        elif dataFromServer.startswith("error|"):
                            messagebox.showerror("שגיאת שרת", "שגיאת שרת: 500")
                        
                        elif dataFromServer.startswith("404"):
                            messagebox.showerror("שגיאה", "הכיתה המבוקשת אינה קיימת")

                        else:
                            messagebox.showerror("שגיאה", dataFromServer)

                except ConnectionRefusedError:
                    messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת")
                    
                except Exception as e:
                    messagebox.showerror("שגיאה", f"אירעה שגיאה: {e}")
            

            tk.Button(frame, text="כניסה", bg="#1a73e8", fg="white", 
                    command=submit).pack(pady=30, ipady=10, ipadx=20)

        new_win = tk.Toplevel(root)
        new_win.title("MashovApp / הרשמה")

        width, height = 520, 860
        x = (new_win.winfo_screenwidth() // 2) - (width // 2)
        y = (new_win.winfo_screenheight() // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        main_frame = tk.Frame(new_win, bg="white", bd=0)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=520, height=840)

        header_frame = tk.Frame(main_frame, bg="#1a73e8", height=160)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📝",
            font=("Arial", 45),
            fg="white",
            bg="#1a73e8"
        ).pack(pady=(25, 0))

        tk.Label(
            header_frame,
            text="יצירת חשבון חדש",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1a73e8"
        ).pack()

        form_frame = tk.Frame(main_frame, bg="white")
        form_frame.pack(fill="both", expand=True, padx=45, pady=10)

        label_style = {
            "font": ("Arial", 10, "bold"),
            "fg": "#333333",
            "bg": "white",
            "anchor": "e"
        }

        entry_style = {
            "font": ("Arial", 12),
            "bg": "#f8f9fa",
            "relief": "solid",
            "bd": 1,
            "justify": "right"
        }

        fields = [
            ("שם פרטי", "firstName"),
            ("שם משפחה", "lastName"),
            ("אימייל", "gmail"),
            ("שם משתמש", "newUsername"),
            ("סיסמה", "newPassword")
        ]

        entries = {}

        for label_text, var_name in fields:
            tk.Label(form_frame, text=label_text, **label_style).pack(fill="x", pady=(10, 2))
            ent = tk.Entry(form_frame, **entry_style)
            ent.pack(fill="x", ipady=6)
            entries[var_name] = ent

        firstName, lastName, gmail, newUsername, newPassword = entries.values()

        gmail.insert(0, "example@gmail.com")

        tk.Label(form_frame, text="כיתה", **label_style).pack(fill="x", pady=(10, 2))
        class_box = ttk.Combobox(
            form_frame,
            values=["ז1", "ז2", "ז3", "ז4", "ז5", "ז6", "ח1", "ח2", "ח3", "ח4", "ח5", "ח6", "ט1", "ט2", "ט3", "ט4", "ט5", "ט6", "י1", "י2", "י3", "י4", "י5", "י6", "יא1", "יא2", "יא3", "יא4", "יא5", "יא6", "יב1", "יב2", "יב3", "יב4", "יב5", "יב6"],
            state="readonly",
            font=("Arial", 12)
        )
        class_box.pack(fill="x", ipady=6)

        tk.Label(form_frame, text="תפקיד", **label_style).pack(fill="x", pady=(10, 2))
        role_box = ttk.Combobox(
            form_frame,
            values=["student", "teacher"],
            state="readonly",
            font=("Arial", 12)
        )
        role_box.pack(fill="x", ipady=6)

        tk.Button(
            form_frame,
            text="צור חשבון עכשיו",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1a73e8",
            activebackground="#1557b0",
            relief="flat",
            cursor="hand2",
            command=attemptSignUp
        ).pack(fill="x", pady=(25, 10), ipady=12)

        footer_frame = tk.Frame(main_frame, bg="white")
        footer_frame.pack(side="bottom", pady=20)

        tk.Label(
            footer_frame,
            text="?כבר יש לך חשבון",
            font=("Arial", 11),
            fg="#999999",
            bg="white"
        ).pack()
        
        def back_to_login_window():
            new_win.destroy()

        tk.Button(
            footer_frame,
            text="חזור למסך ההתחברות",
            font=("Arial", 11, "underline", "bold"),
            fg="#1a73e8",
            bg="white",
            bd=0,
            cursor="hand2",
            command=back_to_login_window,
        ).pack()

        tk.Label(
            footer_frame,
            text="🏫",
            font=("Arial", 40),
            bg="white"
        ).pack(pady=10)

        return new_win


    ###########################################################
    #                שערי האפליקציה        #
    ###########################################################
    

    def open_grades():
        if not current_user_role == "teacher" and not current_user_role == "student":
            messagebox.showerror("שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
            return
        
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.title("עמוד ציונים")

        width, height = 520, 770

        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=730)

        header_frame = tk.Frame(main_frame, bg="#1a73e8", height=150)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📊",
            font=("Arial", 40),
            fg="white",
            bg="#1a73e8"
        ).pack(pady=(18, 0))

        tk.Label(
            header_frame,
            text="ציונים שוטפים",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1a73e8"
        ).pack()

        tk.Label(
            header_frame,
            text="צפייה בכל הציונים והממוצע",
            font=("Arial", 11),
            fg="#dbeafe",
            bg="#1a73e8"
        ).pack()

        avg_frame = tk.Frame(main_frame, bg="#f8fafc", height=90)
        avg_frame.pack(fill="x", padx=25, pady=20)
        avg_frame.pack_propagate(False)

        tk.Label(
            avg_frame,
            text="ממוצע כללי",
            font=("Arial", 14, "bold"),
            fg="#334155",
            bg="#f8fafc"
        ).pack(pady=(10, 0))
        
        if current_user_role == "teacher" or current_user_role == "student":
            grades = [] 
        
        else:
            grades = [
                ("מתמטיקה", 95),
                ("אנגלית", 88),
                ("מדעים", 91),
                ("לשון", 84),
                ("היסטוריה", 90),
                ("תנ\"ך", 93),
                ("ספרות", 87),
                ("גמרא", 97)
        ] 

        total = 0
        for sub, grd in grades:
            total += grd
        
        try:
            average = round(total / len(grades), 2)
        except ZeroDivisionError:
            average = 0
        
        tk.Label(
            avg_frame,
            text=str(average),
            font=("Arial", 28, "bold"),
            fg="#1a73e8",
            bg="#f8fafc",
        ).pack()

        list_container = tk.Frame(main_frame, bg="#f8fafc")
        list_container.pack(fill="both", expand=True, padx=25, pady=10)

        canvas = tk.Canvas(
            list_container,
            bg="#f8fafc",
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            list_container,
            orient="vertical",
            command=canvas.yview
        )

        scrollable_frame = tk.Frame(canvas, bg="#f8fafc")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=430)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for subject, grade in grades:
            card = tk.Frame(
                scrollable_frame,
                bg="white",
                highlightbackground="#e2e8f0",
                highlightthickness=1
            )
            card.pack(fill="x", pady=6, ipady=12)

            tk.Label(
                card,
                text=subject,
                font=("Arial", 13, "bold"),
                fg="#1e293b",
                bg="white"
            ).pack(side="right", padx=18)

            tk.Label(
                card,
                text=grade,
                font=("Arial", 14, "bold"),
                fg="#1a73e8",
                bg="#eff6ff",
                padx=14,
                pady=4
            ).pack(side="left", padx=18)

        footer_frame = tk.Frame(main_frame, bg="#f8fafc", height=70)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        tk.Button(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Arial", 13, "bold"),
            bg="#1a73e8",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(pady=15, ipadx=18, ipady=8)

    def open_doar():
        if not current_user_role == "teacher" and not current_user_role == "student":
            messagebox.showerror("שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
            return
        
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.title("עמוד דואר")

        width, height = 520, 770

        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=730)

        header_frame = tk.Frame(main_frame, bg="#1a73e8", height=150)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📨",
            font=("Arial", 40),
            fg="white",
            bg="#1a73e8"
        ).pack(pady=(18, 0))

        tk.Label(
            header_frame,
            text="דואר נכנס",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1a73e8"
        ).pack()

        tk.Label(
            header_frame,
            text="הודעות ועדכונים מבית הספר",
            font=("Arial", 11),
            fg="#dbeafe",
            bg="#1a73e8"
        ).pack()

        list_container = tk.Frame(main_frame, bg="#f8fafc")
        list_container.pack(fill="both", expand=True, padx=25, pady=20)

        canvas = tk.Canvas(
            list_container,
            bg="#f8fafc",
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            list_container,
            orient="vertical",
            command=canvas.yview
        )

        scrollable_frame = tk.Frame(canvas, bg="#f8fafc")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=430)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        messages = [
            ("הודעה מהמורה", "יש להביא מחברת לשיעור מחר"),
            ("מזכירות", "אסיפת הורים ביום חמישי"),
            ("מערכת", "ציונים חדשים עודכנו"),
            ("הנהלה", "מחר יום לימודים מקוצר"),
            ("מחנך הכיתה", "נא להגיע בזמן")
        ]

        for sender, msg in messages:
            mail_card = tk.Frame(
                scrollable_frame,
                bg="white",
                highlightbackground="#e2e8f0",
                highlightthickness=1
            )
            mail_card.pack(fill="x", pady=7, ipady=10)

            tk.Label(
                mail_card,
                text=sender,
                font=("Arial", 12, "bold"),
                fg="#1a73e8",
                bg="white"
            ).pack(anchor="e", padx=15, pady=(5, 0))

            tk.Label(
                mail_card,
                text=msg,
                font=("Arial", 11),
                fg="#334155",
                bg="white",
                wraplength=380,
                justify="right"
            ).pack(anchor="e", padx=15, pady=(3, 8))

        footer_frame = tk.Frame(main_frame, bg="#f8fafc", height=70)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        tk.Button(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Arial", 13, "bold"),
            bg="#1a73e8",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(pady=15, ipadx=18, ipady=8)
    
        
    def open_class_chat_room():
        global current_user_class
        hebrew_display_map = {
            "7th1": "ז'1", "7th2": "ז'2", "7th3": "ז'3",
            "7th4": "ז'4", "7th5": "ז'5", "7th6": "ז'6",

            "8th1": "ח'1", "8th2": "ח'2", "8th3": "ח'3",
            "8th4": "ח'4", "8th5": "ח'5", "8th6": "ח'6",

            "9th1": "ט'1", "9th2": "ט'2", "9th3": "ט'3",
            "9th4": "ט'4", "9th5": "ט'5", "9th6": "ט'6",

            "10th1": "י'1", "10th2": "י'2", "10th3": "י'3",
            "10th4": "י'4", "10th5": "י'5", "10th6": "י'6",

            "11th1": 'י"א1', "11th2": 'י"א2', "11th3": 'י"א3',
            "11th4": 'י"א4', "11th5": 'י"א5', "11th6": 'י"א6',

            "12th1": 'י"ב1', "12th2": 'י"ב2', "12th3": 'י"ב3',
            "12th4": 'י"ב4', "12th5": 'י"ב5', "12th6": 'י"ב6',
        }

        class_raw = current_user_class  
        simplefiled_class = hebrew_display_map.get(class_raw, class_raw)  
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.title("צ'אט כיתתי")

        width, height = 620, 800
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=580, height=760)

        header = tk.Frame(main_frame, bg="#1a73e8", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"💬 צאט כיתה {simplefiled_class}",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1a73e8"
        ).pack(pady=(20, 5))

        tk.Label(
            header,
            text="שיח פתוח עם הכיתה",
            font=("Arial", 10),
            fg="#dbeafe",
            bg="#1a73e8"
        ).pack()

        chat_container = tk.Frame(main_frame, bg="#f8fafc")
        chat_container.pack(fill="both", expand=True, padx=20, pady=15)

        canvas = tk.Canvas(chat_container, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=canvas.yview)

        messages_frame = tk.Frame(canvas, bg="#f8fafc")

        messages_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=messages_frame, anchor="nw", width=520)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def add_message(name, text, is_me=False):
            outer = tk.Frame(messages_frame, bg="#f8fafc")
            outer.pack(fill="x", pady=6, padx=8)

            side = "right" if is_me else "left"
            bubble_bg = "#1a73e8" if is_me else "white"
            text_fg = "white" if is_me else "#334155"

            bubble = tk.Frame(
                outer,
                bg=bubble_bg,
                padx=12,
                pady=10
            )
            bubble.pack(side=side)

            tk.Label(
                bubble,
                text=name,
                font=("Arial", 9, "bold"),
                bg=bubble_bg,
                fg=text_fg
            ).pack(anchor="e")

            tk.Label(
                bubble,
                text=text,
                font=("Arial", 11),
                bg=bubble_bg,
                fg=text_fg,
                wraplength=320,
                justify="right"
            ).pack(anchor="e", pady=(4, 0))

        add_message("יונתן", "מישהו יודע מה יש במתמטיקה?", False)
        add_message("אוריה", "כן, עמוד 57 תרגילים 1-5", True)
        add_message("מאור", "וגם ללמוד למבחן", False)

        input_frame = tk.Frame(main_frame, bg="#f8fafc", height=80)
        input_frame.pack(fill="x", padx=20, pady=(0, 15))
        input_frame.pack_propagate(False)

        message_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bd=0,
            relief="flat"
        )
        message_entry.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(10, 10),
            pady=18,
            ipady=10
        )

        tk.Button(
            input_frame,
            text="שלח",
            font=("Arial", 11, "bold"),
            bg="#1a73e8",
            fg="white",
            bd=0,
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2"
        ).pack(side="left", padx=10, pady=18)

        footer = tk.Frame(main_frame, bg="white", height=60)
        footer.pack(fill="x")
        footer.pack_propagate(False)

        tk.Button(
            footer,
            text="חזרה",
            font=("Arial", 12),
            bg="#64748b",
            fg="white",
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2",
            command=lambda: open_main_page(current_username)
        ).pack(pady=10)
        
        
    def open_todo_list():
        global current_username, current_user_class
        SERVER_IP = '127.0.0.1'
        PORT = 9999

        try:
            with create_secure_socket() as s:
                print(f"Connecting to {SERVER_IP}:{PORT}...")
                s.connect((SERVER_IP, PORT))

                subject = f"tasks|{current_user_class}|{current_username}"

                s.sendall(subject.encode("utf-8"))

                raw_data = s.recv(1024)
                if not raw_data:
                    messagebox.showerror("שגיאה", "אין תגובה מהשרת")
                    return

                dataFromServer = raw_data.decode("utf-8").strip()
                print(f"Received from server: {dataFromServer}")
                
                dataFromServer = raw_data.decode("utf-8").strip()
                print(f"Received from server: {dataFromServer}")

                if dataFromServer.startswith("username:"):
                    messagebox.showerror("שגיאה", "עליך להירשם למערכת כדי להשתמש באופציה זו")
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
            messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת")
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"אירעה שגיאה: {e}")
                
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.title("To Do List")

        width, height = 620, 800
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=580, height=760)

        header = tk.Frame(main_frame, bg="#1a73e8", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📝 To Do List",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1a73e8"
        ).pack(pady=(18, 5))

        tk.Label(
            header,
            text="המשימות שלך להיום",
            font=("Arial", 10),
            fg="#dbeafe",
            bg="#1a73e8"
        ).pack()

        tasks_frame = tk.Frame(main_frame, bg="#f8fafc")
        tasks_frame.pack(fill="both", expand=True, padx=20, pady=15)

        def add_task(task_text, done=False):
            row = tk.Frame(
                tasks_frame,
                bg="white",
                highlightbackground="#e2e8f0",
                highlightthickness=1
            )
            
            row.pack(fill="x", pady=6)

            var = tk.BooleanVar(value=done)

            def remove_task():
                if var.get(): 
                    if task_text in tasks:
                        tasks.remove(task_text)
                    row.destroy()

            tk.Checkbutton(
                row,
                variable=var,
                command=remove_task,
                bg="white",
                activebackground="white"
            ).pack(side="left", padx=12, pady=12)

            tk.Label(
                row,
                text=task_text,
                font=("Arial", 11),
                bg="white",
                fg="#334155",
                anchor="e"
            ).pack(side="right", fill="x", expand=True, padx=15, pady=12)
        
        def add_task_to_gui():
            if current_user_role == "teacher" or current_user_role == "student":
                add_task(task_text=str(task_entry.get()))
                tasks.append(str(task_entry.get()))
                task_entry.delete(0, tk.END)
                
            else:
                messagebox.showerror("שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
                return
            
        for task in tasks:
            add_task(task)

        input_frame = tk.Frame(main_frame, bg="#f8fafc", height=80)
        input_frame.pack(fill="x", padx=20, pady=(0, 15))
        input_frame.pack_propagate(False)

        task_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bd=0,
            relief="flat"
        )
        task_entry.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(10, 10),
            pady=18,
            ipady=10
        )
        
        def saveTasks():
            if current_user_role == "teacher" or current_user_role == "student":
            
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
                    messagebox.showwarning("שגיאת סנכרון", f"המשימות נשמרו מקומית אך לא בשרת: {e}")
            
            else:
                open_main_page(current_username)
                return

            open_main_page(current_username)
        
        def checkIfValid():
            if current_user_role == "teacher" or current_user_role == "student":
                if task_entry.get().strip() == "":
                    messagebox.showerror("שגיאה", "משימה לא יכולה להיות ריקה")
                    return
                
                if len(tasks) == 7:
                    messagebox.showerror("שגיאה", "הגעת למגבלת המשימות")
                    return
                
            else:
                pass
            
            add_task_to_gui()

        tk.Button(
            input_frame,
            text="הוסף",
            font=("Arial", 11, "bold"),
            bg="#1a73e8",
            fg="white",
            bd=0,
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=checkIfValid,
        ).pack(side="left", padx=10, pady=18)

        footer = tk.Frame(main_frame, bg="white", height=60)
        footer.pack(fill="x")
        footer.pack_propagate(False)

        tk.Button(
            footer,
            text="חזרה",
            font=("Arial", 12),
            bg="#64748b",
            fg="white",
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2",
            command=saveTasks,
        ).pack(pady=10)
        
    def open_reminder():
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
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
                    messagebox.showerror("שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
                    return

                if any(value == "" for value in fields.values()):
                        messagebox.showerror("שגיאה", "בבקשה תמלא את כל הפרטים בטופס")
                        
                else:
                        try:
                                files = os.listdir(".")
                                for file in files:
                                        if os.path.exists("reminder.json"):
                                                messagebox.showerror("שגיאה", "תזכורון אחד כבר קיים, מחק אותו כדי ליצור חדש")
                                                break
                                        
                                        else:      
                                                with open("data/reminder.json", "w", encoding="utf-8") as f:
                                                        json.dump(fields, f, indent=4, ensure_ascii=False)
                                                        messagebox.showinfo("תזכורון מוצלח", "טופס התזכורון נשמר בהצלחה!")
                                                        break
                                
                        except Exception as e:
                                messagebox.showerror("שגיאה", f"ארעה שגיאה בשמירה: {e}")

        def delete_existing():
                files = os.listdir(".")
                for file in files:
                        if os.path.exists("data/reminder.json"):
                                os.remove("data/reminder.json")
                                messagebox.showinfo("הצלחה", "התזכורון הקיים נמחק")
                                break
                        
                else:
                        messagebox.showerror("שגיאה", "לא נמצא תזכורון קיים")
        
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
                                messagebox.showerror("שגיאה", "לא נמצא תזכורון קיים")
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

    def open_freer():
        global days, id_s, id, hr, rs

        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.title("עמוד שיחרורון")

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        def freer_completed():
            if not current_user_role == "teacher" and not current_user_role == "student":
                messagebox.showerror("שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
                return
            
            if days.get() == "" or id.get() == "" or id_s.get() == "" or hr.get() == "" or rs.get() == "":
                messagebox.showerror("שגיאה", "בבקשה תמלא את כל הפרטים בטופס")
                return

            SERVER_IP = '127.0.0.1'
            PORT = 9999

            try:
                with create_secure_socket() as s:
                    print(f"Connecting to {SERVER_IP}:{PORT}...")
                    s.connect((SERVER_IP, PORT))
                    subject = "freer premition"
                    s.sendall(subject.encode('utf-8'))

                    while True:
                        raw_data = s.recv(1024)

                        if not raw_data:
                            break

                        dataFromServer = raw_data.decode('utf-8').strip()

                        if dataFromServer == "200 ok":
                            messagebox.showinfo("!הצלחה", "בקשת השחרור אושרה על ידי השרת")
                            break
                        else:
                            messagebox.showerror("שגיאה!", "בקשת השחרור לא אושרה על ידי השרת")
                            break

            except ConnectionRefusedError:
                messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת. וודא שהוא פועל.")
            except Exception as e:
                messagebox.showerror("שגיאה", f"אירעה שגיאה: {e}")

        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=730)

        header_frame = tk.Frame(main_frame, bg="#1a73e8", height=150)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📄",
            font=("Arial", 40),
            fg="white",
            bg="#1a73e8"
        ).pack(pady=(15, 0))

        tk.Label(
            header_frame,
            text="בקשת שחרור",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1a73e8"
        ).pack()

        tk.Label(
            header_frame,
            text="שליחת בקשת יציאה מסודרת",
            font=("Arial", 11),
            fg="#dbeafe",
            bg="#1a73e8"
        ).pack()

        form_frame = tk.Frame(main_frame, bg="#f8fafc")
        form_frame.pack(fill="both", expand=True, padx=25, pady=20)

        label_style = {
            "font": ("Arial", 11, "bold"),
            "fg": "#334155",
            "bg": "#f8fafc",
            "anchor": "e"
        }

        def add_label(text):
            tk.Label(form_frame, text=text, **label_style).pack(fill="x", pady=(10, 4))

        add_label("ת.ז. של התלמיד/ה")
        id_s = ttk.Entry(form_frame, font=("Arial", 11))
        id_s.pack(fill="x", ipady=6)

        add_label("ת.ז. שלך (ההורה)")
        id = ttk.Entry(form_frame, font=("Arial", 11))
        id.pack(fill="x", ipady=6)

        add_label("יום השחרור")
        days = ttk.Combobox(
            form_frame,
            values=["יום ראשון", "יום שני", "יום שלישי", "יום רביעי", "יום חמישי"],
            state="readonly",
            font=("Arial", 11)
        )
        days.pack(fill="x")

        add_label("שעה")
        hr = ttk.Combobox(
            form_frame,
            values=[
                "9:00", "9:30", "10:00", "10:30",
                "11:00", "11:30", "12:00", "12:30",
                "13:00", "13:30", "14:00", "14:30",
                "15:00", "15:30", "16:00"
            ],
            state="readonly",
            font=("Arial", 11)
        )
        hr.pack(fill="x")

        add_label("סיבה / הערה")
        rs = ttk.Entry(form_frame, font=("Arial", 11))
        rs.pack(fill="x", ipady=6)

        tk.Label(
            form_frame,
            text="בלחיצה על הכפתור הנך מאשר/ת את תנאי השימוש והמדיניות",
            font=("Arial", 10),
            fg="#64748b",
            bg="#f8fafc",
            wraplength=400,
            justify="right"
        ).pack(pady=25)

        tk.Button(
            form_frame,
            text="שלח בקשת שחרור",
            command=freer_completed,
            font=("Arial", 13, "bold"),
            bg="#1a73e8",
            fg="white",
            relief="flat",
            cursor="hand2"
        ).pack(fill="x", ipady=12)

        footer_frame = tk.Frame(main_frame, bg="#f8fafc", height=70)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        tk.Button(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Arial", 13, "bold"),
            bg="#1a73e8",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(pady=15, ipadx=18, ipady=8)
    
    def open_marechet():
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.title("מערכת שעות")

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        # ---------------- טעינת לוגיקה קיימת ----------------
        try:
            with open("data/schedule.json", "r", encoding="utf-8") as f:
                schedule_data = json.load(f)
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בטעינת המערכת: {e}")
            return

        # ---------------- UI ----------------
        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=730)

        header_frame = tk.Frame(main_frame, bg="#1a73e8", height=150)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📅",
            font=("Arial", 40),
            fg="white",
            bg="#1a73e8"
        ).pack(pady=(18, 0))

        tk.Label(
            header_frame,
            text="מערכת שעות",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1a73e8"
        ).pack()

        tk.Label(
            header_frame,
            text="צפייה במערכת השבועית",
            font=("Arial", 11),
            fg="#dbeafe",
            bg="#1a73e8"
        ).pack()

        selector_frame = tk.Frame(main_frame, bg="#f8fafc")
        selector_frame.pack(fill="x", padx=25, pady=20)

        class_cb = ttk.Combobox(
            selector_frame,
            values=list(schedule_data.keys()),
            state="readonly",
            font=("Arial", 11),
            width=10
        )
        class_cb.pack(side="right", padx=8)

        day_cb = ttk.Combobox(
            selector_frame,
            values=["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"],
            state="readonly",
            font=("Arial", 11),
            width=10
        )
        day_cb.pack(side="right", padx=8)

        tk.Label(
            selector_frame,
            text="בחר כיתה ויום:",
            font=("Arial", 11, "bold"),
            bg="#f8fafc",
            fg="#334155"
        ).pack(side="right", padx=10)

        # ---------------- אזור רשימה ----------------
        list_container = tk.Frame(main_frame, bg="#f8fafc")
        list_container.pack(fill="both", expand=True, padx=25, pady=10)

        canvas = tk.Canvas(list_container, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg="#f8fafc")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=430)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def refresh_schedule(event=None):
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            selected_class = class_cb.get()
            selected_day = day_cb.get()

            if not selected_class or not selected_day:
                return

            lessons = schedule_data.get(selected_class, {}).get(selected_day, [])

            for lesson in lessons:
                lesson_card = tk.Frame(
                    scrollable_frame,
                    bg="white",
                    highlightbackground="#e2e8f0",
                    highlightthickness=1
                )
                lesson_card.pack(fill="x", pady=6, ipady=10)

                tk.Label(
                    lesson_card,
                    text=lesson,
                    font=("Arial", 12, "bold"),
                    fg="#1e293b",
                    bg="white",
                    anchor="e",
                    justify="right"
                ).pack(fill="x", padx=15)

        class_cb.bind("<<ComboboxSelected>>", refresh_schedule)
        day_cb.bind("<<ComboboxSelected>>", refresh_schedule)

        footer_frame = tk.Frame(main_frame, bg="#f8fafc", height=70)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        tk.Button(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Arial", 13, "bold"),
            bg="#1a73e8",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(pady=15, ipadx=18, ipady=8)
    
    def open_chatbot_help():
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.title("מערכת שעות")

        width, height = 520, 770
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)
    
    if __name__ == "__main__":
        open_splash_screen()
        

except KeyboardInterrupt:
    print("Keyboard Interrupt. QUITING!")
except ModuleNotFoundError:
    print(f"module not found")
except ConnectionAbortedError:
    print("connection abborted")
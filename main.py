
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
            text="כניסה כאורח  ",
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

        # הגדלנו את הגובה מ-770 ל-880 כדי שארבע שורות כפתורים ייכנסו בצורה יפה
        width, height = 520, 880
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        # הגדלנו את גובה ה-frame המרכזי מ-730 ל-840
        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=840)

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
        content_frame.pack(expand=True, pady=20) # הקטנה קלה של ה-pady כדי לתת עוד מרווח אנכי

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
            text="נוכחות בשיעור",
            bg="#0284c7", 
            command=open_attendance,
            **button_style
        ).grid(row=3, column=0, padx=15, pady=15)

        tk.Button(
            content_frame,
            text="Moodle משימות",
            bg="#0369a1", 
            command=open_moodle_tasks,
            **button_style
        ).grid(row=3, column=1, padx=15, pady=15)

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
                
        # --- ממשק מורה ---
        if current_user_role == "teacher":
            new_win = tk.Toplevel()
            destroy_and_set_new_window(new_win)
            new_win.title("ניהול ציונים - מורה")

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

            header_frame = tk.Frame(main_frame, bg="#1a73e8", height=160)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)

            tk.Label(
                header_frame,
                text="📝",
                font=("Arial", 40),
                fg="white",
                bg="#1a73e8"
            ).pack(pady=(18, 0))

            tk.Label(
                header_frame,
                text="ניהול והזנת ציונים",
                font=("Arial", 24, "bold"),
                fg="white",
                bg="#1a73e8"
            ).pack()

            tk.Label(
                header_frame,
                text="ממשק מורה לעדכון והוספת ציוני תלמידים",
                font=("Arial", 11),
                fg="#dbeafe",
                bg="#1a73e8"
            ).pack()

            form_frame = tk.Frame(main_frame, bg="#f8fafc")
            form_frame.pack(fill="both", expand=True, padx=25, pady=15)
            
            class_students = []

            SERVER_IP = '127.0.0.1'
            PORT = 9999

            with create_secure_socket() as s:
                print(f"Connecting to {SERVER_IP}:{PORT}...")
                s.connect((SERVER_IP, PORT))

                subject = f"get_class_students|{current_user_class}"
                s.sendall(subject.encode("utf-8"))

                raw_data = s.recv(1024)
                if not raw_data:
                    messagebox.showerror("שגיאה", "אין תגובה מהשרת")
                    return

                dataFromServer = raw_data.decode("utf-8").strip()
                print(f"Received from server: {dataFromServer}")
                
                if dataFromServer.startswith("class_students_response|"):
                    res_parts = dataFromServer.split("|")
                    if res_parts[1]:
                        class_students = res_parts[1].split(",") 
                else:
                    messagebox.showerror("שגיאה", f"התקבלה תשובה לא תקינה מהשרת: {dataFromServer}")
                    return

            tk.Label(form_frame, text=":שם התלמיד", font=("Arial", 12, "bold"), fg="#334155", bg="#f8fafc").pack(anchor="e", padx=25, pady=(25, 2))
            student_entry = ttk.Combobox(form_frame, font=("Arial", 12), values=class_students)
            student_entry.pack(fill="x", padx=25, ipady=6)

            tk.Label(form_frame, text=":מקצוע", font=("Arial", 12, "bold"), fg="#334155", bg="#f8fafc").pack(anchor="e", padx=25, pady=(15, 2))
            subject_entry = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid", fg="#1e293b")
            subject_entry.pack(fill="x", padx=25, ipady=6)

            tk.Label(form_frame, text=":ציון חדש", font=("Arial", 12, "bold"), fg="#334155", bg="#f8fafc").pack(anchor="e", padx=25, pady=(15, 2))
            grade_entry = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid", fg="#1e293b")
            grade_entry.pack(fill="x", padx=25, ipady=6)

            def submit_grade():
                student = student_entry.get().strip()
                sub = subject_entry.get().strip() 
                grd = grade_entry.get().strip()
                
                if not student or not sub or not grd:
                    messagebox.showwarning("שגיאה", "אנא מלא את כל השדות")
                    return
                
                SERVER_IP = '127.0.0.1'
                PORT = 9999

                with create_secure_socket() as s:
                    print(f"Connecting to {SERVER_IP}:{PORT}...")
                    s.connect((SERVER_IP, PORT))

                    subject = f"insert_new_grade|{current_user_class}|{grd}|{sub}|{student}"
                    s.sendall(subject.encode("utf-8"))

                    raw_data = s.recv(1024)
                    if not raw_data:
                        messagebox.showerror("שגיאה", "אין תגובה מהשרת")
                        return

                    dataFromServer = raw_data.decode("utf-8").strip()
                    print(f"Received from server: {dataFromServer}")
                    
                    if dataFromServer.startswith("insert_grade_response|"):
                        res_parts = dataFromServer.split("|")
                        status = res_parts[1]
                        
                        if status == "success":
                            messagebox.showinfo("הצלחה", f"הציון {grd} במקצוע {sub} עודכן בהצלחה עבור {student}")
                            
                        
                        else:
                            res_for_failure = res_parts[2]
                            messagebox.showerror("שגיאה", f"{res_for_failure}")
                    
                    else:
                        messagebox.showerror("שגיאה", f"התקבלה תשובה לא תקינה מהשרת: {dataFromServer}")
                        return
                

            save_button = tk.Button(
                form_frame,
                text="עדכן ציון במערכת",
                command=submit_grade,
                font=("Arial", 13, "bold"),
                bg="#1a73e8",
                fg="white",
                relief="flat",
                bd=0,
                cursor="hand2"
            )
            save_button.pack(fill="x", padx=25, pady=35, ipady=10)

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
                        messagebox.showerror("שגיאה", "שגיאה בקבלת הנתונים מהשרת.")
                        new_win.destroy()
                        return
                    
        except Exception as e:
            print(f"Error loading grades: {e}")
            messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת או לטעון את הציונים.")
            new_win.destroy()
            return

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
                text=str(grade),
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
        SERVER_IP = '127.0.0.1'
        PORT = 9999
        
        if not current_user_role == "teacher" and not current_user_role == "student":
            messagebox.showerror("שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
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
                    # השרת מחזיר JSON נקי, לכן ה-loads יעבוד פיקס!
                    messages = json.loads(res_text)
                else:
                    messages = []
                    
        except Exception as e:
            print(f"Error loading mail: {e}")
            messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת או לטעון את ההודעות.")
            # תיקון: הורדנו את new_win.destroy() מכיוון שהחלון עדיין לא נוצר בשלב זה
            return
        
        # שלב 2: יצירת חלון הממשק רק אם המידע נטען בהצלחה
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

        header_frame = tk.Frame(main_frame, bg="#1a73e8", height=170)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="📨", font=("Arial", 40), fg="white", bg="#1a73e8").pack(pady=(18, 0))
        tk.Label(header_frame, text="דואר נכנס", font=("Arial", 24, "bold"), fg="white", bg="#1a73e8").pack()
        tk.Label(header_frame, text="הודעות ועדכונים מבית הספר", font=("Arial", 11), fg="#dbeafe", bg="#1a73e8").pack()

        list_container = tk.Frame(main_frame, bg="#f8fafc")
        list_container.pack(fill="both", expand=True, padx=25, pady=20)

        canvas = tk.Canvas(list_container, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f8fafc")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=430)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # פונקציה פנימית לרענון תצוגת ההודעות במסך
        def refresh_messages():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
                
            for sender, msg in messages:
                mail_card = tk.Frame(scrollable_frame, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
                mail_card.pack(fill="x", pady=7, ipady=10)

                tk.Label(mail_card, text=sender, font=("Arial", 12, "bold"), fg="#1a73e8", bg="white").pack(anchor="e", padx=15, pady=(5, 0))
                tk.Label(mail_card, text=msg, font=("Arial", 11), fg="#334155", bg="white", wraplength=380, justify="right").pack(anchor="e", padx=15, pady=(3, 8))

        refresh_messages()

        # חלון כתיבת הודעה חדשה (למורים)
        def open_teacher_compose_window():
            compose_win = tk.Toplevel(new_win)
            compose_win.title("פרסום הודעה חדשה")
            compose_win.geometry("400x450")
            compose_win.configure(bg="#f0f4f8")
            compose_win.resizable(False, False)
            
            cx = (screen_width // 2) - 200
            cy = (screen_height // 2) - 225
            compose_win.geometry(f"400x450+{cx}+{cy}")
            
            tk.Label(compose_win, text="יצירת עדכון חדש", font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#1a73e8").pack(pady=15)
            tk.Label(compose_win, text="כותרת ההודעה (למשל: הודעה ממורה למתמטיקה):", font=("Arial", 11, "bold"), bg="#f0f4f8").pack(anchor="e", padx=20, pady=(10, 2))
            
            title_entry = tk.Entry(compose_win, font=("Arial", 12), justify="right", bd=1, relief="solid")
            title_entry.pack(fill="x", padx=20, ipady=4)
            
            tk.Label(compose_win, text="תוכן ההודעה:", font=("Arial", 11, "bold"), bg="#f0f4f8").pack(anchor="e", padx=20, pady=(15, 2))
            content_text = tk.Text(compose_win, font=("Arial", 11), bd=1, relief="solid", height=8)
            content_text.pack(fill="x", padx=20)
            
            content_text.tag_configure("rtl", justify="right")
            content_text.bind("<KeyRelease>", lambda event: content_text.tag_add("rtl", "1.0", "end"))
            
            def publish_message():
                title = title_entry.get().strip()
                content = content_text.get("1.0", tk.END).strip()
                
                if not title or not content:
                    messagebox.showwarning("שגיאה", "נא למלא את כל השדות", parent=compose_win)
                    return
                    
                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        subject = f"add_class_doar|{current_user_class}|{title}|{content}"
                        s.sendall(subject.encode('utf-8'))
                        
                        server_response = s.recv(1024).decode('utf-8').strip()
                        
                        if server_response == "200 ok":
                            messages.insert(0, (title, content))
                            messagebox.showinfo("הצלחה", "ההודעה פורסמה בהצלחה!", parent=compose_win)
                            compose_win.destroy()
                            refresh_messages()
                        else:
                            messagebox.showerror("שגיאה", "השרת נכשל בשמירת ההודעה.", parent=compose_win)
                except Exception as e:
                    messagebox.showerror("שגיאה", f"שגיאת תקשורת עם השרת: {e}", parent=compose_win)

            tk.Button(
                compose_win, text="פרסם הודעה לכולם", command=publish_message,
                font=("Arial", 12, "bold"), bg="#10b981", fg="white", relief="flat", cursor="hand2"
            ).pack(pady=25, ipadx=15, ipady=5)

        footer_frame = tk.Frame(main_frame, bg="#f8fafc", height=70)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)

        tk.Button(
            footer_frame, text="חזרה למסך ראשי", command=lambda: open_main_page(current_username),
            font=("Arial", 12, "bold"), bg="#1a73e8", fg="white", relief="flat", bd=0, cursor="hand2"
        ).pack(side="left", padx=20, pady=12, ipadx=10, ipady=6)

        if current_user_role == "teacher":
            tk.Button(
                footer_frame, text="➕ כתיבת הודעה חדשה", command=open_teacher_compose_window,
                font=("Arial", 12, "bold"), bg="#10b981", fg="white", relief="flat", bd=0, cursor="hand2"
            ).pack(side="right", padx=20, pady=12, ipadx=10, ipady=6)
            
        
    def open_class_chat_room():
        global current_username, current_user_class, current_user_role
        
        if not current_user_role in ["student", "teacher"]:
            messagebox.showerror("שגיאה", "פיצ'ר זה זמין למשתמשים רשומים בלבד")
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
        
        new_win = tk.Toplevel()
        destroy_and_set_new_window(new_win)
        new_win.title("צ'אט כיתתי")
        
        width, height = 550, 780
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f8fafc") 
        new_win.resizable(False, False)
        
        main_frame = tk.Frame(new_win, bg="white", relief="solid", bd=1)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=520, height=740)
        
        # כותרת
        header_frame = tk.Frame(main_frame, bg="#1a73e8", height=90) 
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"צ'אט כיתה {simplified_class}", font=("Arial", 16, "bold"), fg="white", bg="#1a73e8").pack(pady=(22, 2))
        tk.Label(header_frame, text="מוצפן מקצה לקצה", font=("Arial", 10), fg="#e8f0fe", bg="#1a73e8").pack()
        
        # אזור הצ'אט (Canvas דינמי לבועות)
        chat_container = tk.Frame(main_frame, bg="#e2e8f0")
        chat_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(chat_container, bg="#e2e8f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#e2e8f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.pack(side="right", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")
        
        # אזור הקלט
        input_frame = tk.Frame(main_frame, bg="white")
        input_frame.pack(fill="x", ipady=5)
        
        msg_entry = tk.Entry(input_frame, font=("Arial", 13), bg="#f1f5f9", relief="flat", justify="right", fg="#1e293b")
        msg_entry.pack(side="right", fill="x", expand=True, padx=12, pady=10, ipady=8)
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
                    # שולח עכשיו גם את תפקיד המשתמש!
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
        
        btn_send = tk.Button(
            input_frame, 
            text="שלח", 
            font=("Arial", 11, "bold"), 
            bg="#1a73e8", 
            fg="white", 
            relief="flat", 
            bd=0, 
            cursor="hand2", 
            command=send_message, 
            width=8
        )
        btn_send.pack(side="left", padx=10, pady=10, ipady=6)
        
        loaded_message_count = 0
        
        def render_bubble(msg_data):
            """ פונקציה שמציירת בועת צ'אט בודדת לפי סוג השולח """
            user = msg_data.get("username", "Unknown")
            text = msg_data.get("message", "")
            time_str = msg_data.get("time", "")
            role = msg_data.get("role", "student")
            
            is_me = (user == current_username)
            is_teacher = (role == "teacher")
            
            # שורת מעטפת להודעה
            row = tk.Frame(scrollable_frame, bg="#e2e8f0")
            row.pack(fill="x", padx=15, pady=6)
            
            # הגדרות עיצוב לבועה
            if is_teacher:
                bg_color = "#fef08a" # צהוב-זהב להבלטת מורה
                fg_color = "#854d0e" # צבע טקסט כהה-זהוב
                border_color = "#eab308"
                anchor_side = "w"
                pack_side = "left"
                header = f"{user} (מורה) • {time_str}"
            elif is_me:
                bg_color = "#dcf8c6" # ירוק וואטסאפ (או כחול מודרני אם תרצה לשנות)
                fg_color = "#000000"
                border_color = "#b2e289"
                anchor_side = "e"
                pack_side = "right"
                header = f"{time_str}"
            else:
                bg_color = "#ffffff" # לבן לתלמידים אחרים
                fg_color = "#000000"
                border_color = "#cbd5e1"
                anchor_side = "w"
                pack_side = "left"
                header = f"{user} • {time_str}"
            
            bubble = tk.Frame(row, bg=bg_color, highlightbackground=border_color, highlightthickness=1)
            bubble.pack(side=pack_side, anchor=anchor_side)
            
            # מסגרת פנימית לריווח (Padding)
            inner_bubble = tk.Frame(bubble, bg=bg_color, padx=10, pady=6)
            inner_bubble.pack()
            
            # כותרת (שם המשתמש + שעה)
            tk.Label(
                inner_bubble, 
                text=header, 
                font=("Arial", 9, "bold" if is_teacher else "normal"), 
                bg=bg_color, 
                fg="#64748b" if not is_teacher else fg_color
            ).pack(anchor=anchor_side, pady=(0, 2))
            
            # גוף ההודעה
            tk.Label(
                inner_bubble, 
                text=text, 
                font=("Arial", 12), 
                bg=bg_color, 
                fg=fg_color, 
                justify="right", 
                wraplength=320 # שבירת שורות אוטומטית בהודעות ארוכות
            ).pack(anchor=anchor_side)
            
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
                    
                    # מצייר רק הודעות חדשות שעוד לא צויירו! יעילות מקסימלית בלי למחוק את המסך
                    if len(history) > loaded_message_count:
                        for msg in history[loaded_message_count:]:
                            render_bubble(msg)
                            
                        loaded_message_count = len(history)
                        
                        # גלילה אוטומטית למטה אחרי שמציירים
                        canvas.update_idletasks()
                        canvas.yview_moveto(1.0)
                        
            except Exception as e:
                print(f"Error loading chat: {e}")
        
        def auto_refresh():
            if new_win.winfo_exists():
                load_chat_history()
                new_win.after(2000, auto_refresh)
                
        # כפתור תחתון חזרה למסך ראשי
        footer_frame = tk.Frame(main_frame, bg="#f8fafc", height=60)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        tk.Button(
            footer_frame,
            text="חזרה למסך ראשי",
            command=lambda: open_main_page(current_username),
            font=("Arial", 11, "bold"),
            bg="#64748b",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(pady=10, ipadx=20, ipady=4)
        
        # הפעלה
        load_chat_history()
        auto_refresh()
        
        
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
                        messagebox.showinfo("סטטוס בקשות", "אין לך בקשות שחרור במערכת.")
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
                            
                        messagebox.showinfo("עדכון בקשה", f"הבקשה שלך ל{day} בשעה {time}:\nסטטוס: {status_heb}")
                        
        except Exception as e:
            messagebox.showerror("שגיאה", f"לא ניתן לבדוק סטטוס: {e}")
    
    def open_freer():            
        global current_user_role, current_username, current_user_class
        
        if current_user_role == "teacher":
            new_win = tk.Toplevel()
            destroy_and_set_new_window(new_win)
            new_win.title("ניהול בקשות שחרור - ממשק מורה")

            width, height = 700, 770 
            screen_width = new_win.winfo_screenwidth()
            screen_height = new_win.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

            new_win.geometry(f"{width}x{height}+{x}+{y}")
            new_win.configure(bg="#f0f4f8")
            new_win.resizable(False, False)

            main_frame = tk.Frame(new_win, bg="white")
            main_frame.place(relx=0.5, rely=0.5, anchor="center", width=660, height=730)

            header_frame = tk.Frame(main_frame, bg="#1a73e8", height=140)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)

            tk.Label(
                header_frame,
                text="📋",
                font=("Arial", 38),
                fg="white",
                bg="#1a73e8"
            ).pack(pady=(12, 0))

            tk.Label(
                header_frame,
                text="מרכז בקשות שחרור",
                font=("Arial", 22, "bold"),
                fg="white",
                bg="#1a73e8"
            ).pack()

            tk.Label(
                header_frame,
                text="צפייה, אישור ודחייה של בקשות יציאה של תלמידים",
                font=("Arial", 11),
                fg="#dbeafe",
                bg="#1a73e8"
            ).pack()

            table_frame = tk.Frame(main_frame, bg="#f8fafc")
            table_frame.pack(fill="both", expand=True, padx=25, pady=20)

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", font=("Arial", 11), rowheight=32, background="#ffffff", fieldbackground="#ffffff")
            style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#e2e8f0", foreground="#334155")
            
            columns = ("id_s", "day", "hour", "reason")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
            
            tree.heading("id_s", text="ת.ז. תלמיד")
            tree.heading("day", text="יום שחרור")
            tree.heading("hour", text="שעה")
            tree.heading("reason", text="סיבה / הערה מההורה")
            
            tree.column("id_s", width=110, anchor="center")
            tree.column("day", width=100, anchor="center")
            tree.column("hour", width=70, anchor="center")
            tree.column("reason", width=280, anchor="e") 

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            def approve_request():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("שימו לב", "אנא בחרו בקשה מהרשימה לאישור")
                    return
                
                # בדיקה מה ה-ID שנשלף מהשורה שנבחרה
                req_id = selected_item[0]
                item_details = tree.item(selected_item)['values']
                student_id = item_details[0]
                
                print(f"[DEBUG CLIENT] Teacher clicked Approve. Selected row iid (req_id): '{req_id}'")

                class_name = current_user_class.get() if hasattr(current_user_class, 'get') else current_user_class
                class_name = str(class_name).strip()

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        update_msg = f"update_request_status|{class_name}|{req_id}|approved"
                        print(f"[DEBUG CLIENT] Sending update message to server: '{update_msg}'")
                        s.sendall(update_msg.encode('utf-8'))

                        raw_data = s.recv(1024)
                        if raw_data:
                            res = raw_data.decode('utf-8').strip()
                            print(f"[DEBUG CLIENT] Server responded to update: '{res}'")
                            
                            if res == "200 ok":
                                messagebox.showinfo("הצלחה", f"בקשת השחרור עבור תלמיד {student_id} אושרה בהצלחה!")
                                tree.delete(selected_item)
                            else:
                                messagebox.showerror("שגיאה", f"השרת החזיר תשובה שלילית: {res}")
                except Exception as e:
                    print(f"[DEBUG CLIENT] Error in approve_request: {e}")
                    messagebox.showerror("שגיאה", f"שגיאת תקשורת עם השרת: {e}")


            def reject_request():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("שימו לב", "אנא בחרו בקשה מהרשימה לדחייה")
                    return
                
                req_id = selected_item[0]
                item_details = tree.item(selected_item)['values']
                student_id = item_details[0]
                
                print(f"[DEBUG CLIENT] Teacher clicked Reject. Selected row iid (req_id): '{req_id}'")

                class_name = current_user_class.get() if hasattr(current_user_class, 'get') else current_user_class
                class_name = str(class_name).strip()

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        update_msg = f"update_request_status|{class_name}|{req_id}|rejected"
                        print(f"[DEBUG CLIENT] Sending update message to server: '{update_msg}'")
                        s.sendall(update_msg.encode('utf-8'))

                        raw_data = s.recv(1024)
                        if raw_data:
                            res = raw_data.decode('utf-8').strip()
                            print(f"[DEBUG CLIENT] Server responded to update: '{res}'")
                            
                            if res == "200 ok":
                                messagebox.showinfo("סטטוס עודכן", f"בקשת השחרור עבור תלמיד {student_id} נדחתה.")
                                tree.delete(selected_item)
                            else:
                                messagebox.showerror("שגיאה", f"השרת החזיר תשובה שלילית: {res}")
                except Exception as e:
                    print(f"[DEBUG CLIENT] Error in reject_request: {e}")
                    messagebox.showerror("שגיאה", f"שגיאת תקשורת עם השרת: {e}")

            def load_requests():
                for item in tree.get_children():
                    tree.delete(item)

                SERVER_IP = '127.0.0.1'
                PORT = 9999

                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        
                        # דיבאג 1: נראה איזו כיתה המורה מנסה לבקש
                        class_name = current_user_class.get() if hasattr(current_user_class, 'get') else current_user_class
                        print(f"[DEBUG CLIENT] Teacher is requesting data for class: '{class_name}'")
                        
                        request_msg = f"get_freer_requests|{class_name}"
                        s.sendall(request_msg.encode('utf-8'))

                        # מנגנון לקבלת המידע המלא (בלולאה) עד שהשרת מסיים לשלוח
                        full_response = ""
                        while True:
                            raw_data = s.recv(4096)
                            if not raw_data:
                                break
                            full_response += raw_data.decode('utf-8')
                        
                        response = full_response.strip()
                        print(f"[DEBUG CLIENT] Raw response from server: {response}") # דיבאג 2

                        if response.startswith("requests_data|"):
                            json_string = response.split("|", 1)[1]
                            print(f"[DEBUG CLIENT] Extracted JSON string: {json_string}") # דיבאג 3
                            
                            if json_string == "{}" or not json_string:
                                print("[DEBUG CLIENT] JSON is empty, nothing to load.")
                                return  
                            
                            all_requests = json.loads(json_string)
                            
                            for req_id, req_info in all_requests.items():
                                print(f"[DEBUG CLIENT] Processing request {req_id}: {req_info}") # דיבאג 4
                                
                                # שים לב: בדוק שהסטטוס ב-JSON שלך הוא באמת באותיות קטנות "pending"
                                if req_info.get("status") == "pending":
                                    row = (
                                        req_info.get("student_id"),
                                        req_info.get("day"),
                                        req_info.get("time"),
                                        req_info.get("reason")
                                    )
                                    tree.insert("", "end", iid=req_id, values=row)
                                    print(f"[DEBUG CLIENT] Successfully inserted row for student: {req_info.get('student_id')}")
                                else:
                                    print(f"[DEBUG CLIENT] Skipped request {req_id} because status is {req_info.get('status')}")
                                    
                except Exception as e:
                    print(f"[DEBUG CLIENT] Error in load_requests: {e}")
                    messagebox.showerror("שגיאה", f"לא ניתן לטעון את בקשות השחרור: {e}")

            load_requests()

            actions_frame = tk.Frame(main_frame, bg="white")
            actions_frame.pack(fill="x", padx=25, pady=(0, 15))

            btn_approve = tk.Button(
                actions_frame,
                text="אשר בקשה ✔",
                command=approve_request,
                font=("Arial", 12, "bold"),
                bg="#10b981", 
                fg="white",
                relief="flat",
                cursor="hand2"
            )
            btn_approve.pack(side="right", fill="x", expand=True, padx=(8, 0), ipady=10)

            btn_reject = tk.Button(
                actions_frame,
                text="דחה בקשה ❌",
                command=reject_request,
                font=("Arial", 12, "bold"),
                bg="#ef4444", 
                fg="white",
                relief="flat",
                cursor="hand2"
            )
            btn_reject.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=10)

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

            return 
                
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

        student_id_var = tk.StringVar()
        parent_id_var = tk.StringVar()
        day_var = tk.StringVar()
        hour_var = tk.StringVar()
        reason_var = tk.StringVar()

        def freer_completed():
            nonlocal student_id_var, parent_id_var, day_var, hour_var, reason_var
            global current_user_role, current_user_class

            if current_user_role != "teacher" and current_user_role != "student":
                messagebox.showerror("שגיאה", "הירשם כדי להשתמש או לראות את פיצר זה")
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
                messagebox.showerror("שגיאה", "בבקשה תמלא את כל הפרטים בטופס")
                return

            SERVER_IP = '127.0.0.1'
            PORT = 9999

            try:
                with create_secure_socket() as s:
                    print(f"Connecting to {SERVER_IP}:{PORT}...")
                    s.connect((SERVER_IP, PORT))
                    
                    subject = f"freer premition|{s_id}|{s_hour}|{s_day}|{s_reason}|{u_class}"
                    s.sendall(subject.encode('utf-8'))

                    while True:
                        raw_data = s.recv(1024)
                        if not raw_data:
                            break

                        dataFromServer = raw_data.decode('utf-8').strip()

                        if dataFromServer == "200 ok":
                            messagebox.showinfo("!הצלחה", "בקשת השיחרור נשלחה בהצלחה ומחכה לאישור המחנך")
                            break
                        else:
                            messagebox.showerror("שגיאה!", "תקלה בשליחת בקשת שיחרור, אנא נסה שוב")
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


        tk.Button(
            header_frame,
            text="➜  בדוק סטטוס בקשות",
            command=lambda: check_my_requests_status(student_id_var.get(), current_user_class), 
            font=("Arial", 10, "bold"),
            bg="#1a73e8",
            fg="white",
            activebackground="#1557b0",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        ).place(x=340, y=12) 

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
        id_s = ttk.Entry(form_frame, font=("Arial", 11), textvariable=student_id_var)
        id_s.pack(fill="x", ipady=6)

        add_label("ת.ז. שלך (ההורה)")
        id = ttk.Entry(form_frame, font=("Arial", 11), textvariable=parent_id_var)
        id.pack(fill="x", ipady=6)

        add_label("יום השחרור")
        days = ttk.Combobox(
            form_frame,
            values=["יום ראשון", "יום שני", "יום שלישי", "יום רביעי", "יום חמישי"],
            state="readonly",
            font=("Arial", 11),
            textvariable=day_var
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
            font=("Arial", 11),
            textvariable=hour_var
        )
        hr.pack(fill="x")

        add_label("סיבה / הערה")
        rs = ttk.Entry(form_frame, font=("Arial", 11), textvariable=reason_var)
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

        try:
            with open("data/schedule.json", "r", encoding="utf-8") as f:
                schedule_data = json.load(f)
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בטעינת המערכת: {e}")
            return

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
            text=":בחר יום וכיתה",
            font=("Arial", 11, "bold"),
            bg="#f8fafc",
            fg="#334155"
        ).pack(side="right", padx=10)

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


    def open_moodle_tasks():
        global current_username, current_user_role, current_user_class

        role = current_user_role if 'current_user_role' in globals() else "student"
        username = current_username if 'current_username' in globals() else "תלמיד"
        class_name = current_user_class if 'current_user_class' in globals() else "9th3"

        SERVER_IP = '127.0.0.1'
        PORT = 9999
        fetched_tasks = []

        # ---------------------------------------------------------
        # שלב א': שליפת המשימות האמיתיות מהשרת בזמן אמת
        # ---------------------------------------------------------
        try:
            with create_secure_socket() as s:
                s.connect((SERVER_IP, PORT))
                request_msg = f"get_moodle_tasks|{class_name}|{username}|{role}"
                s.sendall(request_msg.encode('utf-8'))
                
                raw_data = s.recv(4096) # שימוש בבאפר גדול יותר עבור ה-JSON
                if raw_data:
                    dataFromServer = raw_data.decode('utf-8').strip()
                    if dataFromServer.startswith("get_moodle_tasks_response|success|"):
                        json_str = dataFromServer.split("|", 2)[2]
                        fetched_tasks = json.loads(json_str)
        except Exception as e:
            print(f"גילוי שגיאה בטעינת נתונים: {e}")
            # במקרה של שגיאה הרשימה תישאר ריקה ולא תתקע את פתיחת החלון

        # ---------------------------------------------------------
        # שלב ב': בניית ממשק המשתמש (UI)
        # ---------------------------------------------------------
        new_win = tk.Toplevel()
        new_win.title("מרכז משימות ולמידה דיגיטלית")

        width, height = 550, 750
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=510, height=710)

        header_color = "#0369a1" 
        header_frame = tk.Frame(main_frame, bg=header_color, height=130)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="🎓", font=("Arial", 32), fg="white", bg=header_color).pack(pady=(10, 0))

        title_text = "ניהול והעלאת קישורי משימות" if "teacher" in role or "מורה" in role else "משימות ומטלות פתוחות"
        tk.Label(header_frame, text=title_text, font=("Arial", 18, "bold"), fg="white", bg=header_color).pack()
        tk.Label(header_frame, text=f"{username} שלום (כיתה {class_name})", font=("Arial", 11), fg="#e0f2fe", bg=header_color).pack()

        # --- מסך מורה ---
        if "teacher" in role or "מורה" in role:
            form_frame = tk.LabelFrame(main_frame, text=" יצירת משימה חדשה לכיתה ", font=("Arial", 11, "bold"), bg="white", fg="#0369a1", padx=15, pady=15)
            form_frame.pack(fill="x", padx=20, pady=20)

            tk.Label(form_frame, text="שם המשימה / נושא הלימוד:", font=("Arial", 11), bg="white", fg="#334155").pack(anchor="e", pady=(0, 2))
            task_name_entry = tk.Entry(form_frame, font=("Arial", 12), bg="#f8fafc", bd=1, relief="solid", justify="right")
            task_name_entry.pack(fill="x", pady=(0, 15))

            tk.Label(form_frame, text="קישור למטלה (אופק מטח / Moodle / סרטון):", font=("Arial", 11), bg="white", fg="#334155").pack(anchor="e", pady=(0, 2))
            task_url_entry = tk.Entry(form_frame, font=("Arial", 11), bg="#f8fafc", bd=1, relief="solid", justify="left")
            task_url_entry.insert(0, "https://")
            task_url_entry.pack(fill="x", pady=(0, 15))

            def publish_task():
                name = task_name_entry.get().strip()
                url = task_url_entry.get().strip()
                if not name or url == "https://" or not url:
                    tk.messagebox.showwarning("שדה חסר", "אנא מלא שם משימה וקישור תקין")
                    return
                
                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        subject = f"publish_moodle_task|{class_name}|{url}|{name}"
                        s.sendall(subject.encode('utf-8'))

                        while True:
                            raw_data = s.recv(1024)
                            if not raw_data: break
                            dataFromServer = raw_data.decode('utf-8').strip()

                            if dataFromServer.startswith("publish_moodle_task_response|"):
                                parts = dataFromServer.split("|")
                                if len(parts) > 1 and parts[1] == "success":
                                    tk.messagebox.showinfo("משימה פורסמה", f"המשימה '{name}' פורסמה בהצלחה!")
                                    new_win.destroy() # סגירה ורענון החלון
                                    open_moodle_tasks()
                                else:
                                    tk.messagebox.showerror("שגיאה", "השרת נתקל בשגיאה בעת שמירת המשימה.")
                                break
                except Exception as e:
                    tk.messagebox.showerror("שגיאה", f"אירעה שגיאה בתקשורת: {e}")

            publish_btn = tk.Button(form_frame, text="➕ פרסם קישור למשימה", font=("Arial", 12, "bold"), bg="#10b981", fg="white", bd=0, cursor="hand2", command=publish_task, pady=8)
            publish_btn.pack(fill="x")

            tk.Label(main_frame, text="משימות פעילות כרגע בכיתה:", font=("Arial", 12, "bold"), bg="white", fg="#1e293b").pack(anchor="e", padx=25, pady=(10, 5))
            
            # לולאה דינמית על המשימות שהתקבלו מהשרת
            for index, task in enumerate(fetched_tasks):
                t_name = task.get("name", "משימה ללא שם")
                t_url = task.get("url", "#")
                row_bg = "#f8fafc" if index % 2 == 0 else "white"
                t_row = tk.Frame(main_frame, bg=row_bg, height=45)
                t_row.pack(fill="x", padx=20, pady=2)
                t_row.pack_propagate(False)

                tk.Label(t_row, text=f"• {t_name}", font=("Arial", 11), fg="#475569", bg=row_bg).pack(side="right", padx=10, pady=10)
                tk.Button(t_row, text="פתח קישור 🔗", font=("Arial", 9), fg="#2563eb", bg=row_bg, bd=0, cursor="hand2", command=lambda url=t_url: webbrowser.open(url)).pack(side="left", padx=10, pady=8)

        # --- מסך תלמיד ---
        else:
            # חישוב אחוזים דינמי
            total_tasks = len(fetched_tasks)
            completed_tasks = sum(1 for t in fetched_tasks if t.get("status") == "✅ בוצע")
            pct = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 100

            progress_frame = tk.Frame(main_frame, bg="#f0fdf4", bd=0, height=50)
            progress_frame.pack(fill="x", padx=20, pady=15)
            progress_frame.pack_propagate(False)
            
            tk.Label(
                progress_frame, 
                text=f"📈 הספק המשימות השבוע: {completed_tasks} מתוך {total_tasks} בוצעו ({pct}%)", 
                font=("Arial", 11, "bold"), fg="#166534", bg="#f0fdf4"
            ).pack(side="right", padx=15, pady=15)

            tk.Label(main_frame, text="רשימת קישורים ומטלות לביצוע:", font=("Arial", 12, "bold"), bg="white", fg="#1e293b").pack(anchor="e", padx=22, pady=(5, 5))

            def toggle_status(btn, task_obj):
                # כאן תוכל בהמשך להוסיף שליחה לשרת כדי לעדכן באמת ב-JSON, כרגע זה משנה לוקאלית בחלון
                if btn.cget("text") == "❌ לא בוצע":
                    btn.config(text="✅ בוצע", bg="#10b981", activebackground="#10b981")
                    task_obj["status"] = "✅ בוצע"
                else:
                    btn.config(text="❌ לא בוצע", bg="#f43f5e", activebackground="#f43f5e")
                    task_obj["status"] = "❌ לא בוצע"

            # לולאה דינמית על משימות התלמיד מהשרת
            for index, task in enumerate(fetched_tasks):
                title = task.get("name", "משימה כללית")
                link_url = task.get("url", "#")
                start_status = task.get("status", "❌ לא בוצע") # ברירת מחדל אם אין סטטוס ב-JSON
                start_color = "#10b981" if start_status == "✅ בוצע" else "#f43f5e"

                row_bg = "#f8fafc" if index % 2 == 0 else "white"
                item_row = tk.Frame(main_frame, bg=row_bg, height=65)
                item_row.pack(fill="x", padx=20, pady=4)
                item_row.pack_propagate(False)

                text_sub_frame = tk.Frame(item_row, bg=row_bg)
                text_sub_frame.pack(side="right", padx=10, pady=10)
                tk.Label(text_sub_frame, text=title, font=("Arial", 11, "bold"), fg="#1e293b", bg=row_bg).pack(anchor="e")

                status_btn = tk.Button(item_row, text=start_status, font=("Arial", 10, "bold"), fg="white", bg=start_color, activebackground=start_color, bd=0, width=10, cursor="hand2")
                status_btn.config(command=lambda b=status_btn, t=task: toggle_status(b, t))
                status_btn.pack(side="left", padx=10, pady=18)

                link_btn = tk.Button(item_row, text="🔗 פתח משימה", font=("Arial", 10, "bold"), fg="white", bg="#2563eb", bd=0, cursor="hand2", command=lambda url=link_url: webbrowser.open(url))
                link_btn.pack(side="left", padx=5, pady=18)

        close_btn = tk.Button(main_frame, text="סגור חלון", font=("Arial", 12, "bold"), bg="#f1f5f9", fg="#475569", bd=0, cursor="hand2", command=new_win.destroy)
        close_btn.pack(side="bottom", fill="x", padx=20, pady=20)
    
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
                        messagebox.showerror("שגיאה!", "שגיאת שרת")
                        break

        except ConnectionRefusedError:
            messagebox.showerror("שגיאה", "לא ניתן להתחבר לשרת. וודא שהוא פועל.")
            
        except Exception as e:
            messagebox.showerror("שגיאה", f"אירעה שגיאה: {e}")
        
        role = current_user_role if 'current_user_role' in globals() else "student"
        username = current_username if 'current_username' in globals() else "תלמיד"

        new_win = tk.Toplevel()
        new_win.title("מערכת נוכחות - משוב")
        destroy_and_set_new_window(new_win)

        width, height = 550, 750
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        new_win.geometry(f"{width}x{height}+{x}+{y}")
        new_win.configure(bg="#f0f4f8")
        new_win.resizable(False, False)

        main_frame = tk.Frame(new_win, bg="white")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=510, height=710)

        header_color = "#0284c7" if "teacher" in role or "מורה" in role else "#0ea5e9"
        header_frame = tk.Frame(main_frame, bg=header_color, height=130)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📝",
            font=("Arial", 32),
            fg="white",
            bg=header_color
        ).pack(pady=(10, 0))

        title_text = "ניהול נוכחות כיתתית" if "teacher" in role or "מורה" in role else "מצב נוכחות אישי"
        tk.Label(
            header_frame,
            text=title_text,
            font=("Arial", 20, "bold"),
            fg="white",
            bg=header_color
        ).pack()

        subtitle_text = f"משתמש מחובר: {username}"
        tk.Label(
            header_frame,
            text=subtitle_text,
            font=("Arial", 11),
            fg="#e0f2fe",
            bg=header_color
        ).pack()

        subjects_list = ["שיעור מתמטיקה", "שיעור נביא", "שיעור גמרא", "שיעור אנגלית", "שיעור עברית", "שיעור לשון", "שיעור היסטוריה", "שיעור מדעים", "שיעור תורה", "שיעור ספורט"]

        if "teacher" in role or "מורה" in role:
            class_frame = tk.Frame(main_frame, bg="#f8fafc", height=45)
            class_frame.pack(fill="x", padx=15, pady=15)
            class_frame.pack_propagate(False)
            
            tk.Label(
                class_frame, 
                text=f":בחר מקצוע", 
                font=("Arial", 11, "bold"), 
                fg="#1e293b", 
                bg="#f8fafc"
            ).pack(side="right", padx=(10, 5), pady=10)

            teacher_subject_var = tk.StringVar(value=subjects_list[0])
            subject_dropdown = ttk.Combobox(
                class_frame, 
                textvariable=teacher_subject_var, 
                values=subjects_list, 
                state="readonly", 
                width=12,
                font=("Arial", 10)
            )
            subject_dropdown.pack(side="right", padx=5, pady=10)

            labels_frame = tk.Frame(main_frame, bg="white")
            labels_frame.pack(fill="x", padx=20)
            tk.Label(labels_frame, text="שם התלמיד", font=("Arial", 11, "bold"), fg="#64748b", bg="white").pack(side="right")
            tk.Label(labels_frame, text="סטטוס הגעה וציוד", font=("Arial", 11, "bold"), fg="#64748b", bg="white").pack(side="left", padx=55)

            students = class_students if class_students else ["שגיאה בטעינת תלמידי הכיתה", "שגיאה בטעינת תלמידי הכיתה", "שגיאה בטעינת תלמידי הכיתה", "שגיאה בטעינת תלמידי הכיתה", "שגיאה בטעינת תלמידי הכיתה", "שגיאה בטעינת תלמידי הכיתה"]
            attendance_vars = {}

            for index, student_name in enumerate(students):
                row_bg = "#f8fafc" if index % 2 == 0 else "white"
                row_frame = tk.Frame(main_frame, bg=row_bg, height=50)
                row_frame.pack(fill="x", padx=15, pady=2)
                row_frame.pack_propagate(False)

                tk.Label(
                    row_frame, 
                    text=student_name, 
                    font=("Arial", 12), 
                    fg="#334155", 
                    bg=row_bg
                ).pack(side="right", padx=10, pady=12)

                status_var = tk.StringVar(value="נוכח")
                attendance_vars[student_name] = status_var

                btn_container = tk.Frame(row_frame, bg=row_bg)
                btn_container.pack(side="left", padx=5, pady=10)

                options = [
                    ("חוסר ציוד", "#3B50C5"), 
                    ("חיסור", "#ef4444"), 
                    ("איחור", "#f59e0b"), 
                    ("נוכח", "#10b981")
                ]
                
                for text, active_color in options:
                    rb = tk.Radiobutton(
                        btn_container,
                        text=text,
                        variable=status_var,
                        value=text,
                        indicatoron=0, 
                        font=("Arial", 9, "bold"),
                        fg="#475569",
                        bg="#e2e8f0",
                        selectcolor=active_color,
                        activebackground=active_color,
                        bd=0,
                        width=7,
                        cursor="hand2"
                    )
                    rb.pack(side="left", padx=1)

            def save_attendance_action():
                selected_sub = teacher_subject_var.get()
                
                # 1. מפת כיתות מקומית כדי לתרגם את השם עבור השרת וה-JSON (למשל "ט3" ל-"9th3")
                class_map = {
                    "ז1": "7th1", "ז2": "7th2", "ז3": "7th3", "ז4": "7th4", "ז5": "7th5", "ז6": "7th6",
                    "ח1": "8th1", "ח2": "8th2", "ח3": "8th3", "ח4": "8th4", "ח5": "8th5", "ח6": "8th6",
                    "ט1": "9th1", "ט2": "9th2", "ט3": "9th3", "ט4": "9th4", "ט5": "9th5", "ט6": "9th6",
                    "י1": "10th1", "י2": "10th2", "י3": "10th3", "י4": "10th4", "י5": "10th5", "י6": "10th6",
                    "יא1": "11th1", "יא2": "11th2", "יא3": "11th3", "יא4": "11th4", "יא5": "11th5", "יא6": "11th6",
                    "יב1": "12th1", "יב2": "12th2", "יב3": "12th3", "יב4": "12th4", "יב5": "12th5", "יב6": "12th6"
                }
                server_class_name = class_map.get(current_user_class, current_user_class)
                
                attendance_records = []
                for s_name, s_var in attendance_vars.items():
                    attendance_records.append(f"{s_name}:{s_var.get()}")
                attendance_data_str = ",".join(attendance_records)
                
                SERVER_IP = '127.0.0.1' 
                PORT = 9999
                
                try:
                    with create_secure_socket() as s:
                        s.connect((SERVER_IP, PORT))
                        
                        msg = f"save_attendance|{server_class_name}|{selected_sub}|{attendance_data_str}"
                        s.sendall(msg.encode('utf-8'))
                        
                        raw_response = s.recv(1024)
                        if raw_response:
                            response = raw_response.decode('utf-8').strip()
                            if response == "save_attendance_response|success":
                                messagebox.showinfo("הצלחה", f"יומן הנוכחות עבור שיעור {selected_sub} נשמר בהצלחה בשרת!")

                            else:
                                messagebox.showerror("שגיאה", "השרת נכשל בשמירת הנתונים בקובץ.")
                        else:
                            messagebox.showerror("שגיאה", "לא התקבלה תגובה מהשרת.")
                            
                except Exception as e:
                    messagebox.showerror("שגיאה", f"שגיאת תקשורת עם השרת: {e}")

            save_btn = tk.Button(
                main_frame,
                text="💾 שמור נוכחות ביומן",
                font=("Arial", 14, "bold"),
                bg="#0284c7",
                fg="white",
                bd=0,
                cursor="hand2",
                command=save_attendance_action
            )
            save_btn.pack(side="bottom", fill="x", padx=20, pady=20)
            
            tk.Button(
                main_frame,
                text="חזרה למסך ראשי",
                command=lambda: open_main_page(current_username),
                font=("Arial", 13, "bold"),
                bg="#1a73e8",
                fg="white",
                relief="flat",
                bd=0,
                cursor="hand2"
            ).pack(side="bottom", pady=15, ipadx=18, ipady=4)

        else:
            stats_frame = tk.Frame(main_frame, bg="white")
            stats_frame.pack(fill="x", padx=10, pady=15)
            stats_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="equal")

            cards_data = [
                ("נוכחות", "92%", "#e0f2fe", "#0369a1"),
                ("איחורים", "2", "#fef3c7", "#b45309"),
                ("חיסורים", "1", "#fee2e2", "#b91c1c"),
                ("חוסר ציוד", "3", "#f3e8ff", "#6b21a8"), 
                ("מוצדק", "2", "#f1f5f9", "#475569")
            ]

            for i, (label, val, bg_c, fg_c) in enumerate(cards_data):
                card = tk.Frame(stats_frame, bg=bg_c, bd=0, height=75)
                card.grid(row=0, column=i, padx=3)
                card.pack_propagate(False)

                tk.Label(card, text=val, font=("Arial", 16, "bold"), fg=fg_c, bg=bg_c).pack(pady=(10, 0))
                tk.Label(card, text=label, font=("Arial", 9, "bold"), fg=fg_c, bg=bg_c).pack()

            # אזור סנן המקצועות החכם של התלמיד
            filter_frame = tk.Frame(main_frame, bg="white")
            filter_frame.pack(fill="x", padx=20, pady=(10, 5))

            tk.Label(
                filter_frame, 
                text="היסטוריית אירועי נוכחות", 
                font=("Arial", 13, "bold"), 
                fg="#1e293b", 
                bg="white"
            ).pack(side="right")

            tk.Label(filter_frame, text=":סנן לפי מקצוע",
                     font=("Arial", 10),
                     fg="#64748b",
                     bg="white").pack(side="left", padx=(5, 2))
            
            student_filter_var = tk.StringVar(value="הכול")
            filter_dropdown = ttk.Combobox(
                filter_frame, 
                textvariable=student_filter_var, 
                values=["הכול"] + subjects_list, 
                state="readonly", 
                width=10,
                font=("Arial", 10)
            )
            filter_dropdown.pack(side="left")

            history_container = tk.Frame(main_frame, bg="white")
            history_container.pack(fill="both", expand=True, padx=5)
            
            SERVER_IP = '127.0.0.1' 
            PORT = 9999

            history_events = []

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
                            messagebox.showerror("שגיאה", f"שגיאת שרת: {parts[2]}")
                        else:
                            messagebox.showerror("שגיאה", f"תגובה לא צפויה מהשרת: {response}")
                            
                    elif len(parts) >= 2 and parts[0] == "get_attendance_response":
                        parts_limited = response.split("|", 1)
                        history_events = json.loads(parts_limited[1])
                        
                    elif parts[0] == "SUCCESS":
                        parts_limited = response.split("|", 1)
                        history_events = json.loads(parts_limited[1])
                    elif parts[0] == "ERROR":
                        parts_limited = response.split("|", 1)
                        messagebox.showerror("שגיאה", f"שגיאת שרת: {parts_limited[1]}")
                        
                    else:
                        try:
                            history_events = json.loads(response)
                        except json.JSONDecodeError:
                            messagebox.showerror("שגיאה", f"תגובה לא מוכרת מהשרת: {response}")
                else:
                    messagebox.showerror("שגיאה", "לא התקבלה תגובה מהשרת.")

            def update_filtered_history(event=None):
                for widget in history_container.winfo_children():
                    widget.destroy()

                selected_filter = student_filter_var.get()
                row_index = 0

                for event_data in history_events:
                    subject = event_data.get("subject", "שיעור כללי")
                    date = event_data.get("date", "")
                    status = event_data.get("status", "")
                    
                    if "חיסור" in status or "חוסר" in status:
                        status_color = "#ef4444" 
                    elif "איחור" in status:
                        status_color = "#f59e0b" 
                    else:
                        status_color = "#10b981" 

                    if selected_filter == "הכול" or subject == selected_filter:
                        row_bg = "#f8fafc" if row_index % 2 == 0 else "white"
                        event_row = tk.Frame(history_container, bg=row_bg, height=42)
                        event_row.pack(fill="x", padx=15, pady=2)
                        event_row.pack_propagate(False)

                        tk.Label(
                            event_row, 
                            text=f"{subject}   •   {date}", 
                            font=("Arial", 11, "bold" if "חיסור" in status or "חוסר" in status else "normal"), 
                            fg="#334155", 
                            bg=row_bg
                        ).pack(side="right", padx=15, pady=9)

                        tk.Label(
                            event_row, 
                            text=status, 
                            font=("Arial", 11, "bold"), 
                            fg=status_color, 
                            bg=row_bg
                        ).pack(side="left", padx=15, pady=9)
                        
                        row_index += 1

            filter_dropdown.bind("<<ComboboxSelected>>", update_filtered_history)
            
            update_filtered_history()

            close_btn = tk.Button(
                main_frame,
                text="סגור חלון",
                font=("Arial", 12, "bold"),
                bg="#f1f5f9",
                fg="#475569",
                bd=0,
                cursor="hand2",
                command=new_win.destroy
            )
            close_btn.pack(side="bottom", fill="x", padx=20, pady=15)
        
    
    if __name__ == "__main__":
        open_splash_screen()
        

except KeyboardInterrupt:
    print("Keyboard Interrupt. QUITING!")
except ModuleNotFoundError:
    print(f"module not found")
except ConnectionAbortedError:
    print("connection abborted")
try:
    import os
    import ssl
    import socket
    import json
    import datetime
    import threading
    from utils import hashingAlg

    print(os.getcwd())

    class Server:
        def __init__(self, host='0.0.0.0', port=9999):
            self.host = host
            self.port = port
            self.failed_attempts_tracker = {}
            self.attempts_lock = threading.Lock()
            self.db_lock = threading.Lock() 
            self.attempt_limit = 4

        def load_users(self):
            with self.db_lock:
                try:
                    print("[+] oppening data/users.json and reading it")
                    with open("data/users.json", "r", encoding="utf-8") as f:
                        print("[+] successfuly oppend data/users.json")
                        print("[+] returing the data of users")
                        return json.load(f)
                    
                except FileNotFoundError:
                    print("Error: data/users.json not found. Please create it.")
                    return {}
                
                except Exception as e:
                    print(f"Error loading users: {e}")
                    return {}

        def log_connection(self, addr, username, status):
            with self.db_lock:
                print("[+] oppening data/server_connection_logs.json")
                with open("data/server_connection_logs.json", "a", encoding="utf-8") as f:
                    print("[+] successfuly oppend data/server_connection_logs.json")
                    log_fields = {
                        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "address": str(addr),
                        "username": username,
                        "status": status
                    }
                    
                    print(f"[+] writing a connection log for client: {addr}")
                    f.write(json.dumps(log_fields, ensure_ascii=False) + "\n")
                    print("[+] completed writing the connection log.")

        def handle_login(self, conn, addr, dataFromClient):
            print("[+] handling log in")
            client_ip = addr[0]
            parts = dataFromClient.split("|")
            
            if len(parts) < 3:
                print(f"[+] sending '400 bad request' to client: {addr}")
                conn.sendall("400 bad request".encode('utf-8'))
                return

            print("[+] getting username + password from client")
            username = parts[1]
            passwordFromClient = parts[2]
            print("[+] successfuly got the username + password from the client")
            
            with self.attempts_lock:
                current_attempts = self.failed_attempts_tracker.get(client_ip, 0)
            
            if current_attempts >= self.attempt_limit:
                print("[*] attempt limit reached detected!")
                print("[*] blocking attemptor")
                conn.sendall("attempt limit reached".encode("utf-8"))
                print(f"[+] successfuly blocked login attempt from client: {client_ip} hint: (Limit reached)")
                return

            print("[+] loading users")
            users = self.load_users()
            print("[+] successfully loaded users")
            
            status = "failed"
            if username in users:
                print("[+] username is in users")
                print("[+] collecting user's data")
                userData = users[username]
                storedPassword = userData.get("password", "")
                print("[+] sucessfuly collected user's data")
                
                if ":" in storedPassword:
                    print("[+] found that ':' is in user's data")
                    salt_hex, stored_hash_hex = storedPassword.split(":")
                    salt = bytes.fromhex(salt_hex)
                    stored_hash = bytes.fromhex(stored_hash_hex)
                    
                    if hashingAlg.verify_password(salt, stored_hash, passwordFromClient):
                        print("[+] login suuccesful")
                        print(f"[+] sending '200 ok' to client: {addr}")
                        print("[+] getting user's role")
                        role = userData.get("role", "student") 
                        print("[+] getting user's class name")
                        class_name = userData.get("class", "unknown")
                        print("[+] sending client his role|class name")
                        conn.sendall(f"200 ok|{role}|{class_name}".encode("utf-8"))
                        print("[+] successfuly sent client his role|class name")
                        print("[*] status is success")
                        status = "success"
                        
                        with self.attempts_lock:
                            self.failed_attempts_tracker[client_ip] = 0
                    else:
                        self._send_unauthorized(conn, addr, client_ip)
                else:
                    self._send_unauthorized(conn, addr, client_ip)
            else:
                self._send_unauthorized(conn, addr, client_ip)

            self.log_connection(addr, username, status)

        def _send_unauthorized(self, conn, addr, client_ip):
            print(f"[+] sending '401 unauthorized' to client: {addr}")
            conn.sendall("401 unauthorized".encode('utf-8'))
            print(f"[+] successfuly sent 401 unauthorized to client: {addr}")
            with self.attempts_lock:
                print("[+] updating attempts lock")
                self.failed_attempts_tracker[client_ip] = self.failed_attempts_tracker.get(client_ip, 0) + 1
                print("[+] geting faild attempt")
                print(f"[+] Failed attempt {self.failed_attempts_tracker[client_ip]} from {client_ip}")

        def handle_signup(self, conn, addr, dataFromClient):
            parts = dataFromClient.split("|")
            
            if len(parts) != 10:
                print("[*] found that the length of the request from the client is not equle to 10")
                print(f"[+] sending '400 bad request' to client: {addr}. hint: (check length of client request)")
                conn.sendall("400 bad request".encode('utf-8'))
                print(f"successfuly sent 400 bad request to client: {addr}")
                return

            print("[+] analyzing the data")
            firstName, lastName, gmail, newUsername, newPassword = parts[1:6]
            print(f"[+] done analyzing the data from user: {addr}")
            
            print("[+] getting class map")
            class_map = {
                "ז1": "7th1", "ז2": "7th2", "ז3": "7th3",
                "ז4": "7th4", "ז5": "7th5", "ז6": "7th6",

                "ח1": "8th1", "ח2": "8th2", "ח3": "8th3",
                "ח4": "8th4", "ח5": "8th5", "ח6": "8th6",

                "ט1": "9th1", "ט2": "9th2", "ט3": "9th3",
                "ט4": "9th4", "ט5": "9th5", "ט6": "9th6",

                "י1": "10th1", "י2": "10th2", "י3": "10th3",
                "י4": "10th4", "י5": "10th5", "י6": "10th6",

                "יא1": "11th1", "יא2": "11th2", "יא3": "11th3",
                "יא4": "11th4", "יא5": "11th5", "יא6": "11th6",

                "יב1": "12th1", "יב2": "12th2", "יב3": "12th3",
                "יב4": "12th4", "יב5": "12th5", "יב6": "12th6"
            }

            
            print("[+] getting user's class name|role|access code|new class code?. hint: (is student?)")
            class_raw = parts[6].strip()
            class_name = class_map.get(class_raw, class_raw)
            role = parts[7]
            access_code = parts[8]
            class_code = parts[9]
            hashed_access_code_from_client = hashingAlg.hash_password_no_salt(access_code)
            hashed_class_access_code_from_client = hashingAlg.hash_password_no_salt(class_code)
            
            print("[+] getting current time")
            timeCreated = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"[+] time requested creation is: '{timeCreated}'")

            print("[+] opening data/users.json")
            with self.db_lock:
                try:
                    with open("data/users.json", "r", encoding='utf-8') as f:
                        print("[+] getting global users data")
                        global_users = json.load(f)
                        print("[+] sucessfuly got global users data")
                        
                except FileNotFoundError:
                    print("[*] did not find file data/users.json")
                    print("[*] assinging an empty list")
                    global_users = {}
                    
                for u_name, data in global_users.items():
                    if data.get("gmail_account") == gmail:
                        print(f"[+] found email for user: {u_name}")
                        print(f"[+] sending gmail already exists to client: {addr}")
                        conn.sendall("gmail already exists".encode('utf-8'))
                        print(f"[+] successfuly sent gmail already exists to client: {addr}")
                        return

                if newUsername in global_users:
                    print("[+] found that username is in use")
                    print(f"[+] sending username already exists to client: {addr}")
                    conn.sendall("username already exists".encode('utf-8'))
                    print(f"[+] successfuly sent username already exists to client: {addr}")
                    return
            
            try:
                if role == "teacher":
                    print("[*] getting teachers code")
                    print("[+] opening teacher waitlist codes file")
                    
                    with open("keys/teacher_wait_list_keys.json", mode="r", encoding='utf-8') as f:
                        data = json.load(f)
                        
                        if class_name in data:
                            if data[class_name]["code"].strip() == "":
                                conn.sendall("invalid teacher code".encode('utf-8'))
                                return
                            
                            print("[+] found class name in teacher codes waitlist file")
                            hashed_teacher_waitlist_code = data[class_name]["code"].strip()
                            
                        else:
                            print("[-] class name not found in file")
                            conn.sendall("404".encode('utf-8'))
                            print("[+] successfuly sent client a 404 not found. hint: (class not found in teacher codes waitlist file)")
                            return
                    
            except FileNotFoundError:
                print("[-] Error: keys/teacher_wait_list_keys.json not found")
                return
                
            except json.JSONDecodeError:
                print("[-] Error: Failed to decode JSON")
                return
            
            try:  
                print("[+] oppening keys/students.key. hint: (students code file)")
                with open("data/aval_class_codes.json", "r", encoding='utf-8') as f:  
                    print("[+] successfuly opened keys/students.key. hint: (students code file)")
                    print("[*] getting students code")
                    class_codes_from_file = json.load(f)
                    print("[+] got students code")
                
                class_info = class_codes_from_file.get(class_name.strip())
                
                if class_info and role != "teacher":
                    hashed_current_class_code = class_info.get("class code", 0)
                
                elif role == "teacher":
                    pass
                
                else:
                    print("[+] class does not exists.")
                    print("[=] sending 404 to client. hint: (class does not exists)")
                    conn.sendall("404".encode("utf-8"))
                    print("[+] sent.")
                    return 
                        
            except FileNotFoundError:
                print("[-] Key files missing!")
                print("[*] sending ")
                conn.sendall("error|server configuration error".encode("utf-8"))
                print("[*] successfuly sent client side a server config error")
                return

            if role == "teacher" and hashed_access_code_from_client != hashed_teacher_waitlist_code:
                conn.sendall("invalid teacher code".encode("utf-8"))
                return
            
            elif role == "student" and hashed_class_access_code_from_client != hashed_current_class_code:
                conn.sendall("invalid student code".encode("utf-8"))
                return
            
            elif role not in ["teacher", "student"]:
                conn.sendall("invalid role?".encode("utf-8"))
                return
            
            class_dir = f"classesStudents/{class_name}"
            client_class_name = class_name
            class_file_path = f"{class_dir}/students-{class_name}.json"
            group_chat_path = f"{class_dir}/group_chat-{class_name}.json"
            freer_requests_path = f"{class_dir}/freerrequests-{class_name}.json"

            with self.db_lock:
                os.makedirs(class_dir, exist_ok=True)

                try:
                    with open(class_file_path, "r", encoding='utf-8') as f:
                        class_users = json.load(f)
                        
                    if isinstance(class_users, list):
                        class_users = {u.get("username", str(i)): u for i, u in enumerate(class_users)}
                        
                    teacher_exists = any(user.get('role') == 'teacher' for user in class_users.values())
                    if teacher_exists and role == "teacher":
                        conn.sendall("teacher allready exists in this class".encode('utf-8'))
                        return

                except (FileNotFoundError, json.JSONDecodeError):
                    if role != "teacher":
                        print(f"[+] Class {class_name} not found.")
                        conn.sendall("404".encode('utf-8'))
                        return
                    class_users = {}

                if not os.path.exists(group_chat_path):
                    try:
                        with open(group_chat_path, "w", encoding='utf-8') as f:
                            json.dump({}, f, ensure_ascii=False, indent=4)
                        print(f"[+] Created group chat file for {class_name}")
                    except Exception as e:
                        print(f"[-] Error creating group chat file: {e}")
                        
                if not os.path.exists(freer_requests_path):
                    try:
                        with open(freer_requests_path, "w", encoding='utf-8') as f:
                            json.dump({}, f, ensure_ascii=False, indent=4)
                        print(f"[+] Created freer requests file for {class_name}")
                    except Exception as e:
                        print(f"[-] Error creating freer requests file: {e}")

                          
                class_users[newUsername] = {
                    "id": len(class_users) + 1,
                    "first_name": firstName,
                    "last_name": lastName,
                    "gmail_account": gmail,
                    "role": role,
                    "class": class_name,
                    "tasks": [],
                    "created_at": timeCreated,
                    "grades": [] if role == "student" else "is teacher"
                    }
                
                os.makedirs(os.path.dirname(class_file_path), exist_ok=True)
                with open(class_file_path, "w", encoding='utf-8') as f:
                    json.dump(class_users, f, indent=4, ensure_ascii=False)
                    print(f"[+] successfully updated class file for {class_name}")

                with open("data/users.json", "w", encoding='utf-8') as f:
                    salt, hashed_tuple = hashingAlg.hash_new_password(newPassword)
                    password_to_save = f"{salt.hex()}:{hashed_tuple.hex()}"
                    
                    global_users[newUsername] = {
                        "id": len(global_users) + 1,
                        "password": password_to_save,
                        "first_name": firstName,
                        "last_name": lastName,
                        "gmail_account": gmail,
                        "role": role,
                        "class": class_name,
                        "created_at": timeCreated
                    }        
                    
                    json.dump(global_users, f, indent=4,  ensure_ascii=False)    
                
            with self.db_lock:
                if role == "teacher":
                    with open("data/aval_class_codes.json", "r", encoding="utf-8") as file:
                        codes_from_file = json.load(file)
                    
                    if class_name in codes_from_file:
                        conn.sendall("codeexsists".encode("utf-8"))
                        return

                    with open("data/aval_class_codes.json", "w", encoding='utf-8') as f:
                        new_code_field = {
                            class_name: {
                                "teacher": firstName,
                                "class code": hashed_class_access_code_from_client,
                                "username": newUsername,
                                "gmail account": gmail,
                            }
                        }
                        
                        codes_from_file.update(new_code_field)
                        
                        json.dump(codes_from_file, f, indent=4, ensure_ascii=False)
                
            if role == "teacher":
                with self.db_lock:
                    with open("keys/teacher_wait_list_keys.json", "r", encoding='utf-8') as f: 
                        data_from_teacher_wait_list = json.load(f)                      

                    data_from_teacher_wait_list[class_name]["code"] = ""                      

                    with open("keys/teacher_wait_list_keys.json", "w", encoding='utf-8') as f:  
                        json.dump(data_from_teacher_wait_list, f, indent=4, ensure_ascii=False) 
                    
                    with open(f"classesStudents/{client_class_name}/doar_masseges-{client_class_name}.json", "w", encoding='utf-8') as f:
                        json.dump([], f)
                        
            conn.sendall(f"200 ok|{role}|{class_name}".encode('utf-8'))
            return

        def handle_class_chat(self, conn, dataFromClient):
            parts = dataFromClient.split("|", 3)
            if len(parts) < 4:
                conn.sendall("400 bad request".encode('utf-8'))
                return
            
            class_name, username, message = parts[1], parts[2], parts[3]


        def handle_get_schedule(self, conn, dataFromClient):
            class_name = dataFromClient.split("|")[1]
            try:
                with self.db_lock:
                    with open("data/schedule.json", "r", encoding="utf-8") as f:
                        schedules = json.load(f)
                        class_schedule = schedules.get(class_name, {})
                        conn.sendall(json.dumps(class_schedule, ensure_ascii=False).encode('utf-8'))
          
            except FileNotFoundError:
                conn.sendall("error|file not found".encode('utf-8'))

        def handle_get_tasks(self, conn, dataFromClient):
            parts = dataFromClient.split("|")
            class_name, username = parts[1], parts[2]
            
            with self.db_lock:
                try:
                    with open(f"classesStudents/{class_name}/students-{class_name}.json", "r", encoding='utf-8') as f:
                        students = json.load(f)
                        
                        if username in students:
                            print(f"[+] found that '{username}' is in students, proceeding...")
                            raw_tasks = students[username].get("tasks", [])
                            
                            if raw_tasks == "no tasks": tasks_list = [] 
                            elif isinstance(raw_tasks, str): tasks_list = [raw_tasks]  
                            else: tasks_list = raw_tasks
                                
                            response = json.dumps(tasks_list, ensure_ascii=False)
                            conn.sendall(response.encode('utf-8'))
                            
                        else:
                            conn.sendall(f"username: '{username}' is not in this class?!".encode('utf-8'))
                            
                except FileNotFoundError:
                    conn.sendall("error|class file not found".encode('utf-8'))

        def handle_update_tasks(self, conn, dataFromClient):
            parts = dataFromClient.split("|", 3) 
            if len(parts) < 4:
                conn.sendall("400 bad request".encode('utf-8'))
                return

            class_name, username, new_tasks_json = parts[1], parts[2], parts[3]
            file_path = f"classesStudents/{class_name}/students-{class_name}.json"
            
            with self.db_lock:
                try:
                    with open(file_path, "r", encoding='utf-8') as f:
                        all_students = json.load(f)

                    if username in all_students:
                        all_students[username]["tasks"] = json.loads(new_tasks_json)
                        with open(file_path, "w", encoding='utf-8') as f:
                            json.dump(all_students, f, indent=4, ensure_ascii=False)
                        
                        conn.sendall("200 ok".encode('utf-8'))
                        print(f"[+] Tasks updated for {username} in {class_name}")
                    else:
                        conn.sendall("user not found".encode('utf-8'))
                except Exception as e:
                    print(f"[-] Error updating tasks: {e}")
                    conn.sendall(f"error|{e}".encode('utf-8'))
        
        def handle_freer(self, conn, datafromclient):
                    parts = datafromclient.split("|")
                    if len(parts) < 6:
                        conn.sendall("400 bad request".encode('utf-8'))
                        return

                    student_id = parts[1]
                    hour = parts[2]
                    day = parts[3]
                    reason = parts[4]
                    user_class = parts[5]
                    
                    file_path = f"classesStudents/{user_class}/freerrequests-{user_class}.json"
                    
                    with self.db_lock:

                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                all_requests = json.load(f)
                        except (FileNotFoundError, json.JSONDecodeError):
                            all_requests = {}


                        request_id = f"req_{student_id}_{int(datetime.datetime.now().timestamp())}"
                        
                        new_request = {
                            "student_id": student_id,
                            "time": hour,
                            "day": day,
                            "reason": reason,
                            "status": "pending" 
                        }
                        
                        all_requests[request_id] = new_request
                        
                        try:
                            with open(file_path, "w", encoding="utf-8") as f:
                                json.dump(all_requests, f, indent=4, ensure_ascii=False)
                            
                            print(f"[+] Free request {request_id} saved for student {student_id} in class {user_class}")
                            conn.sendall("200 ok".encode('utf-8'))
                            
                        except Exception as e:
                            print(f"[-] Error saving free request: {e}")
                            conn.sendall(f"error|{e}".encode('utf-8'))
        
        def handle_get_freer_requests(self, conn, datafromclient):
            # מנקים רווחים בלתי נראים ושבירות שורה
            clean_data = datafromclient.strip()
            parts = clean_data.split("|")
            
            if len(parts) < 2:
                conn.sendall("400 bad request".encode('utf-8'))
                return
                
            user_class = parts[1].strip() # מנקים רווחים משם הכיתה (למשל מונע בעיות כמו "9th3 ")
            file_path = f"classesStudents/{user_class}/freerrequests-{user_class}.json"
            
            print(f"[DEBUG SERVER] Looking for requests file at: {file_path}")
            
            with self.db_lock:
                try:
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as f:
                            requests_data = f.read()
                        
                        print(f"[+] Sending requests data to teacher for class {user_class}")
                        conn.sendall(f"requests_data|{requests_data}".encode('utf-8'))
                    else:
                        print(f"[-] Requests file not found for class {user_class}. Sending empty JSON.")
                        conn.sendall("requests_data|{}".encode('utf-8'))
                except Exception as e:
                    print(f"[-] Error reading requests file: {e}")
                    conn.sendall(f"error|{e}".encode('utf-8'))


        def handle_update_request_status(self, conn, datafromclient):
            clean_data = datafromclient.strip()
            parts = clean_data.split("|")
            
            if len(parts) < 4:
                print("[DEBUG SERVER] Error: Received update status command with missing parts.")
                conn.sendall("400 bad request".encode('utf-8'))
                return
                
            user_class = parts[1].strip()
            req_id = parts[2].strip()
            new_status = parts[3].strip()
            
            file_path = f"classesStudents/{user_class}/freerrequests-{user_class}.json"
            print(f"[DEBUG SERVER] Attempting to update status. Class: '{user_class}', Req ID: '{req_id}', New Status: '{new_status}'")
            print(f"[DEBUG SERVER] Target file path: '{file_path}'")
            
            with self.db_lock:
                try:
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as f:
                            all_requests = json.load(f)
                        
                        print(f"[DEBUG SERVER] Loaded existing requests keys: {list(all_requests.keys())}")
                        
                        if req_id in all_requests:
                            all_requests[req_id]["status"] = new_status
                            
                            with open(file_path, "w", encoding="utf-8") as f:
                                json.dump(all_requests, f, indent=4, ensure_ascii=False)
                            
                            print(f"[+] [DEBUG SERVER] Successfully updated {req_id} to {new_status} in JSON file!")
                            conn.sendall("200 ok".encode('utf-8'))
                        else:
                            print(f"[-] [DEBUG SERVER] Error: req_id '{req_id}' was NOT found in the JSON keys!")
                            conn.sendall("error|request not found".encode('utf-8'))
                    else:
                        print(f"[-] [DEBUG SERVER] Error: File '{file_path}' does not exist.")
                        conn.sendall("error|file not found".encode('utf-8'))
                except Exception as e:
                    print(f"[-] [DEBUG SERVER] Exception during status update: {e}")
                    conn.sendall(f"error|{e}".encode('utf-8'))
                    

        def handle_get_student_requests(self, conn, datafromclient):
            clean_data = datafromclient.strip()
            parts = clean_data.split("|")
            
            if len(parts) < 3:
                conn.sendall("400 bad request".encode('utf-8'))
                return
                
            user_class = parts[1].strip()
            student_id = parts[2].strip()
            
            file_path = f"classesStudents/{user_class}/freerrequests-{user_class}.json"
            
            with self.db_lock:
                try:
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as f:
                            all_requests = json.load(f)
                        
                        student_requests = {
                            req_id: req_info for req_id, req_info in all_requests.items()
                            if req_info.get("student_id") == student_id
                        }
                        
                        response_json = json.dumps(student_requests, ensure_ascii=False)
                        conn.sendall(f"student_requests_data|{response_json}".encode('utf-8'))
                    else:
                        conn.sendall("student_requests_data|{}".encode('utf-8'))
                except Exception as e:
                    print(f"[-] Error getting requests for student {student_id}: {e}")
                    conn.sendall(f"error|{e}".encode('utf-8'))
        
        def handle_send_chat_message(self, conn, dataFromClient):
            # פורמט בקשה מעודכן: send_chat_message|class_name|username|role|message
            parts = dataFromClient.split("|", 4)
            if len(parts) < 5:
                conn.sendall("400 bad request".encode('utf-8'))
                return
            
            class_name = parts[1].strip()
            username = parts[2].strip()
            role = parts[3].strip()
            message = parts[4].strip()
            
            os.makedirs("data/chats", exist_ok=True)
            file_path = f"data/chats/{class_name}.json"
            
            with self.db_lock:
                try:
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as f:
                            chat_history = json.load(f)
                    else:
                        chat_history = []
                except Exception:
                    chat_history = []
                
                new_msg = {
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "username": username,
                    "role": role, # הוספנו שמירת תפקיד
                    "message": message
                }
                chat_history.append(new_msg)
                
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(chat_history, f, indent=4, ensure_ascii=False)
                    conn.sendall("200 ok".encode('utf-8'))
                except Exception as e:
                    conn.sendall(f"error|{e}".encode('utf-8'))

        def handle_get_chat_history(self, conn, dataFromClient):
            parts = dataFromClient.split("|")
            if len(parts) < 2:
                conn.sendall("400 bad request".encode('utf-8'))
                return
            
            class_name = parts[1].strip()
            file_path = f"data/chats/{class_name}.json"
            
            with self.db_lock:
                try:
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as f:
                            chat_history = json.load(f)
                    else:
                        chat_history = []
                    
                    conn.sendall(json.dumps(chat_history, ensure_ascii=False).encode('utf-8'))
                except Exception as e:
                    conn.sendall(f"error|{e}".encode('utf-8'))
        
        def get_send_current_user_grades(self, conn, dataFromClient):
            parts = dataFromClient.split("|")
            current_user_class = parts[1]
            current_username = parts[2]
            
            file_path = f"classesStudents/{current_user_class}/students-{current_user_class}.json"
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Server error opening file: {e}")
                conn.sendall(json.dumps({"status": "error", "message": "file_not_found"}).encode("utf-8"))
                return

            current_student_data = data.get(current_username)

            grades = current_student_data.get("grades", [])  

            total = 0
            for sub, grd in grades:
                total += grd
            
            try:
                average = round(total / len(grades), 2)
            except ZeroDivisionError:
                average = 0

            response_payload = {
                "status": "success",
                "grades": grades,
                "average": average
            }

            conn.sendall(json.dumps(response_payload).encode("utf-8"))
            return

        def update_student_grade(self, conn, dataFromClient):
            # פורמט בקשה: updateGrade|כיתה|שם_תלמיד|מקצוע|ציון
            parts = dataFromClient.split("|")
            current_user_class = parts[1]
            target_student = parts[2]
            subject = parts[3]
            new_grade = int(parts[4])

            file_path = f"classesStudents/{current_user_class}/students-{current_user_class}.json"
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                if target_student in data:
                    # שליפת רשימת הציונים הנוכחית של התלמיד
                    grades = data[target_student].get("grades", [])
                    
                    # בדיקה האם המקצוע כבר קיים - אם כן, נעדכן אותו. אם לא, נוסיף חדש.
                    found = False
                    for i, (sub, grd) in enumerate(grades):
                        if sub == subject:
                            grades[i] = [subject, new_grade] # עדכון ציון קיים
                            found = True
                            break
                    
                    if not found:
                        grades.append([subject, new_grade]) # הוספת מקצוע חדש
                        
                    data[target_student]["grades"] = grades
                    
                    # שמירה חזרה לקובץ ה-JSON
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                        
                    conn.sendall(json.dumps({"status": "success"}).encode("utf-8"))
                    
                else:
                    conn.sendall(json.dumps({"status": "error", "message": "student_not_found"}).encode("utf-8"))
                    
            except Exception as e:
                print(f"Server error updating grade: {e}")
                conn.sendall(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
        
        def handle_class_students_request(self, conn, dataFromClient):
            class_students = []
            parts = dataFromClient.split("|")
            current_client_class = parts[1]
            file_path = f"classesStudents/{current_client_class}/students-{current_client_class}.json"
            
            with self.db_lock:
                try:
                    with open(file_path, "r", encoding='utf-8') as f:
                        class_users = json.load(f)
                    
                        for user in class_users:
                            class_students.append(user)
                        
                        if class_students:
                            del class_students[0]
                except Exception as e:
                    print(f"[-] Error loading class students: {e}")
                    conn.sendall(f"class_students_response|".encode('utf-8'))
                    return
            
            students_string = ",".join(class_students)
            conn.sendall(f"class_students_response|{students_string}".encode('utf-8'))
            return
        
        def handle_insert_new_grade(self, conn, datsFromClient):
            try:
                parts = datsFromClient.split("|")
                client_class = parts[1]
                new_grade = parts[2]
                subject = parts[3]
                student = parts[4] 
                
                try:
                    new_grade = int(new_grade)
                except ValueError:
                    pass
                    
                new_grade_payload = [subject, new_grade]
                file_path = f"classesStudents/{client_class}/students-{client_class}.json"

                with self.db_lock:
                    try:
                        with open(file_path, "r", encoding='utf-8') as f:
                            class_data = json.load(f)
                    except FileNotFoundError:
                        conn.sendall("insert_grade_response|error|class file not found".encode('utf-8'))
                        return

                    if student in class_data:
                        if class_data[student].get("role") == "student" and isinstance(class_data[student]["grades"], list):
                            
                            class_data[student]["grades"].append(new_grade_payload)
                            
                            with open(file_path, "w", encoding='utf-8') as f:
                                json.dump(class_data, f, ensure_ascii=False, indent=4)
                            
                            print(f"[+] Successfully added grade {new_grade_payload} to student '{student}'")
                            conn.sendall("insert_grade_response|success".encode('utf-8'))
                        else:
                            print(f"[-] Cannot add grade: user '{student}' is not a student or has invalid grades format")
                            conn.sendall("insert_grade_response|error|user is not a student".encode('utf-8'))
                    else:
                        print(f"[-] Student '{student}' not found in class '{client_class}'")
                        conn.sendall("insert_grade_response|error|student not found".encode('utf-8'))

            except Exception as e:
                print(f"[-] Error in handle_insert_new_grade: {e}")
                try:
                    conn.sendall("insert_grade_response|error|internal server error".encode('utf-8'))
                except:
                    pass
        
        def handle_add_class_doar(self, conn, dataFromClient):
            parts = dataFromClient.split("|", 3)
            if len(parts) < 4:
                conn.sendall("400 bad request".encode('utf-8'))
                return
            
            class_name = parts[1].strip()
            title = parts[2].strip()
            content = parts[3].strip()
            
            file_path = f"classesStudents/{class_name}/doar_masseges-{class_name}.json"
            
            with self.db_lock:
                try:
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding='utf-8') as f:
                            class_messages = json.load(f)
                    else:
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        class_messages = []
                    
                    class_messages.insert(0, [title, content])
                    
                    with open(file_path, "w", encoding='utf-8') as f:
                        json.dump(class_messages, f, ensure_ascii=False, indent=4)
                        
                    print(f"[+] Message added successfully for class {class_name}")
                    conn.sendall("200 ok".encode("utf-8"))
                except Exception as e:
                    print(f"[-] Error in add_class_doar: {e}")
                    conn.sendall(f"error|{e}".encode("utf-8"))

        def handle_get_class_doar(self, conn, dataFromClient):
            parts = dataFromClient.split("|")
            if len(parts) < 2:
                conn.sendall("400 bad request".encode('utf-8'))
                return
                
            class_name = parts[1].strip()
            file_path = f"classesStudents/{class_name}/doar_masseges-{class_name}.json"
            
            with self.db_lock:
                try:
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding='utf-8') as f:
                            class_messages = json.load(f)
                    else:
                        class_messages = []
                        
                    response_json = json.dumps(class_messages, ensure_ascii=False)
                    conn.sendall(response_json.encode("utf-8"))
                except Exception as e:
                    print(f"[-] Error in get_class_doar: {e}")
                    conn.sendall("[]".encode("utf-8"))

        def handle_client(self, conn, addr):
            with conn:
                print(f"[+] New connection from {addr}")
                try:
                    rawDataFromClient = conn.recv(1024)
                    print("[+] handling client")
                    print("[+] listening")
                    if not rawDataFromClient:
                        return
                    
                    dataFromClient = rawDataFromClient.decode('utf-8').strip()
                    
                    if dataFromClient.startswith("login|"):
                        print("[+] received sensitive data. cannot show info") 
                        self.handle_login(conn, addr, dataFromClient)
                        
                    elif dataFromClient.startswith("signUp|"):
                        print("[+] received sensitive data. cannot show info") 
                        self.handle_signup(conn, addr, dataFromClient)
                    
                    elif dataFromClient.startswith("send_chat_message|"): 
                        self.handle_send_chat_message(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("get_chat_history|"):
                        self.handle_get_chat_history(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("freer premition"):
                        print(f"[+] subject received: freer premition | ({addr})")
                        self.handle_freer(conn, dataFromClient)
                    
                    elif dataFromClient.startswith("add_class_doar|"):
                        self.handle_add_class_doar(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("get_class_doar|"):
                        self.handle_get_class_doar(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("get_freer_requests|"):
                        print(f"[+] subject received: get_freer_requests | ({addr})")
                        self.handle_get_freer_requests(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("get_student_requests|"):
                        print(f"[+] subject received: get_student_requests | ({addr})")
                        self.handle_get_student_requests(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("update_request_status|"):
                        print(f"[+] subject received: update_request_status | ({addr})")
                        self.handle_update_request_status(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("get_schedule|"):
                        print(f"[+] subject received: get_schedule | ({addr})")
                        self.handle_get_schedule(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("tasks|"):
                        print(f"[+] subject received: tasks | ({addr})")
                        self.handle_get_tasks(conn, dataFromClient)
                        
                    elif dataFromClient.startswith("update_tasks|"):
                        print(f"[+] subject received: update_tasks | ({addr})")
                        self.handle_update_tasks(conn, dataFromClient)
                    
                    elif dataFromClient.startswith("get_class_students|"):
                        self.handle_class_students_request(conn, dataFromClient)
                    
                    elif dataFromClient.startswith("gradesRequest|"):
                        print(f"[+] subject received: student_get_grades_request | ({addr})")
                        self.get_send_current_user_grades(conn, dataFromClient)    
                    
                    elif dataFromClient.startswith("insert_new_grade|"):
                        self.handle_insert_new_grade(conn, dataFromClient)
                        
                    elif dataFromClient == "guest":
                        with self.db_lock:
                            with open("data/server_connection_logs.json", "a", encoding="utf-8") as f:
                                log_fields = {
                                    "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                    "address": str(addr),
                                    "status": "guest"
                                }
                                print(f"[+] writing a connection log for guest: {addr}")
                                f.write(json.dumps(log_fields, ensure_ascii=False) + "\n")
                                print("[+] completed writing the connection log.")
                                conn.sendall("200 ok".encode('utf-8'))
                                return
                        
                    else:
                        print(f"[+] Unknown command received: {dataFromClient} | ({addr})")
                        
                except ValueError as e:
                    print(f"[+] Error handling client {addr}: {e}")
                except Exception as e:
                    print(f"[+] General error with client {addr}: {e}")

        def start(self):
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            print("opening server key and crt")
            context.load_cert_chain("keys/server.crt", "keys/server.key")
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                print(f"[+] Server is listening on port: '{self.port}'")
                
                with context.wrap_socket(s, server_side=True) as ss:
                    while True:
                        try:
                            conn, addr = ss.accept()
                            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                            client_thread.start()
                        except Exception as e:
                            print(f"[-] Error accepting connection: {e}")

    if __name__ == "__main__":
        server = Server()
        server.start()

except KeyboardInterrupt:
    print("\n[+] KeyboardInterrupt! QUITTING...")
import sqlite3
import datetime
import hashlib
import secrets
import re


class BirthdaysRelatives():
    def __init__(self):
        self.version = "2.0"
        self.name = "Birthdays Relatives"
        self.db = SQLite()
        self.db.init_database()
        self.current_user = None
        self.user_id = None
        self.data_version = "28.02.2026" 
        

    def menu(self):
        print(f"Привет, я консольный бот {self.name}")
        print("Я создан чтобы вы могли посмотреть когда у ваших родственников День рождение!")
        
        while True:
          print("1- ВХОД")
          print("2- РЕГИСТРАЦИЯ")
          print("3- ВЫХОД")
          login_registr = input("ВХОД / РЕГИСТРАЦИЯ / ВЫХОД: ").strip()
          if login_registr == "1":
            self.login()
            self.menu_bot()
          elif login_registr == "2":
            self.registr()
            self.menu_bot()
          elif login_registr == "3":
            return False
          else:
            print("Не найдено. Повторите попытку ")
            continue
          

    def login(self):
       print("ВХОД В АККАУНТ")

       for attemps in range(3):
        print(f"Попытка {attemps + 1} из 3")

        username = input("Логин: ").strip()
        if not username:
           print("Имя не должно быть пустым!")
           continue

        password = input("Пароль: ").strip()
        if not password:
           print("Пароль не должен быть пустым!")

        
        user_id = self.db.authenticate_user(username, password)
        if user_id:
            self.current_user = username
            self.user_id = user_id

            return True
        else:
           print("Неверный логин или пароль! Повторите попытку")
       
       print("Слишком много неудачных попыток")

    def registr(self):
       print("РЕГИСТРАЦИЯ")

       while True:
        username = input("Создайте имя пользователя: ").strip()

        if not username:
            print("Имя пользователя не должно быть пустым")
            continue

        if len(username) < 3:
            print("Имя пользователя не должно быть меньше 3 символов")
            continue

        if len(username) > 40:
            print("Имя пользователя не должно быть больше 40 символов")
            continue

        break

       while True:
        password = input("Теперь пароль пользователя: ").strip()

        if not password:
            print("Пароль пользователя не должен быть пустым!")
            continue
        else:
            break

       while True:
        confirm_password = input("\nПодтвердите свой пароль: ").strip()

        if password != confirm_password:
            print("Пароли не совпадают! Повторите попытку")
            continue
        else:
            break
      
       success = self.db.register_user(username, password)
       if success:
        user_id = self.db.authenticate_user(username, password)
        
        if user_id:
            self.current_user = username
            self.user_id = user_id
            
            print("Теперь вы есть в Базе Данных Birthdays Relatives!")
            print(f"Ваше имя пользователя: {username}")
            print(f"Ваш уникальный id: {self.user_id}")
            print(f"\nДата регистрации: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

            return True
        else:
            print("Ошибка при автоматическом входе после регистрации!")
            return False
       else:
        print("Ошибка при регистрации!")
        return False
        

    def menu_bot(self):
       print("Вы в основном меню")
       print("1- Создать информацию о родственнике")
       print("2- Посмотреть информацию о родственнике")
       print("3- Выход")
       while True:
          create_or_watch_relative = input("Введите что вам нужно (1-3): ").strip()
          if create_or_watch_relative == "1":
            self.create_relative()
          elif create_or_watch_relative == "2":
            self.watch_relative()
          elif create_or_watch_relative == "3":
            break
          else:
            print("Возникла ошибка. Попробуйте снова (1-3)")
            continue

    def create_relative(self):
       print("Создание информации родственника")
       print("Если хотите закончить Enter в 1 параметре создании")

       relative = 0

       while True:
          print(f"Родственник № {relative + 1}")
          name_relative = input("Введите Имя Родственника: ").strip()

          if not name_relative:
             print("Завершение создании информации о родственнике")
             break
          
          date_relative = input("Введите Дату Рождения Родственника (ДД.MM.ГГГГ): ")

          pattern = re.compile(r'^(\d{2})\.(\d{2})\.(\d{4})$')
          match = pattern.match(date_relative)

          if match:
             
             day, month, year = match.groups()

             now_year = datetime.datetime.now().year

             try:
                
                day_int = int(day)
                month_int = int(month) 
                year_int = int(year)
                
                #Проверки дат
                if not (1 <= day_int <= 31):
                    print("День должен быть от 01 до 31")
                    continue
                    
                if not (1 <= month_int <= 12):
                    print("Месяц должен быть от 01 до 12") 
                    continue
                    
                if not (1900 <= year_int <= now_year):  
                    print(f"Год должен быть от 1900 до {now_year}")
                    continue
                
                date_norm = True
                print("Дата родственника записана правильно!")

                 
             except ValueError:
                print("Данной даты не существует. Попробуйте снова. Пример: 31.12.2000")
                date_norm = False
                continue
          else:
            print("Неправильный формат! Попробуйте снова. Используйте ДД.ММ.ГГГГ")
            date_norm = False
            continue
          
          if date_norm == True:
             print("Сохраняем родственника")
             try:
                # Сохраняем в БД
                conn = sqlite3.connect(self.db.db_name)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO birthdays_relatives 
                    (user_id, relative_name, birth_date)
                    VALUES (?, ?, ?)
                """, (self.user_id, name_relative, date_relative))
                
                conn.commit()
                conn.close()
                
                print(f"Родственник '{name_relative}' сохранён!")
                relative += 1
                
             except Exception as br_relative:
                print(f"Ошибка при сохранении: {br_relative}")
                continue

          go = input("Продолжить ли снова? да - да, нажать на кнопку Enter - нет: ").lower().strip()
          if go == "да":
             continue
          elif not go:
             break
          else:
             print("Возникла ошибка. Попробуйте снова (да или Enter)")
             continue
          
       print("1 - Продолжить просмотр")
       print("2 - Выйти в главное меню напоминайки")
       print("3 - Выход в меню аутенфикации")
       print("4 - Полное завершение роботы")

       while True:
           exit_or_not = input("Выберите дальнейшее действие (1-4): ").strip()
           if exit_or_not == "1":
              self.watch_relative()
           elif exit_or_not == "2":
              self.menu_bot()
           elif exit_or_not == "3":
              self.current_user = None
              self.user_id = None
              self.menu()
              break
           elif exit_or_not == "4":
              print("Выхожу...")
              exit(0)
           else:
              print("Произошла ошибка: дальнейшее действие не найдено. Попробуйте снова (1-4)")
          
    def watch_relative(self):
       print("Список ваших родственников:")

       try:
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        
        # Получаем ВСЕХ родственников пользователя
        cursor.execute("""
            SELECT 
                id,
                relative_name, 
                birth_date,
                created_at
            FROM birthdays_relatives 
            WHERE user_id = ?
            ORDER BY relative_name
        """, (self.user_id,))
        
        relatives = cursor.fetchall()
        conn.close()
        
        if not relatives:
            print("У вас пока нет добавленных родственников")
            print("Создайте информацию о первом родственнике")
            return
        
        total_relatives_stat = len(relatives)
        print(f"Всего родственников {total_relatives_stat}")

        for br_relative, rel in enumerate(relatives, 1):
            rel_id, name, birth_date, created_at = rel
            
            print(f"\n{br_relative}. {name}")
            print(f"Дата рождения: {birth_date}")
            
            # Вычисляем возраст
            try:
                birth = datetime.datetime.strptime(birth_date, '%d.%m.%Y')
                today = datetime.datetime.now()
                age = today.year - birth.year
                if (today.month, today.day) < (birth.month, birth.day):
                    age -= 1
                print(f"Возраст: {age} лет")
            except:
                print(f"Возраст: не указан")
            
            
            print(f"Добавлен: {created_at}")
            print(f"ID: {rel_id}")

                
       except Exception as br_relative_0:
        print(f"Ошибка при загрузке данных: {br_relative_0}")
        return


       print("1 - Продолжить просмотр")
       print("2 - Выйти в главное меню напоминайки")
       print("3 - Выход в меню аутенфикации")
       print("4 - Полное завершение роботы")

       while True:
           exit_or_not = input("Выберите дальнейшее действие (1-4): ").strip()
           if exit_or_not == "1":
              self.watch_relative()
           elif exit_or_not == "2":
              self.menu_bot()
           elif exit_or_not == "3":
              self.current_user = None
              self.user_id = None
              self.menu()
              break
           elif exit_or_not == "4":
              print("Выхожу...")
              exit(0)
           else:
              print("Произошла ошибка: дальнейшее действие не найдено. Попробуйте снова (1-4)")


class SQLite():
    def __init__(self):
        self.db_name = "Birthdays_Relatives.db"
        self.init_database() 


    def check_user_exists(self, username):
        #Проверяет, существует ли пользователь
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    

    def init_database(self):
        # Создаёт структуру БД
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT,
            first_seen TIMESTAMP,
            last_seen TIMESTAMP,
            failed_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp TIMESTAMP,
            success INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS birthdays_relatives (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL,
          relative_name TEXT NOT NULL,
          birth_date DATE NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        conn.close()
        
    def get_or_create_user(self, username):
        # Получить пользователя или создать нового пользователя
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        now = datetime.datetime.now()

        cursor.execute("""
        SELECT id FROM users WHERE username = ?
        """, (username,))  

        user = cursor.fetchone()

        if user:
            # Пользователь существует, обновляем last_seen
            cursor.execute("""
            UPDATE users SET last_seen = ? WHERE id = ?
            """, (now, user[0]))
            user_id = user[0]
            print(f"Пользователь '{username}' найден (ID: {user_id})")
        else:
            # Создаём нового пользователя
            cursor.execute("""
            INSERT INTO users (username, first_seen, last_seen)
            VALUES (?, ?, ?)
            """, (username, now, now))
            user_id = cursor.lastrowid
            print(f"Новый пользователь '{username}' создан (ID: {user_id})")
        
        conn.commit()
        conn.close()
        return user_id
    
    def hash_password(self, password, salt=None):
        # Безопасное хэширование паролей 
        if salt is None:
            salt = secrets.token_hex(32)

        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return hashed.hex(), salt
    
    
    def verify_password(self, password, stored_hash, salt):
        # Проверка пароля
        hashed, _ = self.hash_password(password, salt)
        return hashed == stored_hash
    
    def register_user(self, username, password):
        # Безопасная регистрация с безопасным хранением пароля 
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        now = datetime.datetime.now()

        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"Пользователь {username} уже существует")
            conn.close()
            return False
        
        password_hash, salt = self.hash_password(password)

        try:

           cursor.execute("""
           INSERT INTO users (username, password_hash, salt, first_seen, last_seen)
           VALUES (?, ?, ?, ?, ?)
           """, (username, password_hash, salt, now, now))
        
           user_id = cursor.lastrowid
           cursor.execute("""
            INSERT INTO security_logs (user_id, action, timestamp, success)
            VALUES (?, ?, ?, ?)
            """, (user_id, "registration", now, 1))
            
           conn.commit()
           print(f"Пользователь '{username}' успешно зарегистрирован")
           return True
            
        except Exception as br_relatives:
            print(f"Ошибка при регистрации: {br_relatives}")
            conn.rollback()
            return False
            
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        # Безопасная аутентификация пользователя с защитой от брутфорса 
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        now = datetime.datetime.now()

        cursor.execute("""
        SELECT id, password_hash, salt, failed_attempts, locked_until 
        FROM users WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if not user:
            print(f"Пользователь '{username}' не найден")
            conn.close()
            return False
        
        user_id, stored_hash, salt, failed_attempts, locked_until = user

        if locked_until:
            # Проверяем, не строковый ли это формат
            if isinstance(locked_until, str):
                lock_time = datetime.datetime.strptime(locked_until, '%Y-%m-%d %H:%M:%S')
            else:
                lock_time = datetime.datetime.fromisoformat(locked_until)
                
            if lock_time > now:
                print(f"Аккаунт заблокирован до {locked_until}")
                conn.close()
                return False
            
        if self.verify_password(password, stored_hash, salt):
            # Успешная аутентификация
            cursor.execute("""
            UPDATE users SET 
                last_seen = ?,
                failed_attempts = 0,
                locked_until = NULL 
            WHERE id = ?
            """, (now, user_id))

            cursor.execute("""
            INSERT INTO security_logs (user_id, action, timestamp, success)
            VALUES (?, ?, ?, ?)
            """, (user_id, "login", now, 1))
            
            conn.commit()
            conn.close()
            print(f"Успешная аутентификация для '{username}'")
            return user_id
        else:
            # Неверный пароль
            failed_attempts = (failed_attempts or 0) + 1
            print(f"Неверный пароль для '{username}' (попытка {failed_attempts})")

            if failed_attempts >= 5:
                lock_until = now + datetime.timedelta(minutes=45)
                cursor.execute("""
                UPDATE users SET 
                    failed_attempts = ?,
                    locked_until = ?
                WHERE id = ?
                """, (failed_attempts, lock_until.strftime('%Y-%m-%d %H:%M:%S'), user_id))
                print(f"Аккаунт заблокирован до {lock_until}")
            else:
                cursor.execute("""
                UPDATE users SET failed_attempts = ? WHERE id = ?
                """, (failed_attempts, user_id))

            cursor.execute("""
            INSERT INTO security_logs (user_id, action, timestamp, success)
            VALUES (?, ?, ?, ?)
            """, (user_id, "failed_login", now, 0))

            conn.commit()
            conn.close()
            return False
        
if __name__ == "__main__":
   try:
      print("Здравствуете Пользователи!")
      print("Вы запустили Birthdays Relatives. Версия v2.0")

      import time
      time.sleep(3)

      app = BirthdaysRelatives()

      while True:
            # Показываем меню авторизации
            if not app.current_user:
                result = app.menu()
                if result is False:  # Выход
                    break
                elif result is True:  # Успешная авторизация
                    continue
                else:  # Неверный выбор
                    continue
            
            # Показываем главное меню
            menu_result = app.menu_bot()
            if menu_result is None:  # Полный выход
                break
            elif menu_result is False:  # Выход из аккаунта
                continue
                
   except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
   except Exception as br:
        print(f"\n Возникла критическая ошибка: {br}")
        import traceback
        traceback.print_exc()
   finally:
        print("\nBirthdays Relatives завершает работу! До свидания!")
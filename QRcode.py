######################
#     QuartzzDev     #
######################  

import tkinter as tk
import sqlite3
import qrcode
import random
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import messagebox


atthemoment = datetime.now()
date = datetime.strftime(atthemoment, '%c')

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Quartzz QR Onay Sistemi")

        self.language = "eng"  # Varsayılan dil İngilizce

        self.label_username = tk.Label(master, text="Username:" if self.language == "eng" else "Kullanıcı Adı:")
        self.label_password = tk.Label(master, text="Password:" if self.language == "eng" else "Şifre:")
        self.entry_username = tk.Entry(master)
        self.entry_password = tk.Entry(master, show="*")

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()

        self.btn_login = tk.Button(master, text="Login", command=self.initiate_2fa)
        self.btn_login.pack()

        self.generated_code = None

        self.canvas = tk.Canvas(master, width=300, height=300)
        self.canvas.pack()

        self.label_2fa_code = tk.Label(master, text="QR Code Password:" if self.language == "eng" else "QR Kodu Şifresi:")
        self.entry_2fa_code = tk.Entry(master)
        self.btn_confirm_2fa = tk.Button(master, text="Confirm", command=self.confirm_2fa)

        # Dil değiştirme düğmesi
        self.btn_change_language = tk.Button(master, text="Change Language", command=self.change_language)
        self.btn_change_language.pack()

    def initiate_2fa(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Kullanıcı adı ve şifre kontrolü
        if username == "Quartzz" and password == "Dev":
            self.generated_code = self.create_qr_code()
            self.show_qr_code()
            self.show_2fa_code_entry()
            messagebox.showinfo("Two-Factor Authentication", "Please scan the QR code and enter the password.")
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def create_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr_code_num = random.randint(0, 9999999)
        qr.add_data(str(qr_code_num))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        self.qr_code_image = ImageTk.PhotoImage(img)

        return qr_code_num

    def show_qr_code(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.qr_code_image)

    def show_2fa_code_entry(self):
        self.label_2fa_code.pack()
        self.entry_2fa_code.pack()
        self.btn_confirm_2fa.pack()

    def confirm_2fa(self):
        entered_code = self.entry_2fa_code.get()

        if entered_code == str(self.generated_code):
            messagebox.showinfo("Login Successful", "Successfully Logged In.")
            self.save_to_database()
        else:
            messagebox.showerror("Incorrect Password", "Incorrect password. Please try again.")

    def save_to_database(self):
        username = self.entry_username.get()
        generated_code = self.generated_code

        # Connect to the SQLite database
        conn = sqlite3.connect('login_info.db')
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_info (
                id INTEGER PRIMARY KEY,
                username TEXT,
                generated_code INTEGER,
                access_datetime TEXT
            )
        ''')

        # Insert login information into the database
        cursor.execute('''
            INSERT INTO login_info (username, generated_code, access_datetime)
            VALUES (?, ?, ?)
        ''', (username, generated_code, date))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def change_language(self):
        # Dil değiştirme fonksiyonu
        self.language = "eng" if self.language == "tr" else "tr"

        # Dil değiştikçe etiket ve düğme metinlerini güncelle
        self.label_username.config(text="Username:" if self.language == "eng" else "Kullanıcı Adı:")
        self.label_password.config(text="Password:" if self.language == "eng" else "Şifre:")
        self.label_2fa_code.config(text="QR Code Password:" if self.language == "eng" else "QR Kodu Şifresi:")
        self.btn_login.config(text="Login" if self.language == "eng" else "Giriş Yap")
        self.btn_confirm_2fa.config(text="Confirm" if self.language == "eng" else "Onayla")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

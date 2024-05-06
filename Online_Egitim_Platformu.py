import tkinter as tk
from tkinter import ttk
import sqlite3

class Veritabani:
    def __init__(self, db_adi):
        self.conn = sqlite3.connect(db_adi)
        self.cur = self.conn.cursor()
        self.tablolari_olustur()

    def tablolari_olustur(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Kurslar
                            (id INTEGER PRIMARY KEY,
                            kurs_adi TEXT,
                            egitmen TEXT,
                            icerik TEXT)''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Egitmenler
                            (id INTEGER PRIMARY KEY,
                            ad TEXT,
                            uzmanlik_alani TEXT)''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Ogrenciler
                            (id INTEGER PRIMARY KEY,
                            ad TEXT,
                            email TEXT)''')

        self.conn.commit()

    def kurs_olustur(self, kurs_adi, egitmen, icerik):
        self.cur.execute("INSERT INTO Kurslar (kurs_adi, egitmen, icerik) VALUES (?, ?, ?)", (kurs_adi, egitmen, icerik))
        self.conn.commit()

    def kaydol(self, ogrenci_ad, ogrenci_email):
        self.cur.execute("INSERT INTO Ogrenciler (ad, email) VALUES (?, ?)", (ogrenci_ad, ogrenci_email))
        self.conn.commit()

    def tum_kurs_adlari_getir(self):
        self.cur.execute("SELECT kurs_adi FROM Kurslar")
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()

class Kurs:
    def __init__(self, kurs_adi, egitmen, icerik):
        self.kurs_adi = kurs_adi
        self.egitmen = egitmen
        self.icerik = icerik

    def __str__(self):
        return f"Kurs Adı: {self.kurs_adi}\nEğitmen: {self.egitmen}\nİçerik: {self.icerik}"

class Egitmen:
    def __init__(self, ad, uzmanlik_alani):
        self.ad = ad
        self.uzmanlik_alani = uzmanlik_alani

    def __str__(self):
        return f"Eğitmen Adı: {self.ad}\nUzmanlık Alanı: {self.uzmanlik_alani}"

class Ogrenci:
    def __init__(self, ad, email):
        self.ad = ad
        self.email = email

    def __str__(self):
        return f"Öğrenci Adı: {self.ad}\nE-posta: {self.email}"

class OnlineEgitimUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Eğitim Platformu")
        self.root.geometry("600x600")
        self.root.configure(bg='light blue')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='light blue', foreground='black')
        self.style.configure('TLabel', foreground='black')
        self.style.configure('TButton', foreground='black')

        self.db = Veritabani("online_egitim.db")

        self.label = ttk.Label(self.root, text="Hoş Geldiniz!", background='light blue', foreground='yellow', font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.kurs_adi_label = ttk.Label(self.root, text="Kurs Adı:", background='light blue')
        self.kurs_adi_label.pack()
        self.kurs_adi_entry = ttk.Entry(self.root)
        self.kurs_adi_entry.pack()

        self.egitmen_label = ttk.Label(self.root, text="Eğitmen:", background='light blue')
        self.egitmen_label.pack()
        self.egitmen_entry = ttk.Entry(self.root)
        self.egitmen_entry.pack()

        self.icerik_label = ttk.Label(self.root, text="İçerik:", background='light blue')
        self.icerik_label.pack()
        self.icerik_entry = tk.Text(self.root, height=5)  # İçerik kutusunun yüksekliğini azalttık
        self.icerik_entry.pack()

        self.kurs_olustur_button = ttk.Button(self.root, text="Kurs Oluştur", command=self.kurs_olustur)
        self.kurs_olustur_button.pack(pady=10)

        self.ogrenci_ad_label = ttk.Label(self.root, text="Öğrenci Adı:", background='light blue')
        self.ogrenci_ad_label.pack()
        self.ogrenci_ad_entry = ttk.Entry(self.root)
        self.ogrenci_ad_entry.pack()

        self.ogrenci_email_label = ttk.Label(self.root, text="Öğrenci E-posta:", background='light blue')
        self.ogrenci_email_label.pack()
        self.ogrenci_email_entry = ttk.Entry(self.root)
        self.ogrenci_email_entry.pack()

        self.kaydol_button = ttk.Button(self.root, text="Kaydol", command=self.ogrenci_kaydol)
        self.kaydol_button.pack(pady=10)

        self.kurslar_listesi_label = ttk.Label(self.root, text="Kurslar:", background='light blue')
        self.kurslar_listesi_label.pack()
        self.kurslar_listesi = tk.Listbox(self.root, height=5, selectmode="single")  # Kurs listesi için bir Listbox oluşturduk
        self.kurslar_listesi.pack()

        self.ornek_kurslar_ve_egitmenler_ekle()

        self.kurslar_listesi_goster()

    def kurs_olustur(self):
        kurs_adi = self.kurs_adi_entry.get()
        egitmen = self.egitmen_entry.get()
        icerik = self.icerik_entry.get("1.0", tk.END)

        self.db.kurs_olustur(kurs_adi, egitmen, icerik)
        self.kurs_adi_entry.delete(0, tk.END)
        self.egitmen_entry.delete(0, tk.END)
        self.icerik_entry.delete("1.0", tk.END)
        print("Kurs oluşturuldu.")

    def ogrenci_kaydol(self):
        ogrenci_ad = self.ogrenci_ad_entry.get()
        ogrenci_email = self.ogrenci_email_entry.get()

        self.db.kaydol(ogrenci_ad, ogrenci_email)
        self.ogrenci_ad_entry.delete(0, tk.END)
        self.ogrenci_email_entry.delete(0, tk.END)
        print("Öğrenci kaydı tamamlandı.")

    def ornek_kurslar_ve_egitmenler_ekle(self):
        self.db.kurs_olustur("Python Programlama", "Ahmet Yılmaz", "Python programlama dili temelleri.\n\nÖrnek Eğitmenler:\n- Fatma Demir\n- Mehmet Kaya\n- Ayşe Yıldız")
        self.db.kurs_olustur("Veri Bilimi", "Ayşe Kaya", "Veri analizi ve makine öğrenimi.\n\nÖrnek Eğitmenler:\n- Ahmet Can\n- Zeynep Yılmaz\n- Ali Demir")
        self.db.kurs_olustur("Web Geliştirme", "Mehmet Demir", "HTML, CSS ve JavaScript temelleri.\n\nÖrnek Eğitmenler:\n- Fatma Kaya\n- Ayşe Yılmaz\n- Ali Demir")
        self.db.kurs_olustur("Mobil Uygulama Geliştirme", "Fatma Can", "Android ve iOS uygulama geliştirme.\n\nÖrnek Eğitmenler:\n- Ahmet Yıldız\n- Zeynep Demir\n- Mehmet Kaya")

    def kurslar_listesi_goster(self):
        kurslar = self.db.tum_kurs_adlari_getir()
        for kurs_adi in kurslar:
            self.kurslar_listesi.insert(tk.END, kurs_adi)

if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineEgitimUygulamasi(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from tkinter import filedialog

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-posta Gönderme Formu")
        self.root.geometry("600x650")
        
        # E-posta hesap bilgileri
        self.email = "contact@jasperazerbaijan.com"
        self.password = "KQ0H0S0hi//64s"
        self.smtp_server = "mail.jasperazerbaijan.com"
        self.smtp_port = 587
        
        # Ekli dosya listesi
        self.attachments = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="E-posta Gönderme Formu", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Gönderen bilgisi
        sender_frame = ttk.LabelFrame(main_frame, text="Gönderen")
        sender_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(sender_frame, text=f"E-posta: {self.email}").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Label(sender_frame, text=f"SMTP Sunucu: {self.smtp_server}").pack(anchor=tk.W, padx=10, pady=5)
        
        # Alıcı bilgileri
        recipient_frame = ttk.LabelFrame(main_frame, text="Alıcı")
        recipient_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(recipient_frame, text="Alıcı E-posta:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.to_entry = ttk.Entry(recipient_frame, width=50)
        self.to_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(recipient_frame, text="CC:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.cc_entry = ttk.Entry(recipient_frame, width=50)
        self.cc_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(recipient_frame, text="BCC:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.bcc_entry = ttk.Entry(recipient_frame, width=50)
        self.bcc_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        # E-posta içeriği
        content_frame = ttk.LabelFrame(main_frame, text="E-posta İçeriği")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(content_frame, text="Konu:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.subject_entry = ttk.Entry(content_frame, width=50)
        self.subject_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(content_frame, text="Mesaj:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.NW)
        self.message_text = scrolledtext.ScrolledText(content_frame, width=50, height=10)
        self.message_text.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Dosya ekleme
        attachment_frame = ttk.LabelFrame(main_frame, text="Dosya Ekle")
        attachment_frame.pack(fill=tk.X, pady=(0, 10))
        
        add_button = ttk.Button(attachment_frame, text="Dosya Seç", command=self.add_attachment)
        add_button.grid(row=0, column=0, padx=10, pady=5)
        
        self.attachment_label = ttk.Label(attachment_frame, text="Ekli dosya yok")
        self.attachment_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        clear_button = ttk.Button(attachment_frame, text="Temizle", command=self.clear_attachments)
        clear_button.grid(row=0, column=2, padx=10, pady=5)
        
        # Gönder butonu
        send_button = ttk.Button(main_frame, text="E-posta Gönder", command=self.send_email)
        send_button.pack(pady=10)
        
        # Durum çubuğu
        self.status_var = tk.StringVar(value="Hazır")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def add_attachment(self):
        """Dosya ekleme diyaloğunu aç ve seçilen dosyaları listeye ekle"""
        files = filedialog.askopenfilenames(
            title="Eklemek için dosya seçin",
            filetypes=(
                ("Tüm Dosyalar", "*.*"),
                ("PDF Dosyaları", "*.pdf"),
                ("Resim Dosyaları", "*.png;*.jpg;*.jpeg"),
                ("Belge Dosyaları", "*.doc;*.docx;*.xls;*.xlsx;*.ppt;*.pptx")
            )
        )
        
        if files:
            for file in files:
                self.attachments.append(file)
            
            self.update_attachment_label()
    
    def update_attachment_label(self):
        """Eklenen dosya sayısını etikette göster"""
        if not self.attachments:
            self.attachment_label.config(text="Ekli dosya yok")
        else:
            file_count = len(self.attachments)
            file_names = ", ".join([os.path.basename(file) for file in self.attachments[:2]])
            
            if file_count > 2:
                file_names += f" ve {file_count - 2} dosya daha"
                
            self.attachment_label.config(text=file_names)
    
    def clear_attachments(self):
        """Eklenen dosyaları temizle"""
        self.attachments = []
        self.update_attachment_label()
    
    def send_email(self):
        """E-postayı gönder"""
        # Alıcı kontrol
        to_email = self.to_entry.get().strip()
        if not to_email:
            messagebox.showerror("Hata", "Lütfen alıcı e-posta adresi girin.")
            return
        
        # Konu kontrol
        subject = self.subject_entry.get().strip()
        if not subject:
            messagebox.showerror("Hata", "Lütfen e-posta konusu girin.")
            return
        
        # Mesaj kontrol
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Hata", "Lütfen e-posta mesajı girin.")
            return
        
        try:
            self.status_var.set("E-posta gönderiliyor...")
            self.root.update_idletasks()
            
            # E-posta oluştur
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            
            # CC ve BCC ekle
            cc_email = self.cc_entry.get().strip()
            bcc_email = self.bcc_entry.get().strip()
            
            if cc_email:
                msg['Cc'] = cc_email
            
            if bcc_email:
                msg['Bcc'] = bcc_email
            
            # Tüm alıcıları birleştir
            all_recipients = [to_email]
            if cc_email:
                all_recipients.extend(cc_email.split(','))
            if bcc_email:
                all_recipients.extend(bcc_email.split(','))
            
            msg['Subject'] = subject
            
            # Mesaj içeriği
            msg.attach(MIMEText(message, 'plain'))
            
            # Dosya ekleri
            for file in self.attachments:
                with open(file, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype=self.get_subtype(file))
                    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                    msg.attach(attachment)
            
            # SMTP bağlantısı kur ve e-postayı gönder
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # TLS güvenlik bağlantısı kur
            server.login(self.email, self.password)
            server.sendmail(self.email, all_recipients, msg.as_string())
            server.quit()
            
            self.status_var.set("E-posta başarıyla gönderildi.")
            messagebox.showinfo("Başarılı", "E-posta başarıyla gönderildi!")
            
            # Formu temizle
            self.clear_form()
            
        except Exception as e:
            self.status_var.set(f"Hata: {str(e)}")
            messagebox.showerror("Gönderme Hatası", f"E-posta gönderilirken bir hata oluştu:\n{str(e)}")
    
    def get_subtype(self, filename):
        """Dosya uzantısına göre MIME alt tipini belirle"""
        ext = os.path.splitext(filename)[1].lower()
        
        subtypes = {
            '.pdf': 'pdf',
            '.doc': 'msword',
            '.docx': 'vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'vnd.ms-excel',
            '.xlsx': 'vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'vnd.ms-powerpoint',
            '.pptx': 'vnd.openxmlformats-officedocument.presentationml.presentation',
            '.jpg': 'jpeg',
            '.jpeg': 'jpeg',
            '.png': 'png',
            '.gif': 'gif',
            '.txt': 'plain',
            '.zip': 'zip',
            '.rar': 'x-rar-compressed'
        }
        
        return subtypes.get(ext, 'octet-stream')  # Bilinmeyen türler için genel ikili akış
    
    def clear_form(self):
        """Form alanlarını temizle"""
        self.to_entry.delete(0, tk.END)
        self.cc_entry.delete(0, tk.END)
        self.bcc_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.message_text.delete("1.0", tk.END)
        self.clear_attachments()


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()
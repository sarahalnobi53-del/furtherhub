import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
# تأكدي من أن أسماء الملفات مطابقة لما في مجلدك
from database_manger import add_user, login_user, get_resources_by_subject 
from dashboard_page import DashboardFrame
from resources_page import ResourcesPage # استيراد صفحة المصادر التي صممتِها

class AcademicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FurtherHub | ملتقى طلاب كلية الحاسوب")
        self.geometry("1100x750")
        
        self.primary_blue = "#1f538d"
        self.accent_cyan = "#00ADB5"

        try:
            img_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(img_path),
                dark_image=Image.open(img_path),
                size=(180, 180)
            )
        except:
            self.logo_image = None

        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.show_login_page()

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_login_page(self):
        self.clear_container()
        wrapper = ctk.CTkFrame(self.main_container, fg_color="transparent")
        wrapper.pack(expand=True, fill="both", padx=40, pady=40)

        # القسم الأيسر
        left_panel = ctk.CTkFrame(wrapper, corner_radius=25, fg_color=("#F0F2F5", "#252525"))
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))
        if self.logo_image:
            ctk.CTkLabel(left_panel, image=self.logo_image, text="").pack(pady=(60, 10))
        ctk.CTkLabel(left_panel, text="FurtherHub", font=("Segoe UI", 36, "bold"), text_color=self.accent_cyan).pack()
        ctk.CTkLabel(left_panel, text="ملتقى طلاب كلية الحاسوب", font=("Tajawal", 16, "bold"), text_color=(self.primary_blue, "white")).pack(pady=5)
        ctk.CTkLabel(left_panel, text="منصة أكاديمية تُبنى بالمعرفة،\nوتنمو بالتشارك والتعاون الطلابـي.", font=("Tajawal", 13), text_color="gray", justify="center").pack(pady=20, padx=20)
        ctk.CTkButton(left_panel, text="ℹ️ تعرّف علينا أكثر", command=self.show_about_us, fg_color="transparent", text_color="gray", hover_color=("#E0E0E0", "#333333"), font=("Tajawal", 12)).pack(side="bottom", pady=20)

        # القسم الأيمن
        right_panel = ctk.CTkFrame(wrapper, corner_radius=25)
        right_panel.pack(side="right", fill="both", expand=True)
        ctk.CTkLabel(right_panel, text="تسجيل الدخول", font=("Tajawal", 24, "bold"), text_color=(self.primary_blue, self.accent_cyan)).pack(pady=(80, 40))
        self.entry_id = ctk.CTkEntry(right_panel, placeholder_text="الرقم الأكاديمي", width=300, height=48, corner_radius=12, justify="right")
        self.entry_id.pack(pady=12)
        self.entry_pass = ctk.CTkEntry(right_panel, placeholder_text="كلمة المرور", show="*", width=300, height=48, corner_radius=12, justify="right")
        self.entry_pass.pack(pady=12)
        ctk.CTkButton(right_panel, text="دخول", command=self.handle_login, width=300, height=50, corner_radius=12, font=("Tajawal", 15, "bold"), fg_color=(self.primary_blue, self.accent_cyan)).pack(pady=(30, 10))
        ctk.CTkButton(right_panel, text="ليس لديك حساب؟ انضم إلينا", command=self.show_signup_page, fg_color="transparent", text_color=self.primary_blue, font=("Tajawal", 13)).pack()

    def handle_login(self):
        aid = self.entry_id.get()
        pwd = self.entry_pass.get()
        result = login_user(aid, pwd)
        if result:
            self.user_name, self.user_major = result
            self.show_dashboard() # استدعاء الداشبورد
        else:
            messagebox.showerror("خطأ", "البيانات غير صحيحة")

    def show_dashboard(self):
        self.clear_container()
        # نمرر self كـ controller لكي تستطيع البطاقات في الداشبورد مناداتنا
        self.dashboard = DashboardFrame(self.main_container, user_name=self.user_name, user_major=self.user_major)
        self.dashboard.controller = self # ربط مهم جداً
        self.dashboard.pack(fill="both", expand=True)

    # دالة الانتقال لصفحة المصادر الحقيقية عند الضغط على مادة
    def show_resources_page(self, subject_id, subject_name):
        self.clear_container()
        # جلب البيانات من الداتا بيز بناءً على الـ ID
        resources = get_resources_by_subject(subject_id)
        self.res_page = ResourcesPage(self.main_container, self, subject_name, subject_id, resources)
        self.res_page.pack(fill="both", expand=True)

    def show_signup_page(self):
        self.clear_container()
        # ... كود التسجيل (يبقى كما هو بدون تغيير) ...
        # (فقط تأكدي من إضافة زر العودة ليعمل بشكل صحيح)
        card = ctk.CTkFrame(self.main_container, width=450, height=600, corner_radius=25, border_width=1)
        card.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(card, text="انضم لملتقى الطلاب", font=("Tajawal", 26, "bold"), text_color=(self.primary_blue, self.accent_cyan)).pack(pady=(30, 25))
        self.reg_name = ctk.CTkEntry(card, placeholder_text="الاسم الكامل", width=340, height=45, justify="right")
        self.reg_name.pack(pady=8)
        self.reg_id = ctk.CTkEntry(card, placeholder_text="الرقم الأكاديمي", width=340, height=45, justify="right")
        self.reg_id.pack(pady=8)
        self.reg_major = ctk.CTkOptionMenu(card, values=["علوم حاسوب", "ذكاء اصطناعي","أمن سيبراني","هندسة برمجيات", "نظم معلومات"], width=340, height=45, fg_color=self.primary_blue)
        self.reg_major.set("اختر التخصص")
        self.reg_major.pack(pady=8)
        self.reg_pass = ctk.CTkEntry(card, placeholder_text="كلمة المرور", show="*", width=340, height=45, justify="right")
        self.reg_pass.pack(pady=8)
        ctk.CTkButton(card, text="تأكيد الحساب", command=self.handle_signup, width=340, height=50, corner_radius=12, font=("Tajawal", 15, "bold"), fg_color=(self.primary_blue, self.accent_cyan)).pack(pady=25)
        ctk.CTkButton(card, text="العودة لتسجيل الدخول", command=self.show_login_page, fg_color="transparent", text_color="gray").pack()

    def handle_signup(self):
        name = self.reg_name.get()
        aid = self.reg_id.get()
        major = self.reg_major.get()
        pwd = self.reg_pass.get()
        if add_user(name, aid, major, pwd):
            messagebox.showinfo("نجاح", "تم إنشاء الحساب")
            self.show_login_page()
        else:
            messagebox.showerror("خطأ", "الرقم مسجل مسبقاً")

    def show_about_us(self):
        about_win = ctk.CTkToplevel(self)
        about_win.title("حول FurtherHub")
        about_win.geometry("500x550")
        
        # ضمان ظهور النافذة في المقدمة
        about_win.lift()
        about_win.attributes("-topmost", True)
        about_win.focus_force()
        
        about_win.resizable(False, False)
        
        # الأيقونة
    def show_about_us(self):
        about_win = ctk.CTkToplevel(self)
        about_win.title("حول FurtherHub")
        about_win.geometry("500x580")
        
        # لضمان بقاء النافذة في المقدمة
        about_win.lift()
        about_win.attributes("-topmost", True)
        about_win.focus_force()
        about_win.resizable(False, False)
        
        # الأيقونة (اللوجو)
        if self.logo_image:
            ctk.CTkLabel(about_win, image=self.logo_image, text="").pack(pady=(20, 10))
            
        ctk.CTkLabel(about_win, text="منصة FurtherHub", 
                     font=("Tajawal", 22, "bold"), text_color=self.accent_cyan).pack()
        
        # النص الذي اخترتِيه (تم تنسيقه ليظهر بوضوح)
        about_text = (
            " هي فكرة طلابية طموحة تهدف لتنظيم\n"
            "وتسهيل تبادل المصادر التعليمية بين طلاب كلية الحاسب.\n\n"
            "تعتمد المنصة على الشفافية، حيث يمكن للطلاب مشاركة\n"
            "المصادر، كتابة المراجعات، وتقييم المحتوى لضمان جودة\n"
            "المادة العلمية المتداولة."
        )
        
        ctk.CTkLabel(about_win, text=about_text, font=("Tajawal", 13), 
                     text_color=("gray20", "gray85"), justify="center").pack(pady=20, padx=30)

        # بطاقة فريق العمل (سارة، نوف، غدير)
        team_card = ctk.CTkFrame(about_win, corner_radius=15, fg_color=("#E8ECEF", "#2A2A2A"))
        team_card.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkLabel(team_card, text="تطوير وإعداد:", 
                     font=("Tajawal", 12, "bold"), text_color="gray").pack(pady=(10, 0))
        
        ctk.CTkLabel(team_card, text="💎 سارة  •  💎 نوف  •  💎 غدير", 
                     font=("Tajawal", 16, "bold"), text_color=self.primary_blue).pack(pady=(5, 15))
        
        # تذييل النافذة (حقوق الملكية)
        ctk.CTkLabel(about_win, text="بُني بأيدي طلابية.. منكم وإليكم ✨ © 2026", 
                     font=("Tajawal", 10, "italic"), text_color="gray").pack(side="bottom", pady=15)


if __name__ == "__main__":
    app = AcademicApp()
    app.mainloop()

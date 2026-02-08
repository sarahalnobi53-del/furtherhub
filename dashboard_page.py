import customtkinter as ctk
from PIL import Image
import os
from database_manger import get_courses_by_major 

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, user_name, user_major, **kwargs):
        # اعتماد ألوان صفحة المصادر
        self.bg_color = ("#F5F7FA", "#121212")
        super().__init__(parent, fg_color=self.bg_color, **kwargs)
        
        self.user_name = user_name
        self.user_major = user_major.strip() if user_major else "علوم حاسوب"
        self.controller = parent.master if hasattr(parent, 'master') else None
        
        # إعدادات الألوان الموحدة
        self.card_color = ("#FFFFFF", "#1E1E1E")
        self.text_color = ("#1f538d", "#FFFFFF")
        self.accent_color = ("#1f538d", "#00ADB5")
        
        self.setup_ui()

    def setup_ui(self):
        # 1. الشريط العلوي (Header)
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=70) # زدنا الارتفاع قليلاً
        self.header.pack(fill="x", side="top", padx=20, pady=10)
        
        # --- ترتيب العناصر من اليمين إلى اليسار ---

        # أولاً: زر الوضع الليلي (أقصى اليمين)
        self.mode_switch = ctk.CTkSwitch(
            self.header, text="الوضع الليلي",
            command=self.change_appearance_mode, 
            progress_color="#00ADB5",
            text_color=self.text_color,
            font=("Tajawal", 12)
        )
        self.mode_switch.pack(side="right", padx=10)
        
        if ctk.get_appearance_mode() == "Dark":
            self.mode_switch.select()

        # ثانياً: ترحيب المستخدم
        self.user_info = ctk.CTkLabel(
            self.header, text=f"أهلاً، {self.user_name} 👤", 
            font=("Tajawal", 15, "bold"), 
            text_color=self.text_color
        )
        self.user_info.pack(side="right", padx=15)
        
        # ثالثاً: خانة البحث (تم تطويلها لـ 400 بكسل وجعلها أوضح)
        self.search_bar = ctk.CTkEntry(
            self.header, 
            placeholder_text="🔍 ابحث عن مادة برمجية أو هندسية...", 
            width=400, # هنا جعلناه طويلاً كما طلبتِ
            height=40, 
            corner_radius=20, 
            justify="right",
            font=("Tajawal", 13),
            fg_color=self.card_color,
            border_width=2, # جعلنا الحدود أوضح
            border_color=("#E0E0E0", "#333333")
        )
        self.search_bar.pack(side="right", padx=30)

        # 2. منطقة التبويبات (أزرار التخصصات)
        self.tabs_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tabs_frame.pack(fill="x", padx=30, pady=10)

        for text in ["نظم معلومات", "ذكاء اصطناعي", "هندسة برمجيات", "أمن سيبراني", "علوم حاسوب"]:
            is_active = (text == self.user_major)
            btn = ctk.CTkButton(
                self.tabs_frame, text=text, 
                fg_color=self.accent_color if is_active else ("white", "#2B2B2B"),
                text_color="white" if is_active else self.text_color,
                corner_radius=15, height=35,
                border_width=1, border_color="#E0E0E0",
                command=lambda t=text: self.update_view(t)
            )
            btn.pack(side="right", padx=5)

        # 3. عنوان القسم
        self.title_lbl = ctk.CTkLabel(
            self, text=f"موادك الحالية - {self.user_major}", 
            font=("Tajawal", 20, "bold"), 
            text_color=self.text_color
        )
        self.title_lbl.pack(anchor="e", padx=40, pady=10)

        # 4. منطقة عرض المواد (Grid)
        self.grid_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.grid_container.pack(expand=True, fill="both", padx=30, pady=10)

        self.update_view(self.user_major)

    def update_view(self, specialty):
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        
        courses = get_courses_by_major(specialty)
        for i, course in enumerate(courses):
            self.create_card(course, i // 3, i % 3)

    def create_card(self, data, r, c):
        # بطاقة المواد بنفس ستايل بطاقة المصادر
        card = ctk.CTkFrame(self.grid_container, fg_color=self.card_color, 
                             corner_radius=15, border_width=1, border_color=("gray85", "#333333"), cursor="hand2")
        card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
        self.grid_container.grid_columnconfigure(c, weight=1)

        try:
            if data["img_path"] and os.path.exists(data["img_path"]):
                pil_image = Image.open(data["img_path"])
                my_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(180, 120))
                img_lbl = ctk.CTkLabel(card, text="", image=my_image)
                img_lbl.pack(pady=(15, 5))
            else: raise Exception()
        except:
            img_lbl = ctk.CTkLabel(card, text="📚", font=("Arial", 50))
            img_lbl.pack(pady=(15, 5))

        name_lbl = ctk.CTkLabel(card, text=data["name"], font=("Tajawal", 15, "bold"), text_color=self.text_color)
        name_lbl.pack(pady=(5, 15))

        # ربط الضغط
        callback = lambda e, sid=data['id'], sn=data['name']: self.on_card_click(sid, sn)
        card.bind("<Button-1>", callback)
        img_lbl.bind("<Button-1>", callback)
        name_lbl.bind("<Button-1>", callback)

    def on_card_click(self, subject_id, subject_name):
        if self.controller: self.controller.show_resources_page(subject_id, subject_name)

    def change_appearance_mode(self):
        mode = "dark" if self.mode_switch.get() == 1 else "light"
        ctk.set_appearance_mode(mode)

import customtkinter as ctk
from tkinter import messagebox
import webbrowser
# تأكدي أن هذه الملفات موجودة في نفس المجلد
from reviws_window import ReviewsWindow
from ai_uploader import AIUploaderWindow
# الاستيراد من ملف الداتا المعتمد لدينا
from database_manger import get_resources_by_subject, get_comments_by_resource, add_comment

class ResourcesPage(ctk.CTkFrame):
    def __init__(self, parent, controller, subject_name, subject_id, resources_list=None):
        super().__init__(parent)
        self.controller = controller
        self.subject_name = subject_name
        self.subject_id = subject_id
        
        # إذا لم يتم تمرير قائمة، نجلبها من قاعدة البيانات مباشرة
        if resources_list is None:
            self.all_resources = get_resources_by_subject(subject_id)
        else:
            self.all_resources = resources_list
        
        # إعداد الألوان
        self.bg_color = ("#F5F7FA", "#121212") 
        self.card_color = ("#FFFFFF", "#1E1E1E")
        self.text_color = ("#1f538d", "#FFFFFF")
        self.accent_color = ("#1f538d", "#00ADB5")
        
        self.configure(fg_color=self.bg_color)
        
        # بناء الواجهة
        self.create_header()
        self.create_filters()
        
        # منطقة التمرير
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # عرض البيانات الأولية
        self.display_resources("الكل")

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        # 1. زر العودة (أقصى اليسار)
        btn_back = ctk.CTkButton(
            header, text="← عودة", width=80, 
            fg_color="transparent", text_color=self.text_color, border_width=1,
            command=self.go_back
        )
        btn_back.pack(side="left")
        
        # 2. زر إضافة مصدر (بجانب زر العودة)
        self.add_btn = ctk.CTkButton(
            header, text="+ إضافة مصدر", width=120, height=35,
            fg_color=self.accent_color, hover_color="#2c85e1",
            font=("Tajawal", 13, "bold"),
            command=self.open_add_window
        )
        self.add_btn.pack(side="left", padx=10)

        # 3. زر الثيم / الوضع الليلي (أقصى اليمين)
        self.theme_switch = ctk.CTkSwitch(
            header, text="الوضع الليلي", 
            command=self.toggle_theme,
            onvalue="dark", offvalue="light",
            progress_color="#00ADB5",
            text_color=self.text_color,
            font=("Tajawal", 12)
        )
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()
        self.theme_switch.pack(side="right")

        # 4. العنوان (يبقى في المنتصف تماماً)
        title = ctk.CTkLabel(
            header, text=f"مصادر: {self.subject_name}", 
            font=("Tajawal", 22, "bold"), text_color=self.text_color
        )
        title.place(relx=0.5, rely=0.5, anchor="center")

    def create_filters(self):
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=30, pady=10)
        
        categories = ["الكل", "فيديوهات يوتيوب", "مواقع ويب", "مراجع", "نماذج اختبارات"]
        
        for cat in categories:
            btn = ctk.CTkButton(
                filter_frame, text=cat, width=100, height=35,
                corner_radius=18, font=("Tajawal", 13),
                fg_color=("white", "#2B2B2B"),
                text_color=self.text_color,
                border_width=1, border_color="#E0E0E0",
                hover_color=self.accent_color,
                command=lambda c=cat: self.display_resources(c)
            )
            btn.pack(side="right", padx=5)

    def display_resources(self, category_filter):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        if category_filter == "الكل":
            filtered_data = self.all_resources
        else:
            filtered_data = [r for r in self.all_resources if r['category'] == category_filter]

        if not filtered_data:
            ctk.CTkLabel(self.scrollable_frame, text="لا توجد مصادر في هذا القسم حالياً", font=("Tajawal", 16)).pack(pady=50)
            return

        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=1)

        for index, item in enumerate(filtered_data):
            self.create_resource_card(item, index // 2, index % 2)

    def create_resource_card(self, item, r, c):
        icons = {"فيديوهات يوتيوب": "▶️", "مواقع ويب": "🌐", "مراجع": "📚", "نماذج اختبارات": "📝"}
        icon_symbol = icons.get(item['category'], "📁")
        
        card = ctk.CTkFrame(self.scrollable_frame, fg_color=self.card_color, corner_radius=15, border_width=1, border_color=("gray80", "#333333"))
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(card, text=icon_symbol, font=("Arial", 30)).pack(pady=(15, 5))
        
        ctk.CTkLabel(card, text=item['title'], font=("Tajawal", 15, "bold"), text_color=self.text_color).pack()
        
        ctk.CTkLabel(card, text=item['description'], font=("Tajawal", 12), text_color=("gray", "gray70"), wraplength=200).pack(pady=5)

        ctk.CTkButton(
            card, text="تصفح الآن", width=120, height=30,
            fg_color=self.accent_color, font=("Tajawal", 12, "bold"),
            command=lambda link=item['link']: self.open_link(link)
        ).pack(pady=(10, 5))

        ctk.CTkButton(
            card, text="⭐ التقييمات والتعليقات", height=30,
            fg_color="transparent", border_width=1, border_color=self.accent_color,
            text_color=self.accent_color, hover_color=("#f0f0f0", "#2b2b2b"),
            command=lambda r=item: self.open_reviews_window(r)
        ).pack(pady=(5, 15), fill="x", padx=20)

    def open_add_window(self):
        # هنا نفترض أن كود AIUploaderWindow جاهز ويستقبل الـ callback
        add_window = AIUploaderWindow(self, self.subject_id, self.refresh_data)
        add_window.grab_set()
        add_window.focus_set()

    def refresh_data(self):
        self.all_resources = get_resources_by_subject(self.subject_id)
        self.display_resources("الكل")

    def open_reviews_window(self, resource):
        if hasattr(self, 'rev_window') and self.rev_window.winfo_exists():
            self.rev_window.focus()
            return
        self.rev_window = ReviewsWindow(self, resource)

    def open_link(self, link):
        webbrowser.open(link)

    def toggle_theme(self):
        ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")

    def go_back(self):
        # هذه الدالة تتواصل مع الكلاس الأب (Main App) للعودة
        if self.controller:
            self.controller.show_dashboard()
        else:
            self.destroy() # في حالة التجربة المنفصلة

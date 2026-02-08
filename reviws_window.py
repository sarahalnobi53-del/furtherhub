import customtkinter as ctk
from tkinter import messagebox
from database_manger import get_comments_by_resource, add_comment

class ReviewsWindow(ctk.CTkToplevel):
    def __init__(self, parent, resource):
        super().__init__(parent)
        
        self.resource = resource
        self.res_id = resource.get('id')
        
        # 1. إعدادات النافذة (نفس الأبعاد والخصائص)
        self.title(f"آراء الطالبات حول: {resource['title']}")
        self.geometry("450x650")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grab_set() # عزل الخلفية

        # بناء الواجهة
        self.setup_ui()
        # تحميل التعليقات فور التشغيل
        self.load_comments()

    def setup_ui(self):
        # --- الجزء العلوي: الهيدر ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(20, 10), padx=20, fill="x")

        ctk.CTkLabel(
            header_frame, 
            text="التعليقات والتقييمات", 
            font=("Tajawal", 22, "bold"),
            text_color=("#1f538d", "#00ADB5")
        ).pack(anchor="e")

        ctk.CTkLabel(
            header_frame, 
            text="آراء الزملاء حول هذا المورد التعليمي", 
            font=("Tajawal", 12),
            text_color="gray"
        ).pack(anchor="e")

        # --- الجزء الأوسط: إطار التعليقات ---
        self.comments_scroll = ctk.CTkScrollableFrame(
            self, 
            width=400, 
            height=250,
            fg_color="transparent",
            scrollbar_button_color=("#1f538d", "#00ADB5")
        )
        self.comments_scroll.pack(pady=5, padx=15, fill="both", expand=True)

        # --- الجزء السفلي: إضافة تعليق جديد ---
        input_frame = ctk.CTkFrame(self, corner_radius=20, border_width=1)
        input_frame.pack(pady=15, padx=20, fill="x")

        ctk.CTkLabel(input_frame, text="أضفي رأيكِ الخاص", font=("Tajawal", 13, "bold")).pack(pady=(10, 5), padx=20, anchor="e")

        self.name_entry = ctk.CTkEntry(input_frame, placeholder_text="اسمكِ (اختياري)", width=350, justify="right")
        self.name_entry.pack(pady=5)
        
        self.rating_menu = ctk.CTkSegmentedButton(input_frame, values=["1", "2", "3", "4", "5"], font=("Arial", 12, "bold"))
        self.rating_menu.set("5")
        self.rating_menu.pack(pady=5)
        
        self.comment_text = ctk.CTkTextbox(input_frame, width=350, height=70, font=("Tajawal", 12))
        self.comment_text.pack(pady=5)

        ctk.CTkButton(
            input_frame, 
            text="نشر التعليق", 
            font=("Tajawal", 14, "bold"),
            fg_color=("#1f538d", "#00ADB5"),
            height=40,
            command=self.save_comment # ربط الزر بدالة الحفظ
        ).pack(pady=(10, 15))

    def load_comments(self):
        """دالة لعرض التعليقات (تستخدم عند البدء وعند التحديث)"""
        # تنظيف القائمة الحالية قبل العرض
        for widget in self.comments_scroll.winfo_children():
            widget.destroy()

        existing_comments = get_comments_by_resource(self.res_id)

        if not existing_comments:
            ctk.CTkLabel(
                self.comments_scroll, 
                text="لا توجد تعليقات بعد..\nشاركنا رأيك لتفيد غيرك!", 
                font=("Tajawal", 13, "italic"),
                text_color="gray"
            ).pack(pady=50)
        else:
            for comm in existing_comments:
                # تصميم "فقاعة" التعليق (نفس الألوان بالضبط)
                bubble = ctk.CTkFrame(self.comments_scroll, corner_radius=15, fg_color=("#EEEEEE", "#2b2b2b"))
                bubble.pack(fill="x", pady=8, padx=5)
                
                # السطر الأول: الاسم والنجوم
                info_frame = ctk.CTkFrame(bubble, fg_color="transparent")
                info_frame.pack(fill="x", padx=10, pady=(5, 0))
                
                stars = "⭐" * int(comm[1])
                ctk.CTkLabel(info_frame, text=stars, font=("Arial", 12)).pack(side="left")
                ctk.CTkLabel(info_frame, text=comm[0], font=("Tajawal", 12, "bold"), text_color=("#1f538d", "#00ADB5")).pack(side="right")
                
                # السطر الثاني: نص التعليق
                ctk.CTkLabel(
                    bubble, 
                    text=comm[2], 
                    wraplength=350, 
                    justify="right", 
                    font=("Tajawal", 12)
                ).pack(anchor="e", padx=15, pady=(0, 10))

    def save_comment(self):
        user_name = self.name_entry.get().strip() or "طالبة"
        user_msg = self.comment_text.get("1.0", "end").strip()
        
        if user_msg:
            add_comment(self.res_id, user_name, int(self.rating_menu.get()), user_msg)
            
            # بدلاً من إغلاق النافذة وفتحها، نمسح الحقول ونحدث القائمة
            self.comment_text.delete("1.0", "end")
            self.name_entry.delete(0, "end")
            self.load_comments() # إعادة تحميل القائمة لتظهر التعليق الجديد
        else:
            messagebox.showwarning("نقص بيانات", "لطفاً، اكتب تعليقك أولاً قبل الإرسال.")

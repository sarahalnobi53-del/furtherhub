import customtkinter as ctk
from tkinter import messagebox
import re
from database_manger import add_resource 

# --- 1. منطق الفحص الذكي بمواد التخصص ---
def ai_check_resource(description, link):
    # فحص الرابط
    if not re.match(r"https?://", link.strip()):
        return "error", "(httpيجب أن يبدأ بـ ) عذراً، الرابط غير صالح "

    
    academic_keywords = [
        "دورة", "شرح", "تعلم", "كورس", "محاضرة", "كتاب", "برمجة", "خوارزميات",
        "أنظمة المؤسسات", "الطرق الرياضية", "مبادئ الذكاء الاصطناعي", 
        "إنترنت الأشياء", "علم البيانات", "إدارة المخاطر", "الجرائم الإلكترونية",
        "الوسائط المتعددة", "الأنظمة المضمنة", "ريادة الأعمال", "جبر خطي",
        "تحليل وتصميم الخوارزميات", "هندسة البرمجيات", "التصميم الرقمي",
        "معمارية الحاسوب", "لغة التجميع", "مشروع تخرج", "هندسة متطلبات",
        "تصميم البرمجيات", "فحص وتدقيق البرمجيات", "صيانة وتطور البرمجيات",
        "ضمان جودة البرمجيات", "أمنية المعلومات", "إدارة مشاريع",
        "تصميم واجهة المستخدم", "التحليل والتصميم الموجه بالكائنات", "نمذجة البرمجيات",
        "تكامل النظم", "agile", "هياكل متقطعة", "أساسيات الحاسوب", "برمجة حاسوب",
        "قواعد البيانات", "تطوير تطبيقات الويب", "هياكل البيانات", "نظم التشغيل",
        "الشبكات", "أخلاقيات الحوسبة", "الحوسبة السحابية", "تطبيقات الأجهزة النقالة",
        "فيزياء", "تفاضل وتكامل", "احصاء واحتمالات", "ثقافة إسلامية", "لغة عربية",
        "course", "explanation", "book", "lecture", "learn", "programming", 
        "algorithms", "study", "academic", "enterprise systems", 
        "mathematical methods", "artificial intelligence", "ai",
        "internet of things", "iot", "data science", "risk management", 
        "disaster recovery", "cyber crimes", "multimedia systems", 
        "embedded systems", "real-time systems", "entrepreneurship", 
        "physics", "linear algebra", "software engineering", "digital design", 
        "logic design", "computer architecture", "assembly language", 
        "graduation project", "requirements engineering", "software design", 
        "software testing", "software inspection", "software maintenance", 
        "software evolution", "software quality assurance", "sqa", 
        "information security", "cybersecurity", "project management", 
        "user interface design", "ui/ux", "object oriented analysis", 
        "ooad", "software modeling", "systems integration", "discrete structures", 
        "mathematics", "computer fundamentals", "problem solving", 
        "object oriented programming", "oop", "probability", "statistics", 
        "calculus", "research methodology", "database systems", "sql", 
        "web applications development", "data structures", "operating systems", 
        "data communication", "networks", "computing ethics", "cloud computing", 
        "mobile applications development"
    ]
    
    banned_keywords = ["لعبة", "ألعاب", "أغاني", "فيلم", "مجلة", "قصة", "رواية", "أفلام", 
                       "movies", "magazine", "game", "movie", "novel", "story", "music"]

    # تحويل وصف المستخدم إلى حروف صغيرة للفحص الذكي
    desc_lower = description.lower()

    # فحص المحتوى المرفوض أولاً
    if any(word in desc_lower for word in banned_keywords):
        return "rejected", "تم رفض المورد: المحتوى غير تعليمي أو مخالف"
    
    # فحص الانتماء لمواد التخصص
    if any(word in desc_lower for word in academic_keywords):
        return "accepted", "تم قبول المورد بنجاح: مورد أكاديمي معتمد"
    
    return "rejected", "المورد غير واضح أو لا ينتمي لمواد التخصص المعتمدة"

# --- 2. بناء الواجهة الرسومية (UI) ---
class AIUploaderWindow(ctk.CTkToplevel):              
    def __init__(self, parent, subject_id, refresh_callback):
        super().__init__(parent)
        
        # إعدادات البيانات
        self.subject_id = subject_id
        self.refresh_callback = refresh_callback 

        # إعدادات النافذة الجمالية
        self.title("FurtherHub | إضافة مورد أكاديمي")
        self.geometry("520x650")
        self.resizable(False, False)
        self.attributes("-topmost", True) # لتبقى دائماً في المقدمة
        
        # جعل النافذة "Modal" (تمنع التفاعل مع ما خلفها)
        self.grab_set()

        # التصميم الداخلي
        self.setup_ui()

    def setup_ui(self):
        # الإطار الرئيسي بحواف ناعمة
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, border_width=1)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # شعار المنصة أو العنوان الرئيسي
        self.brand_label = ctk.CTkLabel(
            self.main_frame, 
            text="إضافة مورد تعليمي للمادة", 
            font=("Tajawal", 24, "bold"),
            text_color=("#1f538d", "#00ADB5")
        )
        self.brand_label.pack(pady=(35, 40))

        # --- حقل الرابط ---
        self.create_label("رابط المورد (URL)")
        self.link_entry = ctk.CTkEntry(
            self.main_frame, width=380, height=45, 
            placeholder_text="https://example.com/resource",
            justify="left" # الروابط دائماً يسار
        )
        self.link_entry.pack(pady=(5, 15))

        # --- حقل الوصف ---
        self.create_label("وصف المورد (سيتم فحصه ذكياً)")
        self.desc_entry = ctk.CTkTextbox(
            self.main_frame, width=380, height=120, 
            border_width=1, font=("Tajawal", 12),
            activate_scrollbars=True
        )
        self.desc_entry.pack(pady=(5, 15))

        # --- نوع المورد ---
        self.create_label("تصنيف المورد")
        self.type_combo = ctk.CTkComboBox(
            self.main_frame, 
            values=["فيديوهات يوتيوب", "مواقع ويب", "مراجع", "نماذج اختبارات"], 
            width=380, height=40, font=("Tajawal", 12),
            state="readonly" # لمنع المستخدم من الكتابة اليدوية
        )
        self.type_combo.set("اختر التصنيف المناسب")
        self.type_combo.pack(pady=(5, 20))

        # --- زر الإضافة ---
        self.btn_check = ctk.CTkButton(
            self.main_frame, 
            text="تحليل وإضافة المورد الآن", 
            font=("Tajawal", 15, "bold"),
            height=55, width=380,
            corner_radius=12,
            fg_color=("#1f538d", "#00ADB5"),
            hover_color=("#164270", "#008a91"),
            command=self.process_request
        )
        self.btn_check.pack(pady=10)

        # التذييل (Footer) للنتائج
        self.result_label = ctk.CTkLabel(self.main_frame, text="", font=("Tajawal", 13, "bold"))
        self.result_label.pack(pady=10)

    def create_label(self, text):
        """دالة مساعدة لإنشاء العناوين بتنسيق موحد"""
        lbl = ctk.CTkLabel(self.main_frame, text=text, font=("Tajawal", 12, "bold"))
        lbl.pack(anchor="e", padx=55)

    def process_request(self):
        # جلب البيانات وتنظيفها
        desc = self.desc_entry.get("1.0", "end-1c").strip()
        link = self.link_entry.get().strip()
        category = self.type_combo.get()
        
        # فحص الحقول الفارغة
        if not desc or not link or category == "اختر التصنيف المناسب":
            self.show_feedback("❌ برجاء إكمال جميع الحقول", "#e74c3c")
            return

        # استدعاء منطق الفحص (AI Logic) من الملف الأصلي
        from ai_uploader import ai_check_resource 
        status, msg = ai_check_resource(desc, link)
        
        if status == "accepted":
            self.show_feedback("✅ تم قبول المورد ذكياً", "#2ecc71")
            
            # استخراج عنوان تلقائي
            res_title = desc[:30].strip() + "..."
            
            # الحفظ في قاعدة البيانات
            try:
                add_resource(self.subject_id, category, res_title, desc, link)
                messagebox.showinfo("نجاح", f"تم إضافة المورد بنجاح إلى FurtherHub\n\nالمحتوى: {msg}")
                
                # تحديث الصفحة الرئيسية وإغلاق النافذة
                self.refresh_callback() 
                self.destroy()
            except Exception as e:
                messagebox.showerror("خطأ في القاعدة", f"فشل الحفظ: {e}")

        elif status == "rejected":
            self.show_feedback("❌ المورد غير مطابق للمعايير", "#e74c3c")
            messagebox.showwarning("رفض المورد", msg)
        else:
            self.show_feedback("⚠️ خطأ في البيانات", "#f39c12")
            messagebox.showerror("تنبيه", msg)

    def show_feedback(self, text, color):
        """تحديث نص النتيجة أسفل الزر"""
        self.result_label.configure(text=text, text_color=color)

# --- لتجربة النافذة بشكل مستقل (اختياري) ---
if __name__ == "__main__":
    root = ctk.CTk()
    def dummy_refresh(): print("تم التحديث!")
    # تجربة النافذة مع id مادة وهمي
    btn = ctk.CTkButton(root, text="فتح النافذة", command=lambda: AIUploaderWindow(root, 16, dummy_refresh))
    btn.pack(pady=50)
    root.mainloop()

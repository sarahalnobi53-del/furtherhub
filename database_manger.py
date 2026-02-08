import sqlite3

DB_NAME = 'academic_legacy.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. جدول المستخدمين
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   academic_id TEXT UNIQUE, 
                   name TEXT, 
                   major TEXT, 
                   password TEXT)''')
    
    # 2. جدول المواد (بدون progress)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            major TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            img_path TEXT
        )
    ''')

    # 3. جدول المصادر
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            category TEXT,
            title TEXT,
            description TEXT,
            link TEXT,
            FOREIGN KEY (subject_id) REFERENCES Subjects(id)
        )
    ''')

    # 4. جدول التعليقات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER,
            student_name TEXT,
            rating INTEGER,
            comment_text TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resource_id) REFERENCES Resources(id)
        )
    ''')

    conn.commit()
    conn.close()

# --- دوال المستخدمين ---
def add_user(full_name, academic_id, major, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (name, academic_id, major, password) VALUES (?, ?, ?, ?)", 
                       (full_name, academic_id, major, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(academic_id, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, major FROM Users WHERE academic_id = ? AND password = ?", (academic_id, password))
    result = cursor.fetchone()
    conn.close()
    return result

# --- دوال الجلب ---
def get_courses_by_major(major_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject_name, img_path FROM Subjects WHERE major = ?", (major_name.strip(),))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "img_path": r[2]} for r in rows]

def get_resources_by_subject(subject_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # البحث عن المصادر المرتبطة بهذا الـ ID
    cursor.execute("SELECT id, category, title, description, link FROM Resources WHERE subject_id = ?", (subject_id,))
    data = cursor.fetchall()
    
    # تحويل البيانات إلى قائمة قواميس (كما تتوقع واجهتك الاحترافية)
    resources = []
    for r in data:
        resources.append({
            "id": r[0],
            "category": r[1].strip() if r[1] else "", # تنظيف الفئة من المسافات
            "title": r[2],
            "description": r[3],
            "link": r[4]
        })
    
    conn.close()
    
    # سأطبع لك النتيجة في الـ Terminal لتعرفي إذا كانت المشكلة في الداتا أو الواجهة
    print(f"--- فحص المصادر للمادة {subject_id} ---")
    print(f"عدد المصادر المكتشفة: {len(resources)}")
    
    return resources
# --- دالة تعبئة البيانات الكاملة (24 مصدر) ---
def seed_all_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # مسح البيانات القديمة
    cursor.execute("DELETE FROM Resources")
    cursor.execute("DELETE FROM Subjects")
    
    # السحر هنا: تصفير العدادات لتبدأ الأرقام من 1 دائماً
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Subjects'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Resources'")
    
    conn.commit()

    def quick_add_sub(major, name, img):
        cursor.execute("INSERT INTO Subjects (major, subject_name, img_path) VALUES (?, ?, ?)", (major, name, img))
        return cursor.lastrowid

    def quick_add_res(s_id, cat, title, desc, link):
        cursor.execute("INSERT INTO Resources (subject_id, category, title, description, link) VALUES (?, ?, ?, ?, ?)", (s_id, cat, title, desc, link))

    # ١. مادة الرياضيات ١
    math_id = quick_add_sub("هندسة برمجيات", "رياضيات ١", "assets/math.jfif")
    math_res = [
        ("فيديوهات يوتيوب", "د. أحمد حجاج", "شروحات جامعية للرياضيات المتقطعة", "https://youtube.com/@dr.ahmedhagag"),
        ("مواقع ويب", "MIT OpenCourseWare", "محاضرات جامعية عالمية", "https://ocw.mit.edu"),
        ("فيديوهات يوتيوب", "3Blue1Brown", "شرح بصري متقدم للتفاضل والتكامل", "https://youtube.com/@3blue1brown"),
        ("فيديوهات يوتيوب", "University Physics", "قناة متخصصة في الفيزياء والرياضيات", "https://youtube.com/@physics-university"),
        ("مواقع ويب", "Khan Academy", "دروس متقدمة في الجبر والإحصاء", "https://www.khanacademy.org"),
        ("مراجع", "مرجع التفاضل والتكامل", "كتاب أساسي في حساب التفاضل", "https://example.com"),
        ("نماذج اختبارات", "نماذج اختبارات سابقة", "مجموعة من الاختبارات التجريبية", "https://example.com")
    ]
    for r in math_res: quick_add_res(math_id, r[0], r[1], r[2], r[3])

    # ٢. مادة HTML & CSS
    web_id = quick_add_sub("هندسة برمجيات", "HTML & CSS", "assets/html_css.jfif")
    web_res = [
        ("فيديوهات يوتيوب", "قناة جمال", "أساسيات الويب للمبتدئين", "https://youtube.com/@jamal"),
        ("فيديوهات يوتيوب", "الزيرو (Elzero)", "المسار الاحترافي للويب", "https://youtube.com/@elzero"),
        ("فيديوهات يوتيوب", "The Net Ninja", "شروحات بصرية مبسطة", "https://youtube.com/@thenetninja"),
        ("فيديوهات يوتيوب", "freeCodeCamp.org", "تعلم كامل بالمشاريع", "https://youtube.com/@freecodecamp"),
        ("مواقع ويب", "W3Schools", "تعلم تفاعلي لـ HTML/CSS", "https://www.w3schools.com"),
        ("مراجع", "MDN Web Docs", "المرجع الرسمي لمطوري الويب", "https://developer.mozilla.org"),
        ("مراجع", "مرجع تقنيات الويب", "كتاب شامل لتقنيات الحديثة", "https://example.com"),
        ("نماذج اختبارات", "نماذج اختبارات سابقة", "تدريبات عملية على التصميم", "https://example.com")
    ]
    for r in web_res: quick_add_res(web_id, r[0], r[1], r[2], r[3])

    # ٣. مادة برمجة ++C
    cpp_id = quick_add_sub("هندسة برمجيات", "برمجة ++C", "assets/cpp.jfif")
    cpp_res = [
        ("فيديوهات يوتيوب", "قناة أبو هدهود", "المرجع الشامل لحل المشكلات", "https://www.youtube.com/@ProgrammingAdvices"),
        ("فيديوهات يوتيوب", "قناة الزيرو", "أساسيات لغة ++C", "https://www.youtube.com/@ElzeroWebSchool"),
        ("فيديوهات يوتيوب", "Programming with Mosh", "دروس منظمة ومبسطة", "https://www.youtube.com/@programmingwithmosh"),
        ("فيديوهات يوتيوب", "Codezilla", "شروحات مرئية واضحة", "https://www.youtube.com/@Codezilla"),
        ("مواقع ويب", "W3Schools C++", "دروس تفاعلية للغة ++C", "https://www.w3schools.com/cpp/"),
        ("مواقع ويب", "HackerRank", "تدريب على الخوارزميات", "https://www.hackerrank.com/domains/cpp"),
        ("مواقع ويب", "LeetCode", "تحديات التفكير البرمجي", "https://leetcode.com/"),
        ("مراجع", "مرجع لغة ++C", "كتاب تعليمي شامل", "https://en.cppreference.com/"),
        ("نماذج اختبارات", "نماذج اختبارات سابقة", "أسئلة سنوات سابقة", "https://example.com")
    ]
    for r in cpp_res: quick_add_res(cpp_id, r[0], r[1], r[2], r[3])

    # ٤. مادة برمجة بايثون
    python_id = quick_add_sub("هندسة برمجيات", "برمجة بايثون", "assets/python.jfif")
    python_res = [
        ("فيديوهات يوتيوب", "Elzero Web School", "كورس احترافي ومنظم جداً لتعلم بايثون من الصفر للاحتراف", "https://www.youtube.com/playlist?list=PLDoPjvoNmBAyE_gei5d18qkfIe-Z8mSdx"),
        ("فيديوهات يوتيوب", "قناة إبراهيم عادل (OctuCode)", "شرح تفاعلي يركز على التطبيق العملي وبناء المشاريع الحقيقية", "https://www.youtube.com/watch?v=ll3iQi55Q0w"),
        ("فيديوهات يوتيوب", "Codezilla", "أساسيات البرمجة بلغة بايثون في فيديو واحد ممتع وسريع", "https://www.youtube.com/watch?v=jTpx4Sot-Vs"),
        ("مراجع", "مرجع بايثون الشامل", "رابط تجريبي للمصادر الورقية", "https://example.com"),
        ("نماذج اختبارات", "نماذج بايثون", "رابط تجريبي للاختبارات", "https://example.com")
    ]
    for r in python_res: quick_add_res(python_id, r[0], r[1], r[2], r[3])

    # ٥. مادة تصميم منطقي
    logic_id = quick_add_sub("هندسة برمجيات", "تصميم منطقي", "assets/logic_design.jfif")
    logic_res = [
        ("فيديوهات يوتيوب", "NESO Academy - Logic Design", "كورس أجنبي يشرح مرجع التصميم المنطقي بالتفصيل", "https://youtube.com/playlist?list=PLy42_pl2XRL77NMLn3Cqf5h5yF2beUZB5"),
        ("فيديوهات يوتيوب", "قائمة شروحات ممتازة", "فيديوهات عربية مبسطة لمادة التصميم المنطقي", "https://youtube.com/playlist?list=PLSRx5jmWD9u1U8kqwkb43AP35Ssg7yPrS"),
        ("فيديوهات يوتيوب", "سلسلة التصميم المنطقي", "مجموعة فيديوهات تعليمية للمفاهيم الأساسية", "https://youtube.com/playlist?list=PLWCXN2IFIem2O63z0JfhQLycUUtO-EPzg"),
        ("فيديوهات يوتيوب", "شرح الأنظمة العددية", "فيديو يشرح التحويل بين الأنظمة العددية بالتفصيل", "https://youtu.be/0syhWLFdXdM"),
        ("فيديوهات يوتيوب", "أبو هدهود - الدرس ١٣", "أساسيات منطق الحساب والمنطق لكل مبرمج", "https://youtu.be/CrA3v6AHTTo"),
        ("مراجع", "كتاب Digital Logic", "رابط تجريبي للمرجع الأساسي", "https://example.com"),
        ("نماذج اختبارات", "نماذج Logic Design", "رابط تجريبي للتدريبات", "https://example.com")
    ]
    for r in logic_res: quick_add_res(logic_id, r[0], r[1], r[2], r[3])

    # تخصصات أخرى (للعرض فقط)
    quick_add_sub("علوم حاسوب", "هياكل بيانات", "assets/data_structure.jfif")
    quick_add_sub("أمن سيبراني", "مقدمة في التشفير", "assets/crypio.jfif")
    quick_add_sub("ذكاء اصطناعي", "مقدمة AI", "assets/ai.jfif")
    quick_add_sub("نظم معلومات", "إدارة قواعد بيانات", "assets/db_admin.jfif")

    conn.commit()
    conn.close()
    print("✅ تم بنجاح تعبئة كافة المصادر الـ 24 الأصلية!")

# --- بقية الدوال ---
def add_resource(subject_id, category, title, description, link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Resources (subject_id, category, title, description, link) VALUES (?, ?, ?, ?, ?)", (subject_id, category, title, description, link))
    conn.commit()
    conn.close()

def add_comment(resource_id, name, rating, text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Comments (resource_id, student_name, rating, comment_text) VALUES (?, ?, ?, ?)", (resource_id, name, rating, text))
    conn.commit()
    conn.close()

def get_comments_by_resource(resource_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, rating, comment_text, date FROM Comments WHERE resource_id = ? ORDER BY date DESC", (resource_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    seed_all_data()

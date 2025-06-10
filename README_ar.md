# 🧱 Resume Builder – Step 01

**المرحلة الأولى من مشروع إدارة السيرة الذاتية التفاعلية باستخدام Flask**

---

## 🎯 الهدف من هذه المرحلة

توفير واجهة ديناميكية لإدارة أقسام السيرة الذاتية (Resume Sections) بشكل احترافي، تشمل:
- ➕ إضافة قسم جديد
- ✏️ تعديل القسم مباشرة داخل الصفحة
- 🗑 حذف القسم مع تأكيد
- ⬆️⬇️ تغيير ترتيب العرض
- 👁️🚫 إظهار أو إخفاء القسم
- 📄 عرض الفقرات والحقول المرتبطة
- ✅ تنبيهات Flash فورية لكل عملية
- 🌐 دعم الترجمة الكامل باستخدام Flask-Babel

---

## 🧠 التكنولوجيا المستخدمة

- Python 3 + Flask
- SQLAlchemy (ORM)
- Jinja2 (قوالب)
- Flask-Babel (ترجمة)
- HTML + CSS مخصص يدويًا
- Session + Flash messages
- تصميم خفيف بدون Bootstrap أو Tailwind

---

## 📂 هيكل المشروع (المختصر)

```
/templates
  └── admin/resume_builder.html.j2

/routes
  └── admin_builder_routes.py

/models
  └── ResumeSection + Paragraph + Field

/static
  └── css/style.css (اختياري)

/app.py
/config.py
```

---

## 🚀 كيف تبدأ

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

---

## 📌 ملاحظات

- لا يتم استخدام أي إطار تصميم (Bootstrap/Tailwind) في هذه المرحلة عمدًا.
- جميع النصوص تدعم الترجمة باستخدام `gettext` و `{{ _('...') }}`.
- التصميم بسيط، لكن عملي ومهندَس للتوسعة مستقبلاً.

---

## 🛠️ الخطوة التالية

> ✅ Step02: إدارة الفقرات (Paragraphs) داخل كل قسم.

---

## 👨‍💻 المطور

By [@TamerOnLine](https://github.com/TamerOnLine)  
تحت مظلة مشروع [Flask University](https://github.com/Flask-University)
# 🧱 Resume Builder – Step 01

**The first stage of an interactive resume management system built with Flask**

---

## 🎯 Purpose of This Stage

Provide a dynamic interface to manage resume sections professionally, including:
- ➕ Add new section
- ✏️ Edit section inline
- 🗑 Delete section with confirmation
- ⬆️⬇️ Reorder sections visually
- 👁️🚫 Toggle section visibility
- 📄 Display paragraphs and fields under each section
- ✅ Flash messages for user feedback
- 🌐 Full translation support using Flask-Babel

---

## 🧠 Technologies Used

- Python 3 + Flask
- SQLAlchemy (ORM)
- Jinja2 (Templating)
- Flask-Babel (i18n)
- HTML + custom inline CSS
- Session + Flash messaging
- No CSS frameworks (Bootstrap/Tailwind) – by design

---

## 📂 Project Structure (Simplified)

```
/templates
  └── admin/resume_builder.html.j2

/routes
  └── admin_builder_routes.py

/models
  └── ResumeSection + Paragraph + Field

/static
  └── css/style.css (optional)

/app.py
/config.py
```

---

## 🚀 Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

---

## 📌 Notes

- This stage intentionally avoids design frameworks.
- All user-facing text is wrapped in `{{ _('...') }}` for translation.
- The UI is clean, simple, and ready for future enhancements.

---

## 🛠️ Next Step

> ✅ Step02: Manage resume paragraphs dynamically under each section.

---

## 👨‍💻 Developer

By [@TamerOnLine](https://github.com/TamerOnLine)  
Under the umbrella of [Flask University](https://github.com/Flask-University)
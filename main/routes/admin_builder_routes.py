from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.models import db, ResumeSection
from ..i18n_runtime import get_locale

admin_builder_bp = Blueprint("admin_builder", __name__)

# ✅ عرض واجهة بناء السيرة
@admin_builder_bp.route('/admin/resume_builder')
def resume_builder():
    sections = ResumeSection.query.order_by(ResumeSection.order).all()
    return render_template("admin/resume_builder.html.j2", sections=sections)

# ✅ إضافة قسم جديد
@admin_builder_bp.route('/admin/resume_section/add', methods=['POST'])
def add_resume_section():
    title = request.form.get('title')
    lang = request.form.get('lang', 'en')
    order = int(request.form.get('order', 0))
    section = ResumeSection(title=title, lang=lang, order=order)
    db.session.add(section)
    db.session.commit()
    flash("✅ Section added successfully", "success")
    return redirect(url_for('admin_builder.resume_builder'))

# ✅ تعديل قسم
@admin_builder_bp.route('/admin/resume_section/edit/<int:section_id>', methods=['POST'])
def edit_resume_section(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    section.title = request.form.get('title', section.title)
    section.lang = request.form.get('lang', section.lang)
    section.order = int(request.form.get('order', section.order))
    db.session.commit()
    flash("💾 Section updated successfully", "success")
    return redirect(url_for('admin_builder.resume_builder'))

# ✅ حذف قسم
@admin_builder_bp.route('/admin/resume_section/delete/<int:section_id>', methods=['POST'])
def delete_resume_section(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    db.session.delete(section)
    db.session.commit()
    flash("🗑️ Section deleted", "danger")
    return redirect(url_for('admin_builder.resume_builder'))

# ✅ تحريك قسم لأعلى
@admin_builder_bp.route('/admin/resume_section/move_up/<int:section_id>', methods=['POST'])
def move_up(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    previous = ResumeSection.query.filter(
        ResumeSection.order < section.order
    ).order_by(ResumeSection.order.desc()).first()
    if previous:
        section.order, previous.order = previous.order, section.order
        db.session.commit()
        flash("⬆️ Section moved up", "info")
    else:
        flash("⚠️ Already at the top", "warning")
    return redirect(url_for('admin_builder.resume_builder'))

# ✅ تحريك قسم لأسفل
@admin_builder_bp.route('/admin/resume_section/move_down/<int:section_id>', methods=['POST'])
def move_down(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    next_item = ResumeSection.query.filter(
        ResumeSection.order > section.order
    ).order_by(ResumeSection.order.asc()).first()
    if next_item:
        section.order, next_item.order = next_item.order, section.order
        db.session.commit()
        flash("⬇️ Section moved down", "info")
    else:
        flash("⚠️ Already at the bottom", "warning")
    return redirect(url_for('admin_builder.resume_builder'))

# ✅ إظهار/إخفاء قسم
@admin_builder_bp.route('/admin/resume_section/toggle_visibility/<int:section_id>', methods=['POST'])
def toggle_visibility(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    section.is_visible = not section.is_visible
    db.session.commit()
    if section.is_visible:
        flash("👁️ Section is now visible", "success")
    else:
        flash("🙈 Section is now hidden", "warning")
    return redirect(url_for('admin_builder.resume_builder'))

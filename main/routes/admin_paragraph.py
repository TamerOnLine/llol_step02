from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.models import db, ResumeSection, ResumeParagraph
from ..i18n_runtime import get_locale

admin_paragraph = Blueprint("admin_paragraph", __name__)

# ✅ عرض جميع الفقرات داخل قسم معين
@admin_paragraph.route('/section/<int:section_id>/view')
def single_section_view(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    paragraphs = section.paragraphs
    return render_template('admin/single_section_view.j2', section=section, paragraphs=paragraphs)

# ✅ إضافة فقرة
@admin_paragraph.route('/paragraph/add/<int:section_id>', methods=['POST'])
def add_paragraph(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    paragraph_type = request.form.get('type', 'basic')
    order = int(request.form.get('order', 0))
    is_visible = 'is_visible' in request.form

    paragraph = ResumeParagraph(
        resume_section_id=section.id,
        field_type=paragraph_type,
        order=order,
        is_visible=is_visible
    )
    db.session.add(paragraph)
    db.session.commit()
    flash("✅ Paragraph added successfully", "success")
    return redirect(url_for('admin_paragraph.single_section_view', section_id=section.id))

# ✅ تعديل فقرة
@admin_paragraph.route('/paragraph/edit/<int:paragraph_id>', methods=['POST'])
def edit_paragraph(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    paragraph.field_type = request.form.get('type', paragraph.field_type)
    paragraph.order = int(request.form.get('order', paragraph.order))
    paragraph.is_visible = 'is_visible' in request.form
    db.session.commit()
    flash("💾 Paragraph updated successfully", "success")
    return redirect(url_for('admin_paragraph.single_section_view', section_id=paragraph.resume_section_id))

# ✅ حذف فقرة
@admin_paragraph.route('/paragraph/delete/<int:paragraph_id>', methods=['POST'])
def delete_paragraph(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    section_id = paragraph.resume_section_id
    db.session.delete(paragraph)
    db.session.commit()
    flash("🗑️ Paragraph deleted", "danger")
    return redirect(url_for('admin_paragraph.single_section_view', section_id=section_id))

# ✅ إظهار/إخفاء فقرة
@admin_paragraph.route('/paragraph/toggle_visibility/<int:paragraph_id>', methods=['POST'])
def toggle_paragraph_visibility(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    paragraph.is_visible = not paragraph.is_visible
    db.session.commit()
    if paragraph.is_visible:
        flash("👁️ Paragraph is now visible", "success")
    else:
        flash("🙈 Paragraph is now hidden", "warning")
    return redirect(url_for('admin_paragraph.single_section_view', section_id=paragraph.resume_section_id))

# ✅ تحريك فقرة لأعلى
@admin_paragraph.route('/paragraph/move_up/<int:paragraph_id>', methods=['POST'])
def move_up(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    section = paragraph.resume_section
    previous = ResumeParagraph.query.filter(
        ResumeParagraph.resume_section_id == section.id,
        ResumeParagraph.order < paragraph.order
    ).order_by(ResumeParagraph.order.desc()).first()
    if previous:
        paragraph.order, previous.order = previous.order, paragraph.order
        db.session.commit()
        flash("⬆️ Paragraph moved up", "info")
    else:
        flash("⚠️ Already at the top", "warning")
    return redirect(url_for('admin_paragraph.single_section_view', section_id=section.id))

# ✅ تحريك فقرة لأسفل
@admin_paragraph.route('/paragraph/move_down/<int:paragraph_id>', methods=['POST'])
def move_down(paragraph_id):
    paragraph = ResumeParagraph.query.get_or_404(paragraph_id)
    section = paragraph.resume_section
    next_item = ResumeParagraph.query.filter(
        ResumeParagraph.resume_section_id == section.id,
        ResumeParagraph.order > paragraph.order
    ).order_by(ResumeParagraph.order.asc()).first()
    if next_item:
        paragraph.order, next_item.order = next_item.order, paragraph.order
        db.session.commit()
        flash("⬇️ Paragraph moved down", "info")
    else:
        flash("⚠️ Already at the bottom", "warning")
    return redirect(url_for('admin_paragraph.single_section_view', section_id=section.id))

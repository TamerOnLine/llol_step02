from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..models.models import db, ResumeSection
from flask_babel import force_locale
from ..i18n_runtime import get_locale

admin_builder_bp = Blueprint("admin_builder", __name__, url_prefix="/admin/builder")

@admin_builder_bp.route("/")
def resume_builder():
    sections = ResumeSection.query.order_by(ResumeSection.order).all()
    return render_template("admin/resume_builder.html.j2", sections=sections)

@admin_builder_bp.route("/add", methods=["POST"])
def add_resume_section():
    title = request.form.get("title")
    lang = request.form.get("lang")

    max_order = db.session.query(db.func.max(ResumeSection.order)).scalar() or 0
    form_order = request.form.get("order")
    if form_order:
        order = int(form_order)
    else:
        order = max_order + 1

    section = ResumeSection(title=title, lang=lang, order=order)
    db.session.add(section)
    db.session.commit()
    flash(f"✅ Section '{section.title}' added.", "success")
    return redirect(url_for("admin_builder.resume_builder"))

@admin_builder_bp.route("/edit/<int:section_id>", methods=["POST"])
def edit_resume_section(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    section.title = request.form.get("title")
    section.lang = request.form.get("lang")
    section.order = int(request.form.get("order"))
    db.session.commit()
    flash("✅ Section updated successfully!", "success")
    return redirect(url_for("admin_builder.resume_builder"))

@admin_builder_bp.route("/delete/<int:section_id>", methods=["POST"])
def delete_resume_section(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    db.session.delete(section)
    db.session.commit()
    flash(f"🗑 Section '{section.title}' deleted.", "danger")
    return redirect(url_for("admin_builder.resume_builder"))

@admin_builder_bp.route("/api/delete/<int:section_id>", methods=["POST"])
def api_delete_section(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    db.session.delete(section)
    db.session.commit()
    return jsonify({"status": "ok", "message": f"🗑 Section '{section.title}' deleted."})

@admin_builder_bp.route("/move_up/<int:section_id>", methods=["POST"])
def move_up(section_id):
    current = ResumeSection.query.get_or_404(section_id)
    above = ResumeSection.query.filter(ResumeSection.order < current.order).order_by(ResumeSection.order.desc()).first()
    if above:
        current.order, above.order = above.order, current.order
        db.session.commit()
        flash(f"⬆️ Section '{current.title}' moved up.", "info")
    else:
        flash("⚠️ Already at the top.", "warning")
    return redirect(url_for("admin_builder.resume_builder"))

@admin_builder_bp.route("/move_down/<int:section_id>", methods=["POST"])
def move_down(section_id):
    current = ResumeSection.query.get_or_404(section_id)
    below = ResumeSection.query.filter(ResumeSection.order > current.order).order_by(ResumeSection.order.asc()).first()
    if below:
        current.order, below.order = below.order, current.order
        db.session.commit()
        flash(f"⬇️ Section '{current.title}' moved down.", "info")
    else:
        flash("⚠️ Already at the bottom.", "warning")
    return redirect(url_for("admin_builder.resume_builder"))

@admin_builder_bp.route("/toggle_visibility/<int:section_id>", methods=["POST"])
def toggle_visibility(section_id):
    section = ResumeSection.query.get_or_404(section_id)
    section.is_visible = not section.is_visible
    db.session.commit()
    if section.is_visible:
        flash(f"👁️ Section '{section.title}' is now visible.", "success")
    else:
        flash(f"🚫 Section '{section.title}' is now hidden.", "warning")
    return redirect(url_for("admin_builder.resume_builder"))

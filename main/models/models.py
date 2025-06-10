from ..extensions import db

class Section(db.Model):
    """
    Core section table.
    """
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)


class Setting(db.Model):
    """
    Stores configuration settings as key-value pairs.
    """
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)


class ResumeSection(db.Model):
    """
    Resume section with language support and visibility toggle.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    lang = db.Column(db.String(10), nullable=False, default='en')
    is_visible = db.Column(db.Boolean, default=True)

    paragraphs = db.relationship(
        "ResumeParagraph",
        backref="resume_section",
        cascade="all, delete-orphan",
        lazy=True
    )


class ResumeParagraph(db.Model):
    """
    Paragraph unit under a resume section.
    """
    id = db.Column(db.Integer, primary_key=True)
    resume_section_id = db.Column(db.Integer, db.ForeignKey('resume_section.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., basic, with_description, with_date
    order = db.Column(db.Integer, nullable=False)
    is_visible = db.Column(db.Boolean, default=True)

    fields = db.relationship(
        "ResumeField",
        backref="resume_paragraph",
        cascade="all, delete-orphan",
        lazy=True
    )


class ResumeField(db.Model):
    """
    Key-value pair for details in a paragraph.
    """
    id = db.Column(db.Integer, primary_key=True)
    resume_paragraph_id = db.Column(db.Integer, db.ForeignKey('resume_paragraph.id'), nullable=False)
    key = db.Column(db.String(50), nullable=False)  # e.g., title, description, date
    value = db.Column(db.Text, nullable=True)
    is_visible = db.Column(db.Boolean, default=True)


class NavigationLink(db.Model):
    """
    Navigation items for the application menu.
    """
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10), default="")
    endpoint = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, default=0)
    is_visible = db.Column(db.Boolean, default=True)


class LanguageOption(db.Model):
    """
    Supported languages for localization.
    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    order = db.Column(db.Integer, default=0)
    is_visible = db.Column(db.Boolean, default=True)

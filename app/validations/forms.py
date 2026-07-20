from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional


class ValidationForm(FlaskForm):
    decision = SelectField('Keputusan', choices=[
        ('accepted', 'Setujui Hasil Model'),
        ('overridden', 'Ubah Hasil Model'),
    ], validators=[DataRequired()])

    final_class = SelectField('Kelas Final', choices=[
        ('Ringan', 'Ringan'),
        ('Sedang', 'Sedang'),
        ('Berat', 'Berat'),
    ], validators=[DataRequired()])

    initial_clinical_diagnosis = TextAreaField('Diagnosis Klinis Awal', validators=[Optional()])
    override_reason = TextAreaField('Alasan Perubahan', validators=[Optional()])
    clinical_note = TextAreaField('Catatan Klinis', validators=[Optional()])
    submit = SubmitField('Simpan & Kunci Pemeriksaan')

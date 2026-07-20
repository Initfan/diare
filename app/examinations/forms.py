from flask_wtf import FlaskForm
from wtforms import (IntegerField, SelectField, FloatField, TextAreaField,
                     SubmitField, HiddenField)
from wtforms.validators import DataRequired, NumberRange, Optional


class ExaminationForm(FlaskForm):
    patient_id = HiddenField('Patient ID', validators=[DataRequired()])

    age_months = IntegerField('Umur (bulan)', validators=[DataRequired(), NumberRange(min=1, max=200)])
    diarrhea_duration_days = IntegerField('Lama Diare (hari)', validators=[DataRequired(), NumberRange(min=1)])
    bowel_movement_frequency = IntegerField('Frekuensi BAB per hari', validators=[DataRequired(), NumberRange(min=1)])
    body_temperature = FloatField('Suhu Tubuh (°C)', validators=[DataRequired()])

    stool_consistency = SelectField('Konsistensi Feses', choices=[
        ('', '-- Pilih --'), ('Cair', 'Cair'), ('Lembek', 'Lembek')
    ], validators=[DataRequired()])

    stool_color = SelectField('Warna Feses', choices=[
        ('', '-- Pilih --'),
        ('Kuning', 'Kuning'),
        ('Kecoklatan', 'Kecoklatan'),
        ('Kehijauan', 'Kehijauan'),
        ('Kemerahan', 'Kemerahan'),
    ], validators=[DataRequired()])

    has_mucus = SelectField('Ada Lendir', choices=[
        ('', '-- Pilih --'), ('Ya', 'Ya'), ('Tidak', 'Tidak')
    ], validators=[DataRequired()])

    has_blood = SelectField('Ada Darah', choices=[
        ('', '-- Pilih --'), ('Ya', 'Ya'), ('Tidak', 'Tidak')
    ], validators=[DataRequired()])

    has_fever = SelectField('Demam', choices=[
        ('', '-- Pilih --'), ('Ya', 'Ya'), ('Tidak', 'Tidak')
    ], validators=[DataRequired()])

    has_vomiting = SelectField('Muntah', choices=[
        ('', '-- Pilih --'), ('Ya', 'Ya'), ('Tidak', 'Tidak')
    ], validators=[DataRequired()])

    dehydration_sign = SelectField('Tanda Dehidrasi', choices=[
        ('', '-- Pilih --'),
        ('Tidak Ada', 'Tidak Ada'),
        ('Ringan', 'Ringan'),
        ('Sedang', 'Sedang'),
        ('Berat', 'Berat'),
    ], validators=[DataRequired()])

    sex = SelectField('Jenis Kelamin', choices=[
        ('', '-- Pilih --'),
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ], validators=[DataRequired()])

    notes = TextAreaField('Catatan Petugas', validators=[Optional()])
    submit = SubmitField('Simpan & Jalankan Skrining')
    save_draft = SubmitField('Simpan Draft')

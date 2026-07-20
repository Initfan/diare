from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class PatientForm(FlaskForm):
    initials = StringField('Inisial Nama', validators=[DataRequired(), Length(min=1, max=10)])
    medical_record_number = StringField('Nomor Rekam Medis', validators=[Optional(), Length(max=50)])
    birth_date = DateField('Tanggal Lahir', validators=[DataRequired()])
    sex = SelectField('Jenis Kelamin', choices=[
        ('', '-- Pilih --'),
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan')
    ], validators=[DataRequired()])
    submit = SubmitField('Simpan')

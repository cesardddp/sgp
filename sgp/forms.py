
from flask_wtf import FlaskForm
from wtforms import StringField,DateField,BooleanField,SubmitField
from wtforms.fields.html5 import TelField
from wtforms_alchemy import PhoneNumberField
from wtforms.validators import DataRequired

class Projetos_form(FlaskForm):
    cliente_nome = StringField(
        # 'cliente_nome',
        label="Nome do Cliente",
        description = "Insira nome do cliente" ,
        validators=[ DataRequired()])
    telefone = PhoneNumberField(
        'Telefone',
        validators=[ DataRequired()],
        region="BR"
        )

    endereço = StringField('Endereço',validators=[DataRequired()])
    ambientes = StringField('Ambientes',validators=[DataRequired()])
    fotos_medição = StringField('fotos_medição',validators=[ ])
    promobe_arquivos = StringField('promobe_arquivos',validators=[ ])
    renders_jpg = StringField('renders_jpg',validators=[ ])
    medidas_pdf = StringField('medidas_pdf',validators=[ ])
    orçamento = StringField('orçamento',validators=[ ])
    pagamento = StringField('pagamento',validators=[ ])

    data_entrada = DateField('data_entrada',validators=[])
    data_medição = DateField('data_medição',validators=[])
    data_final = DateField('data_final',validators=[])
    data_apresentação = DateField('data_apresentação',validators=[])

    aprovação = BooleanField('aprovação',validators=[])
    submit = SubmitField("Enviar")

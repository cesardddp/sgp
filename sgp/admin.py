from flask_admin.contrib.sqla import ModelView
import uuid
from .forms import Projetos_form
# Flask and Flask-SQLAlchemy initialization here
from flask_admin import Admin

# admin=Admin()

def configure(app):
    admin = Admin(
        app,
        name='Projetos',
        template_mode='bootstrap4',
        # base_template='Projetos_master.html'
        )

    admin.add_view(ProjetoModelView(app.db.Projetos, app.db.session))


class ProjetoModelView(ModelView):
    

    page_size = 10  # the number of entries to display on the list view
    can_view_details = True

    # Removing columns from the list view is easy, just pass a list of column names for the column_excludes_list parameter:
    column_exclude_list = [ ]
    
    # To make columns searchable, or to use them for filtering, specify a list of column names:
    column_searchable_list = []
    column_filters = []
    
    # For a faster editing experience, enable inline editing in the list view:
    column_editable_list = []

    # Or, have the add & edit forms display inside a modal window on the list page, instead of the dedicated create & edit pages:'  
    create_modal = True
    create_modal_template = '/modal/create.html'

    edit_modal = True

    # To remove fields from the create and edit forms:
    form_excluded_columns = ["fotos_medição","promobe_arquivos","renders_jpg","medidas_pdf","orçamento","pagamento",
        "data_medição","data_final","data_apresentação","aprovação"]

    create_template = 'create.html'
    # edit_template = 'sgp_edit.html'
    # list_template = 'sgp_list.html'


    # can_delete = False  # disable model deletion
    # form_overrides = dict(id=uuid.uuid4().bytes);
    # form = Projetos_form


    

    # Add views
    # admin.register(ProjetoModelView, session=db.session)
    # admin.register(Tag, session=db.session)
    # admin.register(Post, session=db.session)
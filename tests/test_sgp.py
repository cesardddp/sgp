from SGP import sgp
import pytest
import os
import tempfile

from SGP.sgp import __version__
from SGP.sgp.app import app

def test_version():
    assert __version__ == '0.1.0'


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            app.db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def teste_novo_projeto(client):
    rv = cliente.get('/')
    assert b'No entreis here so far' in rv.data
from flask_login import current_user

from app.models.server import Server
from app.server.routes import find_server_by_id, find_server_by_name


def test_create_server(client, app):
    client.post('/register',
                data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test',
                      'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})

    with client:
        with app.app_context():
            response = client.post('/create-server',
                                        data={'name': 'example1234', 'cpu': 123, 'memory': 123, 'location': 'Nottingham'})
            assert response.status_code == 200
            assert Server.query.count() == 1
            assert Server.query.first().name == 'example1234'


def test_update_server(client, app):
    client.post('/register',
                data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test',
                      'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})

    client.post('/create-server',
                data={'name': 'example1234', 'cpu': 123, 'memory': 123, 'location': 'Nottingham'})

    response = client.post('/update-server?server_id=1',
                           data={'name': 'example1234', 'cpu': 967, 'memory': 123, 'location': 'Nottingham'})
    with app.app_context():
        assert response.status_code == 200
        assert Server.query.count() == 1
        server = Server.query.filter_by(name='example1234').first()
        assert server.cpu == 967



def test_delete_server_admin_passes(client, app):
    client.post('/register',
                data={'account_type': 'admin', 'email': 'test@gmail.com', 'first_name': 'Test',
                      'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})

    client.post('/create-server',
                data={'name': 'example1234', 'cpu': 123, 'memory': 123, 'location': 'Nottingham'})


    with app.app_context():
        server = Server.query.filter_by(name='example1234').first()
        assert server is not None

    with client:
        client.get('/delete-server?server_id=1')
        # assert current_user.is_admin == True # to fix i need to introduce sessions
        server = Server.query.filter_by(name='example1234').first()
        assert server is None


def test_delete_server_regular_fails(client, app):
    client.post('/register',
                data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test',
                      'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})

    client.post('/create-server',
                data={'name': 'example1234', 'cpu': 123, 'memory': 123, 'location': 'Nottingham'})


    with app.app_context():
        server = Server.query.filter_by(name='example1234').first()
        assert server is not None

    with client:
        client.get('/delete-server?server_id=1')
        assert current_user.is_admin == False
        server = Server.query.filter_by(name='example1234').first()
        assert server is not None

def test_find_server_by_name_found(init_server_table):
    server = find_server_by_name('exampleserver1')
    assert server is not None
    assert server.name == 'exampleserver1'
    assert server.cpu == 123

def test_find_server_by_name_not_found(init_server_table):
    server = find_server_by_name('exampleservernotfound')
    assert server is None

def test_find_server_by_id_found(init_server_table):
    server = find_server_by_id('3')
    assert server is not None
    assert server.name == 'exampleserver3'
    assert server.cpu == 789

def test_find_server_by_id_not_found(init_server_table):
    server = find_server_by_id('23456789')
    assert server is None
from flask_login import current_user

from app.models.server import Server

def test_create(client, app, auth):
    auth.register('Test', 'Smith', 'test@gmail.com', '#Password12345', '#Password12345', 'regular')
    auth.login('test@gmail.com', '#Password12345')

    with client:
        with app.app_context():
            response = client.post('/server/create',
                                        data={'name': 'io9877', 'cpu': 123, 'memory': 123, 'location': 'Nottingham'})
            assert response.status_code == 200
            server = Server.query.filter_by(name='io9877').first()
            assert server is not None


def test_update(client, app, auth):
    auth.register('Test', 'Smith', 'test@gmail.com', '#Password12345', '#Password12345', 'regular')
    auth.login('test@gmail.com', '#Password12345')

    client.post('/server/create',
                data={'name': 'io9877', 'cpu': 123, 'memory': 123, 'location': 'Nottingham'})

    with app.app_context():
        server = Server.query.filter_by(name='io9877').first()
        assert server is not None

    with client:
        response = client.post(f'server/update?server_id={server.id}',
                               data={'name': 'io9877', 'cpu': 967, 'memory': 123, 'location': 'Nottingham'})
        assert response.status_code == 200
        server = Server.query.filter_by(name='io9877').first()
        assert server.cpu == 967



def test_delete_admin_passes(client, app, auth):
    auth.register('Test', 'Smith', 'test@gmail.com', '#Password12345', '#Password12345', 'admin')
    auth.login('test@gmail.com', '#Password12345')

    client.post('/server/create',
                data={'name': 'io9877', 'cpu': 123, 'memory': 123, 'location': 'Nottingham'})


    with app.app_context():
        server = Server.query.filter_by(name='io9877').first()
        assert server is not None

    with client:
        client.get(f'/server/delete?server_id={server.id}' )
        server = Server.query.filter_by(name='io9877').first()
        assert server is None


def test_delete_regular_fails(client, app, auth):
    auth.register('Test', 'Smith', 'test@gmail.com', '#Password12345', '#Password12345', 'regular')
    auth.login('test@gmail.com', '#Password12345')

    client.post('/server/create',
                data={'name': 'io9877', 'cpu': 123, 'memory': 123, 'location': 'Nottingham'})


    with app.app_context():
        server = Server.query.filter_by(name='io9877').first()
        assert server is not None

    with client:
        client.get(f'/server/delete?server_id={server.id}')
        assert current_user.is_admin == False
        server = Server.query.filter_by(name='io9877').first()
        assert server is not None

def test_find_server_by_name_found(init_server_table):
    server = Server.find_server_by_name('aa1234')
    assert server is not None
    assert server.name == 'aa1234'
    assert server.cpu == 123

def test_find_server_by_name_not_found(init_server_table):
    server = Server.find_server_by_name('exampleservernotfound')
    assert server is None

def test_find_server_by_id_found(init_server_table):
    server = Server.find_server_by_id('13')
    assert server is not None
    assert server.name == 'aa3456'
    assert server.cpu == 789

def test_find_server_by_id_not_found(init_server_table):
    server = Server.find_server_by_id('23456789')
    assert server is None
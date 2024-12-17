from app.models.server import Server


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
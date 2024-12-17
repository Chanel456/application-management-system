from app.models.application import Application


def test_find_app_by_name_found(init_application_table):
    application = Application.find_application_by_name('App One')
    assert application is not None
    assert application.name == 'App One'
    assert application.url == 'https://appone.com'

def test_find_app_by_name_not_found(init_application_table):
    application = Application.find_application_by_name('Example App Not Found')
    assert application is None

def test_find_app_by_id_found(init_application_table):
    application = Application.find_application_by_id('13')
    assert application is not None
    assert application.name == 'App Three'
    assert application.url == 'https://appthree.com'

def test_find_app_by_id_not_found(init_application_table):
    application = Application.find_application_by_id('23456789')
    assert application is None

def test_find_app_by_url_found(init_application_table):
    application = Application.find_application_by_url('https://appone.com')
    assert application is not None
    assert application.name == 'App One'
    assert application.production_pods == 1

def test_find_app_by_url_not_found(init_application_table):
    application = Application.find_application_by_url('https://urlnotfound.com')
    assert application is None

def test_find_app_by_bitbucket_found(init_application_table):
    application = Application.find_application_by_bitbucket('https://bitbucket.com/repos/apptwo')
    assert application is not None
    assert application.name == 'App Two'
    assert application.production_pods == 1

def test_find_app_by_bitbucket_not_found(init_application_table):
    application = Application.find_application_by_bitbucket('https:/bitbucketnotfound.com')
    assert application is None
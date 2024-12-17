from app.models.user import User


def test_find_user_by_email_found(init_user_table):
    user = User.find_user_by_email('test.user1@gmail.com')
    assert user is not None
    assert user.first_name == 'Testuser1'
    assert user.last_name == 'Smith'

def test_find_user_by_email_not_found(init_user_table):
    user = User.find_user_by_email('does-not-exist@gmail.com')
    assert user is None
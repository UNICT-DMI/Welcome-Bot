import pytest
from pytest_mock import MockerFixture
import src.main as main

def test_Users() -> None:
    assert main.get_new_user_name(main.User(id=0, first_name='user', is_bot=True, username='user')) == '@user'
    assert main.get_new_user_name(main.User(id=0, first_name='user', is_bot=True)) == 'user'
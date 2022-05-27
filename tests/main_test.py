import asyncio
import pytest
import pytest_asyncio
from pytest_mock import MockerFixture
import src.main as main

users_list = [
    {'func': main.get_new_user_name, 'expected_res': '@user', 'arg': main.User(id=0, first_name='user', is_bot=True, username='user')},
    {'func': main.get_new_user_name, 'expected_res': 'user', 'arg': main.User(id=0, first_name='user', is_bot=True)}
]

@pytest.mark.parametrize('test', users_list)
def test_Users(test: dict) -> None:
    res = test['func'](test['arg'])
    assert res == test['expected_res']

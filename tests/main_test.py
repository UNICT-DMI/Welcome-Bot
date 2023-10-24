import pytest
from pytest_mock import MockerFixture
from telegram import Message, Chat, User, Update
from telegram.ext import Updater
from datetime import datetime
from main import main
from module.shared import welcome
from module.commands.welcome import send_welcome, generate_welcome, get_new_user_name


def get_wel(lan_code: str) -> str:
    wlc_mess_list = welcome[lan_code]

    #first element of the list
    return wlc_mess_list[0].replace("USER","@user")

possible_users = [
    User(id=0, first_name='user', is_bot=True, username='user'),  # bot with username
    User(id=0, first_name='user', is_bot=True),                   # bot without username
    User(id=0, first_name='user', is_bot=False, username='user'), # user with username
    User(id=0, first_name='user', is_bot=False),                   # user without username
    User(id=0, first_name='user', is_bot=False, username='user', language_code='it'), # italian user
    User(id=0, first_name='user', is_bot=False, username='user', language_code='en') # english user (same codepath as language_code=None)
]

tests = [
    {'func': get_new_user_name, 'expected_res': '@user', 'arg': (possible_users[0],)},
    {'func': get_new_user_name, 'expected_res': 'user',  'arg': (possible_users[1],)},
    {'func': get_new_user_name, 'expected_res': '@user', 'arg': (possible_users[2],)},
    {'func': get_new_user_name, 'expected_res': 'user',  'arg': (possible_users[3],)},
    { 
        'func': send_welcome, 
        'expected_res': None, 
        'arg': (Update(0, message=Message(0, new_chat_members=possible_users, chat=Chat(0, type='GROUP'), date=datetime.now())), None),
        'mock_obj': [Message],
        'mock_func': ['reply_text'],
        'mock_ret': [True],
        'is_async': True
    },
    {
        'func': generate_welcome,
        'expected_res': get_wel('it'), 
        'arg': (possible_users[4],), 
        'mock_obj': [main],
        'mock_func': ['randrange'],
        'mock_ret': [0]
    },
    {
        'func': generate_welcome,
        'expected_res': get_wel('en'), 
        'arg': (possible_users[5]), 
        'mock_obj': [main],
        'mock_func': ['randrange'],
        'mock_ret': [0]
    },
    {
        'func': main,
        'expected_res': None, 
        'arg': tuple(), 
        'mock_obj': [main, Updater],
        'mock_func': ['getenv', 'start_polling'],
        'mock_ret': ['123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11', True]
    }
]

@pytest.mark.parametrize('test', tests)
async def test_generic(mocker: MockerFixture, test: dict) -> None:
    spyed_objects = []
    if test.get('mock_obj') is not None:
        for index, obj in enumerate(test['mock_obj']):
            mocker.patch.object(obj, test['mock_func'][index], return_value=test['mock_ret'][index])
            spyed_objects.append(mocker.spy(obj, test['mock_func'][index]))

    if test.get('is_async'):
        res = await test['func'](*test['arg'])
    else:
        res = test['func'](*test['arg'])

    assert res == test['expected_res']
    for index, spy in enumerate(spyed_objects):
        assert spy.spy_return == test['mock_ret'][index]

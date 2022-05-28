import pytest
from pytest_mock import MockerFixture
from telegram import Message, Chat
from datetime import datetime
import src.main as main

possible_users = [
    main.User(id=0, first_name='user', is_bot=True, username='user'),  # bot with username
    main.User(id=0, first_name='user', is_bot=True),                   # bot without username
    main.User(id=0, first_name='user', is_bot=False, username='user'), # user with username
    main.User(id=0, first_name='user', is_bot=False)                   # user without username
]

tests = [
    {'func': main.get_new_user_name, 'expected_res': '@user', 'arg': (possible_users[0],), 'is_async': False},
    {'func': main.get_new_user_name, 'expected_res': 'user',  'arg': (possible_users[1],), 'is_async': False},
    {'func': main.get_new_user_name, 'expected_res': '@user', 'arg': (possible_users[2],), 'is_async': False},
    {'func': main.get_new_user_name, 'expected_res': 'user',  'arg': (possible_users[3],), 'is_async': False},
    { 
        'func': main.send_welcome, 
        'expected_res': None, 
        'arg': (main.Update(0, message=Message(0, new_chat_members=possible_users, chat=Chat(0, type='GROUP'), date=datetime.now())), None),
        'mock_obj': [Message],
        'mock_func': ['reply_text'],
        'mock_ret': [True],
        'is_async': True
    }
]

@pytest.mark.parametrize('test', tests)
async def test_generic(mocker: MockerFixture, test: dict) -> None:
    if test.get('mock_obj') is not None:
        for index, obj in enumerate(test['mock_obj']):
            mocker.patch.object(obj, test['mock_func'][index], return_value=test['mock_ret'][index])

    if test['is_async']:
        res = await test['func'](*test['arg'])
    else:
        res = test['func'](*test['arg'])

    assert res == test['expected_res']


def test_main(mocker: MockerFixture) -> None:
    mocker.patch.object(main, "__name__", "__main__")
    mocker.patch.object(main, 'main', return_value=None)

    assert main.init() == None
    

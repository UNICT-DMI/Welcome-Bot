import pytest
from pytest_mock import MockerFixture
from telegram import Message, Chat
from telegram.ext import Application
from datetime import datetime
import src.main as main


def get_wel(lan_code: str) -> str:

    with open("src/welcome.json", "r") as f:
        wlc_mess_list = main.load(f)[lan_code]['sentences']
    
    #first element of the list
    return wlc_mess_list[0].replace("USER","@user")

possible_users = [
    main.User(id=0, first_name='user', is_bot=True, username='user'),  # bot with username
    main.User(id=0, first_name='user', is_bot=True),                   # bot without username
    main.User(id=0, first_name='user', is_bot=False, username='user'), # user with username
    main.User(id=0, first_name='user', is_bot=False),                   # user without username
    main.User(id=0, first_name='user', is_bot=False, username='user', language_code='it'), # italian user
    main.User(id=0, first_name='user', is_bot=False, username='user', language_code='en') # english user (same codepath as language_code=None)
]

tests = [
    {'func': main.get_new_user_name, 'expected_res': '@user', 'arg': (possible_users[0],)},
    {'func': main.get_new_user_name, 'expected_res': 'user',  'arg': (possible_users[1],)},
    {'func': main.get_new_user_name, 'expected_res': '@user', 'arg': (possible_users[2],)},
    {'func': main.get_new_user_name, 'expected_res': 'user',  'arg': (possible_users[3],)},
    { 
        'func': main.send_welcome, 
        'expected_res': None, 
        'arg': (main.Update(0, message=Message(0, new_chat_members=possible_users, chat=Chat(0, type='GROUP'), date=datetime.now())), None),
        'mock_obj': [Message],
        'mock_func': ['reply_text'],
        'mock_ret': [True],
        'is_async': True
    },
    {
        'func': main.generate_welcome,
        'expected_res': get_wel('it'), 
        'arg': (possible_users[4],), 
        'mock_obj': [main],
        'mock_func': ['randrange'],
        'mock_ret': [0]
    },
    {
        'func': main.generate_welcome,
        'expected_res': get_wel('en'), 
        'arg': (possible_users[5],), 
        'mock_obj': [main],
        'mock_func': ['randrange'],
        'mock_ret': [0]
    },
    {
        'func': main.main,
        'expected_res': None, 
        'arg': tuple(), 
        'mock_obj': [main, Application],
        'mock_func': ['getenv', 'run_polling'],
        'mock_ret': ['123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11', True]
    },
    {
        'func': main.command_start, 
        'expected_res': None, 
        'arg': (main.Update(0, message=Message(0, from_user=possible_users[4], chat=Chat(0, type='GROUP'), date=datetime.now())), None),
        'mock_obj': [Message],
        'mock_func': ['reply_text'],
        'mock_ret': [True],
        'is_async': True
    },
    {
        'func': main.command_start, 
        'expected_res': None, 
        'arg': (main.Update(0, message=Message(0, from_user=possible_users[5], chat=Chat(0, type='GROUP'), date=datetime.now())), None),
        'mock_obj': [Message],
        'mock_func': ['reply_text'],
        'mock_ret': [True],
        'is_async': True
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


def test_init(mocker: MockerFixture) -> None:
    mocker.patch.object(main, '__name__', '__main__')
    mocker.patch.object(main, 'main', return_value=None)
    spy = mocker.spy(main, 'main')

    assert main.init() == None
    assert spy.spy_return == None
    

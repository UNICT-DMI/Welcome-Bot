# Welcome Bot
![CI Badge](https://github.com/QD-2022/Welcome-Bot/actions/workflows/ci.yml/badge.svg)

<p align="center">
    <img src="icon.jpeg" alt="logo" width="200">
</p>

A simple Telegram bot built with [python-telegram-bot](https://python-telegram-bot.org/).
It simply sends a randomized welcome message from a pre-defined message list each time a new user joins a specific group.

## How to use?
Just set a `QDBotToken` env variable, this is your bot token obtained from [BotFather](https://t.me/botfather)

### Example in bash
```bash
export QDBotToken="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" # Your bot token
```

## Write Unit Tests
In order to write Unit Tests, you have to put it inside `tests`.
There are many possibilities, for example it's possible to add a new user appending a `User` object in `possible_users`.
As generic Unit Tests it is possible to add a new test, appending it to `tests`.

### Unit Tests without mocking
To add a new unit test without mocking, there are some examples at the beginning of `tests`, but let's inspect how they're implemented:
- `func`: simply the function to mock
- `expected_res`: the expected returned value of the function to test
- `arg`: a tuple that contains the argument(s) of the function to test (the one previously defined in `func`). In case there are no passing arguments, just add an empty tuple object (`tuple()`)
- `is_async`: this is not a compulsory key, should be added and set to `True` only if the function is asynchronous

### Unit Tests with mocking
If is necessary one or more mock(s), it's possible to append three more keys to the unit test. The test should have the same keys with three more keys:
- `mock_obj`: it's a list of the objects in which there are the functions to mock. In our examples they often refer to the main object (the one imported from src.main)
- `mock_func`: an array of strings, it indicates the functions to mock
- `mock_ret`: a list of the returned values
# anna.money Job challenge

[Русский язык](README_RU.md)

## Task

Write service, that have HTTP method to get factorial. 
Result must be sent to user through WebSocket.

Programm language: Python. Libraries for candidate choice.


## Realization

Asynchronous server made with aiohttp + asyncio. To speedup factorial calculation used memoization,
where, for math calculations do not blocks server, recurse calls changed with explicit awaiting result from cache and initiating new coroutine for `n - 1`
without awaiting.

Require: Python 3.7 or higher.

### Protocol

C - client, S - server

```
General:
    C -> {event} -> S
    C <- {event acknowledge} <- S
    C <- {event result} <- S

Exmple:
    C -> "get_factorial 10" -> S
    C <- "{'event': 'acknowledge', 'meta': {'command': 'get_factorial 10', 'id': '5fb2...'}, 'payload': {}" <- S
    C <- "{'event': 'result', 'meta': {'command': 'get_factorial 10', 'id': '5fb2...'}, 'payload': {'result': 3628800}" <- S
```

### Commands
* `get_factorial N`
* `ping`


## Install and run
I reccomend to use `virtualenv` or `pyenv virtualenv` to create virtual environment. 
After: 

```
$ pip install git@github.com:PavelBass/annamoney-task.git
$ annamoney_task run
```

For run help use `$ annamoney_task run --help`


## Test and linters

To run tests and linters checks you need to run `tox` from the root of repository.
Note: you need to install `tox` first to your environment, for example with `pip install tox` 

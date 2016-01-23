# pytest-describe

This is a fork of [garybernhardt/expecter](https://github.com/garybernhardt/expecter) that hides the internal stack trace for `pytest`.

## Overview

This lets you write tests (using [ropez/pytest-describe](https://github.com/ropez/pytest-describe)) like this:

```python
from expecter import expect


def describe_foobar():

    def it_can_pass():
        expect(2 + 3) == 5

    def it_can_fail():
        expect(2 + 3) == 6
```

and instead of getting output like this:


```sh
=================================== FAILURES ===================================
_________________________ describe_foobar.it_can_fail __________________________

    def it_can_fail():
>       expect(2 + 3) == 6

test_expecter.py:14:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = expect(3), other = 4

    def __eq__(self, other):
        msg = 'Expected %s but got %s' % (repr(other), repr(self._actual))
        if (isinstance(other, basestring) and
                isinstance(self._actual, basestring)):
            msg += normalized_diff(other, self._actual)
        elif len(repr(self._actual)) > 74:
            msg += normalized_diff(pprint.pformat(other),
                                   pprint.pformat(self._actual))
>       assert self._actual == other, msg
E       AssertionError: Expected 6 but got 5

env/lib/python3.5/site-packages/expecter.py:57: AssertionError
====================== 1 failed, 1 passed in 2.67 seconds ======================
```

getting output like this:


```sh
=================================== FAILURES ===================================
_________________________ describe_foobar.it_can_fail __________________________

    def it_can_fail():
>       expect(2 + 3) == 6
E       AssertionError: Expected 6 but got 5

test_expecter.py:14: AssertionError
====================== 1 failed, 1 passed in 2.67 seconds ======================
```

## Installation

```sh
pip install pytest-expecter
```

## Versioning

This plugin's version number will follow `expecter`:

```
M.N.P.postF
```

where:

- `M.N.P` is the version of `expecter` included in the plugin
- `F` is incremented on each release of the plugin for that version

# Eldritch Estate

You are a real estate agent. Sell homes infested with eldritch creatures to your
unsuspecting customers. (Work in progress.)

## Running

NOTE: Eldritch Estate requires Python 3, version 3.4 or newer. It has not been
tested on older versions or on Python 2.

Eldritch Estate expects to run in a graphical environment, and may behave
strangely or fail to run when executed in a console.

### Linux
```
$ python3 setup.py install
$ eldestrl
```

### Windows
```
$ python3 setup.py install
$ eldestrl
```

## Controls
To move on the menu or once in-game, use the Vim keys, hjkl. ('h' is left, 'j'
is down, 'k' is up, and 'l' is right.) To move diagonally, use y, u, b, and n
(up-left, up-right, down-left and down-right respectively). To choose a menu
option, hit Enter. To return to the main menu, press Escape.

## Development
### Windows
Eldritch Estate is written to run on Python 3 (version 3.4 or above). Windows
support is a work in progress. It runs, but may require that you have a compiler
installed that is compatible with your version of Python. (If you've just
downloaded Python 3.5 from the Python Foundation website, that means Visual
C++ 2015. This is not installed automatically with Visual Studio 2015 Community
Edition; see [https://msdn.microsoft.com/en-us/library/60k1461a.aspx](this page)
for details.)

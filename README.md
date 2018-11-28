# 0wned

[![Build Status](https://travis-ci.org/mschwager/0wned.svg?branch=master)](https://travis-ci.org/mschwager/0wned)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/mschwager/0wned?branch=master&svg=true)](https://ci.appveyor.com/project/mschwager/0wned/branch/master)

Python packages allow for [arbitrary code execution](https://en.wikipedia.org/wiki/Arbitrary_code_execution)
at **run time** as well as **install time**. Code execution at **run time** makes
sense because, well, that's what code does. But executing code at **install time**
is a lesser known feature within the Python packaging ecosystem, and a
potentially much more dangerous one.

To test it out let's download this repository:

```
$ git clone https://github.com/mschwager/0wned.git
```

*Don't worry, there's nothing malicious going on, you can [take a look at what's happening yourself](https://github.com/mschwager/0wned/blob/master/setup.py).*

Now let's install the package:

```
$ sudo python -m pip install 0wned/
$ cat /0wned
Created '/0wned' with user 'root' at 1536011622
```

**During `pip` installation `0wned` was able to successfully write to the root
directory! This means that `0wned` can do anything as the root or administrative
user.**

We can reduce the impact of this issue by installing packages with the `--user` flag:

```
$ python -m pip install --user 0wned/
$ cat ~/0wned
Created '/home/tempuser/0wned' with user 'tempuser' at 1536011624
```

# Prevention

You should always be wary of Python packages you're installing on your system,
especially when using root/administrative privileges. There are a few ways to help
mitigate these types of attacks:

* Install only [binary distribution Python wheels](https://pythonwheels.com/) using the `--only-binary :all:` flag. This avoids arbitrary code execution on installation (avoids `setup.py`).
* As mentioned above, install packages [with the local user](https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site) using the `--user` flag.
* Install packages in [hash-checking mode](https://pip.pypa.io/en/stable/reference/pip_install/#hash-checking-mode) using the `--require-hashes` flag. This will protect against remote tampering and ensure you're getting the package you intend to.
* Double check that you've spelled the package name correctly. There may be malicious packages [typosquatting](https://en.wikipedia.org/wiki/Typosquatting) under a similar name.

# Details of the Attack

You can hook almost any `pip` command by extending the correct `setuptools` module.

For example, `0wned` takes advantage of the `install` class to do its thing:

```python
from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        # Insert code here
        install.run(self)

setup(
    ...
    cmdclass={
        'install': PostInstallCommand,
    },
    ...
)
```

And when `pip install` is run our custom `PostInstallCommand` class will be invoked.

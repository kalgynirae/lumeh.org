---
title: You’re Running It Wrong — why your Python imports aren’t working like you expect
author: Colin
# Comments go here in the following format:
#
#  comments:
#    - author: Colin
#      content: >
#        Blah blah blah blah blah
#        blah blah blah.
#    - author: John Smith
#      content: >
#        Blah blah blah.
#
# Please add new comments at the bottom of the list. Good luck!
comments: []
---

You thought you understood how to import things, but then you ran into a problem
where nothing seemed to work like you thought it did.  What happened?  Let's
find out!

If you're in a hurry, skip to the bottom for a **tl;dr**.

## An Example

Consider the following example project:

{% highlight shell %}
$ tree
.
├── demonstrator/
│   ├── __init__.py
│   ├── core.py
│   ├── demo.py
│   ├── demo_relative.py
│   ├── demo_zany.py
│   └── plugins/
│       ├── __init__.py
│       └── color.py
├── README
└── setup.py

2 directories, 9 files
{% endhighlight %}

This project consists of a single package (`demonstrator`) which contains
several modules (`core`, `demo`, `demo_relative`, and `demo_zany`) and a
subpackage (`plugins`) which contains a single module (`color`).  Remember that
the `__init__.py` files are what define these directories as packages in the
first place.

The `demonstrator` package is primarily intended to be imported and used as a
library. But it also contains a few scripts that are designed to be directly
executed (the `demo*` files).

Let's look at the contents of `demo.py`:

{% highlight python %}
from demonstrator import core
from demonstrator.plugins import color

print('The imports worked!')
{% endhighlight %}

And the contents of `demo_relative.py`:

{% highlight python %}
from . import core
from .plugins import color

print('The imports worked!')
{% endhighlight %}

And the contents of `demo_zany.py`:

{% highlight python %}
import core
from plugins import color

print('The imports worked!')
{% endhighlight %}

`demo.py` uses absolute imports, `demo_relative.py` uses relative imports, and
`demo_zany.py` uses absolute imports but assumes that its sibling
modules/packages are at the top level.

Which import styles do you think will work?  Make your guesses now!

## The Right Way

{% highlight shell %}
$ python3 -m demonstrator.demo
The imports worked!
{% endhighlight %}

{% highlight shell %}
$ python3 -m demonstrator.demo_relative
The imports worked!
{% endhighlight %}

{% highlight shell %}
$ python3 -m demonstrator.demo_zany
Traceback (most recent call last):
  File "/usr/lib/python3.5/runpy.py", line 184, in _run_module_as_main
    "__main__", mod_spec)
  File "/usr/lib/python3.5/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/tmp/happy.Qcd/demonstrator/demo_zany.py", line 1, in <module>
    import core
ImportError: No module named 'core'
{% endhighlight %}

Did you guess correctly?  Good.  So did I!

## The Wrong Way

It turns out that many people try to execute the scripts like this:

{% highlight shell %}
$ python3 demonstrator/demo.py
Traceback (most recent call last):
  File "demonstrator/demo.py", line 1, in <module>
    from demonstrator import core
ImportError: No module named 'demonstrator'
{% endhighlight %}

{% highlight shell %}
$ python3 demonstrator/demo_relative.py
Traceback (most recent call last):
  File "demonstrator/demo_relative.py", line 1, in <module>
    from . import core
SystemError: Parent module '' not loaded, cannot perform relative import
{% endhighlight %}

{% highlight shell %}
$ python3 demonstrator/demo_zany.py 
The imports worked!
{% endhighlight %}

Well, look at that; the results are exactly the opposite of what we saw when we
used the `-m` option.

`demo.py` doesn't work when executed this way because the directory that
contains `demonstrator` is not listed in `sys.path`.  This could be fixed using
some manual tweaking of `sys.path`, but it's easier to just execute using the
`-m` option, which solves the problem.

`demo_relative.py` doesn't work when executed this way because files executed by
filename aren't considered part of any package.  This *can't* be fixed except by
using the `-m` option.

`demo_zany.py` works when executed this way because the *directory containing
`demo_zany.py`* gets added to `sys.path`, which means `core` and `plugins` are
both accessible as top-level modules/packages.  This is undesirable because
one of our modules might accidentally shadow one of the standard library
modules/packages if we weren't careful with our modules' names.

## tl;dr

Always execute your scripts using the `python -m package.module` form.  This
will ensure that both absolute and relative imports work as expected.

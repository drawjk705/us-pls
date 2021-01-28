"""
This type stub file was generated by pyright.
"""

"""The :mod:`aliases` module contains a set of matcher *aliases*
that are commonly used when composing matchers and are not meant
to be imported every time.

To use the aliases just import them::

    from expects import *
    from expects.aliases import *

    expect([1, 2]).to(contain_exactly(an(int), 2))

The same code without using the ``an`` alias for the ``be_an`` matcher::

    from expects import *

    expect([1, 2]).to(contain_exactly(be_an(int), 2))

Reference
---------

"""
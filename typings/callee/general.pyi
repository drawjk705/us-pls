"""
This type stub file was generated by pyright.
"""

from callee.base import BaseMatcher

"""
General matchers.

These don't belong to any broader category, and include matchers for common
Python objects, like functions or classes.
"""
class Any(BaseMatcher):
    """Matches any object."""
    def match(self, value):
        ...
    
    def __repr__(self):
        ...
    


class Matching(BaseMatcher):
    """Matches an object that satisfies given predicate."""
    MAX_DESC_LENGTH = ...
    def __init__(self, predicate, desc=...) -> None:
        """
        :param predicate: Callable taking a single argument
                          and returning True or False
        :param desc: Optional description of the predicate.
                     This will be displayed as a part of the error message
                     on failed assertion.
        """
        ...
    
    def match(self, value):
        ...
    
    def __repr__(self):
        """Return a representation of the matcher."""
        ...
    


ArgThat = Matching
class Captor(BaseMatcher):
    """Argument captor.

    You can use :class:`Captor` to "capture" the original argument
    that the mock was called with, and perform custom assertions on it.

    Example::

        captor = Captor()
        mock_foo.assert_called_with(captor)

        # captured value is available as the `arg` attribute
        self.assertEquals(captor.arg.some_method(), 42)
        self.assertEquals(captor.arg.some_other_method(), "foo")

    .. versionadded:: 0.2
    """
    __slots__ = ...
    def __init__(self, matcher=...) -> None:
        """
        :param matcher: Optional matcher to validate the argument against
                        before it's captured
        """
        ...
    
    def has_value(self):
        """Returns whether the :class:`Captor` has captured a value."""
        ...
    
    @property
    def arg(self):
        """The captured argument value."""
        ...
    
    def match(self, value):
        ...
    
    def __repr__(self):
        """Return a representation of the captor."""
        ...
    



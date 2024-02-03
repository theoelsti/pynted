"""
Vinted python library
~~~~~~~~~~~~~~~~~~~~~

Pynted is an vinted library, written in Python.
Basic usage:

   >>> import pynted
   >>> vinted = pynted.Pynted()
   >>> vinted.get_user_by_username("foo")
    <VintedUser foo>


Differents exceptions are raised when an error occured.
You can catch them like this:

   >>> import pynted
   >>> vinted = pynted.Pynted()
   >>> try:
   ...     vinted.get_user_by_username("bar")
   ... except pynted.exceptions.vinted.UserNotFound as e:
   ...     logger.error("User %s not found", e.username)
   User bar not found

"""

__all__ = []

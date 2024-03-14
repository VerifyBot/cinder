"""
A thread-safe sqlite3 wrapper
"""

import sqlite3
import threading


# the goal is to have the same experience as sqlite3, but with thread safety

class SafeConnection(sqlite3.Connection):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, check_same_thread=False, **kwargs)

    # do auto commit
    self.isolation_level = None

    self._lock = threading.Lock()

  def execute(self, *args, **kwargs):
    """Safely execute an SQL query """
    with self._lock:
      return super().execute(*args, **kwargs)

  def executemany(self, *args, **kwargs):
    """Safely execute many SQL queries """
    with self._lock:
      return super().executemany(*args, **kwargs)

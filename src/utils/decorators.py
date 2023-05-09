import time as t
from time import time as curr_time
from typing import Any


def make_delayed_decorator(delay):
  def delayed(func):
    def wrapper(*args, **kwargs):
      t.sleep(delay)

      return func(*args, **kwargs)

    return wrapper

  return delayed


def make_logging_decorator(logger):
  def logging(message):
    def decorator(func):
      def wrapper(*args, **kwargs):
        logger(f'{message}')

        fn_result, exec_time = with_time_estimate(func, *args, **kwargs)

        logger(f'[exec time — {exec_time} secs]')

        return fn_result

      return wrapper

    return decorator

  return logging


def with_time_estimate(func, *args, **kwargs) -> [Any, float]:
  start_time = curr_time()
  fn_result = func(*args, **kwargs)
  end_time = curr_time()

  time_elapsed = end_time - start_time

  return [fn_result, round(time_elapsed, 5)]

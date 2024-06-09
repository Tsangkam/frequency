import time
import threading


class Limiter:
    """A decorator that limits the number of calls to a function within a given period.
    
    Args:
        calls (int): The maximum number of calls within the period.
        period (float): The period in seconds.
        
    Example:
        @Limiter(calls=10, period=10)
        def my_func():
            pass
    """
    def __init__(self, calls=10, period=10):
        self.calls = calls
        self.period = period
        self.calls_record = []
        self.lock = threading.Lock()
        
    def is_full(self):
        return len(self.calls_record) >= self.calls
    
    def get_interval(self):
        if not self.is_full():
            return 0
        
        first_call_time = self.calls_record[0]
        now = time.perf_counter()
        interval = self.period - (now - first_call_time)
        return 0 if interval < 0 else interval
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(self.calls_record)
            with self.lock:
                interval = self.get_interval()
                if interval > 0:
                    time.sleep(self.get_interval())
                if self.is_full():
                    self.calls_record.pop(0)
                self.calls_record.append(time.perf_counter())
            return func(*args, **kwargs)
        return wrapper

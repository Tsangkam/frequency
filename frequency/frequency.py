import time


class frequency_limit:
    def __init__(self, calls=10, period=10):
        self.calls = calls
        self.period = period
        self.calls_record = []
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            
            if len(self.calls_record) >= self.calls:
                first_call_time = self.calls_record.pop(0)
                now = time.time()
                interval = self.period - (now - first_call_time)
                if interval > 0:
                    time.sleep(interval)
            
            self.calls_record.append(time.time())
            return func(*args, **kwargs)
        return wrapper

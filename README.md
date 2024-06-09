# Frequency Limit
Frequency Limit provides a simple way to limit the frequency of a function call.

## Highlights
- Simple and easy-to-use API
- Supports threading and async

## Install

### from wheel
```
pip install frequency-0.1.0-py3-none-any.whl
```

## Usage

#### Limiter Decorator
The `Limiter` decorator limits the frequency of a function call.

```python
from frequency import Limiter

@Limiter(calls=10, period=60)  # limit to 10 calls per minute
def my_function():
    # your code here
```
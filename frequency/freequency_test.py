import time
import unittest
import frequency
import asyncio
import random


class TestFrequency(unittest.TestCase):
    
    def test_limiter(self):
        times = 100             # 执行次数
        duartion_avg = 1        # 平均耗时
        floating = 0.4          # 允许浮动范围
        allowed_error = 0.1     # 允许误差范围
        calls = 5               # 限制调用次数
        period = 5              # 限制时间段
        
        ceil = duartion_avg * (1+floating)
        floor = duartion_avg * (1-floating)
        total_duration = max(times * duartion_avg, times/calls * period)
        delta = total_duration * allowed_error
        
        now = time.perf_counter()
        for _ in range(times):
            foo(floor, ceil)
        end = time.perf_counter()
        self.assertAlmostEqual((end - now), total_duration, delta=delta)
        
    def test_limiter_async(self):
        times = 100             # 执行次数
        duartion_avg = 1        # 平均耗时
        floating = 0.4          # 允许浮动范围
        allowed_error = 0.1     # 允许误差范围
        calls = 5               # 限制调用次数
        period = 5              # 限制时间段
        
        ceil = duartion_avg * (1+floating)
        floor = duartion_avg * (1-floating)
        total_duration = max((times/calls - 1) * period + duartion_avg, times * duartion_avg)
        delta = total_duration * allowed_error
        
        now = time.perf_counter()
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(async_foo(floor, ceil)) for _ in range(times)]
        loop.run_until_complete(asyncio.wait(tasks))
        end = time.perf_counter()
        self.assertAlmostEqual((end - now), total_duration, delta=delta)
        
        
@frequency.Limiter(calls=5, period=5)   
def foo(floor, ceil):
    duration = random.uniform(floor, ceil)
    time.sleep(duration)


@frequency.Limiter(calls=5, period=5)   
async def async_foo(floor, ceil):
    duration = random.uniform(floor, ceil)
    await asyncio.sleep(duration)
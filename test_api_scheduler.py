import unittest
from datetime import datetime, time, timedelta
import api_scheduler  # import your main scheduler.py file

class TestSchedulerFunctions(unittest.TestCase):

    # Test parse_timestamps
    def test_parse_timestamps_valid(self):
        timestamps = ["12:34:56", "01:02:03"]
        result = api_scheduler.parse_timestamps(timestamps, suppress_print=True)
        self.assertEqual(result, [time(12, 34, 56), time(1, 2, 3)])

    def test_parse_timestamps_invalid(self):
        timestamps = ["12:34:56", "invalid", "25:61:00"]
        result = api_scheduler.parse_timestamps(timestamps, suppress_print=True)
        # Only valid times remain
        self.assertEqual(result, [time(12, 34, 56)])

    # Test group_by_time
    def test_group_by_time(self):
        times = [time(12, 0, 0), time(12, 0, 0), time(13, 0, 0)]
        grouped = api_scheduler.group_by_time(times)
        self.assertEqual(len(grouped), 2)
        self.assertEqual(len(grouped[time(12,0,0)]), 2)
        self.assertEqual(len(grouped[time(13,0,0)]), 1)

    # Test wait_until function (just check calculation)
    def test_wait_until_future_seconds(self):
        now = datetime.now()
        future_time = (now + timedelta(seconds=2)).time()
        start = datetime.now()
        api_scheduler.wait_until(future_time)  # Will actually wait ~2 seconds
        end = datetime.now()
        diff = (end - start).total_seconds()
        self.assertTrue(diff >= 1)

if __name__ == "__main__":
    unittest.main()


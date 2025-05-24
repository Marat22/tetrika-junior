import unittest

try:
    from solution import appearance
    from solution import calculate_intersection
    from solution import get_sessions
    from solution import merge_sessions
except ModuleNotFoundError:
    from task3.solution import appearance
    from task3.solution import calculate_intersection
    from task3.solution import get_sessions
    from task3.solution import merge_sessions


class TestGetSessions(unittest.TestCase):
    def test_normal_order(self):
        intervals = [10, 12, 15, 17, 20, 21]
        self.assertListEqual(get_sessions(intervals), [[10, 12], [15, 17], [20, 21]])

    def test_reversed_order(self):
        intervals = [30, 42, 25, 27, 10, 12]
        self.assertListEqual(get_sessions(intervals), [[10, 12], [25, 27], [30, 42]])

    def test_overlapped_sessions(self):
        intervals = [30, 35, 27, 32, 31, 35]
        self.assertListEqual(get_sessions(intervals), [[27, 32], [30, 35], [31, 35]])
    
    def test_repetitions(self):
        intervals = [27, 30, 27, 28]
        self.assertListEqual(get_sessions(intervals), [[27, 28], [27, 30]])

    def test_empty(self):
        intervals = []
        self.assertListEqual(get_sessions(intervals), [])

class TestMergeSessions(unittest.TestCase):
    def test_no_overlap(self):
        sessions = [[10, 20], [25, 30]]
        self.assertListEqual(merge_sessions(sessions), sessions)
    
    def test_overlap(self):
        sessions = [[10, 20], [15, 22]]
        self.assertListEqual(merge_sessions(sessions), [[10, 22]])

    def test_empty(self):
        sessions = []
        self.assertListEqual(merge_sessions(sessions), [])


class TestIntersections(unittest.TestCase):
    def test_empty_pupil(self):
        pupil_sessions = []
        tutor_sessions = [[10, 20], [25, 30]]
        lesson = [10, 30]
        self.assertEqual(calculate_intersection(pupil_sessions, tutor_sessions, lesson), 0)

    def test_empty_tutor(self):
        pupil_sessions = [[10, 20], [25, 30]]
        tutor_sessions = []
        lesson = [10, 30]
        self.assertEqual(calculate_intersection(pupil_sessions, tutor_sessions, lesson), 0)

    def test_empty_pupil(self):
        pupil_sessions = []
        tutor_sessions = [[10, 20], [25, 30]]
        lesson = [10, 30]
        self.assertEqual(calculate_intersection(pupil_sessions, tutor_sessions, lesson), 0)

class TestAppearance(unittest.TestCase):
    def test_default_case(self):
        """Test the example cases provided in the task."""
        res = appearance(
            {
                'lesson': [1594663200, 1594666800],
                'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
            }
        )
        self.assertEqual(res, 3117)

    def test_connected_before_lesson(self):
        res = appearance(
            {
                'lesson': [1594702800, 1594706400],
                'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]
            }
        )
        self.assertEqual(res, 3577)

    def test_disconnected_after_lesson(self):
        res = appearance(
            {
                'lesson': [1594692000, 1594695600],
                'pupil': [1594692033, 1594696347],
                'tutor': [1594692017, 1594692066, 1594692068, 1594696341]
            }
        )
        self.assertEqual(res, 3565)


if __name__ == '__main__':
    unittest.main()

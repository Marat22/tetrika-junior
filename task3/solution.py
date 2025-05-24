def get_sessions(timestamps: list[int]) -> list[list[int]]:
    sessions = []
    for i in range(0, len(timestamps), 2):
        sessions.append([timestamps[i], timestamps[i + 1]])
    sessions.sort()
    return sessions


def merge_sessions(sessions: list[list[int]]) -> list[list[int]]:
    if not sessions:
        return []

    merged = [sessions[0]]
    for current in sessions[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)
    return merged


def calculate_intersection(pupil_sessions: list[list[int]], tutor_sessions: list[list[int]], lesson: list[int]) -> int:
    total_intersection = 0
    i, j = 0, 0
    lesson_start, lesson_end = lesson

    while i < len(pupil_sessions) and j < len(tutor_sessions):
        pupil_start, pupil_end = pupil_sessions[i]
        tutor_start, tutor_end = tutor_sessions[j]

        start = max(pupil_start, tutor_start, lesson_start)
        end = min(pupil_end, tutor_end, lesson_end)

        if start < end:
            total_intersection += end - start

        if pupil_end < tutor_end:
            i += 1
        else:
            j += 1

    return total_intersection


def appearance(intervals: dict[str, list[int]]) -> int:
    pupil_sessions = get_sessions(intervals['pupil'])
    tutor_sessions = get_sessions(intervals['tutor'])

    pupil_sessions = merge_sessions(pupil_sessions)
    tutor_sessions = merge_sessions(tutor_sessions)

    return calculate_intersection(pupil_sessions, tutor_sessions, intervals['lesson'])

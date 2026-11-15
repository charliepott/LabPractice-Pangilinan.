import time
from company.branches import BRANCHES, get_branch

TIME_FORMAT = "%A, %d %B %Y %I:%M:%S %p"


def get_local_time(offset):
    """Get current time at a UTC offset."""
    return time.gmtime(time.time() + offset * 3600)


def format_time(t):
    """Format time into readable text."""
    return time.strftime(TIME_FORMAT, t)


def get_branch_time(code):
    """Get current formatted time at a branch."""
    branch = get_branch(code)

    if branch is None:
        return None

    return format_time(get_local_time(branch["offset"]))


def hour_difference(from_code, to_code):
    """Calculate how many hours the destination is ahead."""
    from_branch = get_branch(from_code)
    to_branch = get_branch(to_code)

    if from_branch is None or to_branch is None:
        return None

    return to_branch["offset"] - from_branch["offset"]


def convert_time(hour, minute, from_code, to_code):
    """Convert time between two branches."""
    difference = hour_difference(from_code, to_code)

    if difference is None:
        return None

    total = hour * 60 + minute + difference * 60
    day_change = total // 1440
    total = total % 1440

    new_hour = total // 60
    new_minute = total % 60

    return (int(new_hour), int(new_minute), int(day_change))


def describe_day_change(day_change):
    """Describe whether the date changes."""
    if day_change > 0:
        return "(next day)"
    elif day_change < 0:
        return "(previous day)"
    else:
        return "(same day)"
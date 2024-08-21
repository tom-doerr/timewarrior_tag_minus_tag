#!/usr/bin/env python3

import subprocess
import sys

def get_tag_time(tag):
    """Get the total time for a given tag using Timewarrior."""
    try:
        result = subprocess.run(['timew', 'summary', tag], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Total' in line:
                time_parts = line.split()
                if len(time_parts) >= 2:
                    return time_parts[-1]
        print(f"No time data found for tag '{tag}'")
        return None
    except subprocess.CalledProcessError:
        print(f"Error: Unable to get time for tag '{tag}'")
        return None

def time_to_seconds(time_str):
    """Convert time string (HH:MM:SS) to seconds."""
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def seconds_to_time(seconds):
    """Convert seconds to time string (HH:MM:SS)."""
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def main():
    if len(sys.argv) != 3:
        print("Usage: python tag_time_diff.py <tag1> <tag2>")
        sys.exit(1)

    tag1, tag2 = sys.argv[1], sys.argv[2]
    
    time1 = get_tag_time(tag1)
    time2 = get_tag_time(tag2)
    
    if time1 is None or time2 is None:
        print("Unable to calculate time difference due to missing data.")
        sys.exit(1)
    
    diff_seconds = time_to_seconds(time1) - time_to_seconds(time2)
    diff_time = seconds_to_time(abs(diff_seconds))
    
    print(f"Time for {tag1}: {time1}")
    print(f"Time for {tag2}: {time2}")
    print(f"Difference ({tag1} - {tag2}): {'-' if diff_seconds < 0 else ''}{diff_time}")

if __name__ == "__main__":
    main()

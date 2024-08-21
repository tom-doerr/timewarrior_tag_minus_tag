#!/usr/bin/env python3

import subprocess
import sys

def get_tag_time(tag):
    """Get the total time for a given tag using Timewarrior."""
    try:
        result = subprocess.run(['timew', 'summary', tag], capture_output=True, text=True, check=True)
        print(f"Raw output for tag '{tag}':")
        print(result.stdout)
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Tracked' in line:
                time_parts = line.split()
                if len(time_parts) >= 2:
                    # Extract only the time part (HH:MM:SS)
                    time_str = time_parts[1]
                    if ':' in time_str:
                        return time_str
        print(f"No valid time data found for tag '{tag}'")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to get time for tag '{tag}'")
        print(f"Error message: {e}")
        return None

def time_to_seconds(time_str):
    """Convert time string (HH:MM:SS) to seconds."""
    try:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except ValueError:
        print(f"Error: Invalid time format '{time_str}'. Expected HH:MM:SS.")
        return None

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
    
    seconds1 = time_to_seconds(time1)
    seconds2 = time_to_seconds(time2)
    
    if seconds1 is None or seconds2 is None:
        print("Unable to calculate time difference due to invalid time data.")
        sys.exit(1)
    
    diff_seconds = seconds1 - seconds2
    diff_time = seconds_to_time(abs(diff_seconds))
    
    print(f"Time for {tag1}: {time1}")
    print(f"Time for {tag2}: {time2}")
    print(f"Difference ({tag1} - {tag2}): {'-' if diff_seconds < 0 else ''}{diff_time}")

if __name__ == "__main__":
    main()

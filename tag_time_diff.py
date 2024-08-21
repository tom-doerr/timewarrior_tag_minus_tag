#!/usr/bin/env python3

import subprocess
import sys

def get_tag_time(tag):
    """Get the total time for a given tag using Timewarrior."""
    try:
        result = subprocess.run(['timew', 'summary', tag], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        total_time = None
        for line in lines:
            if line.strip().startswith('Total'):
                total_time = line.strip().split()[-1]
                break
        
        if total_time:
            return total_time
        else:
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
    
    diff_seconds = abs(seconds1 - seconds2)
    diff_time = seconds_to_time(diff_seconds)
    
    print(f"Time for {tag1}: {time1}")
    print(f"Time for {tag2}: {time2}")
    print(f"Absolute difference between {tag1} and {tag2}: {diff_time}")

if __name__ == "__main__":
    main()

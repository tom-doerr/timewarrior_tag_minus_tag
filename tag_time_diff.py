#!/usr/bin/env python3

import subprocess
import sys
import argparse

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
            return '00:00:00'
    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to get time for tag '{tag}'")
        print(f"Error message: {e}")
        return '00:00:00'

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

def get_total_time():
    """Get the total tracked time for all tags."""
    try:
        result = subprocess.run(['timew', 'summary'], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        total_time = None
        for line in lines:
            if line.strip().startswith('Total'):
                total_time = line.strip().split()[-1]
                break
        
        return total_time if total_time else '00:00:00'
    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to get total time")
        print(f"Error message: {e}")
        return '00:00:00'

def main():
    parser = argparse.ArgumentParser(description="Compare time tracked for two tags or show total tracked time.")
    parser.add_argument('tags', nargs='*', help="Two tags to compare")
    parser.add_argument('-t', '--total', action='store_true', help="Show total tracked time for all tags")
    args = parser.parse_args()

    if args.total:
        total_time = get_total_time()
        print(f"Total tracked time for all tags: {total_time}")
    elif len(args.tags) == 2:
        tag1, tag2 = args.tags
        
        time1 = get_tag_time(tag1)
        time2 = get_tag_time(tag2)
        
        seconds1 = time_to_seconds(time1)
        seconds2 = time_to_seconds(time2)
        
        diff_seconds = abs(seconds1 - seconds2)
        diff_time = seconds_to_time(diff_seconds)
        
        if time1 == '00:00:00' and time2 == '00:00:00':
            print(f"Both tags '{tag1}' and '{tag2}' have no tracked time.")
        else:
            print(f"Time for {tag1}: {time1}")
            if time1 == '00:00:00':
                print(f"No time tracked for tag '{tag1}'")
            
            print(f"Time for {tag2}: {time2}")
            if time2 == '00:00:00':
                print(f"No time tracked for tag '{tag2}'")
            
            print(f"Absolute difference between {tag1} and {tag2}: {diff_time}")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

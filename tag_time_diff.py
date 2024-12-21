#!/usr/bin/env python3

import subprocess
import sys
import argparse
import time

def validate_tag(tag):
    """Validate tag name."""
    if not tag or not isinstance(tag, str):
        raise ValueError("Tag must be a non-empty string")
    if len(tag.strip()) == 0:
        raise ValueError("Tag cannot be only whitespace")
    return tag.strip()

def parse_timewarrior_datetime(dt_str):
    """Convert Timewarrior datetime to seconds since epoch."""
    import datetime
    import time
    # Format: YYYYMMDDTHHMMSSZ
    dt = datetime.datetime.strptime(dt_str, "%Y%m%dT%H%M%SZ")
    return time.mktime(dt.timetuple())

def get_tag_time(tag):
    """Get the total time for a given tag using Timewarrior export."""
    try:
        tag = validate_tag(tag)
        # Check if timewarrior is installed
        try:
            subprocess.run(['timew'], capture_output=True, text=True, timeout=1)
        except FileNotFoundError:
            print("Error: Timewarrior (timew) is not installed")
            print("Install it with: sudo apt install timewarrior")
            sys.exit(1)
        except subprocess.CalledProcessError:
            # This is fine, it just means no active tracking
            pass

        # Get all intervals for today and yesterday to ensure we catch everything
        result = subprocess.run(['timew', 'export', 'today - tomorrow'], 
                              capture_output=True, 
                              text=True, 
                              check=True,
                              timeout=5)

        import json
        intervals = json.loads(result.stdout)
        
        total_seconds = 0
        current_time = time.time()

        for interval in intervals:
            # Check if the interval has our tag
            if tag in interval.get('tags', []):
                start_time = parse_timewarrior_datetime(interval['start'])
                
                # Handle ongoing intervals
                if 'end' in interval:
                    end_time = parse_timewarrior_datetime(interval['end'])
                else:
                    end_time = current_time
                    
                total_seconds += end_time - start_time
        
        if total_seconds == 0:
            return '00:00:00'
            
        # Convert total seconds back to HH:MM:SS
        h, r = divmod(total_seconds, 3600)
        m, s = divmod(r, 60)
        total_time = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
        
        return total_time if total_time else '00:00:00'
    except subprocess.TimeoutExpired:
        print(f"Error: Command timed out while getting time for tag '{tag}'")
        return '00:00:00'
    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to get time for tag '{tag}'")
        print(f"Error message: {e}")
        return '00:00:00'
    except Exception as e:
        print(f"Unexpected error while processing tag '{tag}': {e}")
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
    """Get the total tracked time for all tags using export."""
    try:
        result = subprocess.run(['timew', 'export', 'yesterday - tomorrow'], 
                              capture_output=True, 
                              text=True, 
                              check=True,
                              timeout=5)

        import json
        intervals = json.loads(result.stdout)
        
        total_seconds = 0
        current_time = time.time()

        for interval in intervals:
            start_time = parse_timewarrior_datetime(interval['start'])
            
            # Handle ongoing intervals
            if 'end' in interval:
                end_time = parse_timewarrior_datetime(interval['end'])
            else:
                end_time = current_time
                
            total_seconds += end_time - start_time
    except subprocess.TimeoutExpired:
        print("Error: Command timed out while getting total time")
        return '00:00:00'
    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to get total time")
        print(f"Error message: {e}")
        return '00:00:00'
    except Exception as e:
        print(f"Unexpected error while getting total time: {e}")
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
        
        print(f"Time for {tag1}: {time1}")
        print(f"Time for {tag2}: {time2}")
        print(f"Absolute difference between {tag1} and {tag2}: {diff_time}")
        
        if time1 == '00:00:00' and time2 == '00:00:00':
            print(f"Note: Both tags '{tag1}' and '{tag2}' have no tracked time.")
            print("To start tracking time, use: timew start <tag>")
        elif time1 == '00:00:00':
            print(f"Note: No time tracked for tag '{tag1}'")
            print(f"To start tracking time for {tag1}, use: timew start {tag1}")
        elif time2 == '00:00:00':
            print(f"Note: No time tracked for tag '{tag2}'")
            print(f"To start tracking time for {tag2}, use: timew start {tag2}")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

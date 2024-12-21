#!/usr/bin/env python3

import subprocess
import sys
import argparse

def validate_tag(tag):
    """Validate tag name."""
    if not tag or not isinstance(tag, str):
        raise ValueError("Tag must be a non-empty string")
    if len(tag.strip()) == 0:
        raise ValueError("Tag cannot be only whitespace")
    return tag.strip()

def get_tag_time(tag):
    """Get the total time for a given tag using Timewarrior."""
    try:
        tag = validate_tag(tag)
        # Check if timewarrior is installed
        try:
            subprocess.run(['timew'], capture_output=True, check=True, timeout=1)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: Timewarrior (timew) is not installed or not accessible")
            sys.exit(1)
        
        result = subprocess.run(['timew', 'summary', tag], 
                              capture_output=True, 
                              text=True, 
                              check=True,
                              timeout=5)  # 5 second timeout
        
        lines = result.stdout.split('\n')
        total_time = None
        for line in lines:
            if line.strip().startswith('Total'):
                parts = line.strip().split()
                if len(parts) >= 2:
                    total_time = parts[-1]
                    # Ensure time format is HH:MM:SS
                    if ':' not in total_time:
                        return '00:00:00'
                    # Pad hours if needed
                    if total_time.count(':') == 2:
                        h, m, s = total_time.split(':')
                        total_time = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
                break
        
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
    """Get the total tracked time for all tags."""
    try:
        # Check if timewarrior is installed
        try:
            subprocess.run(['timew'], capture_output=True, check=True, timeout=1)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: Timewarrior (timew) is not installed or not accessible")
            sys.exit(1)
            
        result = subprocess.run(['timew', 'summary'], 
                              capture_output=True, 
                              text=True, 
                              check=True,
                              timeout=5)  # 5 second timeout
        
        lines = result.stdout.split('\n')
        total_time = None
        for line in lines:
            if line.strip().startswith('Total'):
                parts = line.strip().split()
                if len(parts) >= 2:
                    total_time = parts[-1]
                    # Ensure time format is HH:MM:SS
                    if ':' not in total_time:
                        return '00:00:00'
                    # Pad hours if needed
                    if total_time.count(':') == 2:
                        h, m, s = total_time.split(':')
                        total_time = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
                break
        
        return total_time if total_time else '00:00:00'
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
        elif time1 == '00:00:00':
            print(f"Note: No time tracked for tag '{tag1}'")
        elif time2 == '00:00:00':
            print(f"Note: No time tracked for tag '{tag2}'")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

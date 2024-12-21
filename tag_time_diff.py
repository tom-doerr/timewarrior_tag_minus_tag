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
            result = subprocess.run(['timew'], capture_output=True, text=True, timeout=1)
            if "There is no active time tracking." in result.stdout:
                # This is fine, we can continue
                pass
        except FileNotFoundError:
            print("Error: Timewarrior (timew) is not installed")
            print("Install it with: sudo apt install timewarrior")
            sys.exit(1)
        except subprocess.CalledProcessError:
            print("Error: Problem accessing Timewarrior")
            sys.exit(1)
        
        result = subprocess.run(['timew', 'summary', tag], 
                              capture_output=True, 
                              text=True, 
                              check=True,
                              timeout=5)  # 5 second timeout
        
        # Get the total from timewarrior's summary
        total_seconds = 0
        
        # First try to get the total directly from the summary footer
        lines = result.stdout.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('Wk') and not '[4m' in line:
                parts = line.strip().split()
                if len(parts) >= 1 and ':' in parts[-1]:  # Look for the last time value
                    try:
                        h, m, s = map(int, parts[-1].split(':'))
                        total_seconds = h * 3600 + m * 60 + s
                        break
                    except (ValueError, IndexError):
                        continue
        
        # If no total was found, calculate from individual entries
        if total_seconds == 0:
            for line in lines:
                if not line.strip() or '[4m' in line or line.startswith('Wk'):
                    continue
                    
                parts = line.strip().split()
                if len(parts) >= 7:  # Line contains a time entry
                    time_str = parts[-2]
                    if time_str == '-':  # Ongoing tracking
                        now = subprocess.run(['timew', 'get', 'dom.active.duration'], 
                                          capture_output=True, text=True, check=True).stdout.strip()
                        if ':' in now:
                            h, m, s = map(int, now.split(':'))
                            total_seconds = h * 3600 + m * 60 + s
                    elif ':' in time_str:
                        h, m, s = map(int, time_str.split(':'))
                        total_seconds += h * 3600 + m * 60 + s
        
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

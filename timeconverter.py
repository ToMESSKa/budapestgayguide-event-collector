from dateutil import parser
from datetime import datetime, timedelta
import pytz

# Budapest timezone
budapest_tz = pytz.timezone('Europe/Budapest')

# Helper function to parse relative dates like "This Monday" or "This Friday"
def get_day_of_week(target_day, input_time):
    today = datetime.now(budapest_tz)
    current_weekday = today.weekday()  # Monday is 0, Sunday is 6
    days_ahead = target_day - current_weekday

    target_date = today + timedelta(days=days_ahead)

    # Combine target day with the specified time (hour, minute)
    full_date = datetime.combine(target_date.date(), input_time)

    # Make the full_date timezone-aware by localizing it to Budapest
    full_date = budapest_tz.localize(full_date)

    return full_date

# Function to handle "TODAY", "HAPPENING NOW", and relative dates like "This Monday at 1 PM"
def parse_relative_date(date_str):
    today = datetime.now(budapest_tz)

    if "TODAY" in date_str.upper() or "HAPPENING NOW" in date_str.upper():
        return today.strftime("%Y-%m-%d %H:%M:%S")

    # Check for "This [Day] at [time]" (Monday, Tuesday, etc.)
    days_of_week = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    for day_name, day_index in days_of_week.items():
        if f"This {day_name}" in date_str:
            # Parse the time explicitly from the string (after "at")
            remove_mutiple_event_ending = date_str.split("and")[0].strip()
            time_part = remove_mutiple_event_ending.split("at")[-1].strip()
            parsed_time = parser.parse(time_part, fuzzy=True).time()  # Extracts the time portion

            # Get the next occurrence of the target day with the parsed time
            return get_day_of_week(day_index, parsed_time).strftime("%Y-%m-%d %H:%M:%S")

    return None

# Function to parse a single date string without time zones
def parse_date(date_str):
    # Normalize the input by replacing non-breaking spaces with regular spaces
    date_str = date_str.replace("\u202f", " ")
    
    original_date_str = date_str  # Store the original date string
    parsed_date = parse_relative_date(date_str)
    
    if parsed_date:
        return parsed_date
    else:
        try:
            # Parse the date without time zone information
            remove_mutiple_event_ending = date_str.split("and")[0].strip()
            parsed_date = parser.parse(remove_mutiple_event_ending, fuzzy=True, ignoretz=True)

            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return {"original": original_date_str, "error": f"Error parsing date: {str(e)}"}

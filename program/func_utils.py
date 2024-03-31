from datetime import datetime, timedelta
#We need to format our price in such a way that it will be accepted by DED rest API.

# Format number
def format_number(curr_num, match_num):

  """
   The purpose of this function is to format the curr_num based on the format of match_num.
   the function takes the current number (curr_num) and an example number with the desired decimal format 
   (match_num), and returns the correctly formatted string.
   
  """
  #We are making sure this number is now converted to string
  #These lines convert both curr_num and match_num to strings using f-strings.
  curr_num_string = f"{curr_num}"
  match_num_string = f"{match_num}"

  #This line checks if the match_num_string contains a decimal point (".").
  #If a decimal point is found, it means match_num has decimal places.
  #If match_num_string has a decimal point, this line calculates the number of decimal places in match_num.
  #It splits the match_num_string at the decimal point 
  #and takes the length of the second part (index [1]), which represents the decimal places.

  # This line formats curr_num to have the same number of decimal places as match_num.
  #It uses an f-string with the format specifier .{match_decimals}f, where {match_decimals} is replaced 
  #with the number of decimal places calculated earlier.
 
  if "." in match_num_string:
    match_decimals = len(match_num_string.split(".")[1])
    curr_num_string = f"{curr_num:.{match_decimals}f}"

    #this line essentially creates a copy of the string to ensure that the original string remains unchanged.
    curr_num_string = curr_num_string[:]
    return curr_num_string
  else:
    return f"{int(curr_num)}"

  #If match_num does not have decimal places (i.e., it is an integer), 
  #the function returns curr_num as an integer.
  #It converts curr_num to an integer using int() and then formats it as a string using an f-string.

# Format time
def format_time(timestamp):
  return timestamp.replace(microsecond=0).isoformat()


# Get ISO Times
def get_ISO_times():

  # Get timestamps
  date_start_0 = datetime.now()
  #We calculate the starttime from 100 hours before that now time
  #timestamp that goes from 100 hours ago to right now
  date_start_1 = date_start_0 - timedelta(hours=100)
  date_start_2 = date_start_1 - timedelta(hours=100)
  date_start_3 = date_start_2 - timedelta(hours=100)
  date_start_4 = date_start_3 - timedelta(hours=100)

  # Format datetimes
  times_dict = {
    "range_1": {
      "from_iso": format_time(date_start_1),
      "to_iso": format_time(date_start_0),
    },
    "range_2": {
      "from_iso": format_time(date_start_2),
      "to_iso": format_time(date_start_1),
    },
    "range_3": {
      "from_iso": format_time(date_start_3),
      "to_iso": format_time(date_start_2),
    },
    "range_4": {
      "from_iso": format_time(date_start_4),
      "to_iso": format_time(date_start_3),
    },
  }

  # Return result
  return times_dict

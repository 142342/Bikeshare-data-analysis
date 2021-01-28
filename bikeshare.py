import time
import pandas as pd
import numpy as np

###############################################################################
############################ Requirements #####################################
# #1 Popular times of travel:
# - Most common month to travel
# - Most common day of week
# - Most common hour of the day
# #2 Popular stations and trips
# - Most common start station
# - Most common end station
# - Most common trip (same start and end stations)
# #3 Trip duration:
# - Total travel time
# - Average travel time
# #4 User information:
# - Counts of each user by type
# - Counts of each user by gender (NYC & Chicago only)
# - Earliest, latest, and most common year of birth for the users
################### Some questions to ask the user ############################
# 1 - Would you like to see data for Chicago, New York, or Washington?
# 2 - Would you like to filter the data by month, day or not at all?
# 2a - If by month, which month?
# 2b - If by day, which day?
###############################################################################

city_files = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
city_keys = list(city_files.keys())

months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
months_key_list = list(months.keys())
months_val_list = list(months.values())

days = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
days_key_list = list(days.keys())
days_val_list = list(days.values())
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington?\n').strip().lower()
    # handling inappropriate inputs for city name
    while city not in city_keys:
        city = input('City name not found, please enter Chicago, New York, or Washington instead.\n').strip().lower()
    # get user input for month (all, january, february, ... , june)
    month = input('Would you like to see data for January, February, March, April, May, or June?\n').strip().lower()
    # handling inappropriate inputs for month name
    while month not in months_key_list:
        month = input('Month name not found, please enter a month from January to June, inclusively.\n').strip().lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Would you like to see data for Monday, Tuesday... or Sunday?\n').strip().lower()
    # handling inappropriate inputs for day name
    while day not in days_key_list:
        day = input('Day name not found, please enter a day from Monday to Sunday, inclusively.\n').strip().lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into pandas dataframe
    df = pd.read_csv(city_files.get(city))

    # convert the Start Time to a to datetime format
    # year is not needed, since they're all 2017
    df['Start Time'] = pd.to_datetime(df['Start Time'], yearfirst = True)
    #print(df)
    # create new df with columns for month, day, weekday, and hour
    fdf = df
    fdf['month'] = df['Start Time'].dt.month
    fdf['day'] = df['Start Time'].dt.weekday
    fdf['hour'] = df['Start Time'].dt.hour
    fdf['trip'] = "from " + df['Start Station'] + " to " + df['End Station']

    # can also add more filter, based on the day of the month and so on.

    #print(fdf['month'])
    #By seeing the output, they're returned in numbers, hence the creation
    #of dictionaries instead of lists for months and weekdays.
    # filter df by month/day/both or none
    #print(fdf)
    return df, fdf

def time_stats(fdf):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    mcm =fdf['month'].mode()[0] #most common month as an integer
    month_position = months_val_list.index(mcm) #month's position
    most_common_month = months_key_list[month_position].capitalize() #month's name
    print("The most common month for travel is: " + most_common_month)
    # display the most common day of week
    mcd = fdf['day'].mode()[0] #most common day as an integer
    day_position = days_val_list.index(mcd) #day's position
    most_common_day = days_key_list[day_position].capitalize() #day's name
    print("The most common day for travel is: " + most_common_day)
    # display the most common start hour
    most_common_hour = fdf['hour'].mode()[0] #most common hour as integer
    print("The most common hour for travel is: " + str(most_common_hour) + ":00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(fdf):
    """Displays statistics on the most popular stations and trip.
    Args:
        dataframe

    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mcus = fdf['Start Station'].mode()[0] # most common start station
    print(mcus + " is the most common start station")
    # display most commonly used end station
    mces = fdf['End Station'].mode()[0] # most common end station
    print(mces + " is the most common end station")
    # display most frequent combination of start station and end station trip
    mc_trip = fdf['trip'].mode()[0] # most common trip
    print("The most common trip is " + mc_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(fdf):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    duration_total = fdf['Trip Duration'].sum(skipna = True)
    total_rounded = str(round(duration_total, 1))
    print("Total trip durations are: " + total_rounded + " in seconds")
    # display mean travel time
    duration_mean = fdf['Trip Duration'].mean(skipna = True)
    mean_rounded = str(round(duration_mean, 1))
    print("The average trip duration period is: " + mean_rounded + " in seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def appearance_count(fdf, column):
    '''Calculates the
    Args:
        (dataframe) df, having valid data.
        (str) column_name, name of the column for which the count of each type should be returned.
    Returns:
        Nothing
    '''
    print("Here is a count of the appearance of the unique elements in {}".format(column))
    print(fdf[column].value_counts())

def user_stats(fdf, city):
    """Displays statistics on bikeshare users.
    Args:
        dataframe
    Returns:
        Nothing
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    appearance_count(fdf,'User Type')
    print(city)
    # Display counts of gender
    if city == 'washington':
        print("Gender and birth year data are unavailable for Washington")
    else:
        appearance_count(fdf, 'Gender')

    # Display earliest, most recent, and most common year of birth
        print("The oldest customer was born in: " + str(int(fdf['Birth Year'].min()))
    + ", the youngest was born in " + str(int(fdf['Birth Year'].max())) +
     ", while the most common birth year was " + str(int(fdf['Birth Year'].mode()[0])) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_filtered(fdf, month, months, day, days):
    '''Continuously asks the user if he wants to see the raw data, showing 5
    lines at a time.
    Args:
        Takes the dataframe, month, months, day, and days.
        These have already been previously entered through get_filters().
    Returns:
        Nothing, but prints the dataframe 5 lines by 5 lines.
    '''
    #filtered = fdf[(fdf['month'] == month) & (fdf['day'] == day)]
    #fdf = fdf[(fdf['month'] == month) & fdf['day'] == day]

    accepted_inputs = ['yes', 'no']
    m = months.get(month)
    d = days.get(day)
    view = str(input("Do you want to preview a section of the filtered DataFrame?\nAnswer with \'Yes\' or \'No\' \n")).lower().strip()
    pd.set_option('display.max_columns',13)
    if view == 'yes':
        #print the first 5 rows upon the user's request
        print("Below is the first 5 rows of the filtered DataFrame")
        filtered = fdf[(fdf.month == m) & (fdf.day == d)]
        print(filtered.iloc[:5, :])
        start = 0
        end = 5
        view_again = str(input("\nWould you like to view 5 more rows?\nPlease answer with \'Yes\' or \'No\' \n")).lower().strip()
        while view_again not in accepted_inputs:
            view_again = input("Please enter an appropriate input; either \'Yes\' or \'No\' \n").lower().strip()
        #the while loop to print until user does not want to continue
        while view_again == 'yes':
            start+=5
            end+=5
            print("\nBelow are the next 5 rows of the data")
            print(filtered.iloc[start:end, :])
            view_again = str(input("\nWould you like to view 5 more rows?\nPlease answer with \'Yes\' or \'No'\" \n")).lower().strip()
            #checking for unacceptable inputs
            while view_again not in accepted_inputs:
                view_again = input("Please enter an appropriate input; either \'Yes\' or \'No\' \n").lower().strip()

    else: print("You have chosen not to view any of the raw data")

def main():
    while True:
        city, month, day = get_filters()
        df, fdf = load_data(city, month, day)

        time_stats(fdf)
        station_stats(fdf)
        trip_duration_stats(fdf)
        user_stats(fdf, city)
        print_filtered(fdf, month, months, day, days)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

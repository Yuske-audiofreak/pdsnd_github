# bikeshare.py
"""
This file is modified for git hub project.
"""

import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = { 'Jan': 1,
               'Feb': 2,
               'Mar': 3,
               'Apr': 4,
               'May': 5,
               'Jun': 6 }
"""
Jan: January, Feb: February, Mar: March, Apr: April, May: May, Jun: June
"""

DAY_DATA = { 'Sun': 'Sunday',
             'Mon': 'Monday',
             'Tue': 'Tuesday',
             'Wed': 'Wednesday',
             'Thu': 'Thursday',
             'Fri': 'Friday',
             'Sat': 'Saturday' }
"""
This is a filter module for time.
"""

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
    while True:
        city_input = input("Would you like to see data for Chicago, New York City or Washington? \n")
        city = city_input.lower()
        if city in CITY_DATA.keys():
            break

    # get user input for month to filter month (all, january, february, ... , june)
    while True:
        month_input = input("Would you like to filter the data by month? \nJan, Feb, Mar, Apr, May or Jun? Type \"All\" for no month filter: ")
        month_alphabet = month_input.title()

        if month_alphabet == "All":
            month = 0
            break
        elif month_alphabet in MONTH_DATA.keys():
            month = MONTH_DATA[month_alphabet]
            break

    # get user input for day of week to filter month (all, monday, tuesday, ... sunday)
    while True:
        day_of_week_input = input("Which day of week do you want to check? \nSun, Mon, Tue, Wed, Thu, Fri or Sat? Type \"All\" for no day_of_week filter: ")
        day_of_week_head = day_of_week_input.title()

        if day_of_week_head == "All":
            day = "None"
            break
        elif day_of_week_head in DAY_DATA.keys():
            day = DAY_DATA[day_of_week_head]
            break

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

    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to DataFrame
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week, hour of day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour_of_day'] = df['Start Time'].dt.hour

    #filter
    # Filters by month
    if month != 0:
        df = df[df['month'] == month]

    # Filters by day
    if day != "None":
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # If the dataframe has only 1 month information then skip this sentence.
    um = df['month'].unique()
    um2 = len(um)

    mst_cm_month = df['month'].value_counts().idxmax()

    if um2 != 1:
        print("The most common month is {}.".format(mst_cm_month))

    # display the most common day of week
    msc_cm_d_o_w = df['day_of_week'].value_counts().idxmax()

    ud = df['day_of_week'].unique()
    ud1 = len(ud)

    if ud1 != 1:
        print("The most common day of week is {}.".format(msc_cm_d_o_w))

    # display the most common start hour
    mst_cm_h_o_d = df['hour_of_day'].value_counts().idxmax()
    print("The most common start hour is {}.".format(mst_cm_h_o_d))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mst_cm_start_station = df['Start Station'].value_counts().idxmax()
    mst_cm_start_station_count = df['Start Station'].value_counts().max()
    print("The most commonly used start station is {}. Count: {}".format(mst_cm_start_station, mst_cm_start_station_count))

    # display most commonly used end station
    mst_cm_end_station = df['End Station'].value_counts().idxmax()
    mst_cm_end_station_count = df['End Station'].value_counts().max()
    print("The most commonly used end station is {}. Count: {}".format(mst_cm_end_station, mst_cm_end_station_count))

    # display most frequent combination of start station and end station trip
    # groupby: this is a command to count the combination of start station to end station
    mst_cm_start_to_end_station_name2 = df.groupby(['Start Station', 'End Station'])['Start Station'].count().idxmax()
    mst_cm_start_to_end_station_count2 = df.groupby(['Start Station', 'End Station'])['Start Station'].count().max()


    print("'Start Station' & 'End station' \n{}. Count : {}".format(mst_cm_start_to_end_station_name2, mst_cm_start_to_end_station_count2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_days, total_hour_min_sec = convert(total_travel_time)

    print("The total travel time is {} seconds, which is {} days {}.".format(total_travel_time, total_travel_days, total_hour_min_sec))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    mean_travel_days, mean_travel_hour_min_sec = convert(mean_travel_time)

    print('The average is {} seconds, which is {} days {}.'.format(mean_travel_time, mean_travel_days, mean_travel_hour_min_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def convert(seconds):
    days = seconds // (24 * 3600)   # quotient
    seconds = seconds % (24 * 3600) # reminder
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return days, "%d:%02d:%02d" % (hours, minutes, seconds)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("What is the breakdown of users?")
    user_type_counts = df['User Type'].value_counts().to_dict()
    print(user_type_counts)

    # Display counts of gender
    if 'Gender' in df:
        print("What is the breakdown of gender?")
        user_gender_info = df['Gender'].value_counts().to_dict()
        print(user_gender_info)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year_of_birth = df['Birth Year'].min()
        most_recent_year_of_birth = df['Birth Year'].max()
        most_common_year_of_birth = df['Birth Year'].value_counts().idxmax()

        print("What is the oldest, youngest, and most popular year of birth, respectively?")
        print("The oldest year of birth is {}.".format(earliest_year_of_birth))
        print("The youngest year of birth is {}.".format(most_recent_year_of_birth))
        print("The most common year of birth is {}.".format(most_common_year_of_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_row_data(df):
    """Displays row data on bikeshare users"""
    i = 0

    while True:
        for j in range(5):
            print(df[i:i+1])
            i += 1

        restart_show_row_data = input('\nWould you like to continue? Enter yes or no.\n')
        if restart_show_row_data != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()

        print("You chose {}".format(city.title()))
        print("Your filter of the month is {}".format(month))
        print("Your filter of day of week is {}".format(day))


        df = load_data(city, month, day)

        # To check the contents of df
        #print(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_row_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

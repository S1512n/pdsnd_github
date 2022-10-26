import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
current_city = None
current_month= None
current_day = None


def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #global keyword to allow modifying the gobal variables
    global current_city
    global current_month
    global current_day

    cities = ['chicago', 'new york', 'washington']
    city = None
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = None
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    day = None
    print('\n\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in cities:
        city = input('''Which city would you like to explore: Chicago, New York or Washington?\n\n''').lower()
        if city not in cities:
            print("Check spellings!!!")
    #assign the global variable current_city the value of city
    current_city = city
    print("\n\nlet's choose a month..............")
    # get user input for month (all, january, february, ... , june)
    while month not in months:
        month = input('''Which month from January to June would you like to explore: ? Enter 'all' to explore all months \n\n''').lower()
        if month not in months:
            print("Check spellings!!!")
    current_month = month
    print("\n\nlets choose a day..............")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days:
        day = input('''Which day of the week would you like to explore:? Enter 'all' to explore all cities \n\n''').lower()
        if day not in days:
            print("Check spellings!!!")
    current_day = day
    print("\n\n\n\nOK. lets see some stats")
    print('*'*111)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #convert Trip Duration to int
    df['Trip Duration'] = df['Trip Duration'].astype(int)
    #convert Birth Year to int
    try:
        df['Birth Year'] = df['Birth Year'].astype(int)
    except:
        pass
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    df = df.dropna( axis=0 )

    return df


def divide_time(total_sec):
    """Finds the number of days, hours, minutes and seconds in a nuber of seconds
    args:
        (int) total_sec - total trip duration
    returns:
        (int) days - number of days in total trip duration
        (int) hours - number of hours in total trip duration
        (int) minutes - number of minutes in total trip duration
        (int) seconds - number of seconds in total trip duration
    """

    days = total_sec // 86400
    remainder_1 = total_sec % 86400
    hours = remainder_1 // 3600
    remainder_2 = remainder_1 % 3600
    minutes = remainder_2 // 60
    seconds = remainder_2 % 60

    return days, hours, minutes, seconds


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n\n\n')
    start_time = time.time()

    # display the most common month
    if current_month != 'all':
        pass
    elif current_month == 'all':
        print('Most common month is {}\n\n'.format(['january', 'february', 'march', 'april','may', 'june'][(df['month'].mode()[0])-1]))
    # display the most common day of week
    if current_day != 'all':
        pass
    elif current_day == 'all':
        print('Most common day of the week is {}\n\n'.format(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][df['day_of_week'].mode()[0]]))
    # display the most common start hour
    print('Most common hour is {}\n\n'.format(df['hour'].mode()[0]))

    #print time taken execute time_stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*111)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n\n\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most popular start station is {}\n\n'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most popular end station is {}\n\n'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['temp'] = df['Start Station'] +' & '+ df['End Station']
    print('Most popular combination of start and end stations is {}\n\n'.format(df['temp'].mode()[0]))
    df.drop(['temp'], axis = 1)

    #print time taken to execute station_stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*111)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n\n\n')
    start_time = time.time()

    # display total travel time in days, hours, minutes and seconds
    total_sec = df['Trip Duration'].sum()
    days, hours, minutes, seconds = divide_time(total_sec)
    print('Total travel time is {} days {} hours {} minutes and {} seconds \n\n'.format(days,hours, minutes, seconds))

    # display mean travel time
    mean_sec = df['Trip Duration'].mean().astype(int)
    total_sec = mean_sec
    days, hours, minutes, seconds = divide_time(total_sec)
    print('Mean time is {} days {} hours {} minutes and {} seconds\n\n'.format(days,hours,minutes,seconds))

    #print time taken to execute trip_duration_stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*111)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n\n\n')
    start_time = time.time()

    # Display counts of user types
    df2 = df['User Type'].value_counts().reset_index()
    df2.columns = ['User Type', 'Count']
    for index, row in df2.iterrows():
        print(row['User Type'],'\t\t\t',row['Count'],'\n\n')
    df2.drop(['User Type', 'Count'], axis = 1)

    #display counts of gender
    try:
        df3 = df['Gender'].value_counts().reset_index()
        df3.columns = ['Gender', 'Count']
        for index, row in df3.iterrows():
            print(row['Gender'],'\t\t\t\t' ,row['Count'],'\n\n')
        df3.drop(['Gender', 'Count'], axis = 1)
    except:
        print("\n\nGender data not available for Washington")

    # Display earliest, most recent, and most common year of birth
    try:

        print('\n\n\nThe earliest year of birth is {}'.format((df['Birth Year'].min()).astype(int)))
        print('\n\n\nThe most recent year of birth is {} '.format((df['Birth Year'].max()).astype(int)))
        print('\n\n\nThe most common year of birth is {} '.format((df['Birth Year'].mode()[0]).astype(int)))
    except:
        print("\n\nYear of Birth data not available for Washington")

    #print time taken to execute user_stats
    print("\nThis took %s seconds."% (time.time() - start_time))
    print("-"*111)


def raw_data(df):
    """prints raw data five rows at a time"""
    check = True
    while check == True:
        for i in range(0, len(df)-1, 5):
    #if statement checks if end of dataframe is within five rows of current index
            if i+5 < len(df)-1:
    #more_data is set to none to allow entering while loop
                more_data = None
    #prints five rows at a time
                print(df.iloc[i : i + 5])
    #asks user whether to continue
                while more_data not in ['yes', 'no']:
                    more_data = input('\n\n\nWould you like to see more raw data? Enter yes or no.\n').lower()
                    if more_data not in ['yes', 'no']:
                        print("""\n\nPlease enter 'Yes' or 'No'!!!""")
            if more_data.lower() != 'yes':
                break
    #if current index is less than five rows from end of dataframe print remaining rows
            elif i+5 > len(df)-1:
                print(df.iloc[i : len(df)-1])
    #sets check to False to exit while loop
        check = False


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #clears the stored value of restart to allow entering the while loop
        restart = None
        while restart not in ['yes','no']:
            restart = input('\n\n\nWould you like to restart? Enter yes or no.\n').lower()
            if restart not in ['yes','no']:
                print("""\n\nPlease enter 'Yes' or 'No'!!!""")
        if restart.lower() == 'yes':
            continue
        elif restart.lower() == 'no':
            break
    raw_data(df)


if __name__ == "__main__":
	main()

import time
import pandas as pd

# Dictionary mapping city names to their respective CSV files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Dictionary mapping month names to their numeric equivalents
MONTH_DATA = {
    'january': 1, 'february': 2, 'march': 3,
    'april': 4, 'may': 5, 'june': 6, 'all': 7
}

# Dictionary mapping day names to their numeric equivalents
DAY_DATA = {
    'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4,
    'friday': 5, 'saturday': 6, 'sunday': 7, 'all': 8
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Greetings! Let's explore some US bikeshare data!\n")

    city = ''
    while city not in CITY_DATA:
        print("Welcome! Please choose your city: Chicago, New York, or Washington.")
        city = input('Enter city name: ').strip().lower()
        if city not in CITY_DATA:
            print("Please enter a valid city name.\n")

    print(f"\nYou have chosen {city.title()} as your city.\n")

    month = ''
    while month not in MONTH_DATA:
        month = input("Enter a month between January to June, or 'all' to select all months: ").strip().lower()
        if month not in MONTH_DATA:
            print("Invalid input for month. Please enter a valid month or 'all'.\n")

    print(f"Selected month: {month.title()}\n")

    day = ''
    while day not in DAY_DATA:
        day = input("Enter a day or 'all' to select all days: ").strip().lower()
        if day not in DAY_DATA:
            print("Invalid input for day. Please enter a valid day or 'all'.\n")

    print(f"Selected day: {day.title()}\n")

    print(f"You have chosen to view data for city: {city.title()}, month/s: {month.title()}, and day/s: {day.title()}.\n")

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
    print("Loading data...\n")
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        month = MONTH_DATA[month]
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("Calculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Most popular month
    pop_month = df['month'].mode()[0]
    print(f"Most popular month: {pop_month}\n")

    # Most popular day of week
    pop_day = df['day_of_week'].mode()[0]
    print(f"Most popular day of week: {pop_day}\n")

    # Most popular hour of day
    pop_hour = df['hour'].mode()[0]
    print(f"Most popular hour of day: {pop_hour}\n")

    print(f"This took {(time.time() - start_time)} seconds.")
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("Calculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {common_start_station}\n")

    # Most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station: {common_end_station}\n")

    # Most frequent combination of start and end stations
    df['Start End Combo'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_trip = df['Start End Combo'].mode()[0]
    print(f"The most frequent combination of start and end stations: {most_common_trip}\n")

    print(f"This took {(time.time() - start_time)} seconds.")
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    print("Calculating Trip Duration...\n")
    
    # Record the start time for performance measurement
    start_time = time.time()

    # Calculate total travel time
    total_duration = df['Trip Duration'].sum()
    print(f"Total travel time: {total_duration} seconds\n")

    # Calculate average travel time
    average_duration = df['Trip Duration'].mean()
    print(f"Average travel time: {average_duration} seconds\n")

    # Calculate and display the time taken for the calculations
    elapsed_time = time.time() - start_time
    print(f"This took {elapsed_time} seconds.")
    print('-' * 40)



def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("Calculating User Stats...\n")
    start_time = time.time()

    # User type counts
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print(f"Counts of each user type:\n{user_types}\n")
    else:
        print("No 'User Type' data available.\n")

    # Gender counts
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print(f"Counts of gender:\n{genders}\n")
    else:
        print("No 'Gender' data available.\n")

    # Check if 'Birth Year' column exists in the DataFrame
    if 'Birth Year' in df.columns:
        # Calculate the earliest birth year
        earliest_birth_year = int(df['Birth Year'].min())
        
        # Calculate the latest birth year
        latest_birth_year = int(df['Birth Year'].max())
        
        # Calculate the most common birth year
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        
        # Print the statistics
        print(f"Earliest birth year: {earliest_birth_year}\n")
        print(f"Most recent birth year: {latest_birth_year}\n")
        print(f"Most common birth year: {most_common_birth_year}\n")

    else:
        print("No birth year data available.\n")

    print(f"This took {(time.time() - start_time)} seconds.")
    print('-'*40)


def display_data(df):
    """
    Displays 5 rows of data from the DataFrame df based on user input, continuing until user stops.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_loc = 0
    while True:
        show_data = input("Do you want to see 5 rows of data? Enter 'yes' or 'no': ").lower()
        if show_data != 'yes':
            break
        
        # Display 5 rows of data starting from start_loc
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5


def main():
    """
    Main function to call other functions and run the program.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)  # Added to allow interactive data viewing

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

import datetime
from math import sqrt
"""Important period tracker data:
- average cycle length
- average cycle variation
- correlations with period
    - anxiety level
    - stress level
    - sex drive
    - add more later on...
- average ovulation time after period
- average ovulation time
- ovulation time variation"""

STARTING_AVG_CYCLE_LENGTH = 30
STARTING_AVG_PERIOD_LENGTH = 5
STARTING_OVULATION_TIME = 12

first_string = 'avg cycle length, stdev cycle length, avg period length, stdev cycle length, avg ovulation start'

file = 'tracked times.txt'


class Entry:
    """A recorded day
    """

    def __init__(self, date, period=False) -> None:
        """Initialize a day"""
        if date is None:
            date = datetime.datetime.now()
        date_low_res = datetime.date(date.year, date.month, date.day)
        self.date = date_low_res
        self.period = period

    def dif(self, other_day) -> int:
        """find the difference between two days"""
        return (self.date - other_day.date).days

    def __str__(self) -> str:
        out_str = ''
        out_str = out_str + str(self.date.year) + ', '
        out_str = out_str + str(self.date.month) + ', '
        out_str = out_str + str(self.date.day) + ', '
        out_str = out_str + str(self.period)
        return out_str


def add_entry(date, period, period_list) -> None:
    """add entry to period list, date can be None and datetime object"""
    new_entry = Entry(date, period)
    count = 0
    if len(period_list) == 0:
        period_list.append(new_entry)
        return None
    for item in period_list:
        if item.dif(new_entry) == 0:
            period_list[count] = new_entry
            return None
        if item.dif(new_entry) > 1:
            period_list.insert(count, new_entry)
            return None
        count += 1
    period_list.append(new_entry)
    return None


def convert_to_entry(input_entry: str) -> Entry:
    """Convert strings in the format: '2022, 7, 24, False' to a datetime
    object and bool object, and then initialize an Entry object"""

    fix_list = input_entry.split(',')
    date = datetime.date(int(fix_list[0]), int(fix_list[1]), int(fix_list[2]))
    bool_value = fix_list[3].strip()
    if bool_value == 'False':
        bool_value = False
    else:
        bool_value = True
    return Entry(date, bool_value)

def average_cycle_len(stats_list, entry_list) -> float:
    """go through the list of entries until you find a period date, then
    keep going until you find the next period entry, then take the difference
    between the two dates in days and append to a list, if the end of the list
    is reached before a next period is found, do not append to the list, then
    take the average of the list and the current avg_cycle_length stat and
    output that float"""
    avg_list = []
    prev = False
    for item in entry_list:

        if item.period and not prev:
            last_date = item
            prev = True
        elif item.period and prev:
            days_dif = item.dif(last_date)
            avg_list.append(days_dif)
            last_date = item
    if len(avg_list) == 0:
        avg_list.append(stats_list[0])
    total = 0.0
    for item in avg_list:
        total += item
    return total / len(avg_list)

def cycle_stdev(stats_list, entry_list) -> float:
    """Find the standard deviation of period length and output it as float"""
    avg_list = []
    v_list = []
    prev = False
    for item in entry_list:
        if item.period and not prev:
            last_date = item
            prev = True
        elif item.period and prev:
            days_dif = item.dif(last_date)
            avg_list.append(days_dif)
            last_date = item
    if len(avg_list) == 0:
        return 0.0
    else:
        mean = average_cycle_len(stats_list, entry_list)
        for item in avg_list:
            dif = (item - mean)
            sqrd_dif = dif * dif
            v_list.append(sqrd_dif)
        total = 0
        for item in v_list:
            total += item
        if len(v_list) > 1:
            total = total / (len(v_list) - 1)
        return sqrt(total)


def median(entry_list):
    avg_list = []
    prev = False
    for item in entry_list:
        if item.period and not prev:
            last_date = item
            prev = True
        elif item.period and prev:
            days_dif = item.dif(last_date)
            avg_list.append(days_dif)
            last_date = item

    avg_list.sort()
    if len(avg_list) <= 1:
        return 0
    return avg_list[len(avg_list) // 2]

def update_cycle_len(stats_list, entry_list):
    """Change statistics list to reflect current average cycle length"""
    new_avg = average_cycle_len(stats_list, entry_list)
    stats_list[0] = new_avg

def update_cycle_stdev(stats_list, entry_list):
    """Change the statistics list to reflect current stdev cycle length"""
    new_stdev = cycle_stdev(stats_list, entry_list)
    stats_list[1] = new_stdev

def update_all_stats(stats_list, entry_list):
    """Update all stats"""
    update_cycle_stdev(stats_list, entry_list)
    update_cycle_len(stats_list, entry_list)

def read_list(file_name=file) -> tuple:
    """Read the tracked times file and output a list in order"""
    out_list = []
    f = open(file_name, 'r')
    f.readline()
    stat_list = f.readline().split(',')
    for i in range(len(stat_list)):
        stat_list[i] = float(stat_list[i])
    for line in f:
        if line != '\n':
            entry = convert_to_entry(line)
            out_list.append(entry)
    f.close()
    return stat_list, out_list


def write_list(file_name, statistics, entry_list) -> None:
    """Save the tracked information from the list to the file"""
    f = open(file_name, 'w')
    stats = ''
    for item in statistics:
        stats = stats + str(item) + ', '
    lines_out = [first_string + '\n', stats[:-2] + '\n']
    for item in entry_list:
        lines_out.append(str(item) + '\n')
    f.writelines(lines_out)
    f.close()
    return None


if __name__ == '__main__':
    main_lists = read_list(file)
    stats = main_lists[0]
    entries = main_lists[1]
    for entry in entries:
        print (entry)
    print (stats)
    add_entry(datetime.date(2002, 10, 23), False, entries)
    for entry in entries:
        print (entry)
    print (average_cycle_len(stats, entries))
    print (cycle_stdev(stats, entries))
    write_list(file, stats, entries)

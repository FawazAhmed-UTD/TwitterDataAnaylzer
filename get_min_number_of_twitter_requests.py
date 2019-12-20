import json
from datetime import datetime, timedelta
'''
By Fawaz Ahmed from UTD
'''

def read_incident_file(fileName):
    with open(fileName, 'r') as file:
        fileData = json.load(file)
    return fileData


def getDates(fileData):
    sortedDates = []
    for i in range(len(fileData)):
        date = datetime.strptime(fileData[i]['date'], '%m/%d/%y').strftime('%Y-%m-%d')
        if date not in sortedDates:
            sortedDates.append(str(date))
    sortedDates.sort()
    return sortedDates


def getRequests(sortedDates):
    requestDates = []
    since_until_dates = {'Since': '0000-00-00', 'Until': '0000-00-00'}
    requestDates.append(since_until_dates.copy())
    requestDates_position = 0

    for sinceDate in sortedDates:
        untilDate = str(datetime.strptime(sinceDate, '%Y-%m-%d') + timedelta(days=1))[0:10]
        sinceDate_condition2 = str(datetime.strptime(sinceDate, '%Y-%m-%d') - timedelta(days=1))[0:10]

        if requestDates[requestDates_position]['Since'] == '0000-00-00' or \
                requestDates[requestDates_position]['Since'] == sinceDate:
            requestDates[requestDates_position]['Since'] = sinceDate
            requestDates[requestDates_position]['Until'] = untilDate
        elif requestDates[requestDates_position]['Until'] == sinceDate or \
                requestDates[requestDates_position]['Until'] == sinceDate_condition2:
            requestDates[requestDates_position]['Until'] = untilDate
        else:
            requestDates.append(since_until_dates.copy())
            requestDates_position += 1
            requestDates[requestDates_position]['Since'] = sinceDate
            requestDates[requestDates_position]['Until'] = untilDate

    return requestDates


def save_in_json(data):
    with open('requestDates.json', 'w') as file:
        for i in data:
            json.dump(i, file)
            file.write('\n')


if __name__ == '__main__':
    fileData = read_incident_file("reported_incidents_v2.json")
    dates = getDates(fileData)
    requests = getRequests(dates)
    save_in_json(requests)

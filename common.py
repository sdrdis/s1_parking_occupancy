import datetime

def get_direction_orbit(fileid):
    direction = None
    orbit = None
    for el in fileid:
        if (el.startswith('ASC')):
            direction = 'ASCENDING'
        if (el.startswith('DES')):
            direction = 'DESCENDING'
        if (len(el) == 3 and el.isnumeric()):
            orbit = el
            
    return direction, orbit

open_sundays = [
    datetime.datetime(2018, 7, 29),
    datetime.datetime(2018, 8, 5),
    datetime.datetime(2018, 8, 12),
    datetime.datetime(2018, 8, 19),
    datetime.datetime(2018, 8, 26),
    datetime.datetime(2018, 12, 2),
    datetime.datetime(2018, 12, 9),
    datetime.datetime(2018, 12, 16),
    datetime.datetime(2018, 12, 23),
    datetime.datetime(2018, 12, 30),
    datetime.datetime(2019, 7, 28),
    datetime.datetime(2019, 8, 4),
    datetime.datetime(2019, 8, 11),
    datetime.datetime(2019, 8, 18),
    datetime.datetime(2019, 8, 25),
    datetime.datetime(2019, 12, 22),
    datetime.datetime(2019, 12, 29)
]

state_to_category = {
    'Cloudy': 'cloudy',
    'Drizzle': 'rain',
    'Drizzle and Fog': 'rain',
    'Fair': 'sunny',
    'Fog': 'fog',
    'Haze': 'fog',
    'Rain': 'rain',
    'Rain Shower': 'rain',
    'Snow': 'snow',
    'T-Storm': 'storm',
    'Rain with Thunder': 'rain',
    'Sleet': 'snow',
    'Rain and Sleet': 'snow',
    'Snow Grains': 'snow',
    'Snow Shower': 'snow',
    'Snow and Sleet': 'snow',
    'Mist': 'fog',
    'Shallow Fog': 'fog',
    'Showers in the Vicinity': 'rain',
    'Snow Shower': 'snow',
    'Snow and Sleet': 'snow',
    'Thunder': 'storm',
    'Thunder in the Vicinity': 'storm',
    'Unknown Precipitation': 'rain',
    'Wintry Mix': 'snow',
    'Thunder / Wintry Mix': 'snow',
    'Small Hail': 'snow',
    'Drifting Snow': 'snow',
    'Thunder and Small Hail': 'snow',
    'Rain and Snow': 'snow',
    'Thunder and Hail': 'snow',
}

cat_to_id = {
    'sunny': 0,
    'cloudy': 1,
    'fog': 2,
    'rain': 3,
    'storm': 4,
    'snow': 5
}

def get_category(state):
    nstate = state.replace(' / Windy', '')
    nstate = nstate.replace('Heavy ', '')
    nstate = nstate.replace('Light ', '')
    nstate = nstate.replace('Freezing ', '')
    nstate = nstate.replace('Mostly ', '')
    nstate = nstate.replace('Partial ', '')
    nstate = nstate.replace('Partly ', '')
    nstate = nstate.replace('Patches of ', '')
    return state_to_category[nstate]
    
def get_category_id(state):
    if (state is None):
        return -1
    return cat_to_id[get_category(state)]
    
    
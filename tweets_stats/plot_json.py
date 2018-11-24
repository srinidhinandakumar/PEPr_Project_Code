import csv
import json
import folium
import pandas as pd
import matplotlib.pylab as plt

from collections import defaultdict
from geopy.geocoders import Nominatim

geocode_data_file_pos = "stats_parties/geocodes_data_pos.json"
geocode_data_file_neg = "stats_parties/geocodes_data_neg.json"

def plot_line_chart(filename):
    with open(filename) as f:
        data = json.load(f)

    required_data = {}
    for k, v in data.items():
        # date filter - not a super great way though
        if "26-16" <= k <= "27-10":
            key1 = "0" + k.split("-")[0] if len(k.split("-")[0]) < 2 else k.split("-")[0]
            key2 = "0" + k.split("-")[1] if len(k.split("-")[1]) < 2 else k.split("-")[1]
            key = float(key1) + float(key2)/24.0
            print(k, " converted to ", key, " value", v)
            required_data[float(key)] = v

    lists = sorted(required_data.items())
    x, y = zip(*lists)
    plt.plot(x, y)
    plt.xticks(rotation=90)
    plt.show()

def convert_location_to_geocodes(filename):
    geolocator = Nominatim(user_agent="pepr_geocode_getter", timeout = 3)

    with open(filename) as f:
        locations = json.load(f)

    locations = dict(sorted(locations.items(), key=lambda x: -abs(x[1])))

    latitudes = []
    longitudes = []
    names = []
    values = []

    count = 0
    for k, v in locations.items():
        print(k, v)
        location = geolocator.geocode(k, addressdetails = True)

        if count == 100:
            break
        count += 1

        try:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            names.append(location.address)
            values.append(v)
        except Exception as e:
            # if the string is not location or couldn't find geo-coordinates for location
            print(e)

    geocodes_data = {
        'lat': latitudes,
        'lon': longitudes,
        'name': names,
        'value': values
    }

    outfile = open(geocode_data_file, 'w')
    json.dump(geocodes_data, outfile)


def convert_location_to_states(filenames):
    geolocator = Nominatim(user_agent="pepr_geocode_getter", timeout=3)
    sentiments = defaultdict(int)

    for filename in filenames:
        with open(filename) as f:
            locations = json.load(f)

        locations = dict(sorted(locations.items(), key=lambda x: -abs(x[1])))

        count = 0
        for k, v in locations.items():
            # print(k, v)
            location = geolocator.geocode(k, addressdetails=True)

            if count == 120:
                break
            count += 1

            try:
                if location.raw['address']['country'] == 'USA':
                    print(location.raw['address']['state'])
                    sentiments[location.raw['address']['state']] += v
            except Exception as e:
                # if the string is not location or couldn't find address or state for location
                print(e)


    f = open('state_sentiments.csv', 'w')
    for key, value in sentiments.items():
        f.write(key + ',' + str(value) + "\n")

def plot_bubble_chart(geocode_data_file):

    # Make an empty map
    m = folium.Map(location=[37.7837304, -97.4458825], tiles="Mapbox Bright", zoom_start=5)
    folium.Marker(location=[37.926868, -78.024902], popup='Virginia (Speech delivered)').add_to(m)

    with open(geocode_data_file) as f:
        geocodes_data = json.load(f)

    # Make a data frame with dots to show on the map
    data = pd.DataFrame(geocodes_data)
    print(data)

    if "pos" in str(geocode_data_file):
        color = 'green'
    else:
        color = 'crimson'

    # add circles one by one on the map
    for i in range(0, 44):
        try:
            folium.Circle(
                location=[float(data.iloc[i]['lat']), float(data.iloc[i]['lon'])],
                popup=str(data.iloc[i]['name']) + " - " + str(data.iloc[i]['value']) + " tweets",
                radius=abs(data.iloc[i]['value']) * 200,
                color=color,
                fill=True,
            ).add_to(m)
        except Exception as e:
            print(e)

    m.save(str(geocode_data_file) + '.html' )

def plot_bar_chart(tweet_source_filename):
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.pyplot as plt

    plt.rcdefaults()

    with open(tweet_source_filename) as f:
        tweet_source_data = json.load(f)

    objects = []
    values = []

    for k, v in tweet_source_data.items():
        objects.append(k)
        values.append(v)

    objects = objects[:10]
    values = values[:10]

    y_pos = np.arange(len(objects))

    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation=90)
    plt.xlabel('Source')
    plt.ylabel('Number of users')
    plt.title('Top 10 Tweet Sources')
    plt.savefig('bar_chart_tweet_sources.png')

    plt.show()


def plot_charts():

    # line_chart_inputfile = 'stats/date_count.json'
    # plot_line_chart(line_chart_inputfile)
    # print('plotted line chart')

    # tweet_source_filename = 'stats/tweet_source_count.json'
    # plot_bar_chart(tweet_source_filename)
    # print('plotted bar chart')

    # bubble_chart_inputfile = 'stats_parties/location_count_pos.json'
    # convert_location_to_geocodes(bubble_chart_inputfile)
    # print('geocode_data_file is ready!')

    inputfiles = ['stats_parties/location_count_pos.json', 'stats_parties/location_count_neg.json']
    convert_location_to_states(inputfiles)
    print('geocode_data_file is ready!')

    # bubble_chart_inputfile = 'stats_parties/location_count_neg.json'
    # convert_location_to_geocodes(bubble_chart_inputfile)
    # print('geocode_data_file is ready!')

    # plot_bubble_chart(geocode_data_file_pos)
    # print('plotted bubble chart')

    # plot_bubble_chart(geocode_data_file_neg)
    # print('plotted bubble chart')


if __name__ == '__main__':
    plot_charts()
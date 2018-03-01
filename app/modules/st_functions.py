import os
import random
import itertools
import requests


# Split data into fixed-length chunks
def grouper(n, iterable, fillvalue=''):
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


# Grab API key from hidden file
def get_steam_api_key():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    filepath = os.path.abspath(os.path.join(path, os.pardir))
    file_object = filepath + '/steamtime_api_key.txt'

    with open(file_object, 'r') as f:
        data = f.read()
        return data[10:]


# Testing if user has input a vanity URL or 64-bit SteamID
def test_user_input(userinput):
    # Testing if user has input a 64-bit numerical SteamID or vanity url
    if len(userinput) == 17 and not userinput[0].isalpha():
        steam_id = userinput
        url_string = '%s?key=%s&steamids=%s' % (API_PLAYER, API_KEY, steam_id)
        json_data = requests.get(url_string).json()
        display_name = json_data['response']['players'][0]['personaname']
        return [steam_id, display_name]
    else:
        url_string = '%s?key=%s&vanityurl=%s' % (API_URL_STEAMID, API_KEY, userinput)
        steam_id = requests.get(url_string).json()['response']['steamid']
        display_name = userinput
        return [steam_id, display_name]


# Function to organize games into a list with desired bits of data
def parse_data(data, playtime_type, number_of_results, recent, steamid):
    if recent == 1:
        readout = 'In the Last Two Weeks'
    else:
        readout = 'Since 2009'
    minutes_played = []
    try:
        for game in data['response']['games']:
            # Catch KeyErrors here in case an appID has been partially removed, like after a public alpha
            try:
                appid = game['appid']
                game_hash = game['img_logo_url']
                image_url = 'http://media.steampowered.com/steamcommunity/public/images/apps/%s/%s.jpg' % \
                            (appid, game_hash)
                store_page = 'http://store.steampowered.com/app/%s/' % appid
                stats_url = 'http://steamcommunity.com/profiles/%s/stats/%s' % (steamid, appid)
                minutes_played.append([game['name'], game['%s' % playtime_type], image_url, stats_url, store_page])
            except KeyError:
                continue
    # Return 'privacy' if user has set privacy settings blocking two-weeks API
    except KeyError:
        return 'privacy'

    # Using a reverse sort by the 2nd index (minutes played) of each entry for descending order
    minutes_played = sorted(minutes_played, key=lambda index: index[1], reverse=True)

    # Storing sorted minutes_played as a list with an index, game name, hours played string, and icon URL
    minutes_played_new = []
    counter = 0
    total_hours = 0.0
    for entry in minutes_played:
        if number_of_results == 'all':
            pass
        else:
            if counter == int(number_of_results):
                break
        total_hours += entry[1] / 60.0
        counter += 1

    # Additional loop to add pie chart data
    base_color = '#1a87d4'
    accent_color = '#0c3f63'
    counter = 0
    for entry in minutes_played:
        if number_of_results == 'all':
            pass
        else:
            if counter == int(number_of_results):
                break
        hours_played = entry[1] / 60.0
        pie_chart_data = '[{value: %.1f, color:"%s", highlight: "#3FADFB", label: "Total Hours"}, ' \
                         '{value: %.1f, color: "%s", highlight: "#3FADFB", label: "%s"}]' \
                         % (total_hours, base_color, hours_played, accent_color, entry[0])
        minutes_played_new.append([counter + 1, entry[0], '%.1f' % hours_played, entry[2], entry[3], entry[4],
                                   pie_chart_data])
        counter += 1

    return [minutes_played_new, readout, counter, '%.1f' % total_hours]


# Return list of Steam profile stat pages for each game
def get_two_weeks_stats_page(games_list, steamid, two_weeks):
    if two_weeks == 'privacy':
        return ''
    else:
        urls = []
        for game in games_list:
            img_url = game[3]
            end_point = img_url.rfind('/')
            appid = img_url[64:end_point]
            stats_url = 'http://steamcommunity.com/profiles/%s/stats/%s' % (steamid, appid)
            urls.append(stats_url)

        return urls


# Appending stat page URLs to the two_weeks list (not provided by API)
def append_2weeks_stat_pages(two_weeks_stats_pages, two_weeks):
    if two_weeks == 'privacy':
        return
    else:
        index = 0
        for entry in two_weeks[0]:
            list(entry).append(two_weeks_stats_pages[index])
            index += 1


# Return list of games with 0 hours
def hall_of_shame(data):
    shame = []
    for game in data['response']['games']:
        if game['playtime_forever'] == 0:
            appid = game['appid']
            game_hash = game['img_logo_url']
            image_url = 'http://media.steampowered.com/steamcommunity/public/images/apps/%s/%s.jpg' % \
                        (appid, game_hash)
            store_page = 'http://store.steampowered.com/app/%s/' % appid
            shame.append([game['name'], game['playtime_forever'], image_url, store_page])
            random.shuffle(shame)
    return [shame, len(shame)]


# Little bit of code to generate a random hex color
def random_color():
    r = lambda: random.randint(0, 255)
    color = '#%02X%02X%02X' % (r(), r(), r())
    return color


# Function to format data for Charts.js display
def format_data(data_list, chart_type):
    if chart_type == 'donut':
        datasets = ''
        colors = []
        counter = 0
        for value in data_list:
            color = random_color()
            dataset = '{ value: %s, color: "%s", highlight: "#3FADFB", label: "%s"},' % \
                      (value[2], color, value[1])
            datasets += dataset
            counter += 1
            colors.append(color)
        formatted_data = '[%s]' % datasets[:-1]
        return formatted_data, colors

    else:
        chart_data = ''
        chart_labels = ''
        for value in data_list:
            chart_data += '%s,' % (value[2])
            chart_labels += '"%s",' % value[1]
        chart_data = chart_data[:-1]
        chart_labels = chart_labels[:-1]

        formatted_data = '{labels: [%s], datasets: [{ fillColor: "%s", strokeColor: ' \
                         '"rgba(220,220,220,0.8)", highlightFill: "#3FADFB", highlightStroke: ' \
                         '"rgba(220,220,220,1)", data: [%s]}]}' % \
                         (chart_labels, random_color(), chart_data)
        return formatted_data


# Grab input SteamID's friends list, pull out name, profile URL, and avatar
def get_friends(steamid):
    try:
        friends = []
        data = requests.get('%s?key=%s&steamid=%s&format=json' % (API_FRIENDS, API_KEY, steamid)).json()
        for entry in data['friendslist']['friends']:
            friends.append(entry['steamid'])

        # Use grouper to split into sublists because the web API only accepts 100 friends at a time
        full_friends_list = grouper(100, friends)

        friends_new = []

        for item in full_friends_list:
            item_list = list(item)
            friends_string = ','.join(item_list)
            data = requests.get('%s?key=%s&steamids=%s' % (API_PLAYER, API_KEY, friends_string)).json()
            for entry in data['response']['players']:
                steamid = entry['steamid']
                name = entry['personaname']
                avatar = entry['avatarmedium']
                friends_new.append([steamid, name, avatar])

        return [friends_new, len(friends_new)]
    except KeyError:
        print('get_friends has returned private')
        return 'private'


# Function to pull out stats for Statistics page
def statistics(all_data, two_weeks, shame):
    avg_list = []
    least_played = []
    for game in all_data[0]:
        if game[0] == 1 or game[2] == '0.0':
            continue
        else:
            avg_list.append(float(game[2]))
            least_played.append(game)
    # Will get a divide by zero error if no games in avg_list
    if not avg_list:
        avg_game_time = 0
    else:
        avg_game_time = sum(avg_list) / float(len(avg_list))

    total_games_all = len(all_data[0])

    total_hours_all = 0.0
    for game in all_data[0]:
        total_hours_all += float(game[2])

    if two_weeks == 'privacy':
        total_hours_2weeks = 'N/A'
        most_played_current = ['N/A', 'N/A', 'N/A', 'N/A']
        least_played_current = ['N/A', 'N/A', 'N/A', 'N/A']
    else:
        total_hours_2weeks = 0.0
        for game in two_weeks[0]:
            total_hours_2weeks += float(game[2])
        most_played_current = [two_weeks[0][0][1], two_weeks[0][0][2], two_weeks[0][0][3], two_weeks[0][0][5]]
        least_played_current = [two_weeks[0][-1][1], two_weeks[0][-1][2], two_weeks[0][-1][3], two_weeks[0][-1][5]]

    total_games_unplayed = len(shame)
    most_played = [all_data[0][0][1], all_data[0][0][2], all_data[0][0][3], all_data[0][0][5]]

    # Handling edge case of a user only having 1 game
    if least_played:
        least_played = [least_played[-1][1], least_played[-1][2], least_played[-1][3], least_played[-1][5]]
    else:
        least_played = ['N/A', 'N/A', 'N/A', 'N/A']

    colors = [random_color(), random_color(), random_color(), random_color()]
    dataset1 = '[{ value: %s, color: "%s", highlight: "#3FADFB", label: "%s"}, ' \
               '{ value: %s, color: "%s", highlight: "#3FADFB", label: "%s"}]' % \
               (total_games_all - total_games_unplayed, colors[0], 'Played Games', total_games_unplayed, colors[1],
               'Unplayed Games')

    dataset2 = '[{ value: %s, color: "%s", highlight: "#3FADFB", label: "%s"}, ' \
               '{ value: %s, color: "%s", highlight: "#3FADFB", label: "%s"}]' % \
               (most_played[1], colors[2], '%s' % most_played[0],
                total_hours_all, colors[3], 'Total Hours')

    pie_data = [[dataset1, dataset2], colors]
    unplayed_percent = (float(total_games_unplayed) / float(total_games_all)) * 100
    breakdown = hours_breakdown(all_data)

    stats = {
        'avg_game_time': '%.1f' % avg_game_time,
        'total_games_all': total_games_all,
        'total_hours_all': total_hours_all,
        'total_hours_2weeks': str(total_hours_2weeks),
        'total_games_unplayed': total_games_unplayed,
        'most_played': most_played,
        'least_played': least_played,
        'most_played_current': most_played_current,
        'least_played_current': least_played_current,
        'unplayed_percent': '%.0f' % unplayed_percent,
        'breakdown': breakdown
    }

    return [stats, pie_data]


# Function to return 'distinctions' - sort of like badges
def get_distinctions(all_data, two_weeks, stats):
    nerd_alert = []
    super_nerd_alert = []
    hyper_nerd_alert = []
    # Parsing 'all' data and filling in 'nerd alert' lists
    for entry in all_data[0]:
        if float(entry[2]) >= 500.0:
            hyper_nerd_alert.append([entry[3], entry[5]])
        elif 500.0 > float(entry[2]) >= 100.0:
            super_nerd_alert.append([entry[3], entry[5]])
        elif 100.0 > float(entry[2]) >= 50.0:
            nerd_alert.append([entry[3], entry[5]])
    if float(stats[0]['unplayed_percent']) <= 20.0:
        completionist = '%s' % stats[0]['unplayed_percent']
    else:
        completionist = ''
    if float(stats[0]['avg_game_time']) >= 10.0:
        dedication = '%s' % stats[0]['avg_game_time']
    else:
        dedication = ''

    if two_weeks != 'privacy':
        if two_weeks[2] >= 4:
            diverse = '%s' % two_weeks[2]
            focused = ''
        elif two_weeks[2] == 1:
            diverse = ''
            focused = '%s' % two_weeks[2]
        else:
            diverse = ''
            focused = ''
    else:
        diverse = ''
        focused = ''

    # Returning an empty dictionary if no distinctions, so it is not rendered in template
    if not nerd_alert:
        if not super_nerd_alert:
            if not hyper_nerd_alert:
                if not completionist:
                    if not dedication:
                        if not diverse:
                            if not focused:
                                distinctions = {}
                                return distinctions

    distinctions = {
        'nerd_alert': nerd_alert,
        'super_nerd_alert': super_nerd_alert,
        'hyper_nerd_alert': hyper_nerd_alert,
        'completionist': completionist,
        'dedication': dedication,
        'diverse': diverse,
        'focused': focused
    }

    return distinctions


# Additional function to parse out games with > 10 hours, etc
def hours_breakdown(all_data):
    less_than_5 = 0
    five_and_ten = 0
    ten_and_twenty = 0
    twenty_and_fifty = 0
    fifty_and_hundred = 0
    more_than_hundred = 0
    for entry in all_data[0]:
        if 0.0 < float(entry[2]) <= 5.0:
            less_than_5 += 1
        elif 5.0 < float(entry[2]) <= 10.0:
            five_and_ten += 1
        elif 10.0 < float(entry[2]) <= 20.0:
            ten_and_twenty += 1
        elif 20.0 < float(entry[2]) <= 50.0:
            twenty_and_fifty += 1
        elif 50.0 < float(entry[2]) <= 100.0:
            fifty_and_hundred += 1
        elif 100.0 < float(entry[2]):
            more_than_hundred += 1

    labels = ['0.1 - 5 hours', '5 - 10 hours', '10 - 20 hours', '20 - 50 hours', '50 - 100 hours',
              '100+ hours']
    data = [less_than_5, five_and_ten, ten_and_twenty, twenty_and_fifty, fifty_and_hundred, more_than_hundred]
    chart_data = '{labels: %s, datasets: [{ fillColor: "%s", strokeColor: "#FFFFFF", ' \
                 'highlightFill: "#3FADFB", highlightStroke: "rgba(220,220,220,1)", data: %s}]}' % \
                 (labels, random_color(), data)

    breakdown = {
        'less_than_5': less_than_5,
        'five_and_ten': five_and_ten,
        'ten_and_twenty': ten_and_twenty,
        'twenty_and_fifty': twenty_and_fifty,
        'fifty_and_hundred': fifty_and_hundred,
        'more_than_hundred': more_than_hundred,
        'chart_data': chart_data
    }

    return breakdown


# Grabbing user images
def get_user_images(steam_id):
    url_string = '%s?key=%s&steamids=%s&format=json&include_appinfo=1' % (API_PLAYER, API_KEY, steam_id)
    data = requests.get(url_string).json()
    user_image = data['response']['players'][0]['avatarfull']
    user_image_icon = data['response']['players'][0]['avatar']
    return [user_image, user_image_icon]

API_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
API_2_WEEKS = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/'
API_URL_STEAMID = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
API_PLAYER = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
API_FRIENDS = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
API_KEY = get_steam_api_key()
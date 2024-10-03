import json
import requests
import re
import time

import schedule

from eventcollectorselenium import find_events_for_private_page
from timeconverter import parse_date
 
facebook_links = json.loads(requests.get("https://budapestgayguide-backend.onrender.com/getvenuesfacebook").text)
##facebook_links = json.loads(requests.get("http://localhost:8080/getvenuesfacebook").text)



headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def find_events_of_venue_in_response_lines(key, trimmed_response_lines, facebook_link):
    results = []
    def _decode_dict(a_dict):
        try:
            results.append(a_dict[key])
        except KeyError:
            pass
        return a_dict
    json.loads(trimmed_response_lines, object_hook=_decode_dict)
    for venue in results:
        for event in venue:
            event['node']['node']['event_creator']['name']=facebook_link
            if event["node"]["node"]["event_place"] == None:
                event["node"]["node"]["event_place"] = {'__typename': 'FreeformPlace', 'contextual_name': facebook_link, 'location': {'reverse_geocode': {'city': 'Budapest'}}}
    return results


def get_event_list_from_facebook_response_lines(facebook_links, key):
    event_list = []
    isPublic = True
    for link in facebook_links:
        response = ""
        if link["facebook"] == 'https://www.facebook.com/magnumsauna/' or link["facebook"] == 'https://www.facebook.com/szauna69/':
            response = find_events_for_private_page(link["facebook"])
        else:
            response = requests.get(link["facebook"] + 'upcoming_hosted_events', headers=headers).text
        response_lines = []
        for line in response.splitlines():
            if '"__typename":"Event"' in line:
                response_lines.append(line)
        if response_lines != []:
            trimmed_response_lines = trim_response_lines(response_lines, key)
            events_of_venue = find_events_of_venue_in_response_lines(key, trimmed_response_lines,link["facebook"] )
            event_list.extend(events_of_venue)
    return event_list


def trim_response_lines(response_lines, key):
        trimmed_response_lines = re.sub(r'^.*?{', '{', response_lines[0])
        trimmed_response_lines = trimmed_response_lines[:trimmed_response_lines.rfind('</script>')]
        return trimmed_response_lines

def find_venue_id_for_event(facebook_link):
        for item in facebook_links:
            if item['facebook'] == facebook_link:
                return str(item['id'])
        return None

def create_event_details(event_list):
    event_details = []
    for venue in event_list:
        for event in venue:
            new_event = {}
            if event["node"]["node"]["event_place"]["location"] == None or event["node"]["node"]["event_place"]["location"]['reverse_geocode']["city"] == "Budapest":
                new_event["name"] = event["node"]["node"]["name"]
                new_event["url"] = event["node"]["node"]["url"]
                new_event["id"] = event["node"]["node"]["id"]
                new_event["venue_id"] = find_venue_id_for_event(event['node']['node']['event_creator']['name'])
                new_event["location"] = event["node"]["node"]["event_place"]["contextual_name"]
                new_event['time'] = str(parse_date(event["node"]["node"]['day_time_sentence']))
                event_details.append(new_event)
    return event_details


def get_all_events_from_facebook(facebook_links, key):
    event_list = get_event_list_from_facebook_response_lines(facebook_links, key)
    event_details = create_event_details(event_list)
    return event_details
            

def main():
    try:
        print('start')
        events = get_all_events_from_facebook(facebook_links, 'edges')
        ##url = "http://localhost:8080/saveevents"
        url = "https://budapestgayguide-backend.onrender.com/saveevents"
        x = requests.post(url, json=events)
        print(events)
        print(x)
    except Exception as e:
        print(f"An error occurred: {e}")
    

schedule.every().hour.do(main)
    

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
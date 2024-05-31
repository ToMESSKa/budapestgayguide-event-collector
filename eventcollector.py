import json
import requests
import re
 

facebook_links = json.loads(requests.get("http://localhost:8080/getvenuesfacebook").text)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def find_events_of_venue_in_response_lines(key, trimmed_response_lines):
    results = []
    def _decode_dict(a_dict):
        try:
            results.append(a_dict[key])
        except KeyError:
            pass
        return a_dict
    json.loads(trimmed_response_lines, object_hook=_decode_dict)
    return results


def get_event_list_from_facebook_response_lines(facebook_links, key):
    event_list = []
    for link in facebook_links:
        response = requests.get(link["facebook"] + 'upcoming_hosted_events', headers=headers)
        response_lines = []
        for line in response.text.splitlines():
            if '"__typename":"Event"' in line:
                response_lines.append(line)
        if response_lines != []:
            trimmed_response_lines = trim_response_lines(response_lines, key)
            events_of_venue = find_events_of_venue_in_response_lines(key, trimmed_response_lines)
            event_list.extend(events_of_venue)
    return event_list


def trim_response_lines(response_lines, key):
        trimmed_response_lines = re.sub(r'^.*?{', '{', response_lines[0])
        trimmed_response_lines = trimmed_response_lines[:trimmed_response_lines.rfind('</script>')]
        return trimmed_response_lines

def create_event_details(event_list):
    event_details = []
    for venue in event_list:
        for event in venue:
            new_event = {}
            if event["node"]["node"]["event_place"]["location"]['reverse_geocode']["city"] == "Budapest":
                new_event["name"] = event["node"]["node"]["name"]
                new_event["url"] = event["node"]["node"]["url"]
                new_event["id"] = event["node"]["node"]["id"]
                new_event["event_creator"] = event["node"]["node"]["event_creator"]["name"]
                new_event["location"] = event["node"]["node"]["event_place"]["contextual_name"]
                new_event['time'] = event["node"]["node"]['day_time_sentence']
                event_details.append(new_event)
    return event_details


def get_all_events_from_facebook(facebook_links, key):
    event_list = get_event_list_from_facebook_response_lines(facebook_links, key)
    event_details = create_event_details(event_list)
    print(event_details)
    return event_details
            
get_all_events_from_facebook(facebook_links, 'edges')
exit(0)
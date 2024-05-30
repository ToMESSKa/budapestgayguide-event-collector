import json
import requests
import re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
response = requests.get('https://www.facebook.com/garconsbudapest/events', headers=headers)

event_lines = []
for line in response.text.splitlines():
    if '"__typename":"Event"' in line:
        event_lines.append(line)

output_str = re.sub(r'^.*?{', '{', event_lines[0])
output_str = output_str[:output_str.rfind('</script>')]
# print(output_str)

event_data = json.loads(output_str)
res = [val['name'] for key, val in event_data.items() if "name" in val]
print(res)
# json.dumps(event_data, indent=4)

# print(event_data["require"])
exit(0)
import json, random, datetime

# Load your full list
with open('links.json', 'r') as f:
    all_links = json.load(f)

# Pick 3 random ones
# We use the date as a seed so it only changes once a day
random.seed(datetime.date.today().toordinal())
selection = random.sample(all_links, min(len(all_links), 3))

# Build the XML
items = ""
for item in selection:
    items += f"""
    <item>
      <title>{item['title']}</title>
      <link>{item['url']}</link>
      <guid>{item['url']}-{datetime.date.today()}</guid>
    </item>"""

feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"><channel>
  <title>Daily Nostalgia</title>
  {items}
</channel></rss>"""

with open('feed.xml', 'w') as f:
    f.write(feed)

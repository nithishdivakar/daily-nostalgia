import json
import random
import datetime
import email.utils

# --- CONFIGURATION ---
INPUT_FILE = 'links.json'
OUTPUT_FILE = 'feed.xml'
BATCH_SIZE = 17  # How many articles to resurface daily

def generate_rss():
    # 1. Load your link collection
    try:
        with open(INPUT_FILE, 'r') as f:
            all_links = json.load(f)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Create it with a list of {{'title': '...', 'url': '...'}} objects.")
        return
    except json.JSONDecodeError:
        print(f"Error: {INPUT_FILE} is not a valid JSON file.")
        return

    # 2. Setup Dates
    # Today's date for the random seed and display
    today_obj = datetime.date.today()
    date_display = today_obj.strftime("%b %d, %Y")
    
    # Exact RFC 822 format: Thu, 30 Apr 2026 14:52:36 GMT
    rfc_date = email.utils.formatdate(usegmt=True)

    # 3. Deterministic Randomization
    # We use the date's ordinal as a seed so the selection is "random" 
    # but stays the same for the entire calendar day.
    random.seed(today_obj.toordinal())
    
    # Ensure we don't try to sample more links than we actually have
    sample_size = min(len(all_links), BATCH_SIZE)
    selection = random.sample(all_links, sample_size)

    # 4. Construct the XML items
    items_xml = ""
    for item in selection:
        title = item.get('title', 'Untitled Article')
        url = item.get('url', '#')
        
        # We append the date to the title so it looks fresh in your reader
        display_title = f"{title}"
        
        # We use url + date for the GUID so the same article 
        # is treated as "new" if it reappears months later.
        guid = f"{url}-{today_obj.isoformat()}"
        
        items_xml += f"""
    <item>
      <title>{display_title}</title>
      <link>{url}</link>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{rfc_date}</pubDate>
      <description>Resurfaced from your archives on {date_display}.</description>
    </item>"""

    # 5. Build the full RSS shell
    full_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Nostalgia Feed</title>
  <link>https://github.com/nithishdivakar/daily-nostalgia</link>
  <description>Daily random articles from my archives</description>
  <language>en-us</language>
  <lastBuildDate>{rfc_date}</lastBuildDate>
  {items_xml}
</channel>
</rss>"""

    # 6. Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_feed.strip())

    print(f"Successfully generated {OUTPUT_FILE} with {sample_size} articles for {date_display}.")

if __name__ == "__main__":
    generate_rss()

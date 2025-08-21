import feedparser
from datetime import datetime
import xml.etree.ElementTree as ET

# List of RSS feed URLs from trusted Canadian news sources
rss_feeds = [
    "https://www.cbc.ca/cmlink/rss-topstories",
    "https://www.citynews.ca/feed/",
    "https://www.iphoneincanada.ca/feed/",
    "https://www.thewirereport.ca/feed/",
    "https://www.thecanadianpress.com/feed/"
]

# Keywords to filter relevant telecom news
keywords = ["Rogers", "Bell", "Telus", "CRTC", "telecom", "broadband", "wireless", "5G", "internet"]

# Function to check if any keyword is in the title or summary
def is_relevant(entry):
    content = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
    return any(keyword.lower() in content for keyword in keywords)

# Parse all feeds and collect relevant entries
relevant_items = []
for url in rss_feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        if is_relevant(entry):
            relevant_items.append({
                "title": entry.get("title", "No Title"),
                "link": entry.get("link", ""),
                "description": entry.get("summary", ""),
                "pubDate": entry.get("published", datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"))
            })

# Create the RSS XML structure
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Canadian Telecom News Feed"
ET.SubElement(channel, "link").text = "https://yourusername.github.io/telecom_news_feed.xml"
ET.SubElement(channel, "description").text = "Latest news about Rogers, Bell, Telus, CRTC, and telecom trends in Canada"
ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# Add items to the channel
for item in relevant_items:
    item_elem = ET.SubElement(channel, "item")
    ET.SubElement(item_elem, "title").text = item["title"]
    ET.SubElement(item_elem, "link").text = item["link"]
    ET.SubElement(item_elem, "description").text = item["description"]
    ET.SubElement(item_elem, "pubDate").text = item["pubDate"]

# Write the XML to file
tree = ET.ElementTree(rss)
tree.write("telecom_news_feed.xml", encoding="utf-8", xml_declaration=True)

print(f"RSS feed updated with {len(relevant_items)} items.")

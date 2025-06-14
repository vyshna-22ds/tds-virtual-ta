import json
import os
import requests
import time
from datetime import datetime
from requests.exceptions import ConnectionError, Timeout

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 4, 14)
CATEGORY_ID = 34  # TDS-KB category
OUTPUT_FILE = "discourse_data.json"
BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

# Load auth token from auth.json saved by Playwright
def get_auth_cookie():
    if not os.path.exists("auth.json"):
        print("❌ auth.json not found. Please run save_auth.py first.")
        return None
    with open("auth.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    cookies = data.get("cookies", [])
    cookie_header = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
    return cookie_header

def fetch_topics(auth_cookie):
    headers = {
        "Cookie": auth_cookie,
        "User-Agent": "Mozilla/5.0"
    }
    page = 0
    all_topics = []

    while True:
        print(f"📂 Fetching topic list page {page}")
        url = f"{BASE_URL}/c/courses/tds-kb/{CATEGORY_ID}.json?page={page}"
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                print(f"⚠️ Failed to fetch page {page}: {resp.status_code}")
                break

            topic_list = resp.json().get("topic_list", {}).get("topics", [])
            if not topic_list:
                break

            for topic in topic_list:
                try:
                    try:
                        created_at = datetime.strptime(topic["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    except ValueError:
                        created_at = datetime.strptime(topic["created_at"], "%Y-%m-%dT%H:%M:%SZ")

                    print(f"🗓️ Topic {topic['id']} created at {created_at}")

                    if START_DATE <= created_at <= END_DATE:
                        all_topics.append(topic)
                    elif created_at < START_DATE:
                        continue  # Don't stop; keep scanning all pages
                except Exception as e:
                    print(f"⚠️ Skipping topic {topic['id']} due to date parse error: {e}")

            page += 1
            time.sleep(1)
        except (ConnectionError, Timeout) as e:
            print(f"❌ Error fetching topic list page {page}: {e}")
            break

    return all_topics

def fetch_topic_details(topic_ids, auth_cookie):
    headers = {
        "Cookie": auth_cookie,
        "User-Agent": "Mozilla/5.0"
    }
    results = []
    for idx, topic in enumerate(topic_ids):
        url = f"{BASE_URL}/t/{topic['id']}.json"
        print(f"🔗 Fetching topic {idx+1}/{len(topic_ids)}: {url}")

        for attempt in range(3):  # Retry up to 3 times
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code != 200:
                    print(f"⚠️ Failed to fetch topic {topic['id']}: {resp.status_code}")
                    break
                topic_data = resp.json()
                thread_text = ""
                for post in topic_data.get("post_stream", {}).get("posts", []):
                    thread_text += post.get("cooked", "") + "\n---\n"
                results.append({
                    "id": topic["id"],
                    "title": topic["title"],
                    "url": f"{BASE_URL}/t/{topic['slug']}/{topic['id']}",
                    "content": thread_text.strip()
                })
                time.sleep(1)
                break  # Exit retry loop
            except (ConnectionError, Timeout) as e:
                print(f"🔁 Attempt {attempt+1}/3 failed for topic {topic['id']}: {e}")
                time.sleep(2)

    return results

def main():
    auth_cookie = get_auth_cookie()
    if not auth_cookie:
        return

    topics = fetch_topics(auth_cookie)
    print(f"✅ Found {len(topics)} topics in range.")
    details = fetch_topic_details(topics, auth_cookie)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(details)} topics to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
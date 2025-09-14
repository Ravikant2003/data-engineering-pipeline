import requests
from bs4 import BeautifulSoup
import json
import time
import csv
import random
from urllib.parse import urljoin, urlparse
import re

class JobScraper:
    def __init__(self):
        self.jobs_data = []
        self.session = requests.Session()
        # Rotate user agents to avoid detection
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]

    def get_headers(self):
        """Get random headers to avoid detection"""
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    def scrape_github_jobs(self, count=30):
        """Scrape job-related content from GitHub job repositories and discussions"""
        print("Scraping GitHub job-related content...")
        search_queries = [
            "job+description+software+engineer",
            "interview+questions+programming",
            "resume+template+developer",
            "hiring+process+tech"
        ]
        
        for query in search_queries:
            try:
                url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=10"
                response = self.session.get(url, headers=self.get_headers())
                if response.status_code == 200:
                    data = response.json()
                    for repo in data.get('items', []):
                        self.jobs_data.append({
                            "source": "GitHub",
                            "title": repo['name'],
                            "company": repo['owner']['login'],
                            "description": repo.get('description', ''),
                            "type": "repository"
                        })
                time.sleep(2)
            except Exception as e:
                print(f"Error with query {query}: {e}")
                continue

    def scrape_stackoverflow_jobs(self, count=30):
        """Scrape job-related questions from StackOverflow"""
        print("Scraping StackOverflow job-related content...")
        tags = ["career", "job", "interview", "resume", "hiring"]
        for tag in tags:
            try:
                url = f"https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged={tag}&site=stackoverflow&pagesize=10"
                response = self.session.get(url, headers=self.get_headers())
                if response.status_code == 200:
                    data = response.json()
                    for question in data.get('items', []):
                        self.jobs_data.append({
                            "source": "StackOverflow",
                            "title": question['title'],
                            "company": "Community",
                            "description": question.get('body', ''),
                            "type": "question",
                            "score": question.get('score', 0)
                        })
                time.sleep(2)
            except Exception as e:
                print(f"Error with tag {tag}: {e}")
                continue

    def scrape_reddit_jobs(self, count=30):
        """Scrape job-related posts from Reddit"""
        print("Scraping Reddit job-related content...")
        subreddits = ["cscareerquestions", "jobs", "programming", "ITCareerQuestions"]
        for subreddit in subreddits:
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
                headers = self.get_headers()
                headers["User-Agent"] = "JobScraper/1.0"
                response = self.session.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    for post in data['data']['children']:
                        post_data = post['data']
                        self.jobs_data.append({
                            "source": "Reddit",
                            "title": post_data['title'],
                            "company": f"r/{subreddit}",
                            "description": post_data.get('selftext', ''),
                            "type": "discussion",
                            "score": post_data.get('score', 0)
                        })
                time.sleep(3)
            except Exception as e:
                print(f"Error with subreddit {subreddit}: {e}")
                continue

    def scrape_hackernews_jobs(self, count=30):
        """Scrape job-related posts from Hacker News"""
        print("Scraping Hacker News job-related content...")
        try:
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = self.session.get(url, headers=self.get_headers())
            if response.status_code == 200:
                story_ids = response.json()[:50]
                for story_id in story_ids[:count]:
                    try:
                        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                        story_response = self.session.get(story_url, headers=self.get_headers())
                        if story_response.status_code == 200:
                            story = story_response.json()
                            title = story.get('title', '')
                            job_keywords = ['job', 'hiring', 'career', 'interview', 'resume', 'developer', 'engineer', 'programmer']
                            if any(keyword.lower() in title.lower() for keyword in job_keywords):
                                self.jobs_data.append({
                                    "source": "HackerNews",
                                    "title": title,
                                    "company": story.get('by', 'Anonymous'),
                                    "description": story.get('text', ''),
                                    "type": "story",
                                    "score": story.get('score', 0)
                                })
                        time.sleep(1)
                    except Exception:
                        continue
        except Exception as e:
            print(f"Error scraping HackerNews: {e}")

    def scrape_all(self, total_count=60):
        """Main scraping method that tries multiple sources"""
        print(f"Starting to scrape {total_count} job-related entries...")
        try:
            self.scrape_github_jobs(count=15)
            time.sleep(2)
            self.scrape_stackoverflow_jobs(count=15)
            time.sleep(2)
            self.scrape_reddit_jobs(count=15)
            time.sleep(2)
            self.scrape_hackernews_jobs(count=15)
        except Exception as e:
            print(f"Error during scraping: {e}")
        print(f"Total collected: {len(self.jobs_data)} job-related entries")

    def save_raw_data(self, filename="data/raw_jobs.json"):
        """Save raw scraped data to JSON and CSV"""
        import os
        os.makedirs("data", exist_ok=True)
        normalized_data = []
        all_fields = set()
        for entry in self.jobs_data:
            all_fields.update(entry.keys())
        for entry in self.jobs_data:
            normalized_entry = {field: entry.get(field, "") for field in all_fields}
            normalized_data.append(normalized_entry)
        self.jobs_data = normalized_data

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.jobs_data, f, indent=2, ensure_ascii=False)

        csv_filename = filename.replace('.json', '.csv')
        with open(csv_filename, "w", newline='', encoding="utf-8") as f:
            if self.jobs_data:
                fieldnames = sorted(all_fields)
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.jobs_data)

        print(f"Saved {len(self.jobs_data)} entries to {filename} and {csv_filename}")
        return len(self.jobs_data)

if __name__ == "__main__":
    scraper = JobScraper()
    scraper.scrape_all(total_count=60)
    scraper.save_raw_data()

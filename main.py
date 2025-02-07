import feedparser
import requests
from openai import OpenAI
from datetime import datetime, timedelta

def get_research_papers(topic):
    base_url = "http://export.arxiv.org/api/query?"
    query = f"all:{topic}"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": 5,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    try:
        response = requests.get(base_url, params=params)
        feed = feedparser.parse(response.content)
        papers = []
        
        for entry in feed.entries:
            paper = {
                "title": entry.title,
                "authors": [author.name for author in entry.authors],
                "published": entry.published,
                "summary": entry.summary,
                "link": entry.link
            }
            papers.append(paper)
            
        return papers[:5]
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return []

def get_news(topic):
    url = f"https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(url)
        feed = feedparser.parse(response.content)
        news_items = []
        
        for entry in feed.entries[:5]:
            news_item = {
                "title": entry.title,
                "source": entry.source.title,
                "link": entry.link,
                "published": entry.published
            }
            news_items.append(news_item)
            
        return news_items
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
    
def generate_summary(text, context):
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a research assistant. {context}"},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Summary unavailable: {str(e)}"

def process_query(topic):
    papers = get_research_papers(topic)
    paper_content = "\n\n".join(
        [f"Title: {p['title']}\nSummary: {p['summary']}" for p in papers]
    )
    paper_summary = generate_summary(
        paper_content,
        "Summarize the key findings and technologies from these research papers:"
    )
    
    news = get_news(topic)
    news_content = "\n\n".join(
        [f"Headline: {n['title']}\nSource: {n['source']}" for n in news]
    )
    news_summary = generate_summary(
        news_content,
        "Summarize these news articles into key developments:"
    )
    
    return {
        "topic": topic,
        "papers": papers,
        "paper_summary": paper_summary,
        "news": news,
        "news_summary": news_summary
    }
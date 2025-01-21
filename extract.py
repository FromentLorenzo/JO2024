import requests
import sys
import time

# Define the API key and base URL for fetching articles
API_KEY = "76fc9f14-6eea-413b-a56b-d04bd3b49452"
BASE_URL = "https://content.guardianapis.com/search"

# Function to get articles based on sport
def get_articles(sport):
    # Parameters for the API request
    params = {
        "from-date": "2024-07-12",
        "to-date": "2024-08-11",
        "q": f"olympic AND {sport}",
        "page-size": 10,  # Get the 10 most relevant articles
        "order-by": "relevance",  # Sort by relevance
        "api-key": API_KEY,
        "show-fields": "webTitle,webUrl,sectionName,webPublicationDate"  # Include necessary fields
    }
    
    # Send the GET request to fetch articles
    response = requests.get(BASE_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.json().get("response", {}).get("results", []))
        return response.json().get("response", {}).get("results", [])
    else:
        print(f"Error fetching articles: {response.status_code} - {response.text}")
        return []

# Function to get the content of a specific article
def get_article_content(article_url):
    # Make the request to fetch the article content
    article_params = {
        "api-key": API_KEY,
        "show-fields": "body"  # Include full content (body)
    }
    response = requests.get(article_url, params=article_params)

    # Check if the request was successful
    if response.status_code == 200:
        article_data = response.json()
        return article_data['response']['content']['fields']['body']
    else:
        print(f"Error fetching article content: {response.status_code} - {response.text}")
        return None

# Main function to extract articles and process the content
def main(sport):
    # Get the top 10 relevant articles for the specified sport
    articles = get_articles(sport)

    # Process each article
    for article in articles:
        title = article.get("webTitle", "No Title")
        article_id = article["id"]
        article_url = f"https://content.guardianapis.com/{article_id}"
        print(f"Processing article: {title} ({article_url})")

        # Get the full content of the article
        content = get_article_content(article_url)

        if content:
            # Call the extract_links function with the article's content
            extract_triplets(content)

def extract_triplets(content):
    print(content)##PLACEHOLDER

# Example usage: The sport name will be passed as a command-line argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a sport as a parameter.")
        sys.exit(1)

    sport = sys.argv[1]  # Get the sport from the command-line argument
    main(sport)

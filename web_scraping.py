import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.bbc.com/business'
headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic a real browser
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('div', {'data-testid': 'card-text-wrapper'})

    data = []
    for article in articles:
        title = article.find('h2', {'data-testid': 'card-headline'})
        description = article.find('p', {'data-testid': 'card-description'})
        tag = article.find('span', {'data-testid': 'card-metadata-tag'})
        time = article.find('span', {'data-testid': 'card-metadata-lastupdated'})

        if title and description and tag and time:
            data.append({
                'Headline': title.text.strip(),
                'Description': description.text.strip(),
                'TagLine': tag.text.strip(),
                'LastUpdated': time.text.strip(),

            })


    # Create DataFrame and export
    df = pd.DataFrame(data)
    df.to_excel('bbc_news_headlines.xlsx', index=False)
    print("Data has been successfully exported to 'bbc_news_headlines.xlsx'")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

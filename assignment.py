import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the URLs DataFrame
urls_df = pd.read_excel(r"/home/eswar/python/ds/dataextractin/Input.xlsx", engine="openpyxl")

# Iterate through the first 100 rows (or fewer if the DataFrame has fewer rows)
for i in range(min(115, len(urls_df))):
    # Extract URL_ID and URL for each row
    url_id_name = urls_df.iloc[i]['URL_ID']
    url_to_request = urls_df.iloc[i]['URL']

    # Sending a GET request to the URL
    response = requests.get(url_to_request)

    # Check the status of the request and handle the response
    if response.status_code == 200:
        # Request was successful, parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the article title
        article_title = soup.find('h1').text if soup.find('h1') else "Title not found"

        # Extracting the article content within <p> (paragraph) elements
        paragraphs = soup.find_all('p')
        article_content = '\n'.join(paragraph.get_text() for paragraph in paragraphs)

        # Generate the filename using URL_ID
        filename = f"{url_id_name}"

        # Save the extracted data into a text file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Article Title: {str(article_title)}\n\n")
            file.write(f"Article Content:\n{str(article_content)}")

        print(f"Article data saved to {filename}")
    else:
        # Request encountered an error
        print(f"Request for URL {url_to_request} failed with status code:", response.status_code)

# Import Splinter and BeautifulSoup & Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set up Splinter (troubleshooting: chromedriver is in Python library)
browser = Browser('chrome', headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
#img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
#img_url


# # ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
#df

df.to_html()

# # ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# for loop to click link

for i in range(0,4):
    hemispheres_dict = {}
    
    #Find link and click
    hem_image = browser.find_by_css('img[class="thumb"]')[i]
    hem_image.click()
    
    #Parse HTML
    html = browser.html
    hem_image_soup = soup(html, 'html.parser')
    hem_lists = hem_image_soup.find('ul')
    hem_item = hem_lists.find('li')
    hem_image_link = hem_item.find('a')['href']
    final_link = f'https://marshemispheres.com/{hem_image_link}'
    hem_title = hem_image_soup.find('h2', class_='title').text
    browser.back()
    
    #Add title and link to dict
    hemispheres_dict["image_url"] = final_link
    hemispheres_dict["title"] = hem_title
    
    #Add dictionary to list
    hemisphere_image_urls.append(hemispheres_dict)

# 5. Quit the browser
browser.quit()


# Import Splinter and BeautifulSoup & Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Initialize browser, creates data dict, end WebDriver and return scraped data
def scrape_all():
    #Initiate headless driver for deployment   
    browser = Browser('chrome', 'executable_path', headless=True) 

    #Set our news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere": hemispheres(browser)
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data

# ### News Title and Paragraph
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handeling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ### Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# # ### Hemispheres
def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles
    hemisphere_image_urls = []

    try:
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

    except BaseException:
        return None   

    #Add title and link to dict
    hemispheres_dict["image_url"] = final_link
    hemispheres_dict["title"] = hem_title
            
    #Add dictionary to list
    hemisphere_image_urls.append(hemispheres_dict)
    
    return hemisphere_image_urls    

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())
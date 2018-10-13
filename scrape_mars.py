
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import shutil
import time



       


# In[2]:


def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
      
# create mars-data dict that we can insert into mongo
    marsdata = {}
    
# visit https://mars.nasa.gov/news/
    url='https://mars.nasa.gov/news/' 
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    news_titles = soup.find_all('div', class_='content_title')
    news_ps = soup.find_all('div', class_='article_teaser_body')
    # last news title
    titles=[]
    for news in news_titles:
        title=news.find("a").text
        titles.append(title)
        last_news=titles[0]
    # last news paraghragh
    paraghraph=[]
    for p in news_ps:
        par=p.text
        paraghraph.append(par)
        last_news_p=paraghraph[0]
# add our last news and last paraghraph to to Marse_data 
    marsdata["news_title"] = last_news
    marsdata["news_p"] = last_news_p
    
#Mars Featured large size Image
# visit https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

    Feature_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(Feature_url)
# navigate by soliter to site 
    links_found = browser.find_link_by_partial_text("FULL IMAGE")
    links_found.click()
    time.sleep(10)
    links_found = browser.find_link_by_partial_text("more info")
    links_found.click()
    browser.is_element_present_by_css("img", wait_time=1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    url_image= soup.find("img" , class_="main_image")["src"]
    if "httss://www.jpl.nasa.gov:" not in url_image:url_image= "https://www.jpl.nasa.gov"+url_image
#add image url in Mars_data dic
    marsdata["featured_image_url"] = url_image 
    
# print large picture 
    # response = requests.get(featured_image_url, stream=True)
    # with open('img.png', 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)
    
    # from IPython.display import Image
    # Image(url='img.png')
    
#Mars Weather
#visit https://twitter.com/MarsWxReport?lang=en
    twitter_url = 'https://twitter.com/MarsWxReport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)
    html=browser.html
    weather_soup=BeautifulSoup(html,'html.parser')
    results=weather_soup.find_all('div', class_='js-tweet-text-container')
    weather_list=[]
    for item in results:
        weather=item.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
        if "daylight" in weather:
            weather_list.append(weather)
    mars_weather=weather_list[0]
# adding last twitt in Mars data dict 
    marsdata["mars_weather"] = mars_weather 
    
    
#Mars Fact
# visit http://space-facts.com/mars/ explor data with pandas
    fact_url='http://space-facts.com/mars/'
#scraping data from url wiyh pandas data frame
    tables = pd.read_html(fact_url)
# convert first table to dataframe
    df = tables[0]
    df.columns = [' ','Value']
#remove data frame index from html table and justify table 

    mars_facts_html = df.to_html(na_rep = " ", classes="table table-sm table-striped", justify="left", col_space=0,index=False)
    mars_facts_html.replace('\n', '')
    
# save filr directly as html
    df.to_html('Fact.html')
    marsdata["Mars_facts"] = mars_facts_html
    
#Mars Hemispheres
    Hemispheres_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(Hemispheres_url)
    links = ['Cerberus', 'Schiaparelli', 'Syrtis' , 'Valles']
    hemisphere_image_urls=[]
# use for loop to get data for image url and titles and added to list .    
    for link in links:
        hemisphere_image_urls_dic={}
        link_click = browser.find_link_by_partial_text(link)
        link_click.click()
        time.sleep(10)
# browser.is_element_present_by_css("img.wide-image", wait_time=10)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_url=soup.find("a", text="Sample").get("href")
        title=soup.find("h2",class_="title").text
       # if "https://astrogeology.usgs.gov:" not in image_url: image_url = "https://astrogeology.usgs.gov"+image_url
        hemisphere_image_urls_dic['title'] = title
        hemisphere_image_urls_dic['image_url']=image_url
        hemisphere_image_urls.append(hemisphere_image_urls_dic)
        browser.back()
    marsdata["hemisphere_title_urls"] = hemisphere_image_urls     
    browser.quit()
    return marsdata



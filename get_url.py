from selenium import webdriver
from selenium.webdriver.common.by import By

def get_cat_urls():
    url = 'https://shopee.vn/'
    driver = webdriver.Chrome()
    driver.get(url)
    #sleep
    driver.implicitly_wait(2)
    
    urls = []
    list_cat = driver.find_elements(By.CSS_SELECTOR, 'li.image-carousel__item')
    for cat in list_cat:
        # catcol = cat.find_element(By.CSS_SELECTOR, 'div.home-category-list__group')
        list_catcol_item = cat.find_elements(By.CSS_SELECTOR, 'a.home-category-list__category-grid')
        for catcol_item_link in list_catcol_item:
            urls.append(catcol_item_link.get_attribute('href'))
    driver.quit()
    # save to file
    with open('cat_urls.txt', 'w') as f:
        for url in urls:
            f.write(str(url))
            f.write('\n')
    return urls

def get_full_urls():
    # load cat urls from file
    with open('cat_urls.txt', 'r') as f:
        urls = f.read().splitlines()

    driver = webdriver.Chrome()
    full_urls = []

    for url in urls:
        driver.get(url)
        driver.implicitly_wait(5)
        number_of_page = int(driver.find_element(By.CSS_SELECTOR, 'span.shopee-mini-page-controller__total').get_attribute('textContent'))
        print('Number of page: ', number_of_page)
        for i in range(1, number_of_page):
            print('Page: ', i, 'of', number_of_page)
            list_product = driver.find_elements(By.CSS_SELECTOR, 'div.col-xs-2-4.shopee-search-item-result__item')
            for product in list_product:
                try:
                    #scroll to element
                    driver.execute_script("arguments[0].scrollIntoView();", product)
                    url = product.find_element(By.CSS_SELECTOR, 'a')
                    full_urls.append(url.get_attribute('href'))
                except:
                    pass
            # next page
            driver.find_element(By.CSS_SELECTOR, 'button.shopee-button-outline.shopee-mini-page-controller__next-btn').click()

    driver.quit()
    print(len(full_urls))
    print('Done get full urls')
    # save to file
    with open('urls.txt', 'w') as f:
        for url in full_urls:
            f.write(str(url))
            f.write('\n')
    print('Done save to file')

if __name__ == '__main__':
    print(get_full_urls())
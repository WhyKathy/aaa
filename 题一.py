import pandas as pd
import numpy as np
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# 将货币转换列表放到一个csv里面不用每次都爬取
def currency_conversion():
    print('driver准备加载....')
    options = uc.ChromeOptions()
    chrome = uc.Chrome(executable_path=r'E:\6 实习\笔试\chromedriver.exe', options=options)
    print('driver已加载....')
    url = 'https://www.11meigui.com/tools/currency'
    chrome.get(url=url)
    currency_english = []
    currency_chinese = []
    for i in range(5):
        table_path = f'/html/body/main/div/table/tbody/tr[2]/td/table[{i+1}]'
        table = chrome.find_element(By.XPATH, table_path)
        table_list = table.find_elements(By.TAG_NAME, 'tr')
        for list in table_list[2:]:
            tdlist = list.find_elements(By.TAG_NAME,'td')
            currency_english.append(tdlist[4].text)
            currency_chinese.append(tdlist[1].text)
    df = pd.DataFrame({'英文代码':currency_english, '中文货币':currency_chinese})
    df.set_index(['英文代码'],inplace=True)
    df.loc['HKD'] = '港币'
    df.loc['FRF'] = '法国法郎'
    df.loc['DEM'] = '德国马克'
    df.loc['JPY'] = '日元'
    df.loc['CAD'] = '加拿大元'
    df.loc['THP'] = '泰国铢'
    df.loc['RM'] = '林吉特'
    df.loc['NTD'] = '新台币'
    df.loc['ESP'] = '西班牙比塞塔'
    df.loc['ITL'] = '意大利里拉'
    df.loc['INR'] = '印度卢比'
    df.loc['IDR'] = '印尼卢比'
    df.loc['ZAR'] = '南非兰特'
    df = df.reset_index()
    df.to_csv('result.txt', index=False)

def exchange_rate(currency_search):
    print('driver准备加载....')
    options = uc.ChromeOptions()
    chrome = uc.Chrome(executable_path=r'E:\6 实习\笔试\chromedriver.exe', options=options)
    print('driver已加载....')
    url = 'https://www.boc.cn/sourcedb/whpj/'
    chrome.get(url=url)
    # 选择货币
    currency = chrome.find_element(By.ID, 'pjname').click()
    sleep(1)
    s = Select(chrome.find_element(By.ID, 'pjname'))
    s.select_by_visible_text(currency_search)
    sleep(1)
    chrome.find_element(By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input').click()
    sleep(1)
    # 获取价格
    path = f"//html/body/div[1]/div[4]/table/tbody/tr/td[contains(text(), '{date}')]"
    result = chrome.find_element(By.XPATH, path+'//preceding-sibling::td[3]')
    return result.text


if __name__ == "__main__":
    # 获取货币转换列表
    # currency_conversion()
    df = pd.read_csv('result.txt')
    df.set_index(['英文代码'],inplace=True)

    x = input('请输入日期、货币代号并以空格隔开：').split(' ')
    date = x[0]
    date = date[0:4] + '.' +date[4:6]+'.'+date[6:]
    currency_search = x[1].upper()

    # 输出现汇卖出价
    while(1):
        if currency_search.encode('utf-8').isalpha():
            try:
                price = exchange_rate(df.loc[currency_search,'中文货币'])
                print(price)
                break
            except Exception as e:
                currency = input('名称错误，请重新输入(1)：').upper()
        else:
            try:
                price = exchange_rate(currency_search)
                print(price)
                break
            except Exception as e:
                currency = input('名称错误，请重新输入(2)：').upper()

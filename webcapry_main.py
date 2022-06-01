#!/usr/bin/python
# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import g_calendar

debug = False
username = ''
password = ''
target_url = ''

####當專案代號還有在可使用時間內，就會強制(作業內容必須選取)不能自行書寫，work_class_sop是定好依所選作業類別會對應的作業內容

def work_class_sop(class_name):
    if class_name == '休假含輪休':
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/span/span[1]').click() 
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/ul/li[10]/span/span[1]').click() 
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/ul/li[10]/ul/li[1]/span/span[2]').click()
        browser.find_element_by_xpath('//*[@id="btnSelectProjectItemClose"]').click()
    elif class_name == '叫修服務/拆移機' or class_name == '檔案處理' or class_name == '測試':
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/span/span[1]').click() 
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/ul/li[1]/span/span[1]').click() 
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/ul/li[1]/ul/li[5]/span/span[2]').click()
        browser.find_element_by_xpath('//*[@id="btnSelectProjectItemClose"]').click()
    elif class_name == '資料研讀' or class_name == '上課(內部)' or class_name == '上課(產品)':
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[2]/ul/li/ul/li[1]/span/span[1]').click()
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[2]/ul/li/ul/li[1]/ul/li/span/span[2]').click()
        browser.find_element_by_xpath('//*[@id="btnSelectProjectItemClose"]').click()
    elif class_name == '會議(例行會議)':
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/span/span[1]').click() 
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/ul/li[6]/span/span[1]').click()
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/ul/li/ul/li[1]/ul/li[6]/ul/li[7]/span/span[2]').click()
        browser.find_element_by_xpath('//*[@id="btnSelectProjectItemClose"]').click()

browser = webdriver.Firefox()
browser.accept_untrusted_certs = True
browser.get(target_url)
time.sleep(5)
action = ActionChains(browser)

#### 登入MyNote 系統
selectLang = Select(browser.find_element_by_xpath('//*[@id="CultureCbl"]'))
selectLang.select_by_value('zh-TW')

password_input = browser.find_element_by_xpath('//*[@id="UserPasswordTxt"]')
#iframe = browser.find_elements_by_tag_name("iframe")[0]
password_input.click()
password_input.send_keys(password)

username_input = browser.find_element_by_xpath('//*[@id="UserIdTxt"]')
username_input.click()
username_input.send_keys(username)

confirm = browser.find_element_by_xpath('//*[@id="ConfirmIBtn"]')
action.move_to_element(confirm).perform()
confirm.click()

time.sleep(2)
#### 登入MyNote 系統

#### 點選MyNote 連結
my_note_link = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[6]/table/tbody/tr/td[2]/a')))
my_note_link.click()

time.sleep(2)
#### 點選MyNote 連結


#### 切換到操作區iframe
iframe = browser.find_elements_by_tag_name("iframe")[0]
browser.switch_to.frame(iframe)
#### 切換到操作區iframe

cal_events = g_calendar.events()
cal_rows = g_calendar.get_cal_week_info_by_day(cal_events)


#### 一周有七天 
for i in range(7): 
    weeks = browser.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/ul/li')
    note_day = weeks[i].find_element_by_xpath('./div/div').text
    if len(note_day) < 2:
        note_day = "0" + note_day
    #### debug special day
    if debug:
        if note_day == '30':
           pass
        else:
            continue

    work_condition = weeks[i].get_attribute('class')
    if work_condition == 'day':  #### 檢查是否為工作日
        note_input_list = g_calendar.get_one_row_data(cal_rows, note_day)
        if note_input_list == None:
            continue
        weeks[i].click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="btnPrj_td2_0"]').click() #專案選取按鈕
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="swse03projectID"]').click()
        browser.find_element_by_xpath('//*[@id="swse03projectID"]').send_keys(note_input_list[1])
        browser.find_element_by_xpath('//*[@id="swse02btnProjectSelectDBQuery"]').click()
        time.sleep(2)
        row_confirm = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/div[2]/table/tbody/tr')
        browser.execute_script("arguments[0].click()", row_confirm)
        browser.find_element_by_xpath('//*[@id="swse02btnProjectSelectDBOk"]').click()
        time.sleep(1)
        work_class = Select(browser.find_element_by_xpath('//*[@id="td3_0"]'))
        work_class.select_by_visible_text(note_input_list[5])  #### 填入作業類別

        work_context_btn = browser.find_element_by_xpath('//*[@id="btnOpt_td4_0"]')  #### 尋找作業類別按鈕
        
        if work_context_btn.is_displayed():  #### 檢查是否有作業內容選項在畫面上
            browser.find_element_by_xpath('//*[@id="btnOpt_td4_0"]').click()
            time.sleep(1)
            work_class_sop(note_input_list[5])
        else: 
            browser.find_element_by_xpath('//*[@id="td4_0"]').click()
        time.sleep(1)

        #### 作業時間填入
        browser.find_element_by_xpath('//*[@id="td5_0"]').clear()
        browser.find_element_by_xpath('//*[@id="td5_0"]').send_keys('08')
        browser.find_element_by_xpath('//*[@id="td6_0"]').clear()
        browser.find_element_by_xpath('//*[@id="td6_0"]').send_keys('30')
        browser.find_element_by_xpath('//*[@id="td7_0"]').clear()
        browser.find_element_by_xpath('//*[@id="td7_0"]').send_keys('17')
        browser.find_element_by_xpath('//*[@id="td8_0"]').clear()
        browser.find_element_by_xpath('//*[@id="td8_0"]').send_keys('30')
        browser.find_element_by_xpath('//*[@id="td12_0"]').send_keys(note_input_list[3])
        browser.find_element_by_xpath('//*[@id="dailySaveA"]').click()
        #### 作業時間填入

#### 在作業完成後將結果存成PNG檔作佐證資料

browser.save_screenshot(g_calendar.get_current_date() + ".png")


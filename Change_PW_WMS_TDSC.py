from selenium import webdriver 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pytesseract
from PIL import Image
import time
import datetime
import pandas as pd
import os
import traceback



url = "" #URL WMS LINK
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'
user_pw_file = r'C:\\Users\\aphisit.sen\\Desktop\\user_list.xlsx'
warehouse = 'D004' #warehouse ID to uesed


try:
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)
    yesterday =  str(yesterday) 

    if warehouse == 'D004':
        wh = str(2)
    else:
        wh = str(3)

    
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    
    str1 = driver.capabilities['browserVersion']
    str2 = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    print(str1)
    print(str2)
    print(str1[0:3])
    print(str2[0:3])
    if str1[0:3] != str2[0:3]: 
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "details-button"))).click() 
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "proceed-link"))).click() 
    #แคป capthca
    img = driver.find_element(By.XPATH,"//img[@id='checknumImg']")
    time.sleep(3)
    src = img.screenshot("C:\\report\\captcha.png")               
    #แปลง captcha เป็น String
    image = Image.open("C:\\report\\captcha.png")
    th1 = image
    captcha = pytesseract.image_to_string(th1, config='--psm 7 --oem 1 outputbase digits') 
    captcha = captcha.replace(" ", "").strip()
    loop = True

    len_cap = len(captcha) #เอาไว้เช็คจำนวนหน่วยของแคปชา
    print("this is len ",len_cap)
     

    while loop:
        try:            
            if captcha == "" or len_cap <= 3:
                print(" ")
                print(" ")
                print("*** The captcha could not be found !!!. Please try running the program again ***")
                print(" ")
                print(" ")
                time.sleep(1)
                driver.quit()
                #ให้ loop พาออกจาก login ซ้ำๆครับ
                loop = False
                os._exit(1)          
            elif captcha != "" and len_cap >= 4:        
                print(" ")
                print(" ")
                print("Captcha is found")             
                print("Captcha: ",captcha)
                print(" ")
                print(" ")
                username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "CURUSERID")))
                username.clear()
                username.send_keys("USER11")
                password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "CURURPD")))
                password.clear()
                password.send_keys("*Wms1234567")
                #ส่งข้อมูล Captcha ครับ
                captcha_img= driver.find_element(By.ID, 'CHECKNUM')
                captcha_img.send_keys(captcha)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit"))).click()               
                time.sleep(1)
                try:
                    check_force_login = driver.find_element(By.XPATH,'//*[@id="forceLoginContainer"]/div/div[4]/input[1]')
                    if check_force_login.is_displayed():
                        print("Force Login found")
                        check_force_login.click()
                        print("Force Login Click")
                        break
                except NoSuchElementException:
                    pass

                time.sleep(1)
                print("looking for archive")
                try:
                    wh_select_archieve = driver.find_element(By.CLASS_NAME, "wh_select_archieve")
                    print("Archive found")
                except NoSuchElementException:
                    print("Archive not found")
                    pass

                time.sleep(1)
                print("looking for WH")
                try:
                    wh_select = driver.find_element(By.CLASS_NAME,'wh_select')
                except NoSuchElementException:
                    pass
                
                if wh_select.is_displayed():
                    print("WH found")
                    break
            else:
                print("Exit loop login")
                break
            time.sleep(3)
            
        except:
            print('Timeout')

    time.sleep(1)
    try:
        wh_select = driver.find_element(By.CLASS_NAME,'wh_select')
        if wh_select.is_displayed():
            print("WH found")
            # //*[@id="selectButton"]
            WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="selectButton"]'))).click()
            time.sleep(1)
            #Select Warehouse
            WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="selectdiv"]/div[' + wh + ']'))).click()
            WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'confirmBtn'))).click()
            print('Successful Login')
    except NoSuchElementException:
        try:
            wh_select = driver.find_element(By.CLASS_NAME,'wh_achieve')
            if wh_select.is_displayed():
                print("WH found")
                # //*[@id="selectButton"]
                WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="selectButton"]'))).click()
                time.sleep(1)
                #Select Warehouse
                WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="selectdiv"]/div[' + wh + ']'))).click()
                WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'confirmBtn'))).click()
                print('Successful Login')
        except NoSuchElementException:
            pass
        pass
   
    time.sleep(10)
    main_menu_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-menu")))
    main_menu_button.click()
    time.sleep(1)
    menu_search = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fuzzySearchKey"]/span[2]/div/input[1]')))
    menu_search.click()
    time.sleep(1)
    menu_search.send_keys('User Management')
    menu_search.send_keys(u'\ue007')
    time.sleep(1.5)
    #pin menu
    pin_menu = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[24]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/span[2]")))
    pin_menu.click()
    print('Start Read Excel file')
    df = pd.read_excel(user_pw_file, engine='openpyxl', dtype='str')
    df.reset_index(drop=True,inplace=True)
    print(df)
    success_df = pd.DataFrame(columns =['User_ID','reason'])
    error_df = pd.DataFrame(columns =['User_ID','reason'])
    print(df)
    
    for index in df.index:
        user = str(df.iloc[index,0])
        pw = str(df.iloc[index,1])
        print(user)
        print(pw)
        time.sleep(0.5)
        menu_user_management = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[24]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[1]/span/input')))
        menu_user_management.click()
        time.sleep(0.5)
        menu_user_management.clear()
        menu_user_management.send_keys(user)
        menu_user_management.send_keys(u'\ue007')
        time.sleep(0.5)
        try:
            action = ActionChains(driver)
            action.move_to_element(driver.find_element(By.XPATH,('//*[@id="tbody_myGridNav"]/table/tbody/tr[2]'))).perform()
            action.context_click().perform()
            time.sleep(0.5)
            action.move_to_element(driver.find_element(By.XPATH,('/html/body/div[3]/div[2]/table/tbody/tr[7]/td[2]/div'))).perform()
            time.sleep(0.25)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/table/tbody/tr[7]/td[2]/div'))).click()
            time.sleep(0.5)
            #input new password
            new_pw = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[24]/div[2]/div[2]/div/div[2]/div[2]/div[8]/div[3]/div/div/div/div/div[2]/div/div/div/form/div/div/div[1]/div[2]/input')))
            new_pw.click()
            new_pw.send_keys(pw)
            #confirm new password
            new_pw_cf = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[24]/div[2]/div[2]/div/div[2]/div[2]/div[8]/div[3]/div/div/div/div/div[2]/div/div/div/form/div/div/div[2]/div[2]/input')))
            new_pw_cf.click()
            new_pw_cf.send_keys(pw)
            
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[24]/div[2]/div[2]/div/div[2]/div[2]/div[8]/div[3]/div/div/div/div/div[4]/div/div/a[2]'))).click()
            time.sleep(0.5)
    

            try:
                check_pw_error = driver.find_element(By.XPATH,"/html/body/div[24]/div[2]/div[2]/div/div[2]/div[2]/div[10]/div[3]/button")
                if check_pw_error.is_displayed():
                    print("!! Change Password Error !!")
                    row_to_append = pd.DataFrame([{'User_ID':user,'reason':'Old password'}])
                    error_df = pd.concat([error_df,row_to_append])
                    check_pw_error.click()
                    time.sleep(0.25)
                    new_pw_cancle = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[24]/div[2]/div[2]/div/div[2]/div[2]/div[8]/div[3]/div/div/div/div/div[4]/div/div/a[1]')))
                    new_pw_cancle.click()
                    new_pw_cancle = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[24]/div[2]/div[2]/div/div[2]/div[2]/div[8]/div[1]/div[3]/div[5]')))
                    new_pw_cancle.click()
   
            except NoSuchElementException:
                print("Password Change Success")
                row_to_append = pd.DataFrame([{'User_ID':user,'reason':'Success'}])
                success_df = pd.concat([success_df,row_to_append])
                pass
        except NoSuchElementException: 
            print("!! Cannot find user!!")
            row_to_append = pd.DataFrame([{'User_ID':user,'reason':'Error'}])
            error_df = pd.concat([error_df,row_to_append])
            pass
        
        
    if error_df.empty:
        print('Error DataFrame is empty!')
    else:
        print(error_df)
        error_df.to_excel('C:\\Users\\nutthawut.aur\\Desktop\\error_list' + '.xlsx', index = False)

    if success_df.empty:
        print('Success DataFrame is empty!')
    else:
        print(success_df)
        success_df.to_excel('C:\\Users\\nutthawut.aur\\Desktop\\success_list' + '.xlsx', index = False)   
    
    driver.close()
    # Closes the current window
    driver.quit()


    print('DONE')
except Exception as e:
    print(traceback.format_exc())
    f = open('change_password.txt', 'w')
    f.write('An exceptional thing happed - %s' % e)
    f.close()

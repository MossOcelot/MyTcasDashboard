import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get(f"https://course.mytcas.com/universities")
time.sleep(3)

data = {
    'university': '',
    'details': [

    ]
}

g_i = 0
g_j = 0

def get_detail():
    try:
        # หาค่า <dl> ทั้งหมดในหน้า
        dl_elements = driver.find_elements(By.TAG_NAME, 'dl')
        
        details = []
        for dl in dl_elements:
            print("Found <dl> element:")
            
            # หาค่า <dt> และ <dd> ภายใน <dl>
            dt_elements = dl.find_elements(By.TAG_NAME, 'dt')
            dd_elements = dl.find_elements(By.TAG_NAME, 'dd')
            
            # ดึงข้อความจาก <dt>
            for dt in dt_elements:
                details.append([dt.text])
                print("Term:", dt.text)
            
            # ดึงข้อความจาก <dd>

            for i, dd in enumerate(dd_elements):
                details[i].append(dd.text)
                print("Description:", dd.text)
        data['details'][g_i]['course'][g_j]['details_course'].append(details)
    except Exception as e:
        print(f"Error: {e}")

    

    

def get_course():
    global g_j
    ul_element = driver.find_element(By.XPATH, '//*[@id="root"]/main/div[2]/ul')
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

    # ตรวจสอบจำนวน <li>
    num_li = len(li_elements)
    print(f"num: {num_li}")
    for i in range(num_li):
        g_j = i
        ul_element = driver.find_element(By.XPATH, '//*[@id="root"]/main/div[2]/ul')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        
        a_tag = li_elements[i].find_element(By.TAG_NAME, 'a')
        # print course
        data['details'][g_i]['course'].append({'course_name': a_tag.get_attribute('textContent'), 'details_course': []})
        print(a_tag.get_attribute('textContent'))

        driver.execute_script("arguments[0].scrollIntoView();", a_tag)
        try:
            a_tag.click()
            
        except selenium.common.exceptions.ElementClickInterceptedException:
            # ถ้าคลิกไม่ได้ ให้ใช้ JavaScript ในการคลิกธาตุ
            driver.execute_script("arguments[0].click();", a_tag)
        time.sleep(1)
        get_detail()
        driver.back()
        

def get_major_engineering():
    global g_i

    ul_element = driver.find_element(By.XPATH, '//*[@id="root"]/main/div[2]/ul')
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

    # ตรวจสอบจำนวน <li>
    num_li = len(li_elements)
    print(f"num: {num_li}")
    for i in range(num_li):
        g_i = i
        ul_element = driver.find_element(By.XPATH, '//*[@id="root"]/main/div[2]/ul')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

        a_tag = li_elements[i].find_element(By.TAG_NAME, 'a')
        # print major
        data['details'].append({"major": a_tag.get_attribute('textContent'), "course": []})
        print(a_tag.get_attribute('textContent'))
        
        driver.execute_script("arguments[0].scrollIntoView();", a_tag)
        try:
            a_tag.click()
            
        except selenium.common.exceptions.ElementClickInterceptedException:
            # ถ้าคลิกไม่ได้ ให้ใช้ JavaScript ในการคลิกธาตุ
            driver.execute_script("arguments[0].click();", a_tag)
        time.sleep(1)
        get_course()
        driver.back()
        

def get_faculty_university():
    ul_element = driver.find_element(By.XPATH, '//*[@id="root"]/main/div[2]/ul')

    # ค้นหา <li> ภายใน <ul>
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

    # ตรวจสอบจำนวน <li>
    num_li = len(li_elements)
    print(f"num: {num_li}")
    for i, li in enumerate(li_elements):
        a_tag = li.find_element(By.TAG_NAME, 'a')
        if "คณะวิศวกรรมศาสตร์" in a_tag.get_attribute('textContent'):
            print("Found:", a_tag.get_attribute('textContent'))

            # เลื่อนหน้าจอไปที่ธาตุ
            driver.execute_script("arguments[0].scrollIntoView();", a_tag)

            # ลองคลิกธาตุด้วยวิธีปกติ
            try:
                a_tag.click()
                
            except selenium.common.exceptions.ElementClickInterceptedException:
                # ถ้าคลิกไม่ได้ ให้ใช้ JavaScript ในการคลิกธาตุ
                driver.execute_script("arguments[0].click();", a_tag)
            time.sleep(1)
            get_major_engineering()
            time.sleep(5)
            driver.back()
            break
    else:
        print("Element not found1")

def get_university():
    global data, g_i, g_j

    for i in range(80):
        # print(i)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="root"]/main/div[2]/ul/li[{i + 1}]/a'))
            )

            driver.execute_script("arguments[0].scrollIntoView();", element)

            try:
                element.click()
                
            except selenium.common.exceptions.ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", element)
            
            time.sleep(1)
            print("Name:", end=" ")
            name_uni_element = driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/div[2]/h1/span/span/a')
            # University name
            data['university'] = name_uni_element.text

            print(name_uni_element.text)
            get_faculty_university()
            print("------------------")
            # print("data: ", data)
            json_string = json.dumps(data, indent=4, ensure_ascii=False)
            print(json_string)
            with open(f'data{i}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("------------------")
            data = {
                'university': '',
                'details': [

                ]
            }

            g_i = 0
            g_j = 0 
            
            time.sleep(2)
            driver.back()
        except selenium.common.exceptions.NoSuchElementException:
            print(f"Element {i + 1} not found")
        except Exception as e:
            print(e)

def start():
    get_university()

if __name__ == "__main__":
    start()
    driver.quit()

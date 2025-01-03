import re
import requests
import threading
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

fp_config = "config.ini"

def read_config(fp):
    global login_URL, elective_URL, detail_URL, select_URL

    with open(fp, 'r', encoding="utf-8") as f:
        if f: 
            f = f.read()
        else:
            print("[!] 请检查config.ini文件是否存在")
            exit()

        login_URL = re.search("login_URL = (.*)", f).group(1) 
        elective_URL = re.search("elective_URL = (.*)", f).group(1)
        detail_URL = re.search("detail_URL = (.*)", f).group(1)
        select_URL = re.search("select_URL = (.*)", f).group(1)

def open_browser(driver):
    # Goto course selection page
    driver.get(login_URL)
    
    # Detected thus login manually
    '''
    actions = webdriver.ActionChains(driver)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,'j_username')))
    actions.move_to_element(driver.find_element(By.NAME,'j_username')).click()
    for char in account:
        actions.send_keys(char)
        actions.perform()
        time.sleep(random.uniform(0.1,0.3))

    actions.move_to_element(driver.find_element(By.NAME,'j_password')).click()
    for char in password:
        actions.send_keys(char)
        actions.perform()
        time.sleep(random.uniform(0.1,0.3))

    time.sleep(random.uniform(0.1,0.3))
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="login_other"]/input'))).click()
    '''

    WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/dl/dt')))
    driver.get(elective_URL)

    if driver.current_url == elective_URL:
        print("[+] 成功登录选课系统")
    else:
        print("[!] 选课系统未开放, 退出脚本...")
        exit()

def get_keys(driver):
    global jsession, id_key

    for request in driver.requests:
        if not request.response:
            continue

        if request.response.headers['Set-Cookie']:
            if(request.response.headers['Set-Cookie'].find('JSESSIONID') != -1):
                jsession = re.search("JSESSIONID=(.*); Path=/mis;", request.response.headers['Set-Cookie']).group(1)
            if(request.response.headers['Set-Cookie'].find('session_id_key2') != -1):
                id_key = re.search("session_id_key2=(.*);", request.response.headers['Set-Cookie']).group(1)

def get_elecType(driver):
    # Get electiveTypeId 
    with open(fp_config, 'a', encoding="utf-8")as f:
        for idx in range(1,100):
            try:
                type = driver.find_element(By.XPATH,f'/html/body/div[1]/div[2]/div/div/table/tbody/tr[{2*idx-1}]/th').text
                type_id = driver.find_element(By.XPATH,f'/html/body/div[1]/div[2]/div/div/table/tbody/tr[{2*idx}]/td/span/a').get_attribute("href")
                type_id = re.search("id=(.*)", type_id).group(1)

                f.write(f'{type}, {type_id}:\n\n')
            except:
                break

def get_sectId(driver):
    global type_section 
    type_section = dict()

    with open(fp_config,"r+", encoding="utf-8") as f:
        lines = f.readlines()

        for idx, line in enumerate(lines):
            type_id = re.search(', ([a-f0-9]{32}):',line)
            if not type_id:
                continue

            type_id = type_id.group(1)
            driver.get(f"{detail_URL}?id={type_id}") 
            WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div/div/table/thead/tr/th[2]')))

            for subline in lines[idx+1:]:
                section = re.search('([A-Za-z,\s]+ \(\d{4}\))',subline)
                if not section:
                    break
                                           
                section = section.group(1)
                for col in range(1,1000):
                    try:
                        match = driver.find_element(By.XPATH,f'/html/body/div[1]/div[2]/div/div/table/tbody/tr[{col}]/td[2]')
                    except:
                        break   
                    
                    if match.text.strip() == section.strip():
                        section_id = match.get_attribute("id")
                        type_section[type_id] = section_id 

                        print(f"    [-] 找到课程 <{section}> ID: {section_id}")
                        break

def select_section(type_id,section_id):
    
    cookies = {
        "JSESSIONID": jsession,
        "__security_cookie_session_id_key2": id_key
    }
    data = {
        "electiveTypeId" : type_id,
        "id" : section_id
    }
    headers = {
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Chromium";v="131", "Not_A',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://mis.uic.edu.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": f"https://mis.uic.edu.cn/mis/student/es/eleDetail.do?id={type_id}",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Priority": "u=0, i",
        "Connection": "keep-alive"
    }

    print(f"    [-] 正在选课 ID: {section_id}")
    while True:
        respond = requests.post(select_URL, cookies=cookies, data=data, headers=headers)
        if not respond: continue
        if respond.text.find("请勿重复选择") != -1:
            print(f"    [-] 选课成功 ID: {section_id}")
            break
        elif respond.text.find("冲突") != -1:
            print(f"    [-] 选课存在时间冲突 ID: {section_id}")
            break
        elif respond.text.find("满额") != -1:
            print(f"    [-] 课程人数已满 ID: {section_id}")
            break
        

def refresh(driver):
    while True:
        driver.get(elective_URL)
        get_keys(driver)
        time.sleep(3)

if __name__ == "__main__":
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=option)
    t_list = list()

    print("[+] 读取配置文件，请保证config.ini文件在同一目录下")
    read_config(fp_config)
    
    print("[+] 打开选课界面，请手动登录")
    open_browser(driver)

    if input("[+] 是否首次运行脚本？Y/N :").upper() == "Y":
        get_elecType(driver)
        print("[!] 请打开config.ini配置文件，填写选课信息")
        input("完成后按任意键继续...")

    print("[+] 获取选课ID中, 请勿关闭浏览器")  
    get_sectId(driver)
    print("[+] 选课ID获取完成")

    if input("[+] 请在选课开始后输入start开始选课: ").lower() == "start":
        get_keys(driver)
        t_list.append(threading.Thread(target=refresh, args=(driver,),daemon=True))

        for type_id, section_id in type_section.items():
            t_list.append(threading.Thread(target=select_section, args=(type_id,section_id,),daemon=True))

        print(f"[+] 总共启动 {len(t_list)-1} 个选课线程")     
        [t.start() for t in t_list]
        [t.join() for t in t_list]

    input("[+] 选课结束, 按任意键退出...")
            
            
            

        
        

    
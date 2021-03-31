from selenium import webdriver
import json
import time

driver = None

def read():

    login_data = list()

    with open(r'config.json',mode="r") as f:
        res = json.load(f)
    
    res = res["settings"]

    login_data.append(res['reserva_id'])
    login_data.append(res['reserva_pass'])
    login_data.append(res['webdriver_pass'])

    return login_data

def login():
    try:

        dat = read()

        global driver

        driver = webdriver.Chrome(dat[2])

        driver.get('https://id-sso.reserva.be/login/business')

        id_text = driver.find_element_by_id('adm_id')
        pass_text = driver.find_element_by_id('adm_pass')

        id_text.send_keys(dat[0])
        pass_text.send_keys(dat[1])

        btn = driver.find_element_by_xpath('//*[@id="mainform"]/div/input')
        btn.click()

    except Exception as e:
        print(e)
        driver.close()
        return


def get_today():
    try:
        res = list()
        global driver

        login()

        time.sleep(1)

        navigation = driver.find_element_by_xpath('/html/body/header/div[3]/div/div/ul/li[1]/a/span')
        navigation.click()

        time.sleep(1)

        get_cl = driver.find_element_by_xpath('/html/body/form/div/div[3]/div[2]/div[1]/h3/span[2]/a')
        get_cl.click()

        today = driver.find_element_by_xpath('/html/body/form/div/div[3]/div/div[2]/div[2]/div[1]')
        date = today.find_element_by_xpath('div/h4')
        date = date.text
        table = today.find_element_by_tag_name('table')
        tbody = table.find_element_by_tag_name('tbody')
        sched = tbody.find_elements_by_tag_name('tr')

        for s in sched:
            i = list()
            ev = s.find_element_by_xpath('td[@class="menu"]')
            people = s.find_element_by_xpath('td[@data-label="確定"]')
            i.append(ev.text)
            i.append(people.text)
            res.append(i)

        driver.close()
        return [date,res]
    except Exception as e:
        print(e)
        driver.close()
        return


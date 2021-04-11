from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from fpdf import FPDF
from datetime import date
from datetime import datetime
import os
import getpass

#Changes to be made by you

# Add your instagram username and password to authenticate
username = ''
password = ''
# Add whatsapp user's name to whom you need to send the pdf 
# if the contact is not saved, number can also be entered but check the exact format including spaces
whatsapp_name = ''

#Nothing required to be changed after this

def get_people():
    names = []
    sleep(2)
    scroll_box = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
    prev_height, height,j = 0, 1, 1
    while prev_height != height:
        prev_height = height
        sleep(3)
        for i in range(j,1000):
            try:
                name = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li['+str(i)+']/div/div[1]/div[2]/div[1]/span/a')
                try:
                    driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li['+str(i)+']/div/div[1]/div[2]/div[1]/div/span')
                except:
                    names.append(name.get_attribute('title'))
                j += 1
            except:
                break
        height = driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)
    driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
    return names
options = webdriver.ChromeOptions()
pc_name = getpass.getuser()
os.chdir('C:\\Users\\'+pc_name+'\\Downloads')
options.add_argument("user-data-dir=C:\\Users\\"+pc_name+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.add_argument('start-maximized')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

driver = webdriver.Chrome('D:\\df\\Zoom\\chromedriver',options = options)
driver.get("https://instagram.com")
try:
    sleep(5)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(username)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
    sleep(2)

    
    print('Enter your security code')
    x = input()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[1]/div/label/input').send_keys(x)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[2]/button').click()
    sleep(6)
except:
    pass
    
driver.get("https://www.instagram.com/"+username+"/")
sleep(3)

driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
followers = get_people()
print('My Followers')
print(followers)
print(len(followers))
print('')
print('')
print('')

sleep(1)
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
following = get_people()
print('I am following')
print(following)
print(len(following))
print('')
print('')
print('')

not_following_back = [i for i in following if i not in followers]
print('People who are not following me')
print(not_following_back)
print(len(not_following_back))
print('')
print('')
print('')
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 15)
pdf.cell(200,10,txt="People who are not following me",ln=1,align='C')
for i in not_following_back:
    pdf.cell(100,5,'https://www.instagram.com/'+i,ln = 1,align = 'L')

i_am_not = [i for i in followers if i not in following]
print('People whom I am not following')
print(i_am_not)
print(len(i_am_not))
print('')
print('')
print('')

pdf.add_page()
pdf.cell(200,10,txt="People I am not following",ln=1,align='C')
for i in i_am_not:
    pdf.cell(100,5,'https://www.instagram.com/'+i,ln = 1,align = 'L')

day,month,year = str(date.today().day),str(date.today().month),str(date.today().year)
date = day+'-'+month+'-'+year
time = datetime.now().strftime("%H:%M:%S")
pdf.output("instagram "+date+" "+time+".pdf")
driver.get("https://web.whatsapp.com")
while(1):
    try:
        driver.find_element_by_xpath('//span[@title = "{}"]'.format(whatsapp_name)).click()
        break
    except:
        continue
driver.find_element_by_xpath('//div[@title = "Attach"]').click()
driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys("C:\\Users\\"+pc_user+"\\Downloads\\instagram "+date+" "+time+".pdf")
while(1):
    try:
        driver.find_element_by_xpath('//span[@data-icon="send"]').click()
        break
    except:
        continue
sleep(5)

driver.close()

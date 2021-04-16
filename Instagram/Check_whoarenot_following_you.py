#These things has to be changed by the user


# Add your instagram username and password to authenticate
username = ''
password = ''
# Add whatsapp user's name to whom you need to send the pdf 
# Change flag to 1 if you don't want to get file through whatsapp
# if the contact is not saved, number can also be entered but check the exact format including spaces
whatsapp_name = ''
flag = 0
#You need not change anything beyond this

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from fpdf import FPDF
from datetime import date
from datetime import datetime
import os
import getpass

def add_page(text,list):
    pdf.add_page()
    pdf.cell(200,10,txt=text,ln=1,align='C')
    pdf.cell(200,10,str(len(list)),ln=1,align='C')
    for i in list:
        pdf.cell(100,5,'https://www.instagram.com/'+i,ln=1,align='L')
def get_people():
    names = []
    names1 = []
    sleep(2)
    scroll_box = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
    prev_height, height,j = 0, 1, 1
    while prev_height != height:
        prev_height = height
        sleep(1)
        for i in range(j,10000000000):
            try:
                name = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li['+str(i)+']/div/div[1]/div[2]/div[1]/span/a').get_attribute('title')
                try:
                    driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li['+str(i)+']/div/div[1]/div[2]/div[1]/div/span')
                    names1.append(name)
                except:
                    names.append(name)
                j += 1
            except:
                break
        height = driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)
    driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
    return names,names1
options = webdriver.ChromeOptions()
pc_name = getpass.getuser()
os.chdir('C:\\Users\\'+pc_name+'\\Downloads')
options.add_argument("user-data-dir=C:\\Users\\"+pc_name+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.add_argument('start-maximized')
options.add_experimental_option("excludeSwitches", ['enable-automation'])

driver = webdriver.Chrome(ChromeDriverManager().install(),options = options)
driver.get("https://instagram.com")
try:
    sleep(5)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(username)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
    sleep(3)
    try:
        a = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[1]/div/label/input')
        print('Enter your security code')
        x = input()
        a.send_keys(x)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[2]/button').click()
        sleep(6)
    except:
        pass
except:
    pass
    
driver.get("https://www.instagram.com/"+username+"/")
sleep(3)

driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
followers,celeb_followers = get_people()
print('My Followers')
print(followers)
print(len(followers))
print('Celebraties following me')
print(celeb_followers)
print(str(len(celeb_followers))+'\n\n\n')

sleep(1)
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
following,celeb_following = get_people()
print('I am following')
print(following)
print(len(following))
print('Celebraties I am following')
print(celeb_following)
print(str(len(celeb_following))+'\n\n\n')

not_following_back = [i for i in following if i not in followers]
print('People who are not following me')
print(not_following_back)
print(str(len(not_following_back))+'\n\n\n')
pdf = FPDF()
pdf.set_font("Arial", size = 15)
add_page("People who are not following me",not_following_back)

i_am_not = [i for i in followers if i not in following]
print('People whom I am not following')
print(i_am_not)
print(str(len(i_am_not))+'\n\n\n')
add_page("People I am not following",i_am_not)

pdf.add_page()
pdf.cell(200,10,txt="Celebraties I am following",ln=1,align='C')
pdf.cell(200,10,str(len(celeb_following)),ln=1,align='C')
for i in celeb_following:
    pdf.cell(100,5,'https://www.instagram.com/'+i,ln=1,align='L')
add_page("Celebraties following me",celeb_followers)
add_page("People following me",followers)
add_page("People I am following",following)

day,month,year = str(date.today().day),str(date.today().month),str(date.today().year)
date = day+'-'+month+'-'+year
time = datetime.now().strftime("%H-%M-%S")
pdf.output("instagram "+date+" "+time+".pdf")
if(flag):
    driver.close()
    quit()
driver.get("https://web.whatsapp.com")
while(1):
    try:
        driver.find_element_by_xpath('//span[@title = "{}"]'.format(whatsapp_name)).click()
        break
    except:
        continue
driver.find_element_by_xpath('//div[@title = "Attach"]').click()
driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys("C:\\Users\\"+pc_name+"\\Downloads\\instagram "+date+" "+time+".pdf")
while(1):
    try:
        driver.find_element_by_xpath('//span[@data-icon="send"]').click()
        break
    except:
        continue
sleep(5)

driver.close()

os.remove("C:\\Users\\"+pc_name+"\\Downloads\\instagram "+date+" "+time+".pdf")

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests, sys, re, os, time, random, schedule, datetime, json, subprocess, pickle
from colorama import Fore, Back, Style
from getpass import getpass
from plyer import notification

popup = notification.notify

r = Fore.RED
g = Fore.GREEN
w = Fore.WHITE
b = Fore.BLUE
y = Fore.YELLOW
m = Fore.MAGENTA
app_path = os.path.dirname(os.path.abspath(__file__))
# data login & jadwal
if not os.path.exists(os.path.join(app_path, "data.json")):
	print("ERROR: login.json not found! Fill in the data.json file.")
	defaultKeys = {
		"nim": "your_nim_here",
		"password": "your_password_here"
	}
	with open(os.path.join(app_path, "data.json"), 'w') as f:
		json.dump(defaultKeys, f)
	time.sleep(5)
	sys.exit(1)

with open(os.path.join(app_path, "data.json")) as f:
	config = json.load(f)

options = Options()
options.add_argument('--disable-extensions')

driver = webdriver.Chrome('E:\\tools\\chromedriver.exe', chrome_options=options)
sekarang = datetime.datetime.now()

portal = ("http://sima.usm.ac.id/app/")
presensi = ("http://sima.usm.ac.id/akademik/presensi_kuliah")

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
	resource_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	app_path = os.path.dirname(sys.executable)
	exec_path = sys.executable
else:
	app_path = os.path.dirname(os.path.abspath(__file__))
	exec_path = f"python \'{os.path.abspath(__file__)}\'"
	resource_path = app_path

V = '1.7'
def print_logo():
	clear = "\x1b[0m"
	colors = [36, 32, 34, 35, 31, 37]

	x = """
\t+------------------+
\t+                  +
\t+  SIMA BOT V.1.7  +
\t+  Made By NoXLaw  +
\t+   USM The Best   +
\t+                  +
\t+------------------+
"""
	for N, line in enumerate(x.split("\n")):
		sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
		time.sleep(0.05)
print_logo()

# Login
popup(
	app_name = f"SIMA BOT V.{V}",
	title = f"Starting...",
	message = f"Login to sima...",
	app_icon = "favicon.ico"
)
print(b + '    [' + w + '+' + b + '] ' + w + 'Login to sima with nim : ' + b + config['nim'])
try:
	driver.get("http://sima.usm.ac.id")
	cookies = pickle.load(open("cookies.pkl", "rb"))
	for cookie in cookies:
		driver.add_cookie(cookie)
	driver.find_element_by_id('username').send_keys(config['nim'])
	time.sleep(5)
	driver.find_element_by_id('email-id').send_keys(config['password'])
	submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class='mainBtn pull-right'][type='submit']")))
	submit.click()
	pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
except NoSuchElementException:
	exitOnErrorHandler(driver)
popup(
	app_name = f"SIMA BOT V.{V}",
	title = f"SIMA BOT V.{V} - Success",
	message = f"Success Login",
	app_icon = "favicon.ico"
)
print("\tSuccess")

try:
	driver.find_element_by_xpath("//div[@class='alert alert-danger']")
	print("Failed to login, please put your user and password in join.py")
	sys.exit(1)
except SystemExit:
	driver.quit()
	popup(
		app_name = f"SIMA BOT V.{V}",
		title = f"Error",
		message = f"Failed to login. Please input correct data in data.json and run the program again.",
		app_icon = "favicon.ico"
	)
	time.sleep(5)
	sys.exit(1)
except:
	pass

# test
SIA = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Sistem Informasi Akademik']")))
SIA.click()
time.sleep(5)
driver.get(presensi)
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
	driver.add_cookie(cookie)
time.sleep(10)
driver.get("http://sima.usm.ac.id/dashboard/app/")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
	driver.add_cookie(cookie)
time.sleep(5)
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
# time.sleep(10)
# driver.quit()
# print("\tWorkkkk")


# Schedule Page -> Get ongoing matkul
print("scraping schedules...")
try:
	driver.get("http://sima.usm.ac.id/akademik/jadwal_kuliah")
	for cookie in cookies:
		driver.add_cookie(cookie)
	pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
except:
	print("Login ulang...")
	time.sleep(5)
	popup(
		app_name = f"BOT SIMA V.{V}",
		title = f"BOT SIMA V.{V} - Login ulang",
		message = "Please run script again, because cannot scrap schedule in sima..",
		app_icon = "favicon.ico"
	)
	time.sleep(5)
	sys.exit(1)
	driver.quit()

# presensi
def joinPresensi():
	sima = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Sistem Informasi Akademik']")))
	sima.click()
	driver.get(presensi)
	for cookie in cookies:
		driver.add_cookie(cookie)
	time.sleep(70)
	matkul = re.findall(r'', presensi.text)
	print(b + '    [' + w + '+' + b + '] ' + w + '' + b + 'Nama mata kuliah yang akan di presensi: '+matkul)
	driver.find_element_by_xpath("").click()
	time.sleep(10)
	pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
	driver.get(portal)
	for cookie in cookies:
		driver.add_cookie(cookie)
	driver.find_element_by_xpath("//div[@class='alert alert-danger']")
	print("Login ulang...")
	pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
	sys.exit(1)
	time.sleep(3)
	driver.quit()

# jadwal
def monday():
	schedule.every().monday.at(config['senen1']).do(joinPresensi())
	schedule.every().monday.at(config['senen2']).do(joinPresensi())

def tuesday():
	schedule.every().tuesday.at(config['selasa1']).do(joinPresensi())

def wednesday():
	schedule.every().wednesday.at(config['rabu1']).do(joinPresensi())

def thursday():
	schedule.every().thursday.at(config['kamis1']).do(joinPresensi())

def friday():
	schedule.every().friday.at(config['jumat1']).do(joinPresensi())
	schedule.every().monday.at(config['jumat2']).do(joinPresensi())
	schedule.every().monday.at(config['jumat3']).do(joinPresensi())

day = (sekarang.strftime("%a"))
# print(day)

if day=="Mon":
	monday()
elif day=="Tue":
	tuesday()
elif day=="Wed":
	wednesday()
elif day=="Thu":
	thursday()
elif day=="Fri":
	friday()
else:
	print("\tHell Yeahh, Liburan :'v")

sys.exit(1)
driver.quit()
time.sleep(5)
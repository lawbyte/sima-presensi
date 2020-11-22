from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import sys
import re
import os
import time
import random
import schedule
import datetime
import json
import subprocess
import pickle
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

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
	resource_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	app_path = os.path.dirname(sys.executable)
	exec_path = sys.executable
	DRIVER_PATH = os.path.join(resource_path, "chromedriver.exe")
else:
	app_path = os.path.dirname(os.path.abspath(__file__))
	exec_path = f"python \'{os.path.abspath(__file__)}\'"
	resource_path = app_path
	DRIVER_PATH = os.path.join("drivers", "chromedriver.exe")

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

width = 1024
height = 768

option = Options()
# option.headless = True
option.add_argument('--disable-gpu')

driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=option)
driver.implicitly_wait(10)

portal = ("http://sima.usm.ac.id/app/")
presensi = ("http://sima.usm.ac.id/akademik/presensi_kuliah")
jadwal_kuliah = ("http://sima.usm.ac.id/akademik/jadwal_kuliah")

V = '1.9'
def print_logo():
	clear = "\x1b[0m"
	colors = [36, 32, 34, 35, 31, 37]

	x = """
\t\t+------------------+
\t\t+                  +
\t\t+  SIMA BOT V.1.9  +
\t\t+   USM The Best   +
\t\t+                  +
\t\t+------------------+
"""
	for N, line in enumerate(x.split("\n")):
		sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
		time.sleep(0.05)
print_logo()

def scheduler(start_time, date, seconds=0):
	return subprocess.call((
		f'powershell',
		f'$Time = New-ScheduledTaskTrigger -At (Get-Date -Year {date.year} -Month {date.month} -Day {date.day} -Hour {start_time.hour} -Minute {start_time.minute} -Second {seconds}) -Once \n',
		f'$Action = New-ScheduledTaskAction -Execute "{exec_path}" \n',
		f'$Setting = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun -RunOnlyIfNetworkAvailable -MultipleInstances Parallel -Priority 3 -RestartCount 30 -RestartInterval (New-TimeSpan -Minutes 1) \n',
		f'Register-ScheduledTask -Force -TaskName "SIMABot" -Trigger $Time -Action $Action -Settings $Setting -Description "SIMA Auto Presence Submitter {V}" -RunLevel Highest'
	), creationflags=0x08000000)

def exitOnErrorHandler(cur_driver, msg="No internet Connection... restarting in 30~40 seconds."):
	cur_datetime = datetime.datetime.now() + datetime.timedelta(seconds=50)
	scheduler(cur_datetime, cur_datetime, cur_datetime.second)
	popup(
		app_name = f"SIMA BOT V.{V}",
		title = "Error",
		message = f"Error: {msg}",
		app_icon = "favicon.ico"
	)
	cur_driver.quit()
	sys.exit(1)

wait = WebDriverWait(driver, 10)

# Login
popup(
	app_name = f"SIMA BOT V.{V}",
	title = f"Starting...",
	message = f"Login to sima...",
	app_icon = "favicon.ico"
)
print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Login to sima with nim : ' + b + config['nim'])
try:
	driver.get("http://sima.usm.ac.id/")
	driver.refresh()
	# cookies = pickle.load(open("cookies.pkl", "rb"))
	# for cookie in cookies:
	# 	driver.add_cookie(cookie)
	user = wait.until(EC.visibility_of_element_located((By.XPATH, "/html//input[@id='username']")))
	user.send_keys(config['nim'])
	passwd = wait.until(EC.visibility_of_element_located((By.XPATH, "/html//input[@id='email-id']")))
	passwd.send_keys(config['password'])
	submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']//form[@action='http://sima.usm.ac.id/login']//div[@class='submit_field']/input")))
	submit.click()
	# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
except NoSuchElementException:
	exitOnErrorHandler(driver)
try:
	identity = driver.find_element_by_xpath("/html//div[@id='content']/div[@class='box']/div[@class='box-row']//div[@class='col-sm-4']/div/div/div[1]/div//span").text
	# regex = re.findall(r'bold.*? (.+?)<.*?\s{20}(.+)\s{16}.*?<', identity.text)
	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Success login. Hi ' + b + identity)
	popup(
		app_name = f"SIMA BOT V.{V}",
		title = f"SIMA BOT V.{V} - Success",
		message = f"Success Login Hi {identity}",
		app_icon = "favicon.ico"
	)
except NoSuchElementException:
	exitOnErrorHandler(driver)

try:
	driver.find_element_by_xpath("//div[@class='alert alert-danger']")
	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Failed to login, please put your user and password in data.json')
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
def doTesting():
	SIA = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html//div[@id='content']/div[@class='box']//div[@class='card']/div/div[@class='btn-groups']/form[1]/button[@type='submit']/span[1]")))
	SIA.click()
	popup(
		app_name = f"SIMA BOT V.{V}",
		title = f"SIMA BOT V.{V} - Testing...",
		message = "Testing....",
		app_icon = "favicon.ico"
	)
	# click presensi kuliah
	# //div[@id='nav']/nav/ul[@class='nav']/li[4]/a/span[@class='pull-right text-muted']/i[@class='fa fa-caret-down']
	# //div[@id='nav']/nav/ul[@class='nav']/li[3]/a/span[@class='pull-right text-muted']
	pres_kul = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='nav']/nav/ul[@class='nav']/li[3]/a/span[@class='pull-right text-muted']/i[@class='fa fa-caret-down']")))
	pres_kul.click()	
	time.sleep(2)
	jadwall = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='nav']/nav/ul/li[3]/ul[@class='nav nav-sub']//a[@href='http://sima.usm.ac.id/akademik/jadwal_kuliah']")))
	# //div[@id='nav']/nav/ul/li[3]/ul[@class='nav nav-sub']//a[@href='http://sima.usm.ac.id/akademik/jadwal_kuliah']
	jadwall.click()
	# cookies = pickle.load(open("cookies.pkl", "rb"))
	# for cookie in cookies:
	# 	driver.add_cookie(cookie)
	# click matkul ALGORITMA DAN PEMROGRAMAN (SIS18103P)
	algo = wait.until(EC.visibility_of_element_located((By.XPATH, "/html//div[@id='app']/div[3]/div[1]/div/div[1]/span[@class='pull-right']/form[@action='http://sima.usm.ac.id/akademik/jadwal_kuliah/detail/']/button[.='detail']")))	
	algo.click()
	time.sleep(10)
	# logout
	logout = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='content']/div/div[1]/ul[@class='nav nav-sm navbar-tool pull-right']/ul[@class='nav nav-sm navbar-tool pull-right']//a[@href='http://sima.usm.ac.id/logout']/b[.='Sign Out  ']")))	
	logout.click()	
	# //div[@id='content']/div/div[1]/ul[@class='nav nav-sm navbar-tool pull-right']/ul[@class='nav nav-sm navbar-tool pull-right']//a[@href='http://sima.usm.ac.id/logout']
	# driver.get("http://sima.usm.ac.id/dashboard/app/")
	# driver.refresh()
	# cookies = pickle.load(open("cookies.pkl", "rb"))
	# for cookie in cookies:
	# 	driver.add_cookie(cookie)
	# time.sleep(5)
	# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
	sys.exit(1)
	time.sleep(5)
	driver.quit()
	# print("\tWorkkkk")


# Schedule Page -> Get ongoing matkul
# print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Mengambil data jadwal kuliah...')
# try:
# 	driver.refresh()
# 	nx = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html//div[@id='content']/div[@class='box']//div[@class='card']/div/div[@class='btn-groups']/form[1]/button[@type='submit']")))
# 	nx.click()
# 	# print("AAA")
# 	driver.get("http://sima.usm.ac.id/akademik/jadwal_kuliah")
# 	# driver.refresh()
# 	schedule_campuss = driver.find_element_by_xpath('//*[@id="app"]')
# 	get_source = schedule_campuss.get_attribute("innerHTML")
# 	# print(get_source)
# 	data = re.findall(r'<.*?text-.*?">\s{9}(.+?)\s{8}<\/div>.*?\s{8}<span.*?>(.+?)<\/span>', get_source)
# 	# print(data)
# 	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Nama : '+ b +f'{data[0][0]}')
# 	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'NIM  : '+ b +f'{data[0][1]}')
# 	driver.refresh()
	# tgl = datetime.datetime.now().strftime("%d-%m-%Y")
	# dayy = datetime.datetime.now().strftime("%a")
	# if dayy=="Mon":
	# 	harii = "Senin"
	# elif dayy=="Tue":
	# 	harii = "Selasa"
	# elif dayy=="Wed":
	# 	harii = "Rabu"
	# elif dayy=="Thu":
	# 	harii = "Kamis"
	# elif dayy=="Fri":
	# 	harii = "Jumat"
	# # driver.find_element_by_xpath(f"/html//div[@id='app']/div[2]//b[.='Jadwal Kuliah Online Hari  {harii}, Tanggal {tgl} ']")
	# print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Jadwal Kuliah Online Hari  {harii}, Tanggal {tgl}')	
# except:
# 	print("Erorr.")
# 	driver.quit()
# matkul_ongoing = None
# try:
# 	driver.get(presensi)
# 	driver.refresh()
# 	today_schedule = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]')
# 	get_sourceee = today_schedule.get_attribute('innerHTML')
# 	print(get_sourceee)
# 	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Looking schedules ...')
# 	# j = re.findall(r'\d{2}:\d{2}', today_schedule)
# 	# print(j)

# 	for matkul in today_schedule:
# 		get_sourceee = today_schedule.get_attribute('innerHTML')
# 		print("AAAA")
# 		# print(get_sourceee)
# 		jadwal = re.findall(r'<\/i>\s(.*?),\sJam\s(.+?)\s{5}.*?\n.*?\s{13}.*?\n\s{12}.*?de.*?\s{12}.*?\n\s{11}.*?\n\s{4}.*?\n\s{4}.*?\n\s{5}.*?\n\s{6}.*?m-b-xs">(.+?)<\/div>', get_sourceee)
# 		# ('senin', 'senin', 'selasa', 'rabu', 'kamis', 'jumat', 'jumat', 'jumat')
# 		hari = jadwal[0][0], jadwal[1][0], jadwal[2][0], jadwal[3][0], jadwal[4][0], jadwal[5][0], jadwal[6][0], jadwal[7][0]
# 		# ('17.00', '19.40', '17.00', '17.00', '19.40', '17.00', '18.20', '19.40')
# 		jam = jadwal[0][1], jadwal[1][1], jadwal[2][1], jadwal[3][1], jadwal[4][1], jadwal[5][1], jadwal[6][1], jadwal[7][1]
# 		# ('Algoritma dan Pemrograman  (SIS18103P)', 'Manajemen Teknologi Informasi (SIS18104P)', 'Basis Data (SIS18101P)', 'Ekonomi Bisnis (SIS18102)', 'Pancasila (USM18102G)', 'Olah Raga (USM18101P)', 'Matematika (USM18103)', 'Bahasa Indonesia (USM18104)')
# 		materi = jadwal[0][2], jadwal[1][2], jadwal[2][2], jadwal[3][2], jadwal[4][2], jadwal[5][2], jadwal[6][2], jadwal[7][2]
# 		tz_offset = datetime.datetime.now().astimezone().utcoffset() - datetime.timedelta(hours=7)
# 		cur_time = datetime.datetime.now()
# 		today = cur_time.strftime("%a")
# 		if today=="Mon":
# 			if datetime.datetime.now().strftime("%H:%M") == jam[0]:
# 				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[0][:2]), int(jam[0][3:]))) + tz_offset 
# 				name = materi[0]
# 				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
# 				end_time = start_time + datetime.timedelta(hours=1) 
# 				print("Hey bung time for your class")
# 			elif datetime.datetime.now().strftime("%H:%M") == jam[1]:
# 				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[1][:2]), int(jam[1][3:]))) + tz_offset 
# 				name = materi[1]
# 				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[2]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
# 				end_time = start_time + datetime.timedelta(hours=1) 
# 				print("Hey bung time for your class")
# 			else:
# 				print("Error..")
# 		elif today=="Tue":
# 			if datetime.datetime.now().strftime("%H:%M") == jam[2]:
# 				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[2][:2]), int(jam[2][3:]))) + tz_offset 
# 				name = materi[2]
# 				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
# 				end_time = start_time + datetime.timedelta(hours=1) 
# 				print("Hey bung time for your class")
# 			else:
# 				print("Erorr..")
# 		elif today=="Wed":
# 			if datetime.datetime.now().strftime("%H:%M") == jam[3]:
# 				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[3][:2]), int(jam[3][3:]))) + tz_offset 
# 				name = materi[3]
# 				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
# 				end_time = start_time + datetime.timedelta(hours=1) 
# 				print("Hey bung time for your class")
# 			else:
# 				print("Error..")
# 		elif today=="Thu":
# 			if datetime.datetime.now().strftime("%H:%M") == jam[4]:
# 				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[4][:2]), int(jam[4][3:]))) + tz_offset 
# 				name = materi[4]
# 				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
# 				end_time = start_time + datetime.timedelta(hours=1) 
# 				print("Hey bung time for your class")
# 			else:
# 				print("Error..")
# 		elif today=="Fri":
# 			if datetime.datetime.now().strftime("%H:%M") == jam[5]:
# 				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[5][:2]), int(jam[5][3:]))) + tz_offset
# 				name = materi[5]
# 				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
# 				end_time = start_time + datetime.timedelta(hours=1) 
# 				print("Hey bung time for your class")
# 			elif datetime.datetime.now().strftime("%H:%M") == jam[6]:
# 				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[6][:2]), int(jam[6][3:]))) + tz_offset
# 				name = materi[6]
# 				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[2]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
# 				end_time = start_time + datetime.timedelta(hours=1) 
# 				print("Hey bung time for your class")				
# 			elif datetime.datetime.now().strftime("%H:%M") == jam[7]:
# 				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[7][:2]), int(jam[7][3:]))) + tz_offset
# 				name = materi[7]
# 				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[3]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
# 				print("Hey bung time for your class")
# 			else:
# 				print("Error...")				
# 		else:
# 			print("Its a holidayy")
# 		if cur_time > start_time:
# 			matkul_ongoing = {'matkul': name, 'start_time': start_time, 'end_time': end_time, 'press': pres}
# 			break
# except SystemExit:
# 	sys.exit(1)
# except:
# 	pass

# SCHEDULED = False
# # Schedule next run
# ## check if next run is in the same day:
# cur_time = datetime.datetime.now()
# cur_date = datetime.date.today()
# try:
# 	x = "http://http://sima.usm.ac.id/akademik/jadwal_kuliah"
# 	jadwal = re.findall(r'<\/i>\s(.*?),\sJam\s(.+?)\s{5}.*?\n.*?\s{13}.*?\n\s{12}.*?de.*?\s{12}.*?\n\s{11}.*?\n\s{4}.*?\n\s{4}.*?\n\s{5}.*?\n\s{6}.*?m-b-xs">(.+?)<\/div>', x)
# 	# ('senin', 'senin', 'selasa', 'rabu', 'kamis', 'jumat', 'jumat', 'jumat')
# 	hari = jadwal[0][0], jadwal[1][0], jadwal[2][0], jadwal[3][0], jadwal[4][0], jadwal[5][0], jadwal[6][0], jadwal[7][0]
# 	# ('17.00', '19.40', '17.00', '17.00', '19.40', '17.00', '18.20', '19.40')
# 	jam = jadwal[0][1], jadwal[1][1], jadwal[2][1], jadwal[3][1], jadwal[4][1], jadwal[5][1], jadwal[6][1], jadwal[7][1]
# 	# ('Algoritma dan Pemrograman  (SIS18103P)', 'Manajemen Teknologi Informasi (SIS18104P)', 'Basis Data (SIS18101P)', 'Ekonomi Bisnis (SIS18102)', 'Pancasila (USM18102G)', 'Olah Raga (USM18101P)', 'Matematika (USM18103)', 'Bahasa Indonesia (USM18104)')
# 	materi = jadwal[0][2], jadwal[1][2], jadwal[2][2], jadwal[3][2], jadwal[4][2], jadwal[5][2], jadwal[6][2], jadwal[7][2]
# 	for next_run in materi:
# 		if today=="Mon":
# 			start_clock = jam[1]
# 			next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[1][:2]), int(jam[1][3:]))) + tz_offset
# 			next_matkul = jadwal[1][2]
# 		elif today=="Fri":
# 			if datetime.datetime.now().strftime("%H:%M") == jam[6]:
# 				start_clock = jam[6]
# 				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[6][:2]), int(jam[6][3:]))) + tz_offset
# 				next_matkul = jadwal[6][2]
# 			elif datetime.datetime.now().strftime("%H:%M") == jam[7]:
# 				start_clock = jam[7]
# 				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[7][:2]), int(jam[7][3:]))) + tz_offset
# 				next_matkul = jadwal[7][2]
# 			else:
# 				print("Error..")
# 		else:
# 			print("Its a holidayy")
# 		if cur_time < next_start_time:
# 			print(f"next run: {next_matkul} at {start_clock} today")
# 			res = scheduler(next_start_time, cur_date)
# 			if res:
# 				popup(
# 					app_name = f"SIMA BOT V.{V}",
# 					title = "SIMA BOT V.{V} - Error",
# 					message = "Failed to schedule next run. Please run the program again or report to The Maker",
# 					app_icon = "favicon.ico"
# 				)
# 			else:
# 				popup(
# 					app_name = f"SIMA BOT V.{V}",
# 					title = "SIMA BOT V.{V} - Scheduled",
# 					message = f"next run: {next_matkul} at {start_clock}- today",
# 					app_icon = "favicon.ico"
# 				)
# 			SCHEDULED = True
# 			break
# except SystemExit:
# 	sys.exit(1)
# except:
# 	pass

# presence
nx = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html//div[@id='content']/div[@class='box']//div[@class='card']/div/div[@class='btn-groups']/form[1]/button[@type='submit']")))
nx.click()
time.sleep(3)
matkul_ongoing = True
driver.implicitly_wait(0.5)
if matkul_ongoing:
	is_done = False
	cur_time = datetime.datetime.now()
	while not is_done:
		# print(f"trying to submit present for {matkul_ongoing['matkul']} at {matkul_ongoing['start_time'].strftime('%H:%M')}...")
		# print(driver.current_url)
		try:
			# driver.find_element_by_xpath("//div[@id='nav']/nav/ul[@class='nav']//a[@href='http://sima.usm.ac.id/akademik/presensi_kuliah']").click()
			driver.get("http://sima.usm.ac.id/akademik/presensi_kuliah")
			driver.refresh()
			driver.find_element_by_xpath("/html//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']").click()
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Matkul clicked')
		except Exception as e:
			print('error raised')
			print(e)
			exitOnErrorHandler(driver)
		try:
			tombol_presensi = driver.find_element_by_xpath("/html//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/press/']/button[@type='submit']//b[.='Presensi Kuliah']")
			tombol_presensi.click()
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Presence Done...')
			popup(
				title = f"SIMA BOT V.{V} - Status",
				message = f"Presence submitted @{datetime.datetime.now().time().strftime('%H:%M')} for {matkul_ongoing['name']} at {matkul_ongoing['start_time'].strftime('%H:%M')}!",
				app_icon = "favicon.ico"
			)
			is_done = True
		except:
			try:
				data_matkul = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div')
				get_source_data_matkul = data_matkul.get_attribute('innerHTML')
				# print(get_source_data_matkul)
				regex_data_matkul = re.findall(r'""\svalue="(.+?)"', get_source_data_matkul)
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Status Perkuliahan: {regex_data_matkul[0]}')
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Kode Makul: {regex_data_matkul[1]}')
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Nama Makul: {regex_data_matkul[2]}')
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Pertemuan Ke: {regex_data_matkul[3]}')
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Jam Presensi: {regex_data_matkul[4]}')
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f'Hari, Tanggal: {regex_data_matkul[5]}')
				online = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div[@class='col-md-12']//form[@action='#']//input[@value='Online']").text
				popup(
					title = f"SIMA BOT V.{V}",
					message = f"Presence already submitted for {matkul_ongoing['matkul']} at {matkul_ongoing['start_time'].strftime('%H:%M')}!",
					app_icon = "favicon.ico"
				)                
				is_done = True
			except:
				print('error raised')
				exitOnErrorHandler(driver)
			






			# print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f"Presence button was not open yet. Waiting a minute")
			# time.sleep(60)
			# print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + "Sleep done, its will be return from button presence")





		# if datetime.datetime.now() > matkul_ongoing['end_time']:
		# 	popup(
		# 		title = f"SIMA BOT V.{V}",
		# 		message = f"Presence for {matkul_ongoing['name']} is not submitted because it's not open",
		# 		app_icon = "favicon.ico"
		# 	)
		# 	is_done = True
		# if datetime.datetime.now() > (cur_time + datetime.timedelta(minutes=10)):
		# 	cur_time = datetime.datetime.now()
		# 	popup(
		# 		title = f"SIMA BOT V.{V} - Status",
		# 		message = f"Presence for {matkul_ongoing['matkul']} @{cur_time.strftime('%H:%M')} is still waiting for opening...",
		# 		app_icon = "favicon.ico"
		# 	)			
else:
	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'there is no ongoing matkul.')
	sys.exit(1)
	driver.quit()
	popup(
		title = f"SIMA BOT V.{V} - Status",
		message = "No ongoing matkul...",
		app_icon = "favicon.ico"
	)
driver.quit()
time.sleep(10)
# presensi
# def joinPresensi():
# 	driver.get("http://sima.usm.ac.id/app")
#   driver.refresh()
# 	sima = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Sistem Informasi Akademik']")))
# 	sima.click()
# 	driver.get(presensi)
# 	for cookie in cookies:
# 		driver.add_cookie(cookie)
# 	time.sleep(70)
# 	matkul = re.findall(r'', presensi.text)
# 	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + '' + b + 'Nama mata kuliah yang akan di presensi: '+matkul)
# 	driver.find_element_by_xpath("").click()
# 	time.sleep(10)
# 	pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
# 	driver.get(portal)
# 	for cookie in cookies:
# 		driver.add_cookie(cookie)
# 	driver.find_element_by_xpath("//div[@class='alert alert-danger']")
# 	print("Login ulang...")
# 	pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
# 	sys.exit(1)
# 	time.sleep(3)
# 	driver.quit()

# testing = ("16:00")

# # jadwal
# def monday():
# 	schedule.every().monday.at(testing).do(doTesting())
# 	schedule.every().monday.at(config['senen1']).do(joinPresensi())
# 	schedule.every().monday.at(config['senen2']).do(joinPresensi())

# def tuesday():
# 	schedule.every().tuesday.at(config['selasa1']).do(joinPresensi())

# def wednesday():
# 	schedule.every().wednesday.at(config['rabu1']).do(joinPresensi())

# def thursday():
# 	schedule.every().thursday.at(config['kamis1']).do(joinPresensi())

# def friday():
# 	schedule.every().friday.at(config['jumat1']).do(joinPresensi())
# 	schedule.every().monday.at(config['jumat2']).do(joinPresensi())
# 	schedule.every().monday.at(config['jumat3']).do(joinPresensi())

# day = (sekarang.strftime("%a"))
# # print(day)

# if day=="Mon":
# 	monday()
# elif day=="Tue":
# 	tuesday()
# elif day=="Wed":
# 	wednesday()
# elif day=="Thu":
# 	thursday()
# elif day=="Fri":
# 	friday()
# else:
# 	print("\tHell Yeahh, Liburan :'v")
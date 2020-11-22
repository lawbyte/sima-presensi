from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from win10toast import ToastNotifier
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

# CONFIGURATIONS
VER = '1.9'
popup = notification.notify
r = Fore.RED
g = Fore.GREEN
w = Fore.WHITE
b = Fore.BLUE
y = Fore.YELLOW
m = Fore.MAGENTA
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

if not os.path.exists(os.path.join(app_path, "data.json")):
	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'ERROR: data.json not found! Fill in the data.json file.')
	defaultData = {
		"username": "type_your_username_here",
		"password" : "type_your_password_here"
	}
	with open(os.path.join(app_path, "data.json"), 'w') as f:
		json.dump(defaultData, f)
	time.sleep(5)
	sys.exit(1)

with open(os.path.join(app_path, "data.json")) as f:
	config = json.load(f)
option = Options()
option.headless = True
option.add_argument('--ignore-certificate-errors')
option.add_argument('--disable-gpu')

driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=option)
driver.implicitly_wait(10)
toaster = ToastNotifier()

# UTILITY FUNCTIONS

def scheduler(start_time, date, seconds=0):
	return subprocess.call((
		f'powershell',
		f'$Time = New-ScheduledTaskTrigger -At (Get-Date -Year {date.year} -Month {date.month} -Day {date.day} -Hour {start_time.hour} -Minute {start_time.minute} -Second {seconds}) -Once \n',
		f'$Action = New-ScheduledTaskAction -Execute "{exec_path}" \n',
		f'$Setting = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun -RunOnlyIfNetworkAvailable -MultipleInstances Parallel -Priority 3 -RestartCount 30 -RestartInterval (New-TimeSpan -Minutes 1) \n',
		f'Register-ScheduledTask -Force -TaskName "SIMABOT" -Trigger $Time -Action $Action -Settings $Setting -Description "SIMA BOT  Presence Submitter {VER}" -RunLevel Highest'
	), creationflags=0x08000000)

def exitOnErrorHandler(cur_driver, msg="No internet Connection... restarting in 30~40 seconds."):
	cur_datetime = datetime.datetime.now() + datetime.timedelta(seconds=50)
	scheduler(cur_datetime, cur_datetime, cur_datetime.second)
	popup(
		title = f"SIMA BOT V.{VER} - Error",
		message = f"ERROR: {MSG}",
		app_icon = "favicon.ico"
	)
	cur_driver.quit()
	sys.exit(1)

# Login Page
popup(
		title = f"SIMA BOT V.{VER} - Starting",
		message = f"Preparing for presence submitting...",
		app_icon = "favicon.ico"
	)
print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Preparing for login')
try:
	driver.get("http://sima.usm.ac.id/")
	driver.find_element_by_id('username').send_keys(config['nim'])
	driver.find_element_by_id('email-id').send_keys(config['password'])
	driver.find_element_by_xpath("/html/body/div[@class='container']/div[@class='row']/div[@class='col-md-4']//form[@action='http://sima.usm.ac.id/login']//div[@class='submit_field']/input").click()
except NoSuchElementException:
	exitOnErrorHandler(driver)
print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Login in...')
try:
	driver.find_element_by_xpath("//div[@class='alert alert-danger']")
	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Failed to login. Please input correct data in data.json')
	sys.exit(1)
except SystemExit:
	driver.quit()
	popup(
		title = f"SIMA BOT V.{VER} - Error",
		message = f"Failed to login. Please input correct data in data.json and run the program again",
		app_icon = "favicon.ico"
	)
	sys.exit(1)
except:
	pass

# Schedule Page -> Get ongoing matkul
print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Scraping schedules...')
driver.find_element_by_xpath("/html//div[@id='content']/div[@class='box']//div[@class='card']/div/div[@class='btn-groups']/form[1]/button[@type='submit']").click()
driver.get(f"http://sima.usm.ac.id/akademik/presensi_kuliah")
matkul_ongoing = None
try:
	try:
		jadwal_kuliah = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div/div[2]')
	except NoSuchElementException:
		exitOnErrorHandler(driver)
	tz_offset = datetime.datetime.now().astimezone().utcoffset() - datetime.timedelta(hours=7)
	cur_time = datetime.datetime.now()
	for matkul in jadwal_kuliah:
		html_jadwal_kuliah = driver.page_source
		# print(html_jadwal_kuliah)
		# start time configuration
		# example: ['17:00','19:40']
		# cur_hour = datetime.datetime.now().strftime("%H:%M")
		# cur_times = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(datetime.datetime.now().strftime("%H:%M")[:2]), int(datetime.datetime.now().strftime("%H:%M")[3:]))) + tz_offset
		raw_start_time = re.findall(r'\d{2}:\d{2}', html_jadwal_kuliah)
		print(raw_start_time)
		data_time = (datetime.datetime.strptime(raw_start_time[0], "%H:%S") + datetime.timedelta(hours=1)).strftime("%H:%S"), (datetime.datetime.strptime(raw_start_time[1], "%H:%S") + datetime.timedelta(hours=1)).strftime("%H:%S"), (datetime.datetime.strptime(raw_start_time[2], "%H:%S") + datetime.timedelta(hours=1)).strftime("%H:%S")
		print(data_time)
		today = datetime.datetime.now().strftime("%a")
		print(today)
		matkul_name = re.findall(r'<div class="font-bold text-u-c m-b-xs">(.+?)<\/div>', html_jadwal_kuliah)
		print(matkul_name)
		print(cur_time)
		if today=="Mon":
			if cur_hour >= raw_start_time[0] and cur_times <= raw_end_time:
				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[0][:2]), int(raw_start_time[0][3:]))) + tz_offset
				name = matkul_name[0]
				pres = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = raw_end_time1
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			elif datetime.datetime.now().strftime("%H:%M") >= raw_start_time[1] and datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(datetime.datetime.now().strftime("%H:%M")[:2]), int(datetime.datetime.now().strftime("%H:%M")[3:]))) + tz_offset <= raw_end_time2:
				start_time = real_raw_start_time2
				name = matkul_name[1]
				pres = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div/div[@class='row']/div[2]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = raw_end_time2
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		elif today=="Tue":
			if datetime.datetime.now().strftime("%H:%M") >= raw_start_time[0] and datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(datetime.datetime.now().strftime("%H:%M")[:2]), int(datetime.datetime.now().strftime("%H:%M")[3:]))) + tz_offset <= raw_end_time:
				start_time = real_raw_start_time
				name = matkul_name[0]
				pres = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = raw_end_time
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			else:
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
		elif today=="Wed":
			check = datetime.datetime.now().strftime("%H:%M")
			if datetime.datetime.now().strftime("%H:%M") >= raw_start_time[0] and datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(datetime.datetime.now().strftime("%H:%M")[:2]), int(datetime.datetime.now().strftime("%H:%M")[3:]))) + tz_offset <= raw_end_time:
				start_time = real_raw_start_time
				name = matkul_name[0]
				# /html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']
				pres = driver.find_element_by_xpath("/html//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = raw_end_time
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			else:
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
		elif today=="Thu":
			print("WOY WORK APA NGGAK")
			# test_raw_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(23), int(30))) + tz_offset
			# test_end_time = test_raw_start_time + datetime.timedelta(hours=1)	
			# print(test_end_time)
			# print(test_raw_start_time)
			while datetime.datetime.now().strftime("%H:%M") < '23:59':
				print("Waiting..")
				time.sleep(2)
				pass
			if datetime.datetime.now().strftime("%H:%M") == '23:59':
				# print("TESTTTTTTTT")
				# print(int(datetime.datetime.now().strftime("%H:%M")[:2]))
				# print(int(datetime.datetime.now().strftime("%H:%M")[3:]))
				start_time = real_raw_start_time
				print(start_time)		
				name = matkul_name[0]
				print(name)
				# /html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']
				# /html//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']
				# /html//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/press/']/button[@type='submit']//b[.='Presensi Kuliah']
				pres = driver.find_element_by_xpath("/html//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = raw_end_time
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			else:
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error sattt')				
		elif today=="Fri":
			# print("check")
			# while datetime.datetime.now().strftime("%H:%M") < raw_start_time[0]:
			# 	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Waiting...')
			# 	time.sleep(2)
			# 	pass
			if datetime.datetime.now().strftime("%H:%M") >= raw_start_time[0] and datetime.datetime.now().strftime("%H:%M") <= raw_end_time1:
				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[0][:2]), int(raw_start_time[0][3:]))) + tz_offset
				name = matkul_name[0]
				pres = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = raw_end_time1
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			elif datetime.datetime.now().strftime("%H:%M") >= raw_start_time[1] and datetime.datetime.now().strftime("%H:%M") <= raw_end_time2:
				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[1][:2]), int(raw_start_time[1][3:]))) + tz_offset
				name = matkul_name[1]
				pres = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div/div[@class='row']/div[2]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = raw_end_time2
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')				
			if datetime.datetime.now().strftime("%H:%M") >= raw_start_time[2] and datetime.datetime.now().strftime("%H:%M") <= raw_end_time3:
				start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[2][:2]), int(raw_start_time[2][3:]))) + tz_offset
				name = matkul_name[2]
				pres = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div/div[@class='row']/div[3]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = raw_end_time3			
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			else:
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
		else:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Its a holiday')
		if cur_time > start_time and cur_time < end_time:
		# if cur_time < end_time:
			print("TEST OY")
			matkul_ongoing = {'name': name, 'start_time': start_time, 'end_time': end_time, 'link': pres}
			break
except SystemExit:
	sys.exit(1)
except:
	pass

# print(matkul_ongoing['name'])
# Score a present
time.sleep(3)
driver.implicitly_wait(0.5)
if matkul_ongoing:
	is_done = False
	cur_time = datetime.datetime.now()
	while not is_done:
		print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + f"trying to submit present for {matkul_ongoing['name']} at {matkul_ongoing['start_time'].strftime('%H:%M')}-{matkul_ongoing['end_time'].strftime('%H:%M')}...")
		print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + driver.current_url)
		try:
			matkul_ongoing['link'].click()
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'matkul clicked')
		except Exception as e:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error raised')
			print(e)
			exitOnErrorHandler(driver)
		try:
			button_hadir = driver.find_element_by_xpath("/html//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/press/']/button[@type='submit']//b[.='Presensi Kuliah']")
			button_hadir.click()
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'PRESENT DONE!')
			popup(
				title = f"SIMA BOT V.{VER} - Status",
				message = f"Presence submitted @{datetime.datetime.now().time().strftime('%H:%M')} for {matkul_ongoing['name']} at {matkul_ongoing['start_time'].strftime('%H:%M')}-{matkul_ongoing['end_time'].strftime('%H:%M')}!",
				app_icon = "favicon.ico"
			)
			is_done = True
		except:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'button presensi not found')
			try:
				button_tidakhadir = driver.find_element_by_xpath("/html//div[@id='app']/div[2]/div[@class='col-md-12']//form[@action='#']//input[@value='Online']")
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + "You're already present")
				popup(
					title = f"SIMA BOT V.{VER} - Status",
					message = f"Presence already submitted for {matkul_ongoing['name']} at {matkul_ongoing['start_time'].strftime('%H:%M')}-{matkul_ongoing['end_time'].strftime('%H:%M')}!",
					app_icon = "favicon.ico"
				)
				is_done = True
			except:
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'not found')
				# try:
				#     driver.find_element_by_xpath("//div[@class='jconfirm-buttons']/button").click()
				# except:
				#     print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error raised')

				#     exitOnErrorHandler(driver)
				# print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Presence list not open yet. Waiting for a minute...')
				# time.sleep(60)
				# print('sleep done')
		if datetime.datetime.now() > matkul_ongoing['end_time']:
			popup(
				title = f"SIMA BOT V.{VER} - Status",
				message = f"Presence for {matkul_ongoing['name']} is not submitted because it's not open",
				app_icon = "favicon.ico"
			)
			is_done = True
		elif datetime.datetime.now() > (cur_time + datetime.timedelta(minutes=10)):
			cur_time = datetime.datetime.now()
			popup(
				title = f"SIMA BOT V.{VER} - Status",
				message = f"Presence for {matkul_ongoing['name']} @{cur_time.strftime('%H:%M')} is still waiting for opening...",
				app_icon = "favicon.ico"
			)
else:
	print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'there is no ongoing matkul')
	time.sleep(1.5)
	driver.refresh()
	# popup(
	# 	title = f"SIMA BOT V.{VER} - Status",
	# 	message = f"No ongoing matkul...",
	# 	app_icon = "favicon.ico"
	# )	
time.sleep(5)
driver.get("http://sima.usm.ac.id/logout")
driver.quit()
time.sleep(10)
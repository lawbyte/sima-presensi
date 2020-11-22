from selenium import webdriver
from selenium.webdriver import Chrome
import multiprocessing as mp
import time
import datetime
import sys
import signal
import os
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

tgl = datetime.datetime.now().strftime("%d-%m-%Y")
dayy = datetime.datetime.now().strftime("%a")
if dayy=="Mon":
	harii = "Senin"
elif dayy=="Tue":
	harii = "Selasa"
elif dayy=="Wed":
	harii = "Rabu"
elif dayy=="Thu":
	harii = "Kamis"
elif dayy=="Fri":
	harii = "Jumat"
print(f'Jadwal Kuliah Online Hari  {harii}, Tanggal {tgl}')
# is_done = False
# while not is_done:
# 	try:
# 		if datetime.datetime.now().strftime("%H:%M") == '21:26':
# 			print("WORK")
# 			is_done = True
# 			sys.exit(1)
# 	except:
# 		pass


r = Fore.RED
g = Fore.GREEN
w = Fore.WHITE
b = Fore.BLUE
y = Fore.YELLOW
m = Fore.MAGENTA

matkul_ongoing = None
cur_time = datetime.datetime.now()
today = cur_time.strftime("%a")
tz_offset = datetime.datetime.now().astimezone().utcoffset() - datetime.timedelta(hours=7)
today = datetime.datetime.now().strftime("%a")
materi = ['Algoritma dan Pemrograman  (SIS18103P)', 'Manajemen Teknologi Informasi (SIS18104P)', 'Basis Data (SIS18101P)', 'Ekonomi Bisnis (SIS18102)', 'Pancasila (USM18102G)', 'Olah Raga (USM18101P)', 'Matematika (USM18103)', 'Bahasa Indonesia (USM18104)']
jam = ['11:11', '12:12', '13:13']
print(datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(12), int(0))) + tz_offset)
# for check in materi:
# 	if today=="Wed":
# 		if datetime.datetime.now().strftime("%H:%M") == datetime.datetime.now().strftime("%H:%M"):
# 			print(check[:2])
# 			print(check[3:])
# 			break
raw_start_time = datetime.datetime.now().strftime("%H:%M")
# raw_start_time = "12:12"
cur_time = datetime.datetime.now()
for matkul in materi:
	if today=="Mon":
		if datetime.datetime.now().strftime("%H:%M") == raw_start_time:
			start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset 
			name = matkul[0]
			pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
			end_time = start_time + datetime.timedelta(hours=1) 
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		elif datetime.datetime.now().strftime("%H:%M") == raw_start_time:
			start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset 
			name = matkul[0]
			pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[2]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
			end_time = start_time + datetime.timedelta(hours=1) 
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
	elif today=="Tue":
		if datetime.datetime.now().strftime("%H:%M") == raw_start_time:
			start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset 
			name = matkul[0]
			pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
			end_time = start_time + datetime.timedelta(hours=1) 
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		else:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
	elif today=="Wed":
		if datetime.datetime.now().strftime("%H:%M") == datetime.datetime.now().strftime("%H:%M"):
			start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset 
			name = materi[0]
			# /html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']
			pres = ("tml//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
			end_time = start_time + datetime.timedelta(hours=1) 
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		else:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
	elif today=="Thu":
		# if datetime.datetime.now().strftime("%H:%M") == raw_start_time:
		start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset
		name = matkul
		pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
		end_time = start_time + datetime.timedelta(hours=1) 
		print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
	elif today=="Fri":
		if datetime.datetime.now().strftime("%H:%M") == raw_start_time:
			start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset
			name = matkul[0]
			pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
			end_time = start_time + datetime.timedelta(hours=1) 
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		elif datetime.datetime.now().strftime("%H:%M") == raw_start_time:
			start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset
			name = matkul[0]
			pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[2]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
			end_time = start_time + datetime.timedelta(hours=1) 
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')				
		elif datetime.datetime.now().strftime("%H:%M") == raw_start_time:
			start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset
			name = matkul[0]
			pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[3]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		else:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
	else:
		print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Its a holiday')
	if cur_time > start_time and cur_time < end_time:
		print(cur_time)
		print(start_time)
		print(end_time)
		matkul_ongoing = {'name': name, 'start_time': start_time, 'end_time': end_time, 'link': pres}
		break
print(matkul_ongoing['name'])





try:
	# if matkul_ongoing:
	# 	print("TESTT")
	if datetime.datetime.now().strftime("%H:%M") > cur_time:
		print("Euy")
	else:
		print("asasd")
except:
	pass



print(end_time)



if datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(datetime.datetime.now().strftime("%H:%M")[:2]), int(datetime.datetime.now().strftime("%H:%M")[3:]))) + tz_offset == start_time and datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(datetime.datetime.now().strftime("%H:%M")[:2]), int(datetime.datetime.now().strftime("%H:%M")[3:]))) + tz_offset <= end_time:
	print("Testing")



aa, ab, ac = ['data1','data2','data3']
print(aa)
print(ab)
print(ac)



# def process(hr, minute):
# 	while True:
# 		d = datetime.datetime.now()
# 		if d.hour == hr and d.minute == minute:
# 			print("Waiting...")
# 		else:
# 			time.sleep(25)


# p = mp.Process(target=process, args=(23, 30))
# p.start()


t = ['17:00','18:00']
for i, v in enumerate(t):
	t[i] = str(int(v[:2])+1).zfill(2)+v[2:]
print(t)
	# print((datetime.datetime.strptime(a, "%H:%S") + datetime.timedelta(hours=1)).strftime("%H:%S"))
	
# print(a)

# t = ['17:00','18:00']
# dataa = t[0], t[1], t[2]
# print(dataa)

if today == "Mon":
      t = ['data1','data2'] 
if today == "Wed":
      t = ['data1'] 
if today == "Fri":
      t = ['data1','data2','data3'] 
print(t)

# dataa = (datetime.datetime.strptime(raw_start_time[0], "%H:%S") + datetime.timedelta(hours=1)).strftime("%H:%S"), (datetime.datetime.strptime(raw_start_time[1], "%H:%S") + datetime.timedelta(hours=1)).strftime("%H:%S"), (datetime.datetime.strptime(raw_start_time[2], "%H:%S") + datetime.timedelta(hours=1)).strftime("%H:%S")
# print(dataa)









# while datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 50:
# 	print("asas")
# print(datetime.datetime.now().strftime("%H:%M"))
# cur_hour = datetime.datetime.now().strftime("%H:%M")
# cur_tim = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(datetime.datetime.now().strftime("%H:%M")[:2]), int(datetime.datetime.now().strftime("%H:%M")[3:]))) + tz_offset
# data = ['00:20','00:30']
# data_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(0), int(10))) + tz_offset
# while cur_hour < data[0]:
# 	print("Waiting...")
# 	time.sleep(2)
# 	pass
# if cur_hour >= data[0] and cur_tim <= data_time:
# 	print("Presensi")


# sekarang = datetime.datetime.now()
# popup = notification.notify
# V = "1.7"
# tz_offset = datetime.datetime.now().astimezone().utcoffset() - datetime.timedelta(hours=7)
# print(tz_offset)
# popup(
# 	app_name = f"SIMA BOT V.{V}",
# 	title = f"Starting...",
# 	message = f"Preparing for presense submitting...",
# 	app_icon = "favicon.ico",
# 	toast = True,
# 	ticker = "NoXLaw"
# )

# if datetime.datetime.now().strftime("%H:%M") == datetime.datetime.now().strftime("%H:%M"):
# 	print('Work')
# else:
# 	print("Nggak work")

# while True:
# 	blah="\/|-\/"
# 	for l in blah:
# 		sys.stdout.write(l)
# 		sys.stdout.flush()
# 		sys.stdout.write('\b')
# 		time.sleep(0.2)
# 	print("Loading"+l)
# day = (sekarang.strftime("%a"))
# print(day)

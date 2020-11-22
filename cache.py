SCHEDULED = False
# Schedule next run
## Assumption: SIMA always points to the current month page
## check if next run is in the same day:
cur_time = datetime.datetime.now()
cur_date = datetime.date.today()
try:
	next_schedules = driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div/div[2]')
	for next_run in next_schedules:
		raw_start_time, raw_end_time = re.findall(r"\d{2}:\d{2}", next_run)
		get_source_next_matkul = matkul.get_attribute('data-kuliah')
		raw_start_time= re.findall(r"\d{2}:\d{2}", get_source_next_matkul)
		today = cur_time.strftime("%a")
		if today=="Mon":
			if datetime.datetime.now().strftime("%H:%M") == jam[0]:
				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[0][:2]), int(jam[0][3:]))) + tz_offset 
				name = materi[0]
				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = next_start_time + datetime.timedelta(hours=1) 
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			elif datetime.datetime.now().strftime("%H:%M") == jam[1]:
				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[1][:2]), int(jam[1][3:]))) + tz_offset 
				name = materi[1]
				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[2]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = next_start_time + datetime.timedelta(hours=1) 
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		elif today=="Tue":
			if datetime.datetime.now().strftime("%H:%M") == jam[2]:
				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[2][:2]), int(jam[2][3:]))) + tz_offset 
				name = materi[2]
				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = next_start_time + datetime.timedelta(hours=1) 
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			else:
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
		# elif today=="Wed":
		# 	if datetime.datetime.now().strftime("%H:%M") == jam[3]:
		# 		next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[3][:2]), int(jam[3][3:]))) + tz_offset 
		# 		name = materi[3]
		# 		pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
		# 		end_time = next_start_time + datetime.timedelta(hours=1) 
		# 		print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		# 	else:
		# 		print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
		elif today=="Wed":
			if datetime.datetime.now().strftime("%H:%M") == '21:00':
				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(21), int(0))) + tz_offset 
				name = "TEST"
				pres = ("/html//div[@id='app']/div[2]//form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = next_start_time + datetime.timedelta(hours=1) 
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		elif today=="Thu":
			if datetime.datetime.now().strftime("%H:%M") == jam[4]:
				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[4][:2]), int(jam[4][3:]))) + tz_offset 
				name = materi[4]
				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = next_start_time + datetime.timedelta(hours=1) 
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
		elif today=="Fri":
			if datetime.datetime.now().strftime("%H:%M") == jam[5]:
				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[5][:2]), int(jam[5][3:]))) + tz_offset
				name = materi[5]
				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[1]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = next_start_time + datetime.timedelta(hours=1) 
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			elif datetime.datetime.now().strftime("%H:%M") == jam[6]:
				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[6][:2]), int(jam[6][3:]))) + tz_offset
				name = materi[6]
				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[2]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				end_time = next_start_time + datetime.timedelta(hours=1) 
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')				
			elif datetime.datetime.now().strftime("%H:%M") == jam[7]:
				next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(jam[7][:2]), int(jam[7][3:]))) + tz_offset
				end_time = next_start_time + datetime.timedelta(hours=1) 
				name = materi[7]
				pres = ("/html//div[@id='app']/div[2]/div/div[@class='row']/div[3]/div/div[@class='m-v-xs']/form[@action='http://sima.usm.ac.id/akademik/presensi_kuliah/detail/']/button[.='Presensi']")
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Hey bung time for your class')
			else:
				print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Error...')
		else:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Its a holiday')
		if cur_time < next_start_time:
			next_matkul = next_run.get_attribute('data-kuliah')
			print(f"next run: {next_matkul} at {raw_start_time}-{raw_end_time} today")
			res = scheduler(next_start_time, cur_date)
			if res:
				popup(
					title = f"SIMA BOT V.{VER} - Error",
					message = f"Failed to schedule next run. Please run the program again or report to the maker",
					app_icon = "favicon.ico"
				)
			else:
				popup(
					title = f"SIMA BOT V.{VER} - Scheduled!",
					message = f"next run: {next_matkul} at {raw_start_time}-{raw_end_time} today",
					app_icon = "favicon.ico"
				)
			SCHEDULED = True
			break
except SystemExit:
	sys.exit(1)
except:
	pass

if not SCHEDULED:
	## if next run is in the same month:
	next_date = cur_date + datetime.timedelta(days=1)
	if next_date.weekday() >= 5:
		delta = 1 if next_date.weekday() == 6 else 2
		next_date = next_date + datetime.timedelta(days=delta)
	try:
		schedules = driver.find_elements_by_xpath("//td[@class='bg-info']/following-sibling::td | //tr[td[@class='bg-info']]/following::tr/td")
		next_run = None
		for day in schedules:
			if next_date.month != cur_date.month:
				raise Exception('next_date is not current month')
			try:
				next_run = day.find_element_by_xpath(".//div[2]/*/a")
				if next_run:
					break
			except:
				next_date = next_date + datetime.timedelta(days=1)
				if next_date.weekday() >= 5:
					delta = 1 if next_date.weekday() == 6 else 2
					next_date = next_date + datetime.timedelta(days=delta)
		if next_date.month != cur_date.month:
			raise Exception('next_date is not current month')
		raw_start_time, raw_end_time = re.findall(r"\d{2}:\d{2}", next_run.text)
		next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset
		next_matkul = next_run.get_attribute('data-kuliah')
		print(f"next run: {next_matkul} at {raw_start_time}-{raw_end_time} {next_date.strftime('%d/%m/%Y')}")
		res = scheduler(next_start_time, next_date)
		if res:
			popup(
				title = f"SIMA BOT V.{VER} - Error",
				message = f"Failed to schedule next run. Please run the program again or report to the maker",
				app_icon = "favicon.ico"
			)
		else:
			popup(
				title = f"SIMA BOT V.{VER} - Scheduled!",
				message = f"next run: {next_matkul} at {raw_start_time}-{raw_end_time} {next_date.strftime('%d/%m/%Y')}",
				app_icon = "favicon.ico"
			)
		SCHEDULED = True
	except SystemExit:
		sys.exit(1)
	except:
		pass

if not SCHEDULED:
	## if next run is next month:
	next_date = cur_date + datetime.timedelta(days=1)
	if next_date.weekday() >= 5:
		delta = 1 if next_date.weekday() == 6 else 2
		next_date = next_date + datetime.timedelta(days=delta)
	month = ["None", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
	try:
		change_month = driver.find_element_by_xpath("//ul[@class='nav nav-tabs hidden-print']/li[@class='active']/following-sibling::li")
		change_month.click()
		schedules = driver.find_elements_by_xpath(f"//tr[td[div/span]]/td[contains(div, '{month[next_date.month]}')] | //tr[td[div/span]]/td[contains(div, '{month[next_date.month]}')]/following::td | //tr[td[div/span and contains(div, '{month[next_date.month]}')]]/following::tr/td")
		next_run = None
		for day in schedules:
			try:
				next_run = day.find_element_by_xpath(".//div[2]/*/a")
				if next_run:
					break
			except:
				next_date = next_date + datetime.timedelta(days=1)
				if next_date.weekday() >= 5:
					delta = 1 if next_date.weekday() == 6 else 2
					next_date = next_date + datetime.timedelta(days=delta)
		raw_start_time, raw_end_time = re.findall(r"\d{2}:\d{2}", next_run.text)
		next_start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(int(raw_start_time[:2]), int(raw_start_time[3:]))) + tz_offset
		next_matkul = next_run.get_attribute('data-kuliah')
		print(f"next run: {next_matkul} at {raw_start_time}-{raw_end_time} {next_date.strftime('%d/%m/%Y')}")
		res = scheduler(next_start_time, next_date)
		if res:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Scheduler failed...')
			popup(
				title = f"SIMA BOT V.{VER} - Error",
				message = f"Failed to schedule next run. Please run the program again or report to The Maker",
				app_icon = "favicon.ico"
			)
		else:
			print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Scheduler success!')
			popup(
				title = f"SIMA BOT V.{VER} - Scheduled!",
				message = f"next run: {next_matkul} at {raw_start_time}-{raw_end_time} {next_date.strftime('%d/%m/%Y')}",
				app_icon = "favicon.ico"
			)
		SCHEDULED = True
	except:
		print(b + '    [' + r + datetime.datetime.now().strftime("%H:%M") + b + '] ' + w + 'Next schedule cannot be found. Happy holiday! :)')
		popup(
			title = f"SIMA BOT V.{VER} - Happy Holiday After This!",
			message = f"No schedule found - Happy holiday!",
			app_icon = "favicon.ico"
		)
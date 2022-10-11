#!/usr/bin/env python3
# FOR BASECODE OF THIS PROJECT FOLLOWED PYTHON TUTORIAL:
# https://www.youtube.com/watch?v=zG-MMMTdA64&ab_channel=Indently and expanded

# WEATHER RETRIEVAL using openweathermap.org API and GUI application using tkinter -- #env -> pip3 install requests, pandas, tk, pillow
# openweathermap.org api, tkinter GUI framework, python3, pip
# Daniel Darcy

#Key IDEAS
# pip - is the de facto and recommended package-management system written in Python and is used to install
#	and manage software packages. It connects to an online repository of public packages, called the Python Package Index.

# API - An application programming interface is a way for two or more computer programs to communicate
#	with each other. It is a type of software interface, offering a service to other pieces of software.
#	A document or standard that describes how to build or use such a connection or interface is called an API specification.

import requests
import datetime
import pandas as pd
import calendar
from tkinter import *
from tkinter import ttk
import threading
import time
from PIL import Image, ImageTk


API_KEY = '45af2e1b0996895ecfca0348076ad6b2' #GLOBAL constant

# Helper Functions -------------------------------------------------------------------------------------
def button_press():
	global entry
	global string
	string = entry.get() #Extract string inputted by user from entry object and assign to global var string
	label.configure(text = string + " it is.\n Click the \"View Weather\" button.") #Print message with string
	ttk.Button(win, text = "View Weather",width = 10, command = win.destroy).pack(pady = 1) #Create a Button to quit window

def what_city(): #Collects user input to determine what city they want weather stats for
	this_city = input('What is your city?\n') #User inputs here
	#print(this_city) #TEST
	return this_city

def most_frequent(original_list): #Returns most frequent object in list
	return max(set(original_list), key = original_list.count)

def removes_duplicates(original_list): #Removes duplicates from list
	new_list = [] #Create new list
	for element in original_list: #For every element in the original list
		if element not in new_list: #If it is not present yet in the new list
			new_list.append(element) #Add it to the new list
	return new_list #Return the new list that has no duplicates

def preparation(min_temp, rain): #Returns message based on temperature and rainfall amount
	temp_message = '' #Instantiate temp message
	condition_message = 'have a nice day' #Instantiate conditional message

	if min_temp <= 0: #If the minimum temp is less than 0 you need a jacket
		temp_message = 'Wear a jacket'
	elif 0 < min_temp <= 10:
		temp_message = 'Wear a light jacket'
	elif 0 < min_temp <= 20:
		temp_message = 'Wear something casual'
	elif 0 < min_temp <= 30:
		temp_message = 'Wear something light'
	elif min_temp > 30:
		temp_message = 'Hide in shade'

	if rain > 5.0:
		condition_message = 'remember to bring an umbrella'
	return temp_message + ' & ' + condition_message #Return the temperature message and the conditional message together

def get_weather(cityname):
	base_url = 'https://api.openweathermap.org/data/2.5/forecast' #API
	payload = {'q': cityname, 'appid': API_KEY, 'units':'metric'}
	request = requests.get(url=base_url, params=payload)
	data = request.json()
	date_list, time_list, temp_list, condition_list, rain_list = [], [], [], [], []

	win2 = Tk()
	win2.geometry("600x500") #Set the geometry of Tkinter frame
	win2.resizable(False, False) #Makes user unable to resize window
	win2.title('Weather Results')
	#image for background
	image = Image.open("cloud.png") #Add file to project and use next line to resize
	resize_image = image.resize((600,500))
	bg = ImageTk.PhotoImage(resize_image)

	canvas2 = Canvas( win2, width = 600, height = 500) #Create canvas connect to frame and select size
	canvas2.pack(fill = "both") #Pack canvas
	canvas2.create_image( 0, 0, image = bg, anchor = "nw") #Add image to canvas
	ttk.Button(win2, text = "Quit",width = 5, command = win2.destroy).pack(pady = 1) #Create a Button to quit window
	win2.wm_geometry("500x550")

	for item in data['list']: #Find the below values in API documentation
		timestamp = item['dt']
		weather_condition = item['weather'][0]['description']
		temperature = item['main']['temp']

		try: #Prepare for possible error when there is no rain
			rain = item['rain']['3h']
		except Exception:
			rain = 0.0

		converted_timestamp = datetime.datetime.fromtimestamp(timestamp)
		time = converted_timestamp.time()
		current_date = converted_timestamp.date()

		#Adds all the elements wanted to proper new_list
		date_list.append(str(current_date))
		time_list.append(time)
		temp_list.append(temperature)
		condition_list.append(weather_condition)
		rain_list.append(rain)

	raw_data = { #Load lists into raw data Dictionary
		'date' : date_list,
		'time' : time_list,
		'temp' : temp_list,
		'conditions' : condition_list,
		'rain' : rain_list
	}

	df = pd.DataFrame(raw_data) #Load dictionary into dataframe, pd is for pandas import
	#print(df) #TEST PRINT DATAFRAME
	a=50 #Variables for text coordinates (x) (starting points)
	b=50 #(y)
	canvas2.create_text(a, 20, text=cityname + ' 5 Day Weather Forecast', fill="black", font=('Helvetica 20 bold'), anchor='nw')
	dates = removes_duplicates(date_list) #Remove duplicates from dates list
	for current_date in dates: #For this date is dates list
		new_df = df[df['date'].str.contains(current_date)] #Update dataframe
		#print() #Print row
		min_temp, max_temp = min(new_df.temp), max(new_df.temp) #Collect min and max temp from updated dataframe
		total_rain = round(sum(new_df.rain), 2) #Collect total rain from updated dataframe
		average_weather = most_frequent(new_df.conditions.tolist()) #Find most frequesnt weather conditions in updated dataframe

		#Get day of week from calendar
		t_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
		day_of_week = calendar.day_name[t_date.weekday()]

		#Display DataFrame - Use label instead of create text option
		#print(f'{t_date.day} {day_of_week}')
		canvas2.create_text(a, b, text=f'{t_date.day} {day_of_week}', fill="black", font=('Helvetica 15 bold'), anchor='nw')
		#print('-- Weather: ', average_weather, f'(Rain {total_rain}mm)')
		canvas2.create_text(a, b+15, text='-- Weather: ' + average_weather + f' with {total_rain}mm of rain', fill="black", font=('Helvetica 15 bold'), anchor='nw')
		#print(f'-- Min: {min_temp}°C -> Max: {max_temp}°C')
		canvas2.create_text(a, b+30, text=f'-- Min: {min_temp}°C -> Max: {max_temp}°C', fill="black", font=('Helvetica 15 bold'), anchor='nw')
		#print('--', preparation(min_temp, total_rain))
		temp_text = preparation(min_temp, total_rain)
		canvas2.create_text(a, b+45, text='-- ' + temp_text, fill="black", font=('Helvetica 15 bold'), anchor='nw')

		canvas2.pack()
		#a+=10
		b+=(15*5) #Change cursor position for next day

	#print()
	win2.mainloop()
	return df



#MAIN() -----------------------------------------------------------------------------------------------
win= Tk() #Create an instance of Tkinter frame
win.geometry("640x550") #Set the geometry of Tkinter frame
win.resizable(False, False) #Makes user unable to resize window
win.title('City Capture')

image = Image.open("tree.png") #Add file to project and use next line to resize
resize_image = image.resize((640,398))
bg = ImageTk.PhotoImage(resize_image)
canvas1 = Canvas( win, width = 640, height = 400) #Create canvas connect to frame and select size
canvas1.pack(fill = "both") #Pack canvas
canvas1.create_image( 0, 0, image = bg, anchor = "nw") #Add image to canvas

label = Label(win, text = "What city would you like the weather for?", font = ("Courier 22 bold")) #Initialize a Label to display the User Input
label.pack() #Pack label

entry = Entry(win, width = 15) #Create an Entry widget to accept User Input
entry.focus_set() #Sets users focused window to tkinter frame
entry.pack() #Pack text box
button1 = ttk.Button(win, text = "Submit",width = 5, command = button_press).pack(pady = 1) #Create a Button to validate Entry Widget

win.mainloop() #Loop which keeps tkinter frame open until exited
get_weather(string)

#
#
#
#
#
#
#
#
#

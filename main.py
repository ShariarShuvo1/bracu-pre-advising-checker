#https://github.com/ShariarShuvo1/bracu-pre-advising-checker
#Author: Md. Shariar Islam Shuvo
#email: shariaislamshuvo@gmail.com


from bs4 import BeautifulSoup
import requests
from tkinter import *
import tkinter.messagebox
import webbrowser


#Tkinter window setup
root = Tk()
root.title("Pre Advising Checker")
root.configure(background="black")

#setting window size
screen_height = 650
screen_width = 1150
root.geometry(f'{screen_width}x{screen_height}')


#--------------------- classes ----------------------#
class Subject:
    def __init__(self,name,faculty,section, totalSeat,seatBooked,seatAvailable,day1,day2,lab1,lab2,classTime_start,classTime_end,labTime1_start,labTime2_start,labTime1_end,labTime2_end,classRoomNumber,labRoomNumber):
        self.name = name
        self.faculty =faculty
        self.section = section
        self.totalSeat = totalSeat
        self.seatBooked = seatBooked
        self.seatAvailable = seatAvailable
        self.day1 = day1
        self.day2 = day2
        self.lab1 = lab1
        self.lab2 = lab2
        self.classTime_start = classTime_start
        self.classTime_end = classTime_end
        self.labTime1_start = labTime1_start
        self.labTime1_end = labTime1_end
        self.labTIme2_start = labTime2_start
        self.labTIme2_end = labTime2_end
        self.classRoomNumebr = classRoomNumber
        self.labRoomNumber = labRoomNumber

    def __str__(self):
        st = f'{self.section: ^15}{self.name: <13}{self.faculty: <14}{self.seatAvailable: <6}{self.classTime_start: <15}'
        return st


#Check Internet
def internetAvailable():
    availale = False
    url = "https://admissions.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus"
    timeout = 10
    try:
        requests.get(url,timeout=timeout)
        availale = True
    except(requests.ConnectionError,requests.Timeout) as exception:
        availale = False
    return availale


# Function for checking the key pressed and updating the listbox ##used geeksforgeeks code
def checkkey(event):
	value = event.widget.get()
	# get data from l
	if value == '':
		data = courseList
	else:
		data = []
		for item in courseList:
			if value.lower() in str(item).lower():
				data.append(item)
	# update data in listbox
	update(data)

###used geeksforgeeks code
def update(data):
	
	# clear previous data
	courseListViewer.delete(0, 'end')
	# put new data
	for item in data:
		courseListViewer.insert('end', str(item))


if internetAvailable() == False:
    #adding error text
    noInternetLabel = Label(root, text = "Please Connect to the internet\nand restart the application!", bg = "red", fg="black", font=("Arial",45))
    noInternetLabel.place(x=screen_width//2,y=screen_height//2,anchor=CENTER)

else:
    s=requests.Session()
    html = s.get("https://admissions.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus")
    html = BeautifulSoup(html.content,'html.parser')
    rawData = html.find_all('tr')
    allSubjects = list()


    for tr in rawData:
        td = tr.find_all('td')
        name = str(td[1])[str(td[1]).find('>')+1:str(td[1]).find('</'):]
        faculty = str(td[3])[str(td[3]).find('>')+1:str(td[3]).find('</'):]
        section = str(td[5])[str(td[5]).find('>')+1:str(td[5]).find('</'):]
        if(len(section)>3):
            section = int(section[:2])
        else:
            section = int(section)
        totalSeat = int(str(td[7])[str(td[7]).find('>')+1:str(td[7]).find('</'):])
        seatBooked = int(str(td[8])[str(td[8]).find('>')+1:str(td[8]).find('</'):])
        seatAvailable = int(str(td[9])[str(td[9]).find('>')+1:str(td[9]).find('</'):])
        dateTimetxt=str(td[6])[str(td[6]).find('>')+1:str(td[6]).find('</'):]
        timeSlots = list(dateTimetxt.split(')'))
        timeSlots = timeSlots[:len(timeSlots)-1]
        tempList = list()
        for i in range(len(timeSlots)):
            if i ==0:
                tempList.append(timeSlots[i])
            else:
                tempList.append(timeSlots[i][1:])
        timeSlots = tempList
        

        def dayGetter(day1):
            if day1=='Sa':
                day1='Saturday'
            elif day1=='Su':
                day1='Sunday'
            elif day1=='Mo':
                day1='Monday'
            elif day1=='Tu':
                day1='Tuesday'
            elif day1=='We':
                day1='Wednesday'
            elif day1=='Th':
                day1='Thursday'
            elif day1=='Fr':
                day1="Friday"
            return day1
        def stringSeparator(timeSlots):
            if len(timeSlots)==4:
                if(timeSlots[0][:2] == timeSlots[1][:2]):
                    l1 = 0
                    l2 = 1
                    c1 = 2
                    c2 = 3
                elif timeSlots[0][:2] == timeSlots[2][:2]:
                    l1 = 0
                    l2 = 2
                    c1 = 1
                    c2 = 3
                elif timeSlots[0][:2] == timeSlots[3][:2]:
                    l1 = 0
                    l2 = 3
                    c1 = 1
                    c2 = 2
                elif timeSlots[1][:2] == timeSlots[2][:2]:
                    l1 = 1
                    l2 = 2
                    c1 = 0
                    c2 = 3
                elif timeSlots[1][:2] == timeSlots[3][:2]:
                    l1 = 1
                    l2 = 3
                    c1 = 0
                    c2 = 2
                elif timeSlots[2][:2] == timeSlots[3][:2]:
                    l1 = 2
                    l2 = 3
                    c1 = 0
                    c2 = 1
                else:
                    l1=0
                    l2=1
                    c1=2
                    c2=3
                
                lab1 = dayGetter(timeSlots[l1][:2])
                lab2 = dayGetter(timeSlots[l2][:2])

                labTime1_start = timeSlots[l1][3:11]
                labTime1_end = timeSlots[l1][12:20]

                labTime2_start = timeSlots[l2][3:11]
                labTime2_end = timeSlots[l2][12:20]

                labRoomNumber = timeSlots[l1][21:]

                day1 = dayGetter(timeSlots[c1][:2])
                day2 = dayGetter(timeSlots[c2][:2])

                classTime_start = timeSlots[c1][3:11]
                classTime_end = timeSlots[c1][12:20]
                classRoomNumber = timeSlots[c1][21:]
            else:
                c1,c2,l1=(0,1,2)
                lab1 = dayGetter(timeSlots[l1][:2])
                lab2 = ''

                labTime1_start = timeSlots[l1][3:11]
                labTime1_end = timeSlots[l1][12:20]

                labTime2_start = ''
                labTime2_end = ''

                labRoomNumber = timeSlots[l1][21:]

                day1 = dayGetter(timeSlots[c1][:2])
                day2 = dayGetter(timeSlots[c2][:2])

                classTime_start = timeSlots[c1][3:11]
                classTime_end = timeSlots[c1][12:20]
                classRoomNumber = timeSlots[c1][21:]
            

            return (lab1,lab2,labTime1_start,labTime1_end,labTime2_start,labTime2_end,labRoomNumber,day1,day2,classTime_start,classTime_end,classRoomNumber)
                
        
        day1 =''
        day2 = ''
        lab1= ''
        lab2 = ''
        classTime_start =''
        classTime_end =''
        labTime1_start = ''
        labTime1_end = ''
        labTime2_start = ''
        labTime2_end = ''
        classRoomNumber =''
        labRoomNumber =''

        if len(timeSlots)==1:
            day1 = dayGetter(timeSlots[0][:2])
            classTime_start = timeSlots[0][3:11]
            classTime_end = timeSlots[0][12:20]
            classRoomNumber = timeSlots[0][21:]
        elif len(timeSlots)==2:
            day1 = dayGetter(timeSlots[0][:2])
            day2 = dayGetter(timeSlots[1][:2])
            classTime_start = timeSlots[0][3:11]
            classTime_end = timeSlots[0][12:20]
            classRoomNumber = timeSlots[0][21:]
            
        else:
            lab1,lab2,labTime1_start,labTime1_end,labTime2_start,labTime2_end,labRoomNumber,day1,day2,classTime_start,classTime_end,classRoomNumber = stringSeparator(timeSlots)
            
        
        obj = Subject(name,faculty,section, totalSeat,seatBooked,seatAvailable,day1,day2,lab1,lab2,classTime_start,classTime_end,labTime1_start,labTime2_start,labTime1_end,labTime2_end,classRoomNumber,labRoomNumber)
        allSubjects.append(obj)


    courseList = allSubjects





    #------------------- GUI ---------------------------#
    mainFrame = LabelFrame(root,text = "Pre Advising",bg='black')
    mainFrame.grid(row=0,column=0,sticky='n')


    #Search Text
    searchTag = Label(mainFrame,text="Search:",font=("Ariel",15),bg='black')
    searchTag.grid(row=0,column=0,sticky='w')

    #Search box
    entryBox = Entry(mainFrame,width=31,fg='yellow')
    entryBox.grid(row=0,column=1)
    entryBox.bind('<KeyRelease>', checkkey)

    #Titles
    titleString = f"{'Section':<10}{'Course':<12}{'Faculty':<13}{'Free':<10}{'Time':<10}"
    titleForList = Label(mainFrame,text=titleString, font = ("Ariel",13),fg='yellow')
    titleForList.grid(row=1,column=1,sticky='w')
    

    #list box
    courseListViewer = Listbox(mainFrame,width= 33,height = 15)
    courseListViewer.grid(row=2,column=1,sticky='w')
    update(courseList)
    

    selectedCourses = list()






    #--------------------------------RIGHT--------------------------------#
    # Function for checking the key pressed and updating the listbox ##used geeksforgeeks code
    def checkkey_right(event):
        value = event.widget.get()
        # get data from l
        if value == '':
            data = selectedCourses
        else:
            data = []
            for item in selectedCourses:
                if value.lower() in str(item).lower():
                    data.append(item)
        # update data in listbox
        update_right(data)

    ###used geeksforgeeks code
    def update_right(data):
        
        # clear previous data
        courseListViewer_right.delete(0, 'end')
        # put new data
        for item in data:
            courseListViewer_right.insert('end', str(item))
    
    #Right viewer

    #Search box
    entryBox_right = Entry(mainFrame,width=31,fg='yellow')
    entryBox_right.grid(row=0,column=3)
    entryBox_right.bind('<KeyRelease>', checkkey_right)

    #Titles
    titleForList_right = Label(mainFrame,text=titleString, font = ("Ariel",13),fg='yellow')
    titleForList_right.grid(row=1,column=3,sticky='w')

    #list box
    courseListViewer_right = Listbox(mainFrame,width= 33,height = 15)
    courseListViewer_right.grid(row=2,column=3,sticky='w')
    update_right(selectedCourses)
    #--------------------------------RIGHT--------------------------------#


    #--------------------------------Table--------------------------------#
    frame = LabelFrame(root,text="Class Schedule",bg='black')
    frame.grid(row = 1, column=0,sticky='n',padx=0,pady=0)


    totalRow = 8
    totalColumn = 8
    dayNameList = ['Day/Time','Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
    timeNameList = ['08:00 AM\n08:20 AM','09:30 AM\n10:50 AM','11:00 AM\n12:20 PM','12:30 PM\n01:50 PM','02:00 PM\n03:20 PM','03:30 PM\n04:50 PM','05:00 PM\n06:20 PM']
    table = {
        'Saturday': {'08:00 AM': [],'09:30 AM': [],'11:00 AM': [],'12:30 PM': [],'02:00 PM': [],'03:30 PM': [],'05:00 PM': []},
        'Sunday': {'08:00 AM': [],'09:30 AM': [],'11:00 AM': [],'12:30 PM': [],'02:00 PM': [],'03:30 PM': [],'05:00 PM': []},
        'Monday': {'08:00 AM': [],'09:30 AM': [],'11:00 AM': [],'12:30 PM': [],'02:00 PM': [],'03:30 PM': [],'05:00 PM': []},
        'Tuesday': {'08:00 AM': [],'09:30 AM': [],'11:00 AM': [],'12:30 PM': [],'02:00 PM': [],'03:30 PM': [],'05:00 PM': []},
        'Wednesday': {'08:00 AM': [],'09:30 AM': [],'11:00 AM': [],'12:30 PM': [],'02:00 PM': [],'03:30 PM': [],'05:00 PM': []},
        'Thursday': {'08:00 AM': [],'09:30 AM': [],'11:00 AM': [],'12:30 PM': [],'02:00 PM': [],'03:30 PM': [],'05:00 PM': []},
        'Friday': {'08:00 AM': [],'09:30 AM': [],'11:00 AM': [],'12:30 PM': [],'02:00 PM': [],'03:30 PM': [],'05:00 PM': []},
    }
    for r in range(totalRow):
        for c in range(totalColumn):
            if r==0:
                lbl = Label(frame,text=dayNameList[c],font=("Ariel",10,'bold'),fg='#b8b8b8',width=13,height=2,borderwidth=1,relief = 'solid',padx=0,pady=0)
            elif r>0 and c==0:
                lbl = Label(frame,text=timeNameList[r-1],font=("Ariel",10,'bold'),fg='#b8b8b8',width=13,height=3,borderwidth=1,relief = 'solid',padx=0,pady=0)
            else:
                lbl = Label(frame,text="",font=("Ariel",10),fg='white',width=13,height=3,borderwidth=1,relief = 'solid',padx=0,pady=0)
                table[dayNameList[c]][timeNameList[r-1][:8]].append(lbl)
            lbl.grid(row=r,column=c)

    def update_table(selectedCourses):
        for val in table.values():
            for v in val.values():
                v[0].config(text='',fg='white')
        for course in selectedCourses:
            if len(table[course.day1][course.classTime_start][0].cget('text'))<1 and (table[course.day1][course.classTime_start][0].cget('text') != f'{course.name} - Theory'):
                table[course.day1][course.classTime_start][0].config(text=f'{course.name} - Theory')
            elif len(table[course.day1][course.classTime_start][0].cget('text'))>1  and (table[course.day1][course.classTime_start][0].cget('text') != f'{course.name} - Theory'):
                st = table[course.day1][course.classTime_start][0].cget('text')
                st+= f'\n{course.name} - Theory'
                table[course.day1][course.classTime_start][0].config(text=st,fg='red')
            
            if len(table[course.day2][course.classTime_start][0].cget('text'))<1 and (table[course.day2][course.classTime_start][0].cget('text') != f'{course.name} - Theory'):
                table[course.day2][course.classTime_start][0].config(text=f'{course.name} - Theory')
            elif len(table[course.day2][course.classTime_start][0].cget('text'))>1  and (table[course.day2][course.classTime_start][0].cget('text') != f'{course.name} - Theory'):
                st = table[course.day2][course.classTime_start][0].cget('text')
                st+= f'\n{course.name} - Theory'
                table[course.day2][course.classTime_start][0].config(text=st,fg='red')
            
            if len(course.lab1)>2:
                if len(table[course.lab1][course.labTime1_start][0].cget('text'))<1 and (table[course.lab1][course.labTime1_start][0].cget('text') != f'{course.name} - LAB'):
                    table[course.lab1][course.labTime1_start][0].config(text=f'{course.name} - LAB',fg='#a3bfff')
                elif len(table[course.lab1][course.labTime1_start][0].cget('text'))>1  and (table[course.lab1][course.labTime1_start][0].cget('text') != f'{course.name} - LAB'):
                    st = table[course.lab1][course.labTime1_start][0].cget('text')
                    st+= f'\n{course.name} - LAB'
                    table[course.lab1][course.labTime1_start][0].config(text=st,fg='red')
                
                if len(table[course.lab2][course.labTIme2_start][0].cget('text'))<1 and (table[course.lab2][course.labTIme2_start][0].cget('text') != f'{course.name} - LAB'):
                    table[course.lab2][course.labTIme2_start][0].config(text=f'{course.name} - LAB',fg='#a3bfff')
                elif len(table[course.lab2][course.labTIme2_start][0].cget('text'))>1  and (table[course.lab2][course.labTIme2_start][0].cget('text') != f'{course.name} - LAB'):
                    st = table[course.lab2][course.labTIme2_start][0].cget('text')
                    st+= f'\n{course.name} - LAB'
                    table[course.lab2][course.labTIme2_start][0].config(text=st,fg='red')

                
    #--------------------------------Table--------------------------------#

    def subjectAvailability(name):
        for ele in selectedCourses:
            if name == ele.name:
                return True
        return False


    def sectionFinder(section,subject):
        if len(selectedCourses)==8:
            tkinter.messagebox.showinfo("Error!","You have already selected maximum number of courses for 1 semester")
        else:
            for obj in courseList:
                if obj.name == subject and obj.section == section and subjectAvailability(subject):
                    tkinter.messagebox.showinfo("Error!","This subject has already been added")
                    break
                elif obj.name == subject and obj.section == section and obj.seatAvailable<1:
                    tkinter.messagebox.showinfo("Error!","This class is already full")
                    break
                elif obj.name == subject and obj.section == section:
                    selectedCourses.append(obj)
                    break

    #Buttons
    def addBut():
        st = courseListViewer.get(ANCHOR)
        if(len(st)!=0):
            sectionFinder(int(st.split()[0]),st.split()[1])
        else:
            tkinter.messagebox.showinfo("Error!","To add, select from the left panle")
        update_table(selectedCourses)
        update_right(selectedCourses)
    


    def removeBut():
        st = courseListViewer_right.get(ANCHOR)
        if(len(st) ==0):
            tkinter.messagebox.showinfo("Error!","To remove, select from the right panle")
            return
        section = int(st.split()[0])
        subject = st.split()[1]
        obj = None
        for i in range (len(selectedCourses)):
            if selectedCourses[i].section == section and selectedCourses[i].name==subject:
                obj = selectedCourses[i]
                break
        selectedCourses.remove(obj)
        update_table(selectedCourses)
        update_right(selectedCourses)

    def clearBut():
        selectedCourses.clear()
        update_table(selectedCourses)
        update_right(selectedCourses)

    #Add
    addButton = Button(mainFrame,text='Add',command=addBut,font = ('Ariel',15,'bold'), width =6, fg = 'green',padx=0,pady=0)
    addButton.grid(row=2,column=2,sticky='n')
    #Remove
    removeButton = Button(mainFrame,text='Remove',command=removeBut,font = ('Ariel',15,'bold'),width =6,fg='red',padx=0,pady=0)
    removeButton.grid(row=2,column=2,sticky='w')

    #clear
    removeButton = Button(mainFrame,text='Clear',command=clearBut,font = ('Ariel',15,'bold'),width =6,fg='black',padx=0,pady=0)
    removeButton.grid(row=2,column=2,sticky='s')

    #------------------ GUI ----------------------#


    #------------------ Details Panle -----------------------#
    details = LabelFrame(root,text='Details')
    details.grid(row=0,column=1,sticky='n',padx=10,pady=10)

    detailsLabel = Label(details,text = "",font =('Arial',20,'bold'))
    detailsLabel.grid(row=1,column=0,sticky='w')
    Label(details,text=f'Course Initial:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=2,column=0,sticky='w')
    Label(details,text=f'Faculty:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=3,column=0,sticky='w')
    Label(details,text=f'Section:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=4,column=0,sticky='w')
    Label(details,text=f'Total Seat:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=5,column=0,sticky='w')
    Label(details,text=f'Seat Booked:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=6,column=0,sticky='w')
    Label(details,text=f'Free Seat:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=7,column=0,sticky='w')
    Label(details,text=f'Theory Class:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=8,column=0,sticky='w')
    Label(details,text=f'Theory Class Time:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=9,column=0,sticky='w')
    Label(details,text=f'Class Room:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=10,column=0,sticky='w')
    Label(details,text=f'Lab Class:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=11,column=0,sticky='w')
    Label(details,text=f'Theory Class Time:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=12,column=0,sticky='w')
    Label(details,text=f'Lab Room:',font =('Arial',13),width=20,fg='yellow',borderwidth=1,relief = 'solid',padx=0,pady=0).grid(row=13,column=0,sticky='w')


    label1=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label1.grid(row=2,column=1,sticky='w')
    label2=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label2.grid(row=3,column=1,sticky='w')
    label3=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label3.grid(row=4,column=1,sticky='w')
    label4=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label4.grid(row=5,column=1,sticky='w')
    label5=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label5.grid(row=6,column=1,sticky='w')
    label6=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label6.grid(row=7,column=1,sticky='w')
    label7=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label7.grid(row=8,column=1,sticky='w')
    label8=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label8.grid(row=9,column=1,sticky='w')
    label9=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label9.grid(row=10,column=1,sticky='w')
    label10=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label10.grid(row=11,column=1,sticky='w')
    label11=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label11.grid(row=12,column=1,sticky='w')
    label12=Label(details,text=f'',font =('Arial',13),width=20,fg='#fc03f0',borderwidth=1,relief = 'solid',padx=0,pady=0)
    label12.grid(row=13,column=1,sticky='w')
    
    def detailsBut():
        stx = courseListViewer.get(ANCHOR)
        section = int(stx.split()[0])
        subject = stx.split()[1]
        currentObj = None
        for obj in courseList:
            if obj.name == subject and obj.section == section:
                currentObj = obj
                break
        
        label1.config(text=f'{currentObj.name}')
        label2.config(text=f'{currentObj.faculty}')
        label3.config(text=f'{currentObj.section}')
        label4.config(text=f'{currentObj.totalSeat}')
        label5.config(text=f'{currentObj.seatBooked}')
        label6.config(text=f'{currentObj.seatAvailable}')
        label7.config(text=f'{currentObj.day1}, {currentObj.day2}')
        label8.config(text=f'{currentObj.classTime_start} - {currentObj.classTime_end}')
        label9.config(text=f'{currentObj.classRoomNumebr}')
        label10.config(text=f'{currentObj.lab1}')
        label11.config(text=f'{currentObj.labTime1_start} - {currentObj.labTIme2_end}')
        label12.config(text=f'{currentObj.labRoomNumber}')



    detailsButton = Button(details,text = 'Show Details',command=detailsBut,font = ('Ariel',15,'bold'),width =12,fg='#5c0049',padx=0,pady=0)
    detailsButton.grid(row=0,column=0,sticky='w')

    

    #------------------ Details Panle -----------------------#

    #------------------ Linkes --------------------#
    def callback(url):
        webbrowser.open_new(url)

    github = Label(root,text='GitHub', fg="blue", bg='black', cursor="hand",font=("bold"))
    github.grid(row=1,column=1,sticky='sw')
    github.bind("<Button-1>",lambda e: callback("https://github.com/ShariarShuvo1/bracu-pre-advising-checker"))


    myName = Label(root,text='Made by: Shariar Islam Shuvo',fg='yellow',bg='black',cursor='hand')
    myName.grid(row=1,column=1,sticky='s')
    myName.bind("<Button-1>",lambda e: callback("https://www.facebook.com/ShariarShuvo01/"))
    #------------------ Linkes --------------------#





root.mainloop()
#Importing Necessary Libraries
import socket, requests, webbrowser, pyperclip
import tkinter
from tkinter import StringVar
from tkinter import IntVar

#Defining the size of GUI
root = tkinter.Tk()
root.title("LINK SHORTENER AND EXPANDER")
root.geometry("735x362")
root.resizable(False,False)
root.configure(bg='grey20')

#defining variables
i = IntVar()
i.set(4)
stats = StringVar("")
res = StringVar("")
inp = StringVar("")

#defining the function to check the status of api's server
def connect(a):
    i.set(a)
    if a==1:
        c = "chilp.it"
    if a==2:
        c = 'clck.ru'
    if a==3:
        c = 'qps.ru'
    if a==4:
        c = 'tinyurl.com'
    if a==5:
        c = 'is.gd'
    if a==6:
        c = '0x0.st'
    try:
        socket.gethostbyname(c)
        stats.set("[ API >> {} ] [  Connected  ]".format(c))
    except socket.gaierror:
        stats.set("[ API >> {} ] [  No Internet  ]".format(c))

#Pinging to the url shortener
def ping(txt):
    connect(i.get())
    x = stats.get()
    stats.set(txt + x)

ping("Welcome ")

#Defining the function to shorten a URL
def make_shorten(url):
    if not (url.startswith('http://') or url.startswith('https')):
        url = "http://" + url
    if i.get() == 1:
        response = requests.get("http://chilp.it/api.php",params={"url": url})
        if response.ok:
            return response.text.strip()
    if i.get() == 2:
        response = requests.get("https://clck.ru/--",params={"url": url})
        if response.ok:
            return response.text.strip()
    if i.get() == 3:
        response = requests.get("http://qps.ru/api",params={"url": url})
        if response.ok:
            return response.text.strip()
    if i.get() == 4:
        response = requests.get("http://tinyurl.com/api-create.php",params={"url": url})
        if response.ok:
            return response.text.strip()
    if i.get() == 5:
        response = requests.get("https://is.gd/create.php",params={"format": "simple", "url": url})
        if response.ok:
            return response.text.strip()
    if i.get() == 6:
        response = requests.post("https://0x0.st",data={"shorten": url})
        if response.ok:
            return response.text.strip()
    
#defining the function to clear the fields
def reset():
    inp.set("")
    res.set("")
    ping("Ready ")

#defining the function to run when "Shorten Itt!!" Button is pressed
def short():
    res.set("")
    ping("Error...No Link Found ")
    if(inp.get() != ""):
        xl = make_shorten(inp.get())
        res.set(xl)
        stats.set("Done, Copy Shortened link")

#defining the function to run when "UnShorten Itt!!" Button is pressed
def unshort():
    inp.set("")
    ping("Error...No Link Found ")
    if(res.get() != ""):
        c = res.get()
        if not c.startswith('https://'):
            c = 'https://' + c
        r = requests.get(c)
        stats.set("Done, Copy Original link")
        inp.set(r.url)

def open_lnk(v,x):
    if(v!="" and not (v.startswith('could') or v.startswith('Well'))):
        if not (v.startswith('http://') or v.startswith('https://')):
            v = "https://" + v
        if(x==2):
            ping("opening Original link in default browser..")
            webbrowser.open(v)
        elif(x==1):
            ping("opening shortened link in default browser..")
            webbrowser.open(v) 

def copy_clip(v,x):
    if(v!="" and not (v.startswith('could') or v.startswith('well'))):
        if(x==2):
            stats.set("Copied Original link to clipboard!!")
            pyperclip.copy(v)
        elif(x==1):
            stats.set("Copied Shortened link to clipboard!!")
            pyperclip.copy(v)

def click3():
    #api window configuration from here
    stats.set("Please Select api..")
    window = tkinter.Tk()
    window.title("Change API")
    window.resizable(False,False)
    window.configure(bg='grey90')
    
    def clickw():
        ping("API selected....")
        window.destroy()

    tkinter.Label(window, font = ('arial', 12, 'bold'),fg ="red",bg = "grey90",
    text = "Select APIs from below :", bd = 16, anchor = "center").grid(row=1)

    tkinter.Radiobutton(window,bg = "grey90",font = ('arial', 10, 'bold'),text="chilp.it",width=8,variable="",value=1,command=lambda:connect(1)).grid(row=2)
    tkinter.Radiobutton(window,bg = "grey90",font = ('arial', 10, 'bold'),text="clck.ru",width=8,variable="",value=2,command=lambda:connect(2)).grid(row=3)
    tkinter.Radiobutton(window,bg = "grey90",font = ('arial', 10, 'bold'),text="qps.ru",width=8,variable="",value=3,command=lambda:connect(3)).grid(row=4)
    tkinter.Radiobutton(window,bg = "grey90",font = ('arial', 10, 'bold'),text="tinyurl.com",width=8,variable="",value=4,command=lambda:connect(4)).grid(row=5)
    tkinter.Radiobutton(window,bg = "grey90",font = ('arial', 10, 'bold'),text="is.gd",width=8,variable="",value=5,command=lambda:connect(5)).grid(row=6)
    tkinter.Radiobutton(window,bg = "grey90",font = ('arial', 10, 'bold'),text="0x0.st",width=8,variable="",value=6,command=lambda:connect(6)).grid(row=7)
    
    tkinter.Label(window,bg ="grey90",text = "* radio button checks all by default\ndon't worry select ur api by clicking it *",
    relief="groove",borderwidth = 2, anchor = "center").grid(row=9,columnspan=1,sticky=(tkinter.W+tkinter.E))

    tkinter.Button(window,fg = "green",bg = "grey90",
    font = ('comic sans ms', 10, 'bold italic'),width = 12,text = "click me after\nselecting api",command = clickw).grid(row = 8) 
    
tkinter.Label(root, font = ('arial', 16, 'bold'),
text = "Original Link :",fg ="white",bg ="grey20", bd = 8, anchor = "w").grid(row=0) 

#display/enter the original link
tkinter.Entry(root,font = ('arial', 16, 'bold'),
textvariable = inp, bd = 10, width = 30, bg = "powder blue").grid(row=0,column=1)

#button to copy link to clipboard
tkinter.Button(root,bd = 4,fg = "white", text = "Copy to\nClipboard", bg = "green",command = lambda:copy_clip(inp.get(),2)).grid(row = 0,column=2)

#button to open link in browser
tkinter.Button(root,bd = 4,fg = "black", text = "Open in\nBrowser", bg = "pink",command = lambda:open_lnk(inp.get(),2)).grid(column=3,row = 0) 

tkinter.Label(root,font = ('arial', 16, 'bold'),
text = "SHORTENED LINK :",fg ="white",bg ="grey20", bd = 16, anchor = "w").grid(row=1) 

#display/enter the Modified (shortened) link
tkinter.Entry(root,font = ('arial', 16, 'bold'),
textvariable = res, bd = 10, width = 30,bg = "powder blue").grid(column =1,row=1)

#button to copy link to clipboard
tkinter.Button(root,bd = 4,fg = "white",text = "Copy to\nClipboard", bg = "green",command = lambda:copy_clip(res.get(),1)).grid(row = 1,column=2)

#button to open link in browser
tkinter.Button(root,bd = 4,fg = "black",text = "Open in\nBrowser", bg = "pink",command = lambda:open_lnk(res.get(),1)).grid(column=3,row = 1) 

#display the program status
tkinter.Label(root,font = ('arial', 12, 'bold'),fg ="snow",bg ="grey20",
textvariable = stats,relief=tkinter.SUNKEN,anchor = "e").grid(row=7,columnspan=4,sticky=(tkinter.W+tkinter.NE))

#button to run shorten link process
tkinter.Button(root,padx = 8,pady = 4,bd = 8,fg = "black",
font = ('comic sans ms', 16, 'bold italic'),width = 10,text = "SHORT IT!!", bg = "gold",command = short).grid(row = 2) 

#button to Unshortened the link
tkinter.Button(root,padx = 8, pady = 4, bd = 8,fg = "black",
font = ('comic sans ms', 16, 'bold italic'),width = 10, text = "UnSHORT IT!!", bg = "gold",command = unshort).grid(column =1,row = 2,columnspan=3)

#button to clear the fields
tkinter.Button(root,padx = 8,pady = 4,bd = 8,fg = "black",
font = ('arial', 16, 'bold'),width = 10, text = "Clear Fields", bg = "light green",command = reset).grid(row = 3)

#button to change the api's
tkinter.Button(root,padx = 8,pady = 4,bd = 8,fg = "white",
font = ('arial', 16, 'bold'),width = 10, text = "Change API**", bg = "blue",command = click3).grid(row = 3,column=1,columnspan=3)

#button to check the internet
tkinter.Button(root,padx = 8,pady = 4,bd = 8,fg = "black",
font = ('arial', 16, 'bold'),width = 10, text = "Reconnect*", bg = "brown",command = lambda: connect(i.get())).grid(row = 5) 

#button to exit the program
tkinter.Button(root,padx = 8, pady = 4, bd = 8,fg = "yellow", 
font = ('arial', 16, 'bold'),width = 10, text = "EXIT", bg = "red",command = root.quit).grid(column =1,row = 5,columnspan=3)

tkinter.Label(root, font = ('arial', 12, 'bold'),fg ="snow",bg ="grey20",
text = "*Requires Internet Connection\n**Change the Shortened link provider").grid(row=6,columnspan=4) 

root.mainloop()
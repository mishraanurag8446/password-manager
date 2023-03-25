import time
import tkinter as tk
from tkinter import TOP, Y, Label, BOTTOM, X
from tkinter import Frame
import pyperclip
from dbconfig import validateMasterPassword, addEntry, retrieveEntries
from generate import generatePassword

root = tk.Tk()
root.geometry('450x400')
root.title('Password Manager')
haderFrame = Frame(root, bg="gray", borderwidth=2)
haderFrame.pack(side=TOP, fill=Y)
mainFrame = Frame(root)
mainFrame.pack()

statusColor = {'w': 'orange', 'f': 'red', 's': 'green'}

passwordValue, siteNameValue, siteUrlValue, usernameValue, emailValue = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

choosePassCombination = tk.StringVar()
statusValue = tk.StringVar()
status = tk.StringVar()


# siteName = tk.StringVar()
# siteName = tk.StringVar()
# siteName = tk.StringVar()


def verify_login():
    setStatus(status, 'Connecting..', statusColor.get('w'))
    res = validateMasterPassword(passwordValue.get())
    time.sleep(1)
    if res:
        print('password is correct')
        passwordValue.set('')
        loadAddEntry(root, haderFrame, mainFrame)
        setStatus(status, 'Ready', statusColor.get('s'))
    else:
        setStatus(status, 'Invalid username and password', statusColor.get('f'))


def loadLogin(hframe, mframe):
    Label(hframe, text="Login", font=("Arial", 14, "bold")).pack()
    # Create and pack the password label and entry
    password_label = tk.Label(mframe, text="Master Password:")
    password_label.grid(row=2, column=0, padx=15, pady=15)
    password_entry = tk.Entry(mframe, textvariable=passwordValue, show="*")
    password_entry.grid(row=2, column=1, padx=15, pady=15)

    # Create and pack the login button
    login_button = tk.Button(mframe, text="Login", command=verify_login)
    login_button.grid(row=3, column=1, padx=15, pady=15)


def setMenuOption(root):
    mainMenu = tk.Menu(root)
    optionMenu = tk.Menu(mainMenu, tearoff=0)
    optionMenu.add_command(label="Add Entry", command=menuAddEntry)
    optionMenu.add_command(label="Search Entry", command=menuSearchEntry)
    optionMenu.add_command(label="Generate Password", command=menuGeneratePassword)
    root.config(menu=mainMenu)
    mainMenu.add_cascade(label="Menu", menu=optionMenu)


def menuAddEntry():
    loadAddEntry(root, haderFrame, mainFrame)


def menuSearchEntry():
    loadSearchEntry(haderFrame, mainFrame)


def menuGeneratePassword():
    loadGeneratePassword(root, haderFrame, mainFrame)


def loadAddEntry(root, hframe, mframe):
    # Create and pack the password label and entry
    # sitename, siteurl, email, username
    setMenuOption(root)
    # mframe.destroy()
    # hframe.destroy()
    # hframe = Frame(root, bg="gray", borderwidth=2)
    # hframe.pack(side=TOP, fill=Y)
    # mframe = Frame(root)
    # mframe.pack()
    clearFrame(hframe, mframe)

    Label(hframe, text="Add Entry", font=("Arial", 14, "bold")).pack()

    password_label = tk.Label(mframe, text="Site name:")
    password_label.grid(row=2, column=0, padx=15, pady=15)
    password_entry = tk.Entry(mframe, textvariable=siteNameValue)
    password_entry.grid(row=2, column=1, padx=15, pady=15)

    password_label = tk.Label(mframe, text="Site URL:")
    password_label.grid(row=3, column=0, padx=15, pady=15)
    password_entry = tk.Entry(mframe, textvariable=siteUrlValue)
    password_entry.grid(row=3, column=1, padx=15, pady=15)

    password_label = tk.Label(mframe, text="Email :")
    password_label.grid(row=4, column=0, padx=15, pady=15)
    password_entry = tk.Entry(mframe, textvariable=emailValue)
    password_entry.grid(row=4, column=1, padx=15, pady=15)

    password_label = tk.Label(mframe, text="Username")
    password_label.grid(row=5, column=0, padx=15, pady=15)
    password_entry = tk.Entry(mframe, textvariable=usernameValue)
    password_entry.grid(row=5, column=1, padx=15, pady=15)

    password_label = tk.Label(mframe, text="Password")
    password_label.grid(row=6, column=0, padx=15, pady=15)
    password_entry = tk.Entry(mframe, textvariable=passwordValue, show="*")
    password_entry.grid(row=6, column=1, padx=15, pady=15)

    # Create and pack the login button
    login_button = tk.Button(mframe, text="Add", command=clickAddEntry)
    login_button.grid(row=7, column=1, padx=15, pady=15)


def clickAddEntry():
    addEntry(sitename=siteNameValue.get(), siteurl=siteUrlValue.get(), email=emailValue.get(),
             username=usernameValue.get(),
             password=passwordValue.get())
    setStatus(status, f'{siteNameValue.get()} entry added', statusColor.get('w'))
    siteNameValue.set('')
    siteUrlValue.set('')
    emailValue.set('')
    usernameValue.set('')
    passwordValue.set('')


def loadSearchEntry(hframe, mframe):
    # Create and pack the password label and entry
    # sitename, siteurl, email, username
    # mframe.destroy()
    # hframe.destroy()
    # hframe = Frame(root, bg="gray", borderwidth=2)
    # hframe.pack(side=TOP, fill=Y)
    # mframe = Frame(root)
    # mframe.pack()

    clearFrame(hframe, mframe)

    Label(hframe, text="Search Entry", font=("Arial", 14, "bold")).pack()

    password_label = tk.Label(mframe, text="Site name: or")
    password_label.grid(row=2, column=0, padx=15, pady=15)
    password_entry = tk.Entry(mframe, textvariable=siteNameValue)
    password_entry.grid(row=2, column=1, padx=15, pady=15)

    password_label = tk.Label(mframe, text="Site URL:")
    password_label.grid(row=3, column=0, padx=15, pady=15)
    password_entry = tk.Entry(mframe, textvariable=siteUrlValue)
    password_entry.grid(row=3, column=1, padx=15, pady=15)

    # Create and pack the login button
    login_button = tk.Button(mframe, text="Search", command=searchEntry)
    login_button.grid(row=4, column=1, padx=15, pady=15)


def searchEntry():
    retrieveEntries(sitename=siteNameValue.get(), siteurl=siteUrlValue.get())


def loadGeneratePassword(root, hframe, mframe):
    clearFrame(hframe, mframe)
    Label(hframe, text="Generate Password", font=("Arial", 14, "bold")).pack()

    chooseCombination = tk.Label(mframe, text="Choose combination :")
    chooseCombination.grid(row=2, column=0, padx=15, pady=15)

    choosePassCombination.set("Choose combinations")

    # Create a dropdown Menu
    drop = tk.OptionMenu(mframe, choosePassCombination, "Numbers", "String", "Numbers & String", "Number, String & "
                                                                                                 "Special Char")
    drop.grid(row=2, column=1, padx=15, pady=15)

    # Create and pack the login button
    login_button = tk.Button(mframe, text="Generate", command=generatePass)
    login_button.grid(row=4, column=1, padx=15, pady=15)


def generatePass():
    # print('password generated', choosePassCombination.get())'
    pasw = None
    if choosePassCombination.get() == "Numbers":
        pasw = generatePassword('n')
    elif choosePassCombination.get() == "String":
        pasw = generatePassword('s')
    elif choosePassCombination.get() == "Numbers & String":
        pasw = generatePassword('ns')
    else:
        pasw = generatePassword()
    pyperclip.copy(pasw)
    setStatus(status, 'Password has been copied to clip board', statusColor.get('w'))


def clearFrame(hframe, mframe):
    for widget in hframe.winfo_children():
        widget.destroy()
    for widget in mframe.winfo_children():
        widget.destroy()


def setStatus(lb, message, color):
    statusValue.set(message)
    lb.config(background=color)


status = Label(root, textvariable=statusValue, background=statusColor.get('s'), font=("Arial", 10, "bold"),
               foreground="white")
statusValue.set("Ready")
status.pack(side=BOTTOM, fill=X)
loadLogin(haderFrame, mainFrame)
# login.loadLogin(mainFrame).pack()
root.mainloop()

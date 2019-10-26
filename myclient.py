"""

IRC client exemplar.

"""

import sys
import threading
import time
from Tkinter import *
from ttk import *

from ex3utils import Client

selectedUser = "Please select from the box bellow"
selectedUserToUnban = "Select a user to be unbanned"
listOfMessages = []
listIndex = 0
IndexOfMessageToBePrinted = 0

class IRCClient(Client):

    def onMessage(self, socket, message):
        global listOfMessages
        global listIndex
        listOfMessages.append(message)
        return True

root = Tk()

global isAdmin 
# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])
screenName = sys.argv[3]

# Create an IRC client.
client = IRCClient()

# Start client
client.start(ip, port)
# *** register your client here, e.g. ***
client.send('REGISTER %s' % screenName)
isAdmin = (screenName.startswith("admin"))




def sendMessage():
    if userList.get() == "all":
        client.send("SEND " + sentTextBox.get("1.0", END))
    else:
        client.send("SENDTO " + userList.get() + " " + sentTextBox.get("1.0",END))

def quit():
    root.destroy()
    client.stop()

def updateMessagebox():
    global IndexOfMessageToBePrinted
    global listOfMessages
    if (len(listOfMessages) > IndexOfMessageToBePrinted):
        if not (listOfMessages[IndexOfMessageToBePrinted].startswith("all") or listOfMessages[IndexOfMessageToBePrinted].startswith("Banned users are:")):
            messagesTextBox.insert(INSERT, listOfMessages[IndexOfMessageToBePrinted] + "\n")
            IndexOfMessageToBePrinted = IndexOfMessageToBePrinted + 1
        if(listOfMessages[0].startswith("There is already a user with such a user name")):
            root.destroy()
            print("This username is taken")

    threading.Timer(2,updateMessagebox).start()

def updateActiveUserBox():
    client.send("GETUSERS")
    global IndexOfMessageToBePrinted
    global listOfMessages
    #print (listOfMessages[IndexOfMessageToBePrinted])
    if (len(listOfMessages) > IndexOfMessageToBePrinted):
        if(listOfMessages[IndexOfMessageToBePrinted].startswith("all")):
            listOfUsers = listOfMessages[IndexOfMessageToBePrinted].split(",")
            userList['values'] = listOfUsers
            IndexOfMessageToBePrinted = IndexOfMessageToBePrinted + 1
    threading.Timer(5, updateActiveUserBox).start()

def banUser():
    client.send("BAN " + userList.get())

def unbanUser():
    client.send("UNBAN " + bannedList.get())

def updateBannedUserBox():
    client.send("GETBANNED")
    global IndexOfMessageToBePrinted
    global listOfMessages
    print(listOfMessages[IndexOfMessageToBePrinted])
    if (len(listOfMessages) > IndexOfMessageToBePrinted and listOfMessages[IndexOfMessageToBePrinted].startswith("Banned users are:")):
        print("Right if")
        listOfBannedUsers = listOfMessages[IndexOfMessageToBePrinted].split(",")
        print(listOfBannedUsers)
        listOfBannedUsers = listOfBannedUsers[1:len(listOfBannedUsers)]
        bannedList['values'] = listOfBannedUsers
        IndexOfMessageToBePrinted = IndexOfMessageToBePrinted + 1
    threading.Timer(5, updateBannedUserBox).start()


#GUI
messagesTextBox = Text(root, height = 10, width = 80)
messagesTextBox.config(state = 'normal')
messagesTextBox.pack()
sentTextBox = Text(root, height = 2, width = 50)
sentTextBox.config(state = 'normal')
sentTextBox.pack()
button = Button(root, text='Send Message', width=25, command=sendMessage)
button.pack()
buttonQuit = Button(root, text="Quit", command=quit)
buttonQuit.pack()
userList = Combobox(root, width = 10, textvariable = selectedUser, postcommand = updateActiveUserBox, state="readonly")
userList.pack()

if(isAdmin):
    buttonBan = Button(root, text="Ban selected above user", command=banUser)
    buttonBan.pack()
    bannedList = Combobox(root, width = 10, textvariable = selectedUserToUnban, postcommand = updateBannedUserBox, state="readonly")
    bannedList.pack()
    buttonUnban = Button(root, text="Unban user", command=unbanUser)
    buttonUnban.pack()

#updateActiveUserBox()
updateMessagebox()
root.mainloop()
client.stop()

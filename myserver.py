import sys
from ex3utils import Server

connected = 0
userData = {}
bannedUsers = {}

class MyServer(Server):
    def onStart(self):
        print "The server has started"

    def onMessage(self, socket, message):
        global userData
        global bannedUsers
        print "The message \"" + message +"\" was received"
        #devides the message up
        (command, sep, parameter) = message.strip().partition(' ')
        print 'Command is ', command
        #implementation of the register command, it is also checked whether that user already exists
        if(command == "REGISTER"):
            if(parameter in userData or parameter == "all"):
                socket.send("There is already a user with such a user name, please close this window and enter another name")
            elif (parameter in bannedUsers):
                socket.send("You are banned")
            else:
                userData[parameter] = socket
                socket.send("Welcome user " + parameter)
                socket.screenName = parameter

        #implementation of the command for sending a message to all users
        if(command == "SEND"):
            if not socket.screenName in bannedUsers:
                for i in userData:
                    if(i == socket.screenName):
                        socket.send("My Message: " + str(parameter))
                    else:
                        userData[i].send(socket.screenName + " : " + str(parameter))
            else:
                print(command)
                socket.send("You cannot send messages when you are banned")

        #implementation of a command in the Combobox for listing users
        if(command == "GETUSERS"):
            usersWithCommas = "all," + ",".join(userData.keys())
            usersWithCommas = usersWithCommas.replace(socket.screenName, "")
            socket.send(usersWithCommas)

        #implementation of the command for sending a message to a specific user
        if (command == "SENDTO"):
            if not socket.screenName in bannedUsers:
                (privateuser, sep, text) = parameter.strip().partition(' ')
                if(privateuser in userData):
                    socket.send("My private message to " + privateuser + ": " + text)
                    userData[privateuser].send(socket.screenName + "(private): " + text)
                else:
                    socket.send("Please select a user from the box bellow." + privateuser + " is not a used username right now")
            else:
                socket.send("You cannot send messages when you are banned")

        if (command == "BAN" and message):
            if(socket.screenName.endswith("admin")):
                bannedUsers[parameter] = userData[parameter]
                userData[parameter].send("You are banned.")
                del userData[parameter]
            else:
                socket.send("You need to be an admin to perform this action")
        if (command == "UNBAN" and message):
            if(socket.screenName.endswith("admin")):
                 bannedUsers[parameter].send("You are no longer banned. Restart the client!")
                 del bannedUsers[parameter]
            else:
                socket.send("You need to be an admin to perform this action")
        if (command == "GETBANNED"):
            if(socket.screenName.endswith("admin")):
                bannedUsersWithCommas = "Banned users are: ," + ",".join(bannedUsers.keys()) 
                print(bannedUsersWithCommas)
                socket.send(bannedUsersWithCommas)
        print 'Message is ', parameter
        return True

    def onConnect(self, socket):
        global connected
        connected = connected + 1
        print "The connected users are " + str(connected)
        socket.screenName = None


    def onDisconnect(self, socket):
        global connected
        connected = connected - 1
        if (socket.screenName in userData):
            del userData[socket.screenName]
        print "Client has disconnected."
        print "The connected users are " + str(connected)

    def onStop(self):
        print "Server has stopped"

# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = MyServer()

#server = EgoServer()

# Start server
server.start(ip, port)

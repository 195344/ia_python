import socket
import json
import sys

def sendJSON(socket, data):
	msg = json.dumps(data).encode('utf8')
	total = 0
	while total < len(msg):
		sent = socket.send(msg[total:])
		total += sent

if len(sys.argv) > 1:
    port=int(sys.argv[1])
else:
    port=8081

msg = {
    "matricules": ["195344", "195311"],
    "port": port,
    "name": "Grey matter"
}

hote = "localhost"
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.connect((hote, 3001))
    print("Connection on {}".format(port))
    sendJSON(socket,msg)

except:
    print("Erreur lors de l'inscription")

finally:
    print("Close")
    socket.close()

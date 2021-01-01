import paramiko
import json
import socket

#Create server_config.json file and command.txt file
def server_config():
    print('server_config: making config')
    data = {}
    data['0'] = []
    data['0'].append({
        'host': '1.1.1.1',
        'port': '21',
        'user': 'user',
        'password': '123'
    })
    data['1'] = []
    data['1'].append({
        'host': '1.1.1.1',
        'port': '21',
        'user': 'user',
        'password': '123'
    })

    with open('server_config.json', 'w') as outfile:
        json.dump(data,outfile, indent=4)

    f = open('command.txt', 'w+')

    exit()

def execute_command(host,port,user,password):
    command = open('command.txt')

    #Connect with server and make command
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=user, password=password)

    #Executing command
    stdin, stdout, stderr = ssh.exec_command(command.read())

def connect_to(host, port, server_id_string):
    args = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)

    for family, socktype, proto, canonname, sockaddr in args:
        s = socket.socket(family, socktype, proto)
        try:
            s.connect(sockaddr)
        except socket.error:
            print('[' + server_id_string + ']' + ' error while connecting to the server')
            x = input('[' + server_id_string + ']' +
                      ' Try reconnect or switch to next server? [r - reconnect / s - switch] : ')

            if x == 'r':
                print('[' + server_id_string + ']' + ' reconnecting...')
                connect_to(host,port,server_id_string)
            if x == 's':
                return False

        else:
            s.close()
            print('[' + server_id_string + ']' + ' succesful connected')
            return True

def run():
    with open('server_config.json') as json_file:
        data = json.load(json_file)
        count = len(data)
        for server_id in range(count):
            server_id_string = str(server_id)

            print('[' + server_id_string + ']' + ' connecting to server')

            for key in data[server_id_string]:
                # check server connect
                server_is_available = connect_to(key['host'], key['port'], server_id_string)

                if server_is_available:
                    print('[' + server_id_string + ']' + ' executing command on server')
                    execute_command(key['host'], key['port'], key['user'], key['password'])

def main():
    try:
        run()

    except IOError:
        server_config()

if __name__ == '__main__':
    main()
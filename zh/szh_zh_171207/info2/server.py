import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 10001)
sock.bind(server_address)
sock.listen(1)
connection, client_address = sock.accept()

store = "4,3,2,1,0"
store_data = store.split(",")

data = connection.recv(20)
split_data = data.split(",")

result = ""
for i in [0,1,2,3,4]:
    if int(split_data[i]) == 0:
        result += "0,"
        print "0db ", i, result
    elif int(store_data[i]) >= int(split_data[i]) and int(split_data[i]) != 0:
        result += "1,"
        print "1-4db ", i, result
    else:
        result += "-1,"
        print "nemeleg ", i, result

connection.sendall(result)

print result
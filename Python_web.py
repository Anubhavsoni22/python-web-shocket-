import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SQL_SOCKET,socket.SO_REUSEADDR,1)

server_socket.bind((IP,PORT))
server_socket.listen()

socket_list = [server_socket]

client = {}


def receive_message(client_socket):
    try:
        messege_header = client_socket.recv(HEADER_LENGTH)
        if not len(messege_header):
            return False
      
        messege_length = int(messege_header.decode('utf-8').strip())
        return {"header": messege_header,"data": client_socket.recv(messege_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [],socket_list)

    for notified_socket in  read_sockets:
        if notified_socket == server_socket:
           client_socket, client_address = server_socket.accept()

           user = receive_message(client_socket)
           if user is False:
               continue 

             socket_list.append(client_socket)

             client[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} Username:{user['data'].decode('utf-8')}")

          else:
              messege = receive_message(notified_socket)

              if messege is False:
                  print(f"closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                  sockets_list.remove(notified_socket)
                  del client[notified_socket]
                  continue

              user = clients[notified_socket]
              print(f"Recived message from{user['data'].decode('utd-8')}:{messege['data'].decode('utd-8')}")

              for client_socket in client:
                  if client_socket is notified_socket:
                      client_socket.send(user['header'] + user['data'] + messege['header'] + messsge['data'] )


for notified_socket in exception_sockets:
    socket_list.remove(notifid_socket)
    del client[]


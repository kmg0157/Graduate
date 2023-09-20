from TCP_server import Server
from json_file import write_json

def main():
    json_writer=write_json('C:/Users/user/Desktop/gps sender/send_data.json')
    socket_server=Server()

    try:
        print('Server Start!')
        json_writer.initialize_json_file()

        while True:       
            data=socket_server.run_server()
            json_writer.save_data_to_json(data)
    
    except KeyboardInterrupt:
        pass

    json_writer.close_json_file()

if __name__=='__main__':
    main()
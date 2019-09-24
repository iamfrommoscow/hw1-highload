from conf_parser import *
from worker import *
from multiprocessing import Process
import socket
import argparse

def newSocketConnection(host='0.0.0.0', port = 80):
    print('host: ', host, ' port: ', port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(8)
    s.setblocking(False)
    return s

def createWorker(socket_connection, document_root):
    Worker(document_root, socket_connection)

def main():
    parser = argparse.ArgumentParser(description='hw1-highload')
    parser.add_argument('--config-file', type=str,  dest='config_file', default='/etc/httpd.conf', help='httpd config address')
    args = parser.parse_args()
    config = parseConfigFile(args.config_file)
    socket_connection = newSocketConnection(config['host'], config['port'])
    processes = []
    try:
        for number_of_process in range(config['cpu_limit']):
            print('WORKER {} START'.format(number_of_process))
            process = Process(target=createWorker, args=(socket_connection, config['document_root']))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

    except KeyboardInterrupt:
        for number_of_process, process in enumerate(processes):
            print('WORKER {} STOP'.format(number_of_process))
            process.terminate()
        socket_connection.close()




if __name__ == '__main__':
    main()
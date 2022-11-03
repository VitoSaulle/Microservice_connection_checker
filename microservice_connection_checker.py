import socket
import json

HOST = None
MICROSERVICES = None
OTHERSERVICES = None

def upload_configurations(filename):
    try:
        json_data = open(filename)
        json_data = json.load(json_data)

        try:
            global HOST, MICROSERVICES, OTHERSERVICES
            HOST = json_data["HOST"]
            MICROSERVICES = json_data["MICROSERVICES"]
            OTHERSERVICES= json_data["OTHERSERVICES"]
        except Exception as ex:
            print("Property file not formatted properly", ex)
            return False
        
        return True
    except Exception as e:
        print("An error occurred while reading json file {}".format(filename),e)
        return False


def test_connection(name, port, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((HOST, port))
        return True
    except socket.error as ex:
        print(name,' -> ','failed to ping due to', ex)
        return False


def test_microservices():
    for name, port in MICROSERVICES.items():
        status = test_connection(name, port)
        if status == True:
            print(name, ' -> ','up and running')

def test_otherservices():
    for name, port in OTHERSERVICES.items():
        status = test_connection(name, port)
        if status == True:
            print(name, ' -> ','up and running')



if __name__ == '__main__':
    if upload_configurations("config.json") == True:
        print("\nConfiguration loaded successfully...\n")
        print("**********  Will now attempt to TCP ping microservices  **********\n")
        test_microservices()
        print("\n**********  Will now attempt to TCP ping the databases or other services **********\n")
        test_otherservices()
    input("\nPress enter to exit...")

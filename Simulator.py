from multiprocessing.connection import answer_challenge
from pyModbusTCP.server import ModbusServer
import time
import yaml

serverSlave =  ModbusServer(host= "192.168.1.8", port = 5021, no_block=True)

frequency = 10
time_delay = 1/frequency

def read_holdings(address):
    ans = serverSlave.data_bank.get_holding_registers(address,1)
    return ans[0]
    
def update_value(register, value):
    
     key_to_update = 'holding_register_'+str(register)
     with open("file.yml",'r') as f:  
        data = yaml.safe_load(f)
        data_loaded = list(data)
        data[key_to_update] = str(value)
     with open("file.yml", 'w') as file:
        yaml.dump(data,file)
            


try: 
        print("Starting server...")
        serverSlave.start()
        print("Server is online")
        
        while True:
            register_value = read_holdings(1)
            print("I'm reading from register : {}".format(register_value))
            time.sleep(time_delay)
            print("Update yaml file ")
            update_value(1,register_value)
            print("Writing to holding register")
            serverSlave.data_bank.set_holding_registers(20,[register_value*2])
            time.sleep(1)
            serverSlave.data_bank.set_holding_registers(1,[44])
            continue
    
except Exception as err:
    print(f"Exception: {err}")
    print("Shutdown server")
    serverSlave.stop()

from netmiko import Netmiko

info_router = {
    'device_type':'cisco_ios', 
    'ip':'192.168.11.140', 
    'username':'onur',
    'password':'onur',
    'secret':'onur'
}
info_fortigate = {
    "device_type":"fortinet", 
    "host":"192.168.11.133", 
    "username":"admin",
    "password":"admin"
}

connection_router = Netmiko(**info_router)
print("Connected to cisco router..")
connection_fortigate = Netmiko(**info_fortigate)
print("Connected to fortigate..")


table = connection_router.send_command('show ip route static ')
with open(file="cisco_routes.txt", mode="w", encoding="utf-8") as file: 
    file.write(table)

table_ = []

table = table.split("\n")[11:]
c = 0
while True: 
    try:
        if c >= len(table): 
            break
        info = table[c]
        if "S*" in info: 
            info = info.split()[1], info.split()[4]
            table_.append(info)
            c += 1

        elif "subnetted" in info: 
            subnet = info.split()[0].split("/")[1]
            c += 1
            while True: 
                if "via" not in table[c]: 
                    break
                elif "via" in table[c]: 
                    info = table[c].split()[1] + "/" + subnet, table[c].split()[4].strip(",")
                    table_.append(info)
                    c+=1      
    except Exception as err: 
        print(err)
    
port = input("Which port do you want to use to create static route in Fortigate:(port name) ")
with open(file="forticonfig.txt",mode="w",encoding="utf-8") as file: 
    file.write("config router static\n")
    for i in table_: 
        file.write(f"edit 0\nset dst {i[0]}\nset gateway {i[1]}\nset device {port}\nnext\n")
    file.write("end\n")

res = connection_fortigate.send_config_from_file("forticonfig.txt")
print(res)
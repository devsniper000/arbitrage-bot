import subprocess
from exchange_config import *
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
import time
from os import path
from colorama import Style, Fore, init
init()
def emergency_convert_list(pair_to_sell,exlist):
    i=0
    for echange in exlist:
        try:
            if ex[echange].has['cancelAllOrders'] and ex[echange].fetchOpenOrders(pair_to_sell) != []:
                ex[echange].cancelAllOrders(pair_to_sell)
                print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Successfully canceled all orders on {echange}.")
            bal = get_balance(echange,pair_to_sell)
            bal-=bal*0.01
            if bal>(float(10)/float(ex[echange].fetch_ticker(pair_to_sell)['last'])):
                ex[echange].createMarketSellOrder(symbol=pair_to_sell,amount=round(bal,3))
                print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Successfully sold {bal} {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            else: print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Not enough {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            i+=1
        except Exception as e:
            print(f'{Style.DIM}[{time.strftime("%H:%M:%S", time.gmtime(time.time()))}]{Style.RESET_ALL} Problem on {echange}. Error:    {e}')

try:
    if len(sys.argv) < 2:
        input_list = ["mode (fake-money, classic, delta-neutral)", "renew time (in minutes)", "balance to use", "symbol", "exchanges list separated without space with commas (,)"]
        output = []
        
        for inputt in input_list:
            output.append(input(inputt+" >>> "))
        balance=output[2]
        with open(f"start_balance.txt","w") as f:
            f.write(balance)
            f.close()
        with open(f"balance.txt","w") as f:
            f.write(balance)
            f.close()
        
        mode = output[0]

        subprocess.run([how_do_you_usually_launch_python,f"main.py",output[0],output[1],output[2],output[3],output[4]])
        

    else:
        
        if len(sys.argv) < 6 or len(sys.argv) > 6:
            print("Not correctly configured. Usage:\n \n{how_do_you_usually_launch_python} run.py <mode> <symbol-renew-time> <balance-to-use> <crypto pair> <exchanges list separated without space with commas (,)>\n")
            sys.exit(1)
        args = sys.argv
        mode = args[1]
        balance = args[3]
        with open(f"start_balance.txt","w") as f:
            f.write(balance)
            f.close()
        with open(f"balance.txt","w") as f:
            f.write(balance)
            f.close()
        
        symbol=args[4]
        renew=args[2]
        ex_list=args[5]
        print("""
    █▄▄ ▄▀█ █▀█ █▄▄ █▀█ ▀█▀ █ █▄░█ █▀▀   ▄▀█ █▀█ █▄▄ █ ▀█▀ █▀█ ▄▀█ █▀▀ █▀▀   █▀ █▄█ █▀ ▀█▀ █▀▀ █▀▄▀█
    █▄█ █▀█ █▀▄ █▄█ █▄█ ░█░ █ █░▀█ ██▄   █▀█ █▀▄ █▄█ █ ░█░ █▀▄ █▀█ █▄█ ██▄   ▄█ ░█░ ▄█ ░█░ ██▄ █░▀░█""")
        print(f" \n{Fore.YELLOW}{Style.BRIGHT}FULL VERSION{Style.RESET_ALL}\n \nGithub: nelso0\nTwitter: @nelsorex\nDiscord: nelsorex\n")
        i=0

        while True:
            if i>=1 and p.returncode==1:
                sys.exit(1)
            if mode == "fake-money":
                p=subprocess.run([how_do_you_usually_launch_python,"bot-fake-money.py",symbol,balance,renew,symbol,ex_list])
                with open(f"balance.txt") as f:
                    balance=f.read()
            elif mode == "classic":
                p=subprocess.run([how_do_you_usually_launch_python,"bot-classic.py",symbol,balance,renew,symbol,ex_list])
                with open(f"balance.txt") as f:
                    balance=f.read()
            elif mode == "delta-neutral":
                p=subprocess.run([how_do_you_usually_launch_python,"bot-delta-neutral.py",symbol,balance,renew,symbol,ex_list])
                with open(f"balance.txt") as f:
                    balance=f.read()
            else:
                print(f"Mode input is incorrect.")
                sys.exit(1)
            i+=1
except KeyboardInterrupt:
    if ctrl_c_handling and mode!='fake-money':
        print(" \n \n \n")
        answered = False
        while answered == False:
            inp = input(f"{Style.DIM}{get_time()}{Style.RESET_ALL} CTRL+C was pressed. Do you want to sell all crypto back? (y)es / (n)o\n \ninput: ")
            if inp == "y" or inp == "Y" or inp == "yes" or inp == "Yes":
                answered = True
                emergency_convert_list(symbol,[ex_list.split(',')[i] for i in range(len(ex_list.split(',')))])
                sys.exit(1)
            if inp == "n" or inp == "N" or inp == "no" or inp == "No":
                answered = True
                sys.exit(1)
            else:
                answered = False
    else:
        pass


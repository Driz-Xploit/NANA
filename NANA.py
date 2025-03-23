# import library
import io
import sys
import time
import os
import ipaddress
import socket
import threading
import json
### clear screen
def clear():
        if os.name == 'nt':
                os.system('cls')
        else:
                os.system('clear')
### module checker
mod_not_installed = []
not_installed_status = False
def main_mod(list_mod):
        try: # install modul if 'requirements.txt' is exist
                        file_to_mod = 'requirements.txt'
                        open(file_to_mod, 'r')
                        os.system(f'pip install -r {file_to_mod}')
        except FileNotFoundError: # install modul if 'requirements.txt' isn't exist
                install_mod(list_mod)

# install modul if 'requirements.txt' isn't exist
def install_mod(mod_install):
        mod = ' '.join(mod_install)
        os.system(f'pip install {mod}')
##### testing some import proccess
def test_mod():
        global mod_not_installed, not_installed_status
        try:
                import nmap
        except ModuleNotFoundError:
                not_installed_status = True
                mod_not_installed.append('python-nmap')
        ##$
        try:
                from tabulate import tabulate
        except ModuleNotFoundError:
                not_installed_status = True
                mod_not_installed.append('tabulate')
        ##$
        try:
                from colorama import Fore
        except ModuleNotFoundError:
                not_installed_status = True
                mod_not_installed.append('colorama')
        ##$
        if not_installed_status == True:
                print('Installing module.....')
                main_mod(mod_not_installed)
#$#
test_mod()
##### import proccess
import nmap
from tabulate import tabulate as table
from colorama import Fore, Style, init
# colorama get ready
init()
# clean all of user screen
clear()
# NANA banner
nana = fr"""{Fore.YELLOW}{Style.BRIGHT}                              .
                         ....:  .
                  .+==:..        :.=*::.
              .::::+***.         . -+*=.
                .******=.  :-.   .   +-.
                 *: +***. --:-:. .-  :.:
                 -:::-*-:-%*-+.-++*. *=.           +-------+-----+--------+------------------+
                ..: .:=::=++    *:+-.+::      <----| NANA! |    ~~InfoGath-Active-Tools~~    |
             .::: :  =:=--.      :*=-:..           +-------+-----+--------+------------------+
             .....-: -..-#=.  ..::*-. - :..        |By Driz-Xploit!, Indo-Exploit Developer  |
              :..  .: -.  ==.==: -.= .:+  .:       +----------------------+------------------+
             .-. ..  ..-   .:##+:. .   --...
             ::    .. . .   .***:::...    .:
             -=       ::.    :::.:.       -:
             .-       :=        : -.     .::
              .       :-        : .:     :.
                     .          .  -
                    .-           .
                    -***---::.::-+-
                   '+:=+++##***++=+'
                   +'-==:--+==+-=-'+
                      :*++:*++=
                      .*++:*+*-
                      +++* =+*=
                     ++*=  :*+=
                    :*+*   :*+=
                     ++=   :*++
                            -=:{Fore.CYAN}
"""
# print NANA banner
print(nana)
### Global variables
target = None
web = None
parameter = None
method = None
nm = None
target_table = None
type_target = None
# is the input of user is an ip?
def isip(input):
        try:
                ipaddress.ip_address(input)
                return True
        except ValueError:
                return False
# target input proccess
def Options():
        try:
                print("|#>Example target input: 'example.com', '192.168.x.x', etc.")
                domainip = input("|-->Enter the target for NANA!: ")
                # block None or injected input
                if ("|" in domainip) or ("&" in domainip) or (";" in domainip) or ("$" in domainip):
                        print("|---> Invalid input detected!")
                        print(f"+--------------------------------------------------------------------------------------->")
                        return False, None
                elif not domainip:
                        print("|-->Do you have a target?, find your target. exit()!")
                        print(f"+--------------------------------------------------------------------------------------->")
                        return False, None
                # is the input is domain or ip?
                else:
                        global web, type_target
                        result = isip(domainip)
                        if result:
                                print(f"|--->Target NANA!, is an IP!: {domainip}")
                                web = "N/A"
                                type_target = "IP"
                                return True, domainip
                        else:
                                print(f"|--->Target NANA!, is a DOMAIN!: {domainip}")
                                type_target = "DOMAIN"
                                web = domainip
                                domainip = "".join(socket.gethostbyname(domainip))
                                print(f"|--->Ipv4 is: {domainip}")
                                return True, domainip
        except socket.gaierror:
                print("|------->Ups! NANA see an invalid input!.")
                print("|----------->Please enter the valid domain without spaces, http:// or https://")
                print(f"+--------------------------------------------------------------------------------------->")
                return False, None
        except ValueError:
                print("|------------->Ups! NANA see an invalid input!.")
                print(f"+--------------------------------------------------------------------------------------->")
                return False, None
        return domainip
# after user input the target, is the target is up?
def isup(target_ping):
        print(f"+--------------------------------------------------------------------------------------->[NANA!, wait a second!]<")
        if os.name == "nt":
                check = os.system(f"ping -n 5 -w 1 {target_ping}")
        else:
                check = os.system(f"ping -c 5 {target_ping} -W 1")
        print(f"+--------------------------------------------------------------------------------------->[NANA!, DONE!]<")
        if check == 0:
                clear()
                print(f"+--------------------------------------------------------------------------------------->[NANA!, DONE!]<")
                print("|------>NANA!, target is up!. Let\'s begin!.<-------------------------------------------->")
        else:
                print("|------>NANA!, target isn\'t up!. NANA can't scanning!, is there any wrong on your input?.")
                sys.exit()
############# options for view the report
tableopt = (f"""{Fore.RED}+---------------------------------------------------------------+
| {Fore.YELLOW}1. Simple Table (Summarize)                                   {Fore.RED}|
| {Fore.YELLOW}2. Json Format (Details)                                      {Fore.RED}|
| {Fore.YELLOW}3. Save Simple Table to file                                  {Fore.RED}|
| {Fore.YELLOW}4. Save Json Format to file                                   {Fore.RED}|
| {Fore.YELLOW}5. Back to ~                                                  {Fore.RED}|
| {Fore.YELLOW}6. Change Target                                              {Fore.RED}|
| {Fore.YELLOW}7. Exit                                                       {Fore.RED}|
+---------------------------------------------------------------+{Fore.CYAN}""")
# options for nmap scan speed
spener = (f"""{Fore.RED}+---------------------------------------------------------------+
| {Fore.YELLOW}1. Very Slow (-T1)                                            {Fore.RED}|
| {Fore.YELLOW}2. Slow      (-T2)                                            {Fore.RED}|
| {Fore.YELLOW}3. Normal    (-T3)                                            {Fore.RED}|
| {Fore.YELLOW}4. Fast      (-T4)                                            {Fore.RED}|
| {Fore.YELLOW}5. Very Fast (-T5)                                            {Fore.RED}|
| {Fore.YELLOW}6. Back to Nmap Parameter options                             {Fore.RED}|
+---------------------------------------------------------------+{Fore.CYAN}""")
# proccess of view the report to user
def table_show(RE_TABLE, RE_JSON):
        temp_opt = 0
        while temp_opt != 7:
                clear()
                try:
                        print(tableopt)
                        temp_opt = int(input("|---->NANA!, I will show the results based on your options!: "))
                        if temp_opt == 1:
                                clear()
                                print(RE_TABLE)
                                temp = input(f"{Fore.RED}(Press enter for continue){Fore.CYAN}")
                        elif temp_opt == 2:
                                clear()
                                print(Fore.CYAN+RE_JSON)
                                temp = input(f"{Fore.RED}(Press enter for continue){Fore.CYAN}")
                        elif temp_opt == 3:
                                temp_opt2 = None
                                while temp_opt2 != "n":
                                        clear()
                                        try:
                                                temp_opt2 = input(f"|-->NANA!, Do you want to save json format result on '{target}-table'(y/n)?: ")
                                                if temp_opt2 == "y":
                                                        f = open(f"{target}-table", "w")
                                                        output_1 = io.StringIO()
                                                        sys.stdout = output_1
                                                        print(RE_TABLE)
                                                        sys.stdout = sys.__stdout__
                                                        f.write(output_1.getvalue())
                                                        output_1.close()
                                                        f.close()
                                                        print("Done!")
                                                        input("(press enter for continue)")
                                                        break
                                                elif temp_opt2 == "n":
                                                        break
                                        except ValueError:
                                                pass
                        elif temp_opt == 4:
                                temp_opt3 = None
                                while temp_opt3 != "n":
                                        clear()
                                        try:
                                                temp_opt3 = input(f"|-->NANA!, Do you want to save json format result on '{target}-json'(y/n)?: ")
                                                if temp_opt3 == "y":
                                                        f = open(f"{target}-json", "w")
                                                        output_2 = io.StringIO()
                                                        sys.stdout = output_2
                                                        print(RE_JSON)
                                                        sys.stdout = sys.__stdout__
                                                        f.write(output_2.getvalue())
                                                        output_2.close()
                                                        f.close()
                                                        print("Done!")
                                                        input("(press enter for continue)")
                                                        break
                                                elif temp_opt3 == "n":
                                                        break
                                        except ValueError:
                                                pass
                        elif temp_opt == 5:
                                clear()
                                opt2()
                        elif temp_opt == 6:
                                restart()
                        elif temp_opt == 7:
                                print(f"{Fore.RED}|-~--~->NANA!, Good Bye!<-~-~-|")
                                sys.exit()
                        elif (temp_opt <= 0) or (temp_opt >= 7):
                                pass
                except ValueError:
                        pass
# restart for change the target
def restart():
        python = sys.executable
        os.execl(python, python, *sys.argv)
# after all options from user choice, is user want to execute the options?
def runner():
        global parameter
        tem_opt = 0
        tem_opt2 = 0
        tem_opt3 = 0
        while tem_opt != 2:
                clear()
                temp_head = ["Target", "Domain/Hostname", "Method", "Parameter", "Type"]
                temp_list = [[target, web, method, parameter, type_target]]
                temp_table = table(temp_list, temp_head, tablefmt='grid', colalign=('center', 'left', 'right'), missingval='')
                print(temp_table)
                try:
                        tem_opt = input("|-->Execute?(y/n): ")
                        if tem_opt == "y":
                                while (tem_opt2 != "y") and (tem_opt2 != "n"):
                                        tem_opt2 = input("|--> Do you want to use '-p-' to scan all ports?(y/n): ")
                                        if tem_opt2 == "y":
                                                parameter += " -p-"
                                        else:
                                                pass
                                while (tem_opt3 != "y") and (tem_opt3 != "n"):
                                        tem_opt3 = input("|----> Do you want to use '-Pn' to skip ping ICMP scan?(y/n): ")
                                        if tem_opt3 == "y":
                                                        parameter += " -Pn"
                                        else:
                                                pass
                                checkmethod()
                        elif tem_opt == "n":
                                clear()
                                opt2()
                        else:
                                print("please input the valid input! --> 'y' or 'n'")
                except ValueError:
                        print("please input the valid input! --> 'y' or 'n'")
# result for target information table
def Info_target():
        global target
        target_head = ["IPV4", "Web", "Hostname", "Type"]
        try:
                host = socket.gethostbyaddr(target)[0]
        except socket.herror:
                host = "N/A"
        target_table_re = [[target, web, host, type_target]]
        Info_table = table(target_table_re, target_head, tablefmt='grid', missingval='')
        return Info_table
# Version scanning
def Version():
        global web, target, nm
        nm = nmap.PortScanner()
        #
        nmapproccess(nm)
        ##
        Version_table = sV(nm)
        temp_head = ["Port", "Name", "Status", "Product", "Version", "CPE", "Extrainfo"]
        ##
        web = web or ""
        ##
        target_re = Info_target()
        table_re = table(Version_table, temp_head, tablefmt='grid', missingval='')
        ##
        json_plain = nm[target]
        json_dumps = json.dumps(json_plain, indent=2)
        ##
        RE = (Fore.GREEN+target_re+"\n"+Fore.CYAN+table_re)
        table_show(RE, json_dumps)

# frame of animation of proccess scanning
scanning_animation = ["-", "\\", "|", "/"]
# animation of proccess scanning
def scan_ani():
        for i in scanning_animation:
                clear()
                print(f"Wait a second!, NANA is scanning... ({i})")
                time.sleep(1)
# nmap is scanning...
def nmapscan(nm):
        global parameter, target
        nm.scan(target, arguments=f'{parameter}')
# nmap scanning thread
def nmapproccess(nm):
        global parameter
        scan = threading.Thread(target=nmapscan, args=(nm,))
        scan.start()
        while scan.is_alive():
                scan_ani()
        scan.join
# Make the result of version scanning
def sV(nm):
        global target
        temp_table = []
        for proto in nm[target].all_protocols():
                for port in nm[target][proto].keys():
                        lport = port
                        name = nm[target][proto][port].get('name', '')
                        status = nm[target][proto][port].get('state', '')
                        #
                        Product = nm[target][proto][port].get('product', '')
                        if Product == "":
                                Product = ""
                        #
                        Version = nm[target][proto][port].get('version', '')
                        if Version == "":
                                Version = ""
                        #
                        cpe = nm[target][proto][port].get('cpe', '')
                        if cpe == "":
                                cpe = ""
                        ##
                        extrainfo = nm[target][proto][port].get('extrainfo', '')
                        if extrainfo == "":
                                extrainfo = ""
                        ###
                        temp_table.append([lport, name, status, Product, Version, cpe, extrainfo])
        return temp_table
# check method for execute
def checkmethod():
        clear()
        global method
        if method == "Service":
                Version()
# user options for speed of scanning
def speedin():
        clear()
        topt = 0
        global parameter
        while (topt != 6):
                print(spener)
                #
                try:
                        topt = int(input(f"|-/{target}/Nmap/Speedscan/-> Enter the options!: "))
                        if topt == 1:
                                clear()
                                parameter += " -T1"
                                runner()
                        elif topt == 2:
                                clear()
                                parameter += " -T2"
                                runner()
                        elif topt == 3:
                                clear()
                                parameter += " -T3"
                                runner()
                        elif topt == 4:
                                clear()
                                parameter += " -T4"
                                runner()
                        elif topt == 5:
                                clear()
                                parameter += " -T5"
                                runner()
                        elif topt == 6:
                                clear()
                                nminput()
                        elif (topt <= 0) or (topt >= 7):
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|------>NANA!, Enter the valid input!(1-6)")
                except ValueError:
                        clear()
                        print(f"+--------------------------------------------------------------------------------------->")
                        print("|------>NANA!, Enter the valid input!(1-6)")
#
opt2banner = (f"""{Fore.RED}+---------------------------------------------------------------+
| {Fore.YELLOW}1. Use Nmap only (Details scanning)                           {Fore.RED}|
| {Fore.YELLOW}2. Use Naabu only (Fast scanning)                             {Fore.RED}|
| {Fore.YELLOW}3. Use Naabu + Nmap (Fast and Details scanning)               {Fore.RED}|
| {Fore.YELLOW}4. Change the target                                          {Fore.RED}|
| {Fore.YELLOW}5. Exit                                                       {Fore.RED}|
+---------------------------------------------------------------+{Fore.CYAN}""")
#
nmopt = (f"""{Fore.RED}+------------------------------------------------------------------------->
| {Fore.YELLOW}1. Service scanning (-sV)                                               {Fore.RED}|
| {Fore.YELLOW}2. Agressive scanning (-A)                                              {Fore.RED}|
| {Fore.YELLOW}3. Fast scanning (-F)                                                   {Fore.RED}|
| {Fore.YELLOW}4. Script default scanning (-sC)                                        {Fore.RED}|
| {Fore.YELLOW}5. options or custom script scanning (--script options)                 {Fore.RED}|
| {Fore.YELLOW}6. Os detection scanning (-O)                                           {Fore.RED}|
| {Fore.YELLOW}7. Back to /~                                                           {Fore.RED}|
+-------------------------------------------------------------------------+{Fore.CYAN}""")
#
def nminput():
        nmin = 0
        global parameter
        global method
        while nmin != 7:
                try:
                        print(nmopt)
                        nmin = int(input(f"|-/{target}/Nmap-> Enter the options!: "))
                        #
                        if nmin == 1:
                                method = "Service"
                                parameter = "-sV"
                                speedin()
                        elif nmin == 2:
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|----------NANA!, coming soon...")
                        elif nmin == 3:
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|----------NANA!, coming soon...")
                        elif nmin == 4:
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|----------NANA!, coming soon...")
                        elif nmin == 5:
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|----------NANA!, coming soon...")
                        elif nmin == 6:
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|----------NANA!, coming soon...")
                        elif nmin == 7:
                                clear()
                                opt2()
                        elif (nmin <= 0) or (nmin >= 8):
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|------>NANA!, Enter the valid input!(1-4)")
                except ValueError:
                        clear()
                        print(f"+--------------------------------------------------------------------------------------->")
                        print("|------>NANA!, Enter the valid input!(1-4)")
################################################################################# execute
def opt2():
        opti2 = 0
        while opti2 != 5:
                print(opt2banner)
                try:
                        opti2 = int(input(f"|-/{target}/-> Enter the option!: "))
                        if opti2 == 1:
                                clear()
                                nminput()
                        elif opti2 == 2:
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|----------NANA!, coming soon...")
                        elif opti2 == 3:
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|----------NANA!, coming soon...")
                        elif opti2 == 4:
                                clear()
                                restart()
                        elif opti2 == 5:
                                print(f"{Fore.RED}|--->NANA!, Good Bye!<---|")
                                sys.exit()
                        elif (opti2 <= 0) or (opti2 >= 6):
                                clear()
                                print(f"+--------------------------------------------------------------------------------------->")
                                print("|------>NANA!, Enter the valid input!(1-4)")
                except ValueError:
                        clear()
                        print(f"+--------------------------------------------------------------------------------------->")
                        print("|------>NANA!, Enter the valid input!(1-4)")
                except KeyboardInterrupt:
                        print(f"{Fore.RED}\n|-~--~->NANA!, Good Bye!<-~-~-|")
                        sys.exit()
def main():
        try:
                global target
                status_temp, target = Options()
                if status_temp:
                        isup(target)
                        opt2()
                else:
                        pass
        except KeyboardInterrupt:
                print("Good Bye!")
main()

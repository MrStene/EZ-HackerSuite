import os
import pyfiglet
import cracker
import scanner
import dirbuster
import logincracker
import cracker2


def _clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_cracker_cli():
    """Runs cracker in terminal

    This function is called to run crack() from cracker.py.
    input() is used to provide the crack() function with the necessary arguments.
    """
    cracker_banner = pyfiglet.figlet_format("EZ   PASSWORD   CRACKER")
    print(cracker_banner)
    choose_hashes = input("Where are the hashes you want to crack located?: ")
    choose_wordlist = input("Where is the wordlist you want to use located: ")
    choose_hash_type = input("md5, sha1, sha256, sha512: ")
    choose_file_location = input("Where do you want to store the result? (Optional): ")
    cracker.crack(choose_hashes, choose_wordlist, choose_hash_type, choose_file_location)


# Work in Progress
def run_cracker_cli_2():
    """Runs cracker in terminal

    This function is called to run crack() from cracker.py.
    input() is used to provide the crack() function with the necessary arguments.
    """
    cracker_banner = pyfiglet.figlet_format("EZ   PASSWORD   CRACKER")
    print(cracker_banner)
    choose_hashes = input("Where are the hashes you want to crack located?: ")
    choose_wordlist = input("Where is the wordlist you want to use located: ")
    choose_hash_type = input("md5, sha1, sha256, sha512: ")
    choose_threads = int(input("How many threads do you wish to use?"))
    choose_file_location = input("Where do you want to store the result? (Optional): ")
    cracker2.run_crack(choose_hashes, choose_wordlist, choose_hash_type, choose_file_location, choose_threads)


def run_scanner_cli():
    """Runs the scanner in terminal

    This function is called to run either run_arp() or run_port_scan() from scanner.py.
    input() is used to provide the functions with the necessary arguments.
    """

    # Creates a Banner
    scanner_banner = pyfiglet.figlet_format("EZ   SCANNER")
    print(scanner_banner)

    # Choose which tool to use
    scanner_service = input("Do you want to scan a network for IP addresses or Scan a host for open ports? \n \n"
                            " 1: Network \n 2: Ports \n \n Enter your choice here: ").lower()

    # If network scan is selected, scapy.arping() is called.
    if scanner_service == "1" or scanner_service == "network":
        ip_address = input("\n\n Enter the network you want to scan (ex 192.168.1.0/24): ")
        scanner.run_arp(ip_address)

    # If ports are chosen, run_port_scan() is called.
    elif scanner_service == "2" or scanner_service == "ports":
        t_host = input("\nWhat host do you want to target? \n Enter IP or Hostname: ")
        s_port = int(input("Which ports do you want to scan? (min: 1, max: 65535) \n Start Port: "))
        e_port = int(input(" End Port: "))
        thr = int(input("How many threads do you want to use? \n Enter Amount: "))
        scanner.run_port_scan(t_host, s_port, e_port, thr)


def bust_cli():
    """Runs the directory busting in Terminal

    This function is called to call the run_brute_force_directories() from dirbuster.py
    input() is used to provide the function with the necessary arguments.
    """

    # Creating banner
    buster_banner = pyfiglet.figlet_format("EZ DIRECTORY BUSTER")
    print(buster_banner)

    # Receives user input to be used as arguments
    target_host = input("What target to attack: ")
    wordlist_file = input("Choose a wordlist to use: ")
    threads_amount = input("How many threads to use: ")
    save_file = input("Where to store the result? (optional): ")
    dirbuster.run_brute_force_directories(wordlist_file, int(threads_amount), target_host, save_file)


def run_login_cracker_cli():
    """Runs the login cracker in terminal.

    This function is called to call run_login_cracker() from logincracker.py.
    input() is used to provide the function with the necessary arguments.
    """

    # creates a banner
    login_cracker_banner = pyfiglet.figlet_format("EZ LOGIN CRACKER")
    print(login_cracker_banner)

    url = input("Choose URL that contains a login form: ")
    form = logincracker.find_login_form(url)
    if form is not None:
        logincracker.print_form(form)
        u_index = int(input("Identify the username input: #"))
        p_index = int(input("Identify the password input: #"))
        users_file = input("Where is the file containing usernames?")
        password_file = input("Where is the file containing passwords?")
        logincracker.run_login_cracker(url, u_index, p_index, users_file, password_file)
    else:
        print("No Login Form Found")


# Welcome Page and Service Selector
welcome_banner = pyfiglet.figlet_format("W e l c o m e   t o \nE Z   H a c k e r   \nS u i t e !")
print(welcome_banner)
select_print = "What would you like to do? \n \n 1: Crack a password \n 2: Network Scanning \n " \
               "3: Directory Busting \n 4: Login Cracker \n 5: Cracker2 (WIP) \n\n"
print(select_print)

services = {
    "1": run_cracker_cli,
    "2": run_scanner_cli,
    "3": bust_cli,
    "4": run_login_cracker_cli,
    "5": run_cracker_cli_2
}

# Runs the function corresponding to a number. If valid number is entered
keep_running = True
while keep_running:
    service_index = input("Type tool number (ex: 1): ")
    service = services.get(service_index)
    if service is not None:
        _clear_screen()
        service()
        keep_running_input = input("Continue hacking? y/n").lower()
        if keep_running_input == "n":
            keep_running = False
        elif keep_running_input != "y":
            print("Invalid response, exiting program")
            keep_running = False
    else:
        print("Illegal value " + service_index + ", try again")
    print(select_print)

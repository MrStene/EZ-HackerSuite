import scapy.all as scapy
import socket
import threading
from queue import Queue
import time


def port_scan(port: int, host: str):
    """Scans for open ports

    This function takes a port nr. and a host as input. It then scans the targeted host:port.
    If the port is open, the host and port is printed.
    """

    # print_lock is used to make sure that threads are not trying to print at the same time
    print_lock = threading.Lock()

    # Creates the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # How long it takes before the connection times out. Less time = more efficient, more time = more accurate
    socket.setdefaulttimeout(1)

    # Tries to connect to the host:port. if successful, print that it's open.
    try:
        con = s.connect((host, port))
        with print_lock:
            print("{0}: port {1} is open".format(host, port))
        con.close()
    except:
        pass


# All threads wait for ports to be added to the queue and calls port_scan.
def _threader(target: str, port_queue: Queue):
    while True:
        port = port_queue.get()
        port_scan(port, target)
        port_queue.task_done()


# Runs the port scanner
def run_port_scan(target_host: str, start_port: int, end_port: int, threads: int):
    start_time = time.time()
    port_queue = Queue()
    print("Port Scan Started")

    # How many threads that will be used
    for x in range(threads):
        t = threading.Thread(target=_threader, args=(target_host, port_queue,))
        t.daemon = True
        t.start()

    # How many ports that will be scanned, specified by worker number
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    port_queue.join()
    print("DONE! \nTime taken: ", time.time() - start_time)


def run_arp(ip_address):
    start_time = time.time()
    print("Network Scan Started")
    scapy.arping(ip_address)
    print("DONE! \nTime taken: ", time.time() - start_time)

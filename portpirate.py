

        import socket
        import sys
        import threading
        from datetime import datetime
        import argparse
        import subprocess
        import time
        from colorama import Fore, Style
        from concurrent.futures import ThreadPoolExecutor
        from queue import Queue
         
        VERSION = "1.0.0"
        TIMEOUT = 0.5
        THREADS = 50
        open_ports = []
        stop_event = threading.Event()
        queue = Queue()
         
        parser = argparse.ArgumentParser(description="portpirate - a simple, lightweight portscanner written in Python")
        parser.add_argument("target", help="The target IP/hostname")
        parser.add_argument("-p", "--port", help="Specify port(s) to scan. Scan a single port, a comma separated list of ports, a range of ports or use the keyword \\"all\" to scan all 65,535 ports")
        parser.add_argument("-t", "--threads", help="Number of threads to use (default=50)", type=int, default=THREADS)
        parser.add_argument("-o", "--timeout", help="Timeout for port connection attempts (default=0.5)", type=float, default=TIMEOUT)
        args = parser.parse_args()
         
        threads = args.threads
        timeout = args.timeout
        port = args.port
        target = args.target
         
         
        # Prints the banner
        def banner():
            banner = f"""
                              __         .__               __          
        ______   ____________/  |_______ |__|___________ _/  |_  ____  
        \____ \ /  _ \_  __ \   __\____ \|  \_  __ \__  \\   __\/ __ \
        |  |_> >  <_> )  | \/|  | |  |_> >  ||  | \// __ \|  | \  ___/
        |   __/ \____/|__|   |__| |   __/|__||__|  (____  /__|  \___  >
        |__|                      |__|                  \/          \/  
         
        Version:     {VERSION}
        """
            print(banner)
         
         
        # Displays the target IP/hostname and target port(s)
        def target_info(target, port):
            print(50*"-")
            print(f":: Target          {target}")
            print(f":: Port(s)         {port}")
            print(f":: Threads         {threads}")
            print(f":: Timeout         {timeout}")
            print(50*"-")
         
         
        # Loading animation to be displayed while nmap scan is running
        def loading_animation():
            message = "Scanning open ports with nmap"
            index = 0
            print("\n")
            while not stop_event.is_set():
                sys.stdout.write(f"\r{message}{'.' * index}")
                sys.stdout.flush()
                index = ((index + 1) % 5)
                time.sleep(0.1)
         
         
        # thread that executes loading_animation()
        def animation_thread():
            animation_thread = threading.Thread(target=loading_animation)
            animation_thread.start()
         
         
        # Connects to the target IP:port pair
        def scanner(ip, timeout, port):
            with socket.socket() as s:
                s.settimeout(timeout)
                try:
                    s.connect((ip, port))
                    print(f"[+]    {ip}:{Fore.GREEN}{port}{Style.RESET_ALL}")
                    open_ports.append(port)
                except socket.error:
                    pass
                except KeyboardInterrupt:
                    sys.exit()
         
         
        # Creates a thread pool using ThreadPoolExecutor and submits a task for every port in target_ports
        def threaded_scanner(ip, timeout, threads):
            with ThreadPoolExecutor(max_workers=threads) as executor:
                while not queue.empty():
                    port = queue.get()
                    executor.submit(scanner, ip, timeout, port)
                executor.shutdown(wait=True)
         
         
        # Scans the open ports using nmap
        def nmap_scan(ip, open_ports):
            global stop_event
            result = subprocess.run(["nmap", "-sC", "-sV", "-p", ",".join(map(str, open_ports)), ip], capture_output=True, text=True)
            stop_event.set()
            print(f"\r{result.stdout}")
         
         
        banner()
         
        if port.isdigit():
            queue.put(int(port))
            target_info(target, port)
         
        elif "," in port:
            ports = port.split(",")
            for port in ports:
                queue.put(int(port))
            target_info(target, ports)
         
        elif "-" in port:
            range_str = port
            range_elements = range_str.split("-")
            start_value, end_value = map(int, range_elements)
            for port in range(start_value, end_value + 1):
                queue.put(port)
            target_info(target, range_str)
         
        elif port.lower() == "all":
            for port in range(1, 65536):
                queue.put(port)
            target_info(target, "1-65535")
         
         
        def main():
            try:
                ip_addr = socket.gethostbyname(target)
         
                date_now = datetime.now()
                print(f"Scan started at {date_now}")
                t1_start = time.perf_counter()
         
                threaded_scanner(ip_addr, timeout, threads)
         
                t2_stop = time.perf_counter()
                elapsed = t2_stop - t1_start
                formatted_elapsed = format(elapsed, ".6f")
                print(f"Scan completed in {formatted_elapsed} seconds")
         
                animation_thread()
                nmap_scan(ip_addr, open_ports)
         
            except socket.gaierror:
                print("Invalid IP/hostname")
         
            except KeyboardInterrupt:
                stop_event.set()
                sys.exit()
         
         
        if __name__ == "__main__":
            main()


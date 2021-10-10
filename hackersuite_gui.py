import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from contextlib import redirect_stdout
import cracker
import scanner
import dirbuster
import logincracker

header = ("Arial", 20)


def browse_files(entry: tk.Entry):
    """Select a File

    This function can be used to select a file from the computer's file explorer.
    It takes an Entry as argument. This entry is changed to display the name of the file.
    """

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="select a file",
                                          filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    entry.delete(0, "end")
    entry.insert(0, filename)


def save_file(entry: tk.Entry):
    """Creates a file

        This function can be used to create a file using the computer's file explorer.
        It takes an Entry as argument. This entry is changed to display the name of the file.
        If an existing file is chosen, one can replace the old file with a new one, using the same name.
        """

    filename = filedialog.asksaveasfilename(initialdir="/",
                                            title="Select a file",
                                            filetypes=(('All files', '*.*'), ('Text files', '*.txt')))
    entry.delete(0, "end")
    entry.insert(0, filename)


class HackerSuiteGUI(tk.Tk):
    """Parent widget to the hacker tools GUI."""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "EZ Hacker Suite")
        tk.Tk.geometry(self, "800x600")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Cracker, Scanner, DirBuster, LoginCracker):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class StartPage(tk.Frame):
    """Provides a list of menu items redirecting to the different hacker tools.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.rowconfigure((1, 2, 3, 4), weight=1)
        self.columnconfigure(0, weight=1)
        label = tk.Label(self, text="Welcome to EZ Hacker Suite", font=header)
        label.grid(row=0, column=0, pady=20)
        button1 = ttk.Button(self, text="Password Cracker", width=30,
                             command=lambda: controller.show_frame(Cracker))
        button1.grid(row=1, column=0)
        button2 = ttk.Button(self, text="Scanner", width=30,
                             command=lambda: controller.show_frame(Scanner))
        button2.grid(row=2, column=0)
        button3 = ttk.Button(self, text="Directory Buster", width=30,
                             command=lambda: controller.show_frame(DirBuster))
        button3.grid(row=3, column=0)
        button4 = ttk.Button(self, text="Login Cracker", width=30,
                             command=lambda: controller.show_frame(LoginCracker))
        button4.grid(row=4, column=0)


class Cracker(tk.Frame):
    """An interface to the password cracking tool."""

    def __init__(self, parent, controller):
        # Creates StringVars to later use as arguments in run_cracker()
        choose_hash_type = tk.StringVar()
        output_string = tk.StringVar()

        # A dictionary used to create radio buttons. More values may easily be added
        hashes = {"MD5": "md5",
                  "SHA1": "sha1",
                  "SHA256": "sha256",
                  "SHA512": "sha512"}

        # When called, starts a background thread. run_cracker_gui() redirects terminal output to output_string
        def _run_cracker(hash_file, wordlist, hash_algorithm, file_location):
            output_string.set("")
            background_thread = threading.Thread(target=self.run_cracker_gui,
                                                 args=(
                                                     output_string, hash_file, wordlist, hash_algorithm, file_location))
            background_thread.start()

        tk.Frame.__init__(self, parent)

        self.columnconfigure((0, 1), weight=1)

        # Title
        title_label = tk.Label(self, text="EZ Password Cracker", font=header)
        title_label.grid(row=1, column=0, columnspan=2, sticky="WE")

        # Back to start page button
        button1 = ttk.Button(self, text="Back to start page",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0, sticky="NW")

        # Choose File containing hash values, entry and button
        choose_file_entry1 = tk.Entry(self, width=40)
        choose_file_entry1.grid(row=2, column=1, sticky="W", pady=10)
        choose_file_button1 = ttk.Button(self, text="* Choose Hashes", width=20,
                                         command=lambda: browse_files(choose_file_entry1))
        choose_file_button1.grid(row=2, column=0, sticky="E")

        # Choose wordlist, label and button
        choose_file_entry2 = tk.Entry(self, widt=40)
        choose_file_entry2.grid(row=3, column=1, sticky="W", pady=10)
        choose_file_button2 = ttk.Button(self, text="* Choose Wordlist", width=20,
                                         command=lambda: browse_files(choose_file_entry2))
        choose_file_button2.grid(row=3, column=0, sticky="E")

        # Choose where to save the result, label and button
        choose_file_entry3 = tk.Entry(self, width=40)
        choose_file_entry3.grid(row=4, column=1, sticky="W", pady=10)
        choose_file_button3 = ttk.Button(self, text="Save Result to", width=20,
                                         command=lambda: save_file(choose_file_entry3))
        choose_file_button3.grid(row=4, column=0, sticky="E")

        # Frame containing all radio button. All buttons are created using the for loop
        radio_frame = ttk.LabelFrame(self, text="Hash Algorithm")
        radio_frame.grid(row=5, column=0, columnspan=2, pady=10)
        column_index = 0
        for text, value in hashes.items():
            ttk.Radiobutton(radio_frame, text=text, variable=choose_hash_type, value=value).grid(row=1,
                                                                                                 column=column_index,
                                                                                                 sticky="W")
            column_index += 1

        # Run Cracker button
        crack_button = ttk.Button(self, text="Crack!",
                                  command=lambda: _run_cracker(choose_file_entry1.get(), choose_file_entry2.get(),
                                                               choose_hash_type.get(), choose_file_entry3.get()))
        crack_button.grid(row=6, column=0, columnspan=2)

        # Open the file containing the result
        open_result_button = ttk.Button(self, text="Open File",
                                        command=lambda: os.startfile(choose_file_entry3.get()))
        open_result_button.grid(row=7, column=0, columnspan=2)

        # Result, Canvas, Frame, Scrollbar, Label
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(row=8, column=0, columnspan=2)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_propagate(False)
        result_canvas = tk.Canvas(canvas_frame, bg="white")
        result_canvas.grid(row=0, column=0, sticky="news")
        v_bar = ttk.Scrollbar(canvas_frame, orient="vertical", command=result_canvas.yview)
        v_bar.grid(row=0, column=1, sticky="ns")
        h_bar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=result_canvas.xview)
        h_bar.grid(row=1, column=0, sticky="we")
        result_canvas.configure(yscrollcommand=v_bar.set, xscrollcommand=h_bar.set)
        result_frame = tk.Frame(result_canvas)
        result_canvas.create_window((0, 0), window=result_frame, anchor="nw")
        result_label = tk.Label(result_frame, textvariable=output_string, bg="white", justify=tk.LEFT)
        result_label.grid()
        result_frame.update_idletasks()
        canvas_frame.config(width=450 + v_bar.winfo_width(), height=300)
        result_frame.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))


    def run_cracker_gui(self, output: tk.StringVar, hashes: str,
                        wordlist: str, hash_algorithm_name: str, file_location: str):
        """To redirect the output of crack() to StringVar

        This function takes the output of crack() and redirects it to a StringVar,
        used to display the output in a GUI interface.
        To be called as a background thread.
        """

        redirector = StdoutRedirector(output)
        with redirect_stdout(redirector):
            cracker.crack(hashes, wordlist, hash_algorithm_name, file_location)


class Scanner(tk.Frame):
    def __init__(self, parent, controller):
        # StringVars that will later be used as arguments in function
        output_string_net = tk.StringVar()
        output_string_port = tk.StringVar()

        # When called, starts a background thread. run_arp() redirects terminal output to output_string
        def _run_network_scan(ip_add: str):
            output_string_net.set("")
            background_thread = threading.Thread(target=self.run_arp_gui,
                                                 args=(output_string_net, ip_add))
            background_thread.start()

        # When called, starts a background thread. run_port_scan_gui() redirects terminal output to output_string
        def _run_port_scan(target_host: str, start_port: int, end_port: int, threads: int):
            output_string_port.set("")
            background_thread = threading.Thread(target=self.run_port_scan_gui,
                                                 args=(output_string_port, target_host, start_port, end_port, threads))
            background_thread.start()

        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=4)
        self.columnconfigure((1, 2, 3, 4), weight=1)

        # Back to start page button
        button1 = ttk.Button(self, text="Back to Start Page", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0, sticky="NW")

        # Welcome text, label
        title_label = tk.Label(self, text="Welcome to EZ Scanner", font=header)
        title_label.grid(row=1, column=0, columnspan=6)

        # NETWORK SCANNER
        # -------------------------------------------

        # Choose host to scan, Label and Entry box
        entry_label1 = tk.Label(self, text="Enter a network to scan")
        entry_label1.grid(row=2, column=0)
        subdomain_entry = tk.Entry(self)
        subdomain_entry.grid(row=3, column=0)

        #Example Label
        example_label = tk.Label(self, text="Example: 192.168.1.0/24")
        example_label.grid(row=4, column=0)

        # Run Network scanner, button
        net_run_button = tk.Button(self, text="Run Network Scan",
                                   command=lambda: _run_network_scan(subdomain_entry.get()))
        net_run_button.grid(row=5, column=0)

        # Result, Canvas, Frame, Scrollbar, Label
        net_canvas_frame = tk.Frame(self)
        net_canvas_frame.grid(row=6, column=0)
        net_canvas_frame.grid_rowconfigure(0, weight=1)
        net_canvas_frame.grid_columnconfigure(0, weight=1)
        net_canvas_frame.grid_propagate(False)
        net_result_canvas = tk.Canvas(net_canvas_frame, bg="white")
        net_result_canvas.grid(row=0, column=0, sticky="news")
        net_v_bar = ttk.Scrollbar(net_canvas_frame, orient="vertical", command=net_result_canvas.yview)
        net_v_bar.grid(row=0, column=1, sticky="ns")
        net_h_bar = ttk.Scrollbar(net_canvas_frame, orient="horizontal", command=net_result_canvas.xview)
        net_h_bar.grid(row=1, column=0, sticky="we")
        net_result_canvas.configure(yscrollcommand=net_v_bar.set, xscrollcommand=net_h_bar.set)
        net_result_frame = tk.Frame(net_result_canvas)
        net_result_canvas.create_window((0, 0), window=net_result_frame, anchor="nw")
        net_result_label = tk.Label(net_result_frame, textvariable=output_string_net, bg="white", justify=tk.LEFT)
        net_result_label.grid()
        net_result_frame.update_idletasks()
        net_canvas_frame.config(width=300 + net_v_bar.winfo_width(), height=400)
        net_result_frame.bind("<Configure>",
                              lambda e: net_result_canvas.configure(scrollregion=net_result_canvas.bbox("all")))

        # PORT SCANNER
        # -----------------------------------------

        # Choose host, label and button
        entry_label2 = tk.Label(self, text="Choose a host and ports to scan")
        entry_label2.grid(row=2, column=1, columnspan=4)
        port_host_label = tk.Label(self, text="Host:")
        port_host_label.grid(row=3, column=1, sticky="E")
        port_host_entry = tk.Entry(self)
        port_host_entry.grid(row=3, column=2, sticky="W")

        # How many threads to use, Entry and Label
        threads_port_label = tk.Label(self, text="Threads:")
        threads_port_label.grid(row=3, column=3, sticky="E")
        threads_port_entry = tk.Entry(self)
        threads_port_entry.grid(row=3, column=4, sticky="W")

        # How many ports, Entries and Labels
        start_port_label = tk.Label(self, text="Start Port:")
        start_port_label.grid(row=4, column=1, sticky="E")
        start_port_entry = tk.Entry(self)
        start_port_entry.grid(row=4, column=2, sticky="W")
        end_port_label = tk.Label(self, text="End Port:")
        end_port_label.grid(row=4, column=3, sticky="E")
        end_port_entry = tk.Entry(self)
        end_port_entry.grid(row=4, column=4, sticky="W")

        # Run port scanner, button
        port_button = tk.Button(self, text="Run Port Scan",
                                command=lambda: _run_port_scan(port_host_entry.get(), int(start_port_entry.get()),
                                                               int(end_port_entry.get()),
                                                               int(threads_port_entry.get())))
        port_button.grid(row=5, column=1, columnspan=4)

        # Result, Canvas, Frame, Scrollbar, Label
        port_canvas_frame = tk.Frame(self)
        port_canvas_frame.grid(row=6, column=1, columnspan=4)
        port_canvas_frame.grid_rowconfigure(0, weight=1)
        port_canvas_frame.grid_columnconfigure(0, weight=1)
        port_canvas_frame.grid_propagate(False)
        port_result_canvas = tk.Canvas(port_canvas_frame, bg="white")
        port_result_canvas.grid(row=0, column=0, sticky="news")
        port_v_bar = ttk.Scrollbar(port_canvas_frame, orient="vertical", command=port_result_canvas.yview)
        port_v_bar.grid(row=0, column=1, sticky="ns")
        port_h_bar = ttk.Scrollbar(port_canvas_frame, orient="horizontal", command=port_result_canvas.xview)
        port_h_bar.grid(row=1, column=0, sticky="we")
        port_result_canvas.configure(yscrollcommand=port_v_bar.set, xscrollcommand=port_h_bar.set)
        port_result_frame = tk.Frame(port_result_canvas)
        port_result_canvas.create_window((0, 0), window=port_result_frame, anchor="nw")
        port_result_label = tk.Label(port_result_frame, textvariable=output_string_port, bg="white", justify=tk.LEFT)
        port_result_label.grid()
        port_result_frame.update_idletasks()
        port_canvas_frame.config(width=300 + port_v_bar.winfo_width(), height=400)
        port_result_frame.bind("<Configure>",
                               lambda e: port_result_canvas.configure(scrollregion=port_result_canvas.bbox("all")))


    def run_arp_gui(self, output, ip_add: str):
        """To redirect the output of scapy.arping() to StringVar

        This function takes the output of scapy.arping() and redirects it to a StringVar,
        used to display the output in a GUI interface.
        To be called as a background thread.
        """

        redirector = StdoutRedirector(output)
        with redirect_stdout(redirector):
            scanner.run_arp(ip_add)

    def run_port_scan_gui(self, output: tk.StringVar, target_host: str, start_port: int, end_port: int, threads: int):
        """To redirect the output of run_port_scan() to StringVar

        This function takes the output of run_port_scan() and redirects it to a StringVar,
        used to display the output in a GUI interface.
        To be called as a background thread.
        """

        redirector = StdoutRedirector(output)
        with redirect_stdout(redirector):
            scanner.run_port_scan(target_host, start_port, end_port, threads)


class DirBuster(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        output_string = tk.StringVar()

        self.columnconfigure((0, 1, 2, 3), weight=1)

        def _run_buster_gui(wordlist: str, threads: int, target_ip: str, save_to_file):
            background_thread = threading.Thread(target=self.bust_gui,
                                                 args=(output_string, wordlist, threads, target_ip, save_to_file))
            background_thread.start()

        # Title and and back to Start Page Button
        button1 = ttk.Button(self, text="Back to Start Page", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0, sticky="NW")
        title_label = tk.Label(self, text="EZ Directory Busting", font=header)
        title_label.grid(row=1, column=0, columnspan=4)

        # Target Label and Entry
        target_label = tk.Label(self, text="Target:")
        target_label.grid(row=2, column=0, sticky="E")
        target_entry = tk.Entry(self, width=30)
        target_entry.grid(row=2, column=1, sticky="W")

        # Choose wordlist file entry and button
        choose_file_entry = tk.Entry(self, bg="white", width=30)
        choose_file_entry.grid(row=3, column=1, sticky="W")
        choose_file_button = ttk.Button(self, text="* Choose Wordlist", width=16,
                                        command=lambda: browse_files(choose_file_entry))
        choose_file_button.grid(row=3, column=0, sticky="E")

        result_file_entry = tk.Entry(self, bg="white", width=30)
        result_file_entry.grid(row=3, column=3, sticky="W")
        result_file_button = ttk.Button(self, text="Save to", width=16,
                                        command=lambda: save_file(result_file_entry))
        result_file_button.grid(row=3, column=2, sticky="E")

        # Amount of Threads Label and Entry
        threads_label = tk.Label(self, text="Threads:")
        threads_label.grid(row=2, column=2, sticky="E")
        threads_entry = tk.Entry(self, width=30)
        threads_entry.grid(row=2, column=3, sticky="W")

        run_button = ttk.Button(self, text="Run Buster", width=30,
                                command=lambda: _run_buster_gui(choose_file_entry.get(), int(threads_entry.get()),
                                                                target_entry.get(), result_file_entry.get()))
        run_button.grid(row=6, column=0, columnspan=4)

        space2 = tk.Label(self)
        space2.grid(row=5)

        # Result, Canvas, Frame, Scrollbar, Label
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(row=8, column=0, columnspan=4)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_propagate(False)
        result_canvas = tk.Canvas(canvas_frame, bg="white")
        result_canvas.grid(row=0, column=0, sticky="news")
        v_bar = ttk.Scrollbar(canvas_frame, orient="vertical", command=result_canvas.yview)
        v_bar.grid(row=0, column=1, sticky="ns")
        h_bar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=result_canvas.xview)
        h_bar.grid(row=1, column=0, sticky="we")
        result_canvas.configure(yscrollcommand=v_bar.set, xscrollcommand=h_bar.set)
        result_frame = tk.Frame(result_canvas)
        result_canvas.create_window((0, 0), window=result_frame, anchor="nw")
        result_label = tk.Label(result_frame, textvariable=output_string, bg="white", justify=tk.LEFT)
        result_label.grid()
        result_frame.update_idletasks()
        canvas_frame.config(width=400 + v_bar.winfo_width(), height=350)
        result_frame.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))

    def bust_gui(self, output: tk.StringVar, wordlist: str, threads: int, target_ip: str, save_to_file: str):
        """To redirect the output of run_brute_force_directories() to StringVar

        This function takes the output of run_brute_force_directories() and redirects it to a StringVar,
        used to display the output in a GUI interface.
        To be called as a background thread.
        """
        redirector = StdoutRedirector(output)
        with redirect_stdout(redirector):
            dirbuster.run_brute_force_directories(wordlist, threads, target_ip, save_to_file)


class LoginCracker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.columnconfigure((0, 1, 2, 3), weight=1)

        output_string = tk.StringVar()

        def _show_form_gui(url):
            output_string.set("")
            background_thread = threading.Thread(target=self.show_form_gui,
                                                 args=(output_string, url))
            background_thread.start()

        def _run_login_cracker_gui(url, u_index, p_index, users_file, password_file):
            output_string.set("")
            background_thread = threading.Thread(target=self.run_login_cracker_gui,
                                                 args=(output_string, url, u_index, p_index, users_file, password_file))
            background_thread.start()

        # Title and and back to Start Page Button
        button1 = ttk.Button(self, text="Back to Start Page", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0, sticky="NW")
        title_label = tk.Label(self, text="EZ Login Cracker", font=header)
        title_label.grid(row=0, column=0, columnspan=4, rowspan=2)

        # Target/URL Button and Label
        url_label = tk.Label(self, text="URL:")
        url_label.grid(row=2, column=0, sticky="E")
        url_entry = tk.Entry(self, width=30)
        url_entry.grid(row=2, column=1, sticky="W")

        # Username index label and entry
        u_index_label = tk.Label(self, text="Username Index:")
        u_index_label.grid(row=3, column=0, sticky="E")
        u_index_entry = tk.Entry(self, width=30)
        u_index_entry.grid(row=3, column=1, sticky="W")

        # Password index label and entry
        p_index_label = tk.Label(self, text="Password Index:")
        p_index_label.grid(row=3, column=2, sticky="E")
        p_index_entry = tk.Entry(self, width=30)
        p_index_entry.grid(row=3, column=3, sticky="W")

        # Choose Username file
        choose_users_file_entry = tk.Entry(self, width=30)
        choose_users_file_entry.grid(row=4, column=1, sticky="W")
        choose_users_file_button = ttk.Button(self, text="Choose Usernames",
                                              command=lambda: browse_files(choose_users_file_entry))
        choose_users_file_button.grid(row=4, column=0, sticky="E")

        # Choose Password file
        choose_passwords_file_entry = tk.Entry(self, width=30)
        choose_passwords_file_entry.grid(row=4, column=3, sticky="W")
        choose_password_file_button = ttk.Button(self, text="Choose Passwords",
                                                 command=lambda: browse_files(choose_passwords_file_entry))
        choose_password_file_button.grid(row=4, column=2, sticky="E")

        space_label = tk.Label(self)
        space_label.grid(row=5)

        form_information = tk.Label(self, text="Show form to find username and password indexes")
        form_information.grid(row=6, column=0, columnspan="4")

        # Show form button
        show_form_button = ttk.Button(self, text="Show Form", width=20,
                                      command=lambda: _show_form_gui(url_entry.get()))
        show_form_button.grid(row=7, column=0, columnspan=4)

        # Run Button
        run_button = ttk.Button(self, text="Run Login Cracker", width=20,
                                command=lambda: _run_login_cracker_gui(url_entry.get(), int(u_index_entry.get()),
                                                                       int(p_index_entry.get()),
                                                                       choose_users_file_entry.get(),
                                                                       choose_passwords_file_entry.get()))
        run_button.grid(row=8, column=0, columnspan=4)

        space_label2 = tk.Label(self)
        space_label2.grid(row=9)

        # Result, Canvas, Frame, Scrollbar, Label
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(row=10, column=0, columnspan=4)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_propagate(False)
        result_canvas = tk.Canvas(canvas_frame, bg="white")
        result_canvas.grid(row=0, column=0, sticky="news")
        v_bar = ttk.Scrollbar(canvas_frame, orient="vertical", command=result_canvas.yview)
        v_bar.grid(row=0, column=1, sticky="ns")
        h_bar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=result_canvas.xview)
        h_bar.grid(row=1, column=0, sticky="we")
        result_canvas.configure(yscrollcommand=v_bar.set, xscrollcommand=h_bar.set)
        result_frame = tk.Frame(result_canvas)
        result_canvas.create_window((0, 0), window=result_frame, anchor="nw")
        result_label = tk.Label(result_frame, textvariable=output_string, bg="white", justify=tk.LEFT)
        result_label.grid()
        result_frame.update_idletasks()
        canvas_frame.config(width=400 + v_bar.winfo_width(), height=350)
        result_frame.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))

    def show_form_gui(self, output: tk.StringVar, url: str):
        """To redirect the output of print_forms() to StringVar

        This function takes the output of print_forms() and redirects it to a StringVar,
        used to display the output in a GUI interface.
        To be called as a background thread.
        """
        form = logincracker.find_login_form(url)
        redirector = StdoutRedirector(output)
        with redirect_stdout(redirector):
            if form is not None:
                logincracker.print_form(form)

    def run_login_cracker_gui(self, output: tk.StringVar, url: str, u_index: int,
                              p_index: int, users_file: str, password_file: str):
        """To redirect the output of run_login_cracker() to StringVar

        This function takes the output of run_login_cracker() and redirects it to a StringVar,
        used to display the output in a GUI interface.
        To be called as a background thread.
        """
        redirector = StdoutRedirector(output)
        with redirect_stdout(redirector):
            logincracker.run_login_cracker(url, u_index, p_index, users_file, password_file)


# StdoutRedirector is later used together with redirect_stdout. Used to redirect output to GUI
class StdoutRedirector:
    def __init__(self, str_var: tk.StringVar):
        self.text = ""
        self.str_var = str_var

    def write(self, to_write: tk.StringVar):
        self.text += to_write
        self.str_var.set(self.text)


app = HackerSuiteGUI()
app.mainloop()

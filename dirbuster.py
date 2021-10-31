import queue
import threading
import time
import urllib3
import urllib.error as u_error

ext = [".php", ".html", ".txt"]


# This function adds all the words from a wordlist to a Queue
def _add_wordlist_to_queue(wordlist: str, words_queue: queue.Queue) -> queue.Queue:
    with open(wordlist) as file:
        raw = file.readline()
        while raw:
            word = raw.strip()
            words_queue.put(word)
            raw = file.readline()
    return words_queue


def brute_force_directories(words_queue: queue, target: str, result_queue: queue, extensions: list = None):
    """Goes through all the words in a Queue to discover directories and files.

    This function gets the words from a Queue and tries to find url paths on a web server.
    To work, the function need a queue, a target and a list of extensions (optional).
    """
    while not words_queue.empty():
        try_this_word = words_queue.get()
        try_list = []

        # Checks to see if the word contains an extension or not. If not, the word is used as a directory
        if "." not in try_this_word:
            try_list.append("{}/{}".format(target, try_this_word))
            try_list.append("{}/{}/".format(target, try_this_word))
            try_list.append("{}.{}".format(try_this_word, target))
        else:
            try_list.append("{}/{}".format(target, try_this_word))

        # If extensions are available, the extensions will be added to the word
        if extensions and "." not in try_this_word:
            for ex in extensions:
                try_list.append("{}/{}{}".format(target, try_this_word, ex))

        # quote is used to making it safe for use as URL components by quoting special characters
        for brute_force in try_list:
            # url = "{}".format(u_parse.quote(brute_force))
            url = brute_force

            # Sends a GET request to targeted url
            try:
                http = urllib3.PoolManager()
                response = http.request("GET", url=url)

                # If a response other than 404 is received, print status and url
                if len(response.data) and response.status != 404:
                    success_string = "[{}] => {}".format(response.status, url)
                    print(success_string)
                    result_queue.put(success_string)

            # In an error occurs and it is not 404, the error and the url will be printed.
            # MaxRetryError may occur when trying to reach a subdomain that doesn't exist.
            except(u_error.URLError, u_error.HTTPError, urllib3.exceptions.MaxRetryError):
                if hasattr(u_error.HTTPError, "code") and u_error.HTTPError.code != 404:
                    success_string = "Exception! [{}] => {}".format(u_error.HTTPError.code, url)
                    print(success_string)
                    result_queue.put(success_string)
                pass
        words_queue.task_done()


def run_brute_force_directories(wordlist: str, threads: int, target_ip: str, save_file: str = None):
    """Runs brute_force_directories with several threads

    This function creates several threads that calls the brute_force_directories function.
    It also runs _add_wordlist_to_queue. The function needs a wordlist, amount of threads and target
    as arguments.
    """

    start_time = time.time()
    print("Started Directory Busting")
    words_queue = queue.Queue()
    result_queue = queue.Queue()
    _add_wordlist_to_queue(wordlist, words_queue)
    for i in range(threads):
        t = threading.Thread(target=brute_force_directories, args=(words_queue, target_ip, result_queue, ext,))
        t.daemon = True
        t.start()
    words_queue.join()
    if save_file != "":
        with open(save_file, "a") as file:
            for success_string in result_queue.queue:
                file.write(success_string+"\n")
    print("DONE! \nTime taken: ", time.time() - start_time)

import hashlib
import threading
import time
import queue


def get_hash_function(hash_type: str) -> hashlib:
    """A function used to choose hash algorithm.

    This function is created to easily choose a hashing algorithm,
    by translating a string value (input) to a hashlib function (output)
    """

    if hash_type == "md5":
        return hashlib.md5
    elif hash_type == "sha1":
        return hashlib.sha1
    elif hash_type == "sha256":
        return hashlib.sha256
    elif hash_type == "sha512":
        return hashlib.sha512
    else:
        print("Enter a valid hash algorithm")
        exit()


def _build_queue(words_queue: queue, word_file: str) -> queue:
    """This function reads all words from a wordlist and puts them in a Queue"""

    with open(word_file, "r") as file:
        raw = file.readline()
        while raw:
            word = raw.strip()
            words_queue.put(word)
            raw = file.readline()
    return words_queue


def _threader(word_list: list, hash_queue: queue, hash_algorithm_name: str, result_queue: queue):
    while True:
        hash_value = hash_queue.get()
        crack(hash_value, word_list, hash_algorithm_name, result_queue)
        hash_queue.task_done()


def crack(hash_value: str, word_list: list, hash_algorithm_name: str, result_queue: queue):
    hash_algorithm = get_hash_function(hash_algorithm_name)
    for word in word_list:
        hashed_word = hash_algorithm(word.encode("utf")).hexdigest()
        if hashed_word == hash_value:
            print("Password Found: {0} = {1}".format(word, hash_value))
            result_queue.put(word)
            break


def run_crack(hash_file: str, word_file: str, hash_algorithm_name: str, file_location: str, threads: int):
    start_time = time.time()
    hash_queue = queue.Queue()
    result_queue = queue.Queue()
    word_list = []
    print("Building wordlist from file!")
    with open(word_file, "r") as file:
        for line in file:
            word = line.strip()
            word_list.append(word)

    print("Cracking started")

    for i in range(threads):
        t = threading.Thread(target=_threader, args=(word_list, hash_queue, hash_algorithm_name, result_queue,))
        t.daemon = True
        t.start()

    _build_queue(hash_queue, hash_file)
    hash_queue.join()
    print("DONE! \nTime taken:", time.time() - start_time)

    if file_location != "":
        file_time = time.time()
        print("Started writing result to file...")
        with open(file_location, "w") as file:
            for password in result_queue.queue:
                file.write(password + "\n")
        print("All passwords written to file after", time.time() - file_time)

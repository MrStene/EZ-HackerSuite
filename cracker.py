import hashlib
import time


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


def crack(hashes: str, wordlist: str, hash_algorithm_name: str, file_location: str):
    """Tries to crack every password in a wordlist.

    This function loops through every word in a file containing hash values,
    and tries to match it with a word from a separate file/wordlist.
    If a match is found, it may be added to a file, if chosen.
    The match may also only be printed to terminal.
    """

    start_time = time.time()
    hash_algorithm = get_hash_function(hash_algorithm_name)
    print("Cracking Started")

    # Opens all the files that will be used
    with open(hashes, "r") as hash_list, open(wordlist, "r") as word_file:

        # Loops through all hash values
        for hash_value in hash_list:
            hashed_password = hash_value.strip()
            word_file.seek(0, 0)

            # All hash values are compared to each word in a wordlist
            for word in word_file:
                password = word.strip()
                hashed_word = hash_algorithm(password.encode("utf")).hexdigest()

                # If a match is found, it is printed to the terminal and written to file (if selected)
                if hashed_word == hashed_password:
                    print("Password Found: {0} = {1}".format(password, hashed_password))
                    if file_location != "":
                        with open(file_location, "a") as result_file:
                            result_file.write("{}\n".format(password))
                    break

    print("DONE! \nTime taken: ", time.time() - start_time)

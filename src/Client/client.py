import requests

r = requests.get("http://localhost:5000/listdogs/")
print( r.text )


def main():
    r = requests.get("http://localhost:5000/listdogs/")
    print( r.text )
    while True: # no do while in python :(
        command = input(">")
        if len(command) == 0:
            continue
        command = command.split()
        if command[0].lower() == 'a':
            r = requests.get("http://localhost:5000/adddog/" + command[1])
        elif command[0].lower() == 'l':
            r = requests.get("http://localhost:5000/listdogs/")
        if command[0].lower() == 'd':
            r = requests.get("http://localhost:5000/removedog/" + command[1])
        elif command[0].lower() == 'q':
            return
        print(r.text)




if __name__ == "__main__":
    main()

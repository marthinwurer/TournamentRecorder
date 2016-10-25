"""
This python program runs a simple shell to query the database remotely.
"""
import requests

import tr_api

def concat_end(lst, start_index):
    total = None
    for i in range( start_index, len(lst)):
        if total == None:
            total = lst[i]
        else:
            total = total + " " + lst[i]
    return total


def main():
    while True: # no do while in python :(
        result = None
        command = input(">")
        if len(command) == 0:
            continue
        command = command.split()

        try:
            if command[0].lower() == 'ap':
                # concatenate the command strings after a certain point together so
                # that first and last names can be added. 
                name = concat_end(command, 2)
                if name == None:
                    raise IndexError("No name")
                result = tr_api.addPlayer(command[1], name)
            elif command[0].lower() == 'lp':
                result = tr_api.listPlayers()
            elif command[0].lower() == 'exit':
                return

            else:
                print("Invalid command")
                continue
        except IndexError:
            print("Invalid number of parameters")
            continue

        print( result)




if __name__ == "__main__":
    main()

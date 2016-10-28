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
            if command[0].lower() == 'cp':
                # concatenate the command strings after a certain point together so
                # that first and last names can be added. 
                name = concat_end(command, 2)
                if name == None:
                    raise IndexError("No name")
                result = tr_api.createPlayer(int(command[1]), name)
            elif command[0].lower() == 'ct':
                # concatenate the command strings after a certain point together so
                # that first and last names can be added. 
                name = concat_end(command, 2)
                if name == None:
                    raise IndexError("No name")
                result = tr_api.createTournament(name, int(command[1]))
            elif command[0].lower() == 'sp':
                # concatenate the command strings after a certain point together so
                # that first and last names can be added. 
                name = concat_end(command, 1)
                if name == None:
                    raise IndexError("No name")
                result = tr_api.searchPlayers(name)
            elif command[0].lower() == 'ap':
                result = tr_api.addPlayer(int(command[1]),int(command[2]))
            elif command[0].lower() == 'rp':
                result = tr_api.removePlayer(int(command[1]),int(command[2]))
            elif command[0].lower() == 'lp':
                result = tr_api.listPlayers()
            elif command[0].lower() == 'lt':
                result = tr_api.listTournaments(None, None)
            elif command[0].lower() == 'ltp':
                result = tr_api.listTournamentPlayers(int(command[1]))
            elif command[0].lower() == 'fr':
                result = tr_api.finishRound(int(command[1]))
            elif command[0].lower() == 'genpairings':
                result = tr_api.generatePairings(int(command[1]))
            elif command[0].lower() == 'gp':
                result = tr_api.getPlayer(int(command[1]))
            elif command[0].lower() == 'lm':
                result = tr_api.matchList(int(command[1]))
            elif command[0].lower() == 'lr':
                result = tr_api.roundList(int(command[1]))
            elif command[0].lower() == 'st':
                result = tr_api.startTournament(int(command[1]))
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

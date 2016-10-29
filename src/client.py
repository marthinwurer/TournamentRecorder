"""
This python program runs a simple shell to query the database remotely.
Autor: TangentTally
"""
import json

import tr_api

def concat_end(lst, start_index):
    total = None
    for i in range( start_index, len(lst)):
        if total == None:
            total = lst[i]
        else:
            total = total + " " + lst[i]
    return total


def print_help():

    print(
"""
ap p_id t_id - add a player with id p_id to the tournament with id t_id
cp DCI name - create a player with DCI number (id) and name. Name can have spaces.
ct rounds name - create a new tournament with max number of rounds and name. name can have spaces.
fr r_id - finish a round with the given ID
genpairings t_id - generate the pairings for a given round.
gp p_id - get the information for a given player
lp - list all players in the system
lt - list all tournaments in the system
ltp t_id - list all the players in a given tournament
ml r_id - list all the matches in a round
rp p_id t_id - remove a given player from a given tournament
rl t_id - list the rounds in a tournament
sp partial_name - Search for a partial name in the list of players
smr m_id, p1_wins, p2_wins, draws - sets the results of a match, with wins and draws
st t_id - starts a tournament and generates the pairings for the first round.
""")



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
                print(result)
            elif command[0].lower() == 'rp':
                result = tr_api.removePlayer(int(command[1]),int(command[2]))
                print(result)
            elif command[0].lower() == 'lp':
                result = tr_api.listPlayers()
                table_print(result)
            elif command[0].lower() == 'lt':
                result = tr_api.listTournaments(None, None)
                table_print(result)
            elif command[0].lower() == 'ltp':
                result = tr_api.listTournamentPlayers(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'fr':
                result = tr_api.finishRound(int(command[1]))
                print(result)
            elif command[0].lower() == 'genpairings':
                result = tr_api.generatePairings(int(command[1]))
                print(result)
            elif command[0].lower() == 'gp':
                result = tr_api.getPlayer(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'lm':
                result = tr_api.matchList(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'lr':
                result = tr_api.roundList(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'st':
                result = tr_api.startTournament(int(command[1]))
                print(result)
            elif command[0].lower() == 'smr':
                result = tr_api.setMatchResults(
                        int(command[1]), int(command[2]), int(command[3]), int(command[4]))
                print(result)


            elif command[0].lower() == 'help':
                print_help()
                continue



            elif command[0].lower() == 'exit':
                return

            else:
                print("Invalid command")
                continue
        except IndexError:
            print("Invalid number of parameters")
            continue



def table_print(result):
    if isinstance(result, dict):
        print(json.dumps(result["rows"], sort_keys=True, indent=4))

    else:
        print("API return Error")


if __name__ == "__main__":
    main()

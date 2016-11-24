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
lm r_id - list all the matches in a round
rp p_id t_id - remove a given player from a given tournament
lr t_id - list the rounds in a tournament
sp partial_name - Search for a partial name in the list of players
smr m_id, p1_wins, p2_wins, draws - sets the results of a match, with wins and draws
st t_id - starts a tournament and generates the pairings for the first round.

exit - exits the shell
help - show this message
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
                table_print(result)
            elif command[0].lower() == 'ct':
                # concatenate the command strings after a certain point together so
                # that first and last names can be added. 
                name = concat_end(command, 2)
                if name == None:
                    raise IndexError("No name")
                result = tr_api.createTournament(name, int(command[1]))
                table_print(result)
            elif command[0].lower() == 'sp':
                # concatenate the command strings after a certain point together so
                # that first and last names can be added. 
                name = concat_end(command, 1)
                if name == None:
                    raise IndexError("No name")
                result = tr_api.searchPlayers(name)
                table_print(result)
            elif command[0].lower() == 'ap':
                result = tr_api.addPlayer(int(command[1]),int(command[2]))
                table_print(result)
            elif command[0].lower() == 'rp':
                result = tr_api.removePlayer(int(command[1]),int(command[2]))
                table_print(result)
            elif command[0].lower() == 'lp':
                result = tr_api.listPlayers()
                table_print(result)
            elif command[0].lower() == 'lt':
                result = tr_api.listTournaments(None, None)
                table_print(result)
            elif command[0].lower() == 'ltp':
                result = tr_api.listTournamentPlayers(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'latp':
                result = tr_api.listActiveTournamentPlayers(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'fr':
                result = tr_api.finishRound(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'genpairings':
                result = tr_api.generatePairings(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'gp':
                result = tr_api.getPlayer(int(command[1]))
                player_print(result)
            elif command[0].lower() == 'lm':
                result = tr_api.matchList(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'lr':
                result = tr_api.roundList(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'st':
                result = tr_api.startTournament(int(command[1]))
                table_print(result)
            elif command[0].lower() == 'smr':
                result = tr_api.setMatchResults(
                        int(command[1]), int(command[2]), int(command[3]), int(command[4]))
                table_print(result)

            elif command[0].lower() == 'help':
                print_help()
                continue

            elif command[0].lower() == 'exit':
                return

            else:
                print("Invalid command")
                continue
        except ValueError:
            print("Invalid parameter type")
            continue
        except IndexError:
            print("Invalid number of parameters")
            continue


def table_print(result):
    # result["rows"] returns list of dicts
    if 'rows' in list(result.keys()):
        try:

            keys = list(result['rows'][0].keys())
        except IndexError:
            print("No results found")
            return
        values = []
        output = ''
        length = 0
        value_order = {'id': 0}
        if 'id' in keys:
            output = output + " {:>10}"
            values.append("ID")
            length += 11

        if 'name' in keys:
            output = output + " {:>30}"
            values.append("Name")
            length += 31

        if 'num_players' in keys:
            output = output + "  {:>12}"
            values.append("# of Players")
            length += 14

        if 'p_id' in keys:  # Know we are printing Tournament Player
            output = output + " {:>10}"
            values.append("P_ID")
            length += 11
            # Dropped printing
            output = output + "  {:>7}"
            values.append("Dropped")
            length += 9
            # standings
            output = output + "  {:>7}"
            values.append("standing")
            length += 9

        if 'table_number' in keys:  # Know we are printing Matches
            output = output + "  {:>7}"
            values.append("Table #")
            length += 9
            # P1_ID printing
            output = output + "  {:>5}"
            values.append("P1_ID")
            length += 7
            # P2_ID printing
            output = output + "  {:>5}"
            values.append("P2_ID")
            length += 7
            # P1_wins printing
            output = output + "  {:>7}"
            values.append("P1_wins")
            length += 9
            # P2_wins printing
            output = output + "  {:>7}"
            values.append("P2_wins")
            length += 9
            # Draws printing
            output = output + "  {:>5}"
            values.append("Draws")
            length += 7

        if 'number' in keys:  # Know we are printing Rounds
            output = output + "  {:>7}"
            values.append("Round #")
            length += 9
            # Start Date printing
            output = output + " {:>20}"
            values.append("Start")
            length += 21
            # Draws printing
            output = output + " {:>20}"
            values.append("End")
            length += 21

        print(output.format(*values))
        print('-' * length)
        values.clear()
        for row in result['rows']:
            attributes = list(row.keys())
            values.append(row['id'])

            if 'table_number' in attributes:
                values.append(row['table_number'])
                values.append(row['p1_id'])
                p2 = row['p2_id']
                if row['p2_id'] is None:
                    p2 = '-'
                values.append(p2)
                p1 = row['p1_wins']
                if row['p1_wins'] is None:
                    p1 = '-'
                values.append(p1)
                p2 = row['p2_wins']
                if row['p2_wins'] is None:
                    p2 = '-'
                values.append(p2)
                draw = row['draws']
                if row['draws'] is None:
                    draw = '-'
                values.append(draw)

            elif 'number' in attributes:
                values.append(row['number'])
                values.append(row['start_date'])
                end = row['end_date']
                if row['end_date'] is None:
                    end = ''
                values.append(end)

            elif 'p_id' in attributes:
                values.append(row['name'])
                values.append(row['p_id'])
                drop = 1
                if row['dropped'] is None:
                    drop = 0
                values.append(drop)
                values.append(row['standing'])

            elif 'num_players' in attributes:
                values.append(row['name'])
                values.append(row['num_players'])

            else:
                values.append(row['name'])

            print(output.format(*values))
            values.clear()

    elif 'outcome' in list(result.keys()):
        if result['outcome']:
            print('Success')
        else:
            print('Fail, Contact Dev')
            try:
                print(result['reason'])
            except:
                pass



def player_print(result):
    print(" {:>10} {:>30}".format('ID', 'Name'))
    print('-' * 42)
    print(" {:>10} {:>30}".format(result['id'], result['name']))


if __name__ == "__main__":
    main()

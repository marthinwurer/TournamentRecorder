from tkinter import *
from tkinter import messagebox
import tr_api

class clientApp ( Tk ) :
    # base widgets/modules
    g_master = None
    g_menubar = None

    # entry box input
    input_tournName = None
    input_tournMaxRounds = None
    input_playerDCI = None
    input_playerName = None

    activeTourn = None

    def __init__  ( self, master ) :
        global g_master
        global g_menubar

        self.g_master = master
        self.g_master.title ( "Tournament Recorder" )

        label = Label ( self.g_master, text = "" )
        label.pack ()

        self.g_master.minsize ( 500,500 )

        self.g_menubar = Menu (self. g_master )

        self.g_master.config ( menu = self.g_menubar )

        self.action_createMenu ()

    def action_createMenu ( self ) :
        global g_menubar
        self.create_menu_file ( )
        self.create_menu_tourn ( )
        self.create_menu_players ( )

    def create_menu_file ( self ) :
        global g_menubar

        menu_file = Menu ( self.g_menubar )
        menu_file.add_command ( label = "Exit", command = self.g_master.quit )

        self.g_menubar.add_cascade ( label = "File", menu = menu_file )

    def create_menu_tourn ( self ):
        menu_tourn = Menu ( self.g_menubar )
        menu_tourn.add_command ( label = "List Tournament", command = self.action_listTournaments )
        menu_tourn.add_command ( label = "Start Tournament", command = self.action_startTournament )

        menu_tourn.add_separator ()

        menu_tourn.add_command ( label = "Create Tournament", command = self.action_createTournament )

        self.g_menubar.add_cascade ( label = "Tournaments", menu = menu_tourn )

    def create_menu_players ( self ) :
        menu_players = Menu ( self.g_menubar )
        menu_players.add_command ( label = "List Player", command = self.action_listPlayers )
        menu_players.add_separator ()
        menu_players.add_command ( label = "Create Player", command = self.action_createPlayer )
        # menu_players.add_command ( label = "Add Player", command = self.action_addPlayer )

        self.g_menubar.add_cascade ( label = "Players", menu = menu_players )

    def action_listTournaments ( self ) :
        '''
        creates a new window to submit results of a match.
        '''

        self.win_listTourn = Tk()  # create the new window
        self.win_listTourn.title ( "Tournaments" )  # set the title of window
        Label ( self.win_listTourn, text="Tournaments", font = ( "Helvetica", 16 ) ).pack ( )

        frame_tournList = Frame ( self.win_listTourn )  # create a frame
        frame_tournList.pack ( side = "top", padx = 20, pady = 20 )  # and place it on the top

        # create the labels that define what each input box is used for, and align them
        Label ( frame_tournList, text = "Tournament Name" ).grid ( row = 0, column = 0, sticky = W )
        Label ( frame_tournList, text = "# of PLayers" ).grid ( row = 0, column = 1, sticky = W )

        tournaments = tr_api.listTournaments ( None, None )
        row_num = 0
        if "rows" not in tournaments.keys ( ):
            messagebox.showerror (
                "List Tournaments",
                "Database Communication Error"
            )
            return
        elif len ( tournaments["rows"] ) > 0:
            tourn_list = tournaments["rows"]
            for i in range ( 0, len ( tourn_list ) ):
                row_num = i+1
                Label ( frame_tournList, text = tourn_list[i]["name"] ).grid ( row = row_num, column = 0)
                Label ( frame_tournList, text = tourn_list[i]["num_players"] ).grid ( row = row_num, column = 1 )
                # Button(frame_tournList, text="Select", command= lambda j=i: print("List matches for " + str(tourn_list[j]["id"]))).grid(row=row_num, column=2)
                Button ( frame_tournList, text = "Select", command = lambda j=i: self.action_selectTournament ( tourn_list[j]["id"] ) ).grid ( row = row_num, column = 2 )

        # create the submit and cancel buttons
        btn_listTourn_close = Button(frame_tournList, text="Cancel", command=self.win_listTourn.destroy)

        # align the buttons
        btn_listTourn_close.grid(row=row_num+1, column=1)

        # bind these keystrokes
        self.win_listTourn.bind('<Escape>', self.win_listTourn.destroy)

        self.win_listTourn.mainloop()

    def action_selectTournament ( self, tourn_id ) :
        global activeTourn

        print ( "Selected Tournament " + str ( tourn_id ) )

        self.activeTourn = tourn_id

    def action_startTournament ( self ) :
        if ( self.activeTourn is None ) :
            messagebox.showerror(
                "Start Tournament",
                "Invalid selected tournament"
            )
            return
        print ( "Starting Tournament" )
        tr_api.startTournament ( activeTourn )

    def action_createTournament ( self ) :
        '''
            creates a new to submit tournament data.
        '''
        print ( "Creating Tournament" )

        global input_tournName
        global input_tournMaxRounds
        global win_createTourn

        self.win_createTourn = Tk ()                            # create the new window
        self.win_createTourn.title ( "Tournament Creation" )    # set the title of window
        self.win_createTourn.minsize ( 200, 100 )               # set the minimum (default) size
        Label ( self.win_createTourn, text="Create a new Tournament" ).pack ()

        frame_tournForm = Frame ( self.win_createTourn )        # create a frame
        frame_tournForm.pack ( side = "top" )                   #   and place it on the top

        # create the labels that define what each input box is used for, and align them
        Label ( frame_tournForm, text = "Tournament Name" ).grid ( row = 0, sticky = W )
        Label ( frame_tournForm, text = "Max Rounds" ).grid ( row = 1, sticky = W )

        # create the entry boxes and align them
        self.input_tournName = Entry ( frame_tournForm )
        self.input_tournName.grid ( row = 0, column = 1)
        self.input_tournMaxRounds = Entry ( frame_tournForm )
        self.input_tournMaxRounds.grid ( row = 1, column = 1)

        # create the submit and cancel buttons
        btn_createTourn_submit = Button ( frame_tournForm, text = "Submit", command = self.event_createTourn_submit )
        btn_createTourn_cancel = Button ( frame_tournForm, text = "Cancel", command = self.win_createTourn.destroy )

        # align the buttons
        btn_createTourn_submit.grid ( row = 2, column = 0 )
        btn_createTourn_cancel.grid ( row = 2, column = 1 )

        # bind these keystrokes
        self.win_createTourn.bind ( '<Return>', self.event_createTourn_submit )
        self.win_createTourn.bind ( '<Escape>', self.win_createTourn.destroy )

        self.win_createTourn.mainloop ()

    def event_createTourn_submit ( self ) :
        '''
            used to handle creation of tournament
        '''
        global input_tournName
        global input_tournMaxRounds

        global text_createTourn_failMsg

        # get the input values
        tournName = self.input_tournName.get ( )
        tournMaxRounds = self.input_tournMaxRounds.get ( )

        if ( len ( tournName ) >= 4 and tournMaxRounds.isdigit () ) :   # check values
            print ( "create tournament success" )
            tr_api.createTournament(tournName, tournMaxRounds)
            self.win_createTourn.destroy ( )    # destroy window on db submission
        else : # values are not valid, check what failed
            print ( "create tournament failed" )
            if ( len ( tournName ) < 4 ) :
                messagebox.showerror(
                    "Create Tournaments",
                    "tournament name length must be greater that 4"
                )
                print ( "Error: tournName length < 4" )

                return

            if ( not tournMaxRounds.isdigit () ) :
                messagebox.showerror(
                    "Create Tournaments",
                    "tournament max rounds must be greater than 1"
                )
                print ( "Error: tourn max rounds < 1" )

                return

        print ( "tournName: " + tournName )
        print ( "tournMaxRounds: " + tournMaxRounds )

    def action_listPlayers ( self ) :
        '''
            creates a new window to view player data.
        '''
        print ( "Listing Players" )

        self.win_listPlayer = Tk ()
        self.win_listPlayer.title ( "Players Viewer" )
        self.win_listPlayer.minsize ( 600, 400 )
        Label ( self.win_listPlayer, text = "Players Viewer" ).pack ()

        frame_playerFind = Frame ( self.win_listPlayer )
        frame_playerFind.pack ( side = "top" )
        frame_playerList = Frame ( self.win_listPlayer )
        frame_playerList.pack ( expand = True, side = "left")

        Label ( frame_playerFind, text = "Search For:" ).grid ( row = 0 )
        self.input_playerList_searchName = Entry ( frame_playerFind )
        self.input_playerList_searchName.grid ( row = 0, column = 1 )

        btn_playerFind_find = Button ( frame_playerFind, text = "Find", command = self.event_findPlayer ).grid ( row = 0, column = 2 )

        Label ( frame_playerList, fg = "blue", text = "DCI #" ).grid ( row = 0, column = 0 )
        Label ( frame_playerList, fg = "blue", text = "Player Name" ).grid ( row = 0, column = 1 )
        Label ( frame_playerList, fg = "blue", text = "----" ).grid ( row = 0, column = 2 )

        playerList = tr_api.listPlayers ( ) ['rows']

        row_count = 1
        for player in playerList :
            Label ( frame_playerList, text = player["id"] ).grid ( row = int(row_count), column = 0 )
            Label ( frame_playerList, text = player["name"] ).grid ( row = int(row_count), column = 1 )
            btn_playerEntry_add = Button ( frame_playerList, text = "Add" )
            btn_playerEntry_add.grid ( row = row_count, column = 2 )
            row_count += 1

        # scroll_playerList = Scrollbar ( frame_playerList )
        # scroll_playerList.pack ( side = "right", fill = "y" )
        # scroll_playerList.config ( command = win_listPlayer.yview )

    def event_findPlayer ( self ) :
        '''
            create the findPlayer window
        '''

        print ( "Finding player" )

        self.win_findPlayer = Tk ()
        self.win_findPlayer.title ( "Player Finder" )
        self.win_findPlayer.minsize ( 400, 200 )
        Label ( self.win_findPlayer, text = "Players Finder" ).pack ()

        scroll_playerList = Scrollbar ( self.win_findPlayer )
        scroll_playerList.pack ( side = "right", fill = "y" )

        self.list_playerList = Listbox ( self.win_findPlayer, yscrollcommand = scroll_playerList.set, selectmode = "multiple" )
        self.list_playerList.config ( width = "95" )
        self.list_playerList.pack ( side = "left", fill = "both" )

        scroll_playerList.config ( command = self.list_playerList.yview )

        playerList = tr_api.searchPlayers ( self.input_playerList_searchName.get () ) ['rows']

        for player in playerList :
            entry = str ( player["id"] ) + " " + player["name"]
            self.list_playerList.insert ( END, entry )

        btn_playerEntry_add = Button ( self.win_findPlayer, text = "Add to Active", command = self.action_addPlayer )
        btn_playerEntry_add.pack ()
        btn_playerEntry_cancel = Button ( self.win_findPlayer, text = "Cancel", command = self.win_findPlayer.quit )
        btn_playerEntry_cancel.pack ()

    def action_createPlayer ( self ) :
        '''
            creates a new window to submit new player data.
        '''
        print ( "Creating Player" )

        global input_playerDCI
        global input_playerName
        global win_createPlayer

        global text_createPlayer_failMsg

        self.win_createPlayer = Tk ()                       # create the new window
        self.win_createPlayer.title ( "Create Player" )     # set the title of window
        self.win_createPlayer.minsize ( 200, 100 )          # set the minimum (default) size
        Label ( self.win_createPlayer, text="Create a new Player" ).pack ()

        frame_playerForm = Frame ( self.win_createPlayer )   # create a frame
        frame_playerForm.pack ( side = "top" )               #   and place it on the top

        # create the labels that define what each input box is used for, and align them
        Label ( frame_playerForm, text = "DCI #" ).grid ( row = 0, sticky = W )
        Label ( frame_playerForm, text = "Name" ).grid ( row = 1, sticky = W )

        # create the entry boxes and align them
        self.input_playerDCI = Entry ( frame_playerForm )
        self.input_playerDCI.grid ( row = 0, column = 1 )
        self.input_playerName = Entry ( frame_playerForm )
        self.input_playerName.grid ( row = 1, column = 1 )

        # create the submit and cancel buttons
        btn_createPlayer_submit = Button ( frame_playerForm, text = "Submit", command = self.event_createPlayer_submit )
        btn_createPlayer_cancel = Button ( frame_playerForm, text = "Cancel", command = self.win_createPlayer.destroy )

        # align the buttons
        btn_createPlayer_submit.grid ( row = 2, column = 0 )
        btn_createPlayer_cancel.grid ( row = 2, column = 1 )

        # bind these keystrokes
        self.win_createPlayer.bind ( '<Return>', self.event_createPlayer_submit )
        self.win_createPlayer.bind ( '<Escape>', self.win_createPlayer.destroy )

        self.win_createPlayer.mainloop ()

    def event_createPlayer_submit ( self ) :
        '''
            used to handle creation of tournament
        '''
        global input_playerDCI
        global input_playerName

        global text_createPlayer_failMsg

        # get the input values
        playerDCI = self.input_playerDCI.get ( )
        playerName = self.input_playerName.get ( )

        if ( playerDCI.isdigit () and len ( playerName ) >= 3 ) :   # check values
            print ( "create player success" )

            self.win_createPlayer.destroy ( )    # destroy window on db submission
        else : # values are not valid, check what failed
            print ( "create player failed" )
            if ( len ( playerName ) < 3 ) :
                self.text_createPlayer_failMsg.set ( "player name length must be at least 3" )
                print ( "Error: tournName length < 4" )

            if ( not playerDCI.isdigit () ) :
                self.text_createPlayer_failMsg.set ( "max rounds must be a number" )
                print ( "Error: tourn max rounds not int" )

        print ( "playerDCI: " + playerDCI )
        print ( "playerName: " + playerName )

        tr_api.createPlayer ( playerDCI, playerName )

    def action_addPlayer ( self ) :
        if ( self.activeTourn is None ) :
            messagebox.showerror (
                "Start Tournament",
                "Invalid selected tournament"
            )
            print ( "error: invalid conditions" )
            return
        print ( "Adding Player" )

        items = self.list_playerList.curselection ( ) # returns a tuple
        selected = []
        for i in items :
            selected.append ( self.list_playerList.get ( i ) )

        print ( selected )

        for e in selected :
            tr_api.addPlayer ( activeTourn, e.split ( )[0] )

    def action_match_results ( self ) :
        '''
            creates a new window to submit results of a match.
        '''
        print ( "Match Results" )


        global input_player1Wins
        global input_player2Wins
        global input_matchDraws
        global win_matchResult

        global text_matchResult_failMsg

        self.win_matchResult = Tk ()                   # create the new window
        self.win_matchResult.title ( "Match" )        # set the title of window
        self.win_matchResult.minsize ( 200, 100 )      # set the minimum (default) size
        Label ( self.win_matchResult, text="Input Match Results" ).pack ()

        frame_matchForm = Frame ( self.win_matchResult )   # create a frame
        frame_matchForm.pack ( side = "top" )               # and place it on the top

        # create the labels that define what each input box is used for, and align them
        Label ( frame_matchForm, text = "Player 1 wins:" ).grid ( row = 0, sticky = W )
        Label (frame_matchForm , text = "Draws:" ).grid ( row = 1, column = 1, sticky = W )
        Label ( frame_matchForm, text = "Player 2 Wins:" ).grid ( row = 2, sticky = W )

        # create the entry boxes and align them
        self.input_player1Wins = Entry ( frame_matchForm )
        self.input_player1Wins.grid ( row = 0, column = 1 )
        self.input_matchDraws = Entry ( frame_matchForm )
        self.input_matchDraws.grid (row = 1, column = 3)
        self.input_player2Wins = Entry ( frame_matchForm )
        self.input_player2Wins.grid ( row = 2, column = 1 )

        # create the submit and cancel buttons
        btn_matchResult_submit = Button ( frame_matchForm, text = "Submit", command = self.event_matchResult_submit )
        btn_matchResult_cancel = Button ( frame_matchForm, text = "Cancel", command = self.win_matchResult.destroy )

        # align the buttons
        btn_matchResult_submit.grid ( row = 3, column = 0 )
        btn_matchResult_cancel.grid ( row = 3, column = 1 )

        # bind these keystrokes
        self.win_matchResult.bind ( '<Return>', self.event_matchResult_submit )
        self.win_matchResult.bind ( '<Escape>', self.win_matchResult.destroy )

        self.win_matchResult.mainloop ()

if ( __name__ == "__main__" ) :
    g_client = Tk ( )
    g_clientGUI = clientApp ( g_client )
    g_client.update ( )
    g_client.mainloop ()

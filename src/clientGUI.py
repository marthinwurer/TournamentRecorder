from tkinter import *
from tkinter import messagebox
import tkinter.font
import tr_api

class clientApp ( Tk ) :
    # base widgets/modules
    g_master                = None
    g_menubar               = None

    # entry box input
    input_tournName         = None
    input_tournMaxRounds    = None
    input_playerDCI         = None
    input_playerName        = None

    activeTourn             = None
    startedTourn            = None

    activeRound             = None

    def __init__(self, master):
        # super().__init__()
        global g_master
        global g_menubar

        self.g_master = master
        self.g_master.title ( "Tournament Recorder" )

        label = Label ( self.g_master, text = "" )
        label.pack ()

        self.g_master.minsize ( 500,500 )

        self.g_menubar = Menu ( self. g_master )

        self.g_master.config ( menu = self.g_menubar )

        self.action_createMenu ()

        # find a fixed width font for the player lists.
        font_tuple = tkinter.font.families()
        if 'Courier New' in font_tuple:
            self.fixed_font = ('Courier New', 11)#tkinter.font.Font(family='Courier New')
        elif 'Ubuntu Mono' in font_tuple:
            self.fixed_font = ('Ubuntu Mono', 11)#tkinter.font.Font(family='Ubuntu Mono')
        else:
            self.fixed_font = tkinter.font.Font(family='Arial')


    def action_createMenu ( self ) :
        global g_menubar
        self.create_menu_file ( )
        self.create_menu_tourn ( )
        self.create_menu_rounds ( )
        self.create_menu_matches ( )
        self.create_menu_players ( )

    def create_menu_file ( self ) :
        global g_menubar

        menu_file = Menu ( self.g_menubar )
        menu_file.add_command ( label = "Exit",
                                command = self.g_master.quit )

        self.g_menubar.add_cascade ( label = "File",
                                     menu = menu_file )

    def create_menu_tourn ( self ):
        menu_tourn = Menu ( self.g_menubar )
        menu_tourn.add_command ( label = "List Tournament",
                                 command = self.action_listTournaments )
        menu_tourn.add_separator ( )

        menu_tourn.add_command ( label = "Start Tournament",
                                 command = self.action_startTournament )
        menu_tourn.add_separator ()

        menu_tourn.add_command ( label = "Create Tournament",
                                 command = self.action_createTournament )

        self.g_menubar.add_cascade ( label = "Tournaments",
                                     menu = menu_tourn )

    def create_menu_players ( self ) :
        menu_players = Menu ( self.g_menubar )
        menu_players.add_command ( label = "List Player",
                                   command = self.action_listPlayers )
        menu_players.add_command ( label = "List Active Player",
                                   command = self.action_listActivePlayers )

        menu_players.add_separator ()

        menu_players.add_command ( label = "Create Player",
                                   command = self.action_createPlayer )

        self.g_menubar.add_cascade ( label = "Players",
                                     menu = menu_players )

    def create_menu_rounds ( self ) :
        menu_rounds = Menu ( self.g_menubar )
        menu_rounds.add_command ( label = "List Rounds",
                                  command = self.action_listRounds )

        menu_rounds.add_separator ()

        menu_rounds.add_command ( label = "Finish Round",
                                  command = self.action_finishRound )
        menu_rounds.add_command ( label = "Generate Pairings",
                                  command = self.action_generatePairings )

        self.g_menubar.add_cascade ( label = "Rounds",
                                     menu = menu_rounds )

    def create_menu_matches ( self ) :
        menu_matches = Menu ( self.g_menubar )
        menu_matches.add_command ( label = "List Matches",
                                   command = self.action_MatchViewer )

        self.g_menubar.add_cascade ( label = "Matches",
                                     menu = menu_matches )
    def action_listTournaments ( self ) :
        """
        creates a new window to submit results of a match.
        """

        self.win_listTourn = Tk()  # create the new window
        self.win_listTourn.title ( "Tournaments" )  # set the title of window
        Label (
            self.win_listTourn,
            text="Tournaments",
            font = ( "Helvetica", 16 ) ).pack ( )

        frame_tournList = Frame ( self.win_listTourn )  # create a frame
        frame_tournList.pack (
            side = "top",
            padx = 20,
            pady = 20 )  # and place it on the top

        # create the labels that define what each input box is used for, and align them
        Label (
            frame_tournList,
            text = "Tournament Name" ).grid (
                row = 0,
                column = 0,
                sticky = W )
        Label (
            frame_tournList,
            text = "# of PLayers" ).grid (
                row = 0,
                column = 1,
                sticky = W )

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
                Button ( frame_tournList, text = "Select", command = lambda j=i: self.event_selectTournament ( tourn_list[j]["id"] ) ).grid ( row = row_num, column = 2 )

        # create the submit and cancel buttons
        btn_listTourn_close = Button(frame_tournList, text="Cancel", command=self.win_listTourn.destroy)

        # align the buttons
        btn_listTourn_close.grid(row=row_num+1, column=1)

        # bind these keystrokes
        self.win_listTourn.bind('<Escape>', self.win_listTourn.destroy)

        self.win_listTourn.mainloop()

    def event_selectTournament ( self, tourn_id ) :
        global activeTourn

        print ( "Selected Tournament " + str ( tourn_id ) )

        self.activeTourn = tourn_id
        self.win_listTourn.destroy ( )
        self.action_listPlayers ( )
        self.action_listActivePlayers ( )

    def action_startTournament ( self ) :
        if ( self.activeTourn is None ) :
            messagebox.showerror(
                "Tournament",
                "Invalid selected tournament"
            )
            return
        print ( "Starting Tournament" )
        result = tr_api.startTournament ( self.activeTourn )
        if ( result["outcome"] is False ) : # failed to start
            messagebox.showerror (
                "Tournament",
                "Selected Tournament has already been started"
            )
            return
        else :
            print ( "successfully started tournament")
            self.startedTourn = self.activeTourn

    def action_createTournament ( self ) :
        """
            creates a new to submit tournament data.
        """
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
        """
            used to handle creation of tournament
        """
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

    def action_listRounds ( self ) :
        """
        creates a new window to submit results of a match.
        """

        if ( self.startedTourn is None and self.activeTourn is None ) :
            messagebox.showerror (
                "List Round",
                "no known tournament satisfied"
            )
            print ( "Error: invalid tournament satisfied" )

            return

        self.win_listRound = Tk()                       # create the new window
        self.win_listRound.title ( "Round Viewer" )     # set the title of window
        self.win_listRound.minsize ( 400, 200 )         # set the minimum (default) size
        Label ( self.win_listRound, text="Round Viewer", font = ( "Helvetica", 16 ) ).pack ( )

        frame_roundList = Frame ( self.win_listRound )  # create a frame
        frame_roundList.pack ( side = "top", padx = 20, pady = 20 )  # and place it on the top

        # create the labels that define what each input box is used for, and align them
        Label ( frame_roundList, text = "Rounds" ).grid ( row = 0, column = 0, sticky = W )
        Label ( frame_roundList, text = "----" ).grid ( row = 0, column = 1, sticky = W )

        rounds = tr_api.roundList ( self.activeTourn )
        row_num = 0
        if "rows" not in rounds.keys ( ):
            messagebox.showerror (
                "List Rounds",
                "Database Communication Error"
            )
            return
        elif len ( rounds["rows"] ) > 0:
            round_list = rounds["rows"]
            for i in range ( 0, len ( round_list ) ):
                row_num = i+1
                Label ( frame_roundList, text = round_list[i]["number"] ).grid ( row = row_num, column = 0)
                Button ( frame_roundList, text = "Select", command = lambda j=i: self.event_selectRound ( round_list[j]["id"] ) ).grid ( row = row_num, column = 1 )

        # create cancel buttons
        Button ( frame_roundList, text = "Cancel", command = self.win_listRound.destroy ).grid ( row = row_num + 1, column = 1)

        # bind these keystrokes
        self.win_listRound.bind ( '<Escape>', self.win_listRound.destroy )

    def displayError(self, result, title):
        try:
            if result['outcome'] == False:
                messagebox.showerror (
                    title,
                    "Failure: " + result['reason']
                )
        except:
            if result['outcome'] == False:
                messagebox.showerror (
                    title,
                    "Failure"
                )


    def event_selectRound ( self, r_id ) :
        global activeRound

        self.activeRound = r_id

        self.action_MatchViewer ( )

    def action_finishRound ( self ) :
        print ( "finishing round " + str(self.activeRound) )

        if ( self.activeRound is None ) :
            messagebox.showerror (
                "Finish Round",
                "no known round selected"
            )
            print ( "Error: invalid tournament satisfied" )

            return

        result =  tr_api.finishRound(self.activeRound)
        print( result)

        self.displayError(result, "Finish Round")

        if 'done' in result:
            messagebox.showinfo (
                "Tournament Finished",
                "This tournament has finished"
            )


    def action_generatePairings(self):
        title = "Generate Pairings"
        if ( self.activeRound is None ) :
            messagebox.showerror (
                title,
                "no known round selected"
            )
            print ( "Error: invalid tournament satisfied" )

            return

        result = tr_api.generatePairings( self.activeTourn)

        if result['outcome'] == False:
            messagebox.showerror (
                "Match List",
                "Failure: " + result['reason']
            )

        self.displayError(result, title)

    def matchframeupdate(self, match_list, row_num):
        i = row_num - 1
        Label ( self.frame_matchList, text = match_list[i]["id"] ).grid ( row = row_num, column = 0 )

        if (  match_list[i]["p1_id"] is None) :
            Label ( self.frame_matchList, text = "-" ).grid ( row = row_num, column = 1 )
        else :
            Label ( self.frame_matchList, text = match_list[i]["p1_name"]).grid ( row = row_num, column = 1 )

        if (  match_list[i]["p2_id"] is None ) :
            Label ( self.frame_matchList, text = "-" ).grid ( row = row_num, column = 2 )
        else :
            Label ( self.frame_matchList, text = match_list[i]["p2_name"]).grid ( row = row_num, column = 2 )

        Label ( self.frame_matchList, text = match_list[i]["table_number"] ).grid ( row = row_num, column = 3 )

        if ( match_list[i]["p1_wins"] is None ) :
            Label ( self.frame_matchList, text = "-" ).grid ( row = row_num, column = 4 )
        else :
            Label ( self.frame_matchList, text = match_list[i]["p1_wins"] ).grid ( row = row_num, column = 4 )

        if ( match_list[i]["p2_wins"] is None ) :
            Label ( self.frame_matchList, text = "-" ).grid ( row = row_num, column = 5 )
        else :
            Label ( self.frame_matchList, text = match_list[i]["p2_wins"] ).grid ( row = row_num, column = 5 )

        if ( match_list[i]["draws"] is None ) :
            Label ( self.frame_matchList, text = "-" ).grid ( row = row_num, column = 6 )

        else :
            Label ( self.frame_matchList, text = match_list[i]["draws"] ).grid ( row = row_num, column = 6 )

        Button ( self.frame_matchList, text = "Select", command = lambda j=i: self.action_match_results ( match_list[j]["id"] , match_list[j]["id"]) ).grid ( row = row_num, column = 7 )


    def action_MatchViewer ( self ) :
        """
        creates a new window to submit results of a match.
        """

        if ( self.activeRound is None ) :
            messagebox.showerror (
                "Match List",
                "no known round selected"
            )
            print ( "Error: invalid tournament satisfied" )

            return

        self.win_listMatches = Tk()  # create the new window
        self.win_listMatches.title ( "Match Viewer" )  # set the title of window
        Label ( self.win_listMatches, text = "Match Viewer", font = ( "Helvetica", 16 ) ).pack ( )

        self.frame_matchList = Frame ( self.win_listMatches )  # create a frame
        self.frame_matchList.pack ( side = "top", padx = 20, pady = 20 )  # and place it on the top

        # create the labels that define what each input box is used for, and align them
        Label ( self.frame_matchList, fg = "blue", text = "Matches" ).grid ( row = 0, column = 0, sticky = W )
        Label ( self.frame_matchList, fg = "blue", text = "Player 1" ).grid ( row = 0, column = 1)
        Label ( self.frame_matchList, fg = "blue", text = "Player 2" ).grid ( row = 0, column = 2)
        Label ( self.frame_matchList, fg = "blue", text = "Table Location" ).grid ( row = 0, column = 3, sticky = W )
        Label ( self.frame_matchList, fg = "blue", text = "Player 1 Wins" ).grid ( row = 0, column = 4, sticky = W )
        Label ( self.frame_matchList, fg = "blue", text = "Player 2 Wins" ).grid ( row = 0, column = 5, sticky = W )
        Label ( self.frame_matchList, fg = "blue", text = "Draws" ).grid ( row = 0, column = 6, sticky = W )
        Label ( self.frame_matchList, fg = "blue", text = "----" ).grid ( row = 0, column = 7, sticky = W )

        matches = tr_api.matchList ( self.activeRound )
        row_num = 0
        if "rows" not in matches.keys ( ):
            messagebox.showerror (
                "List Matches",
                "Database Communication Error"
            )
            return
        elif len ( matches["rows"] ) > 0:
            match_list = matches["rows"]
            # print ( match_list )
            for i in range ( 0, len ( match_list ) ):
                row_num = i+1
                print(match_list[i])

                self.matchframeupdate(match_list, row_num)

        # bind these keystrokes
        self.win_listMatches.bind ( '<Escape>', self.win_listMatches.destroy )

    def update_matches(self, match):

        matches = tr_api.matchList ( self.activeRound )
        row_num = 0
        if "rows" not in matches.keys ( ):
            messagebox.showerror (
                "List Matches",
                "Database Communication Error"
            )
            return
        elif len ( matches["rows"] ) > 0:
            match_list = matches["rows"]
            # print ( match_list )
            for i in range ( 0, len ( match_list ) ):
                if match_list[i]["id"] == match:

                    row_num = i+1

                    # delete the previous matches
                    for row in self.frame_matchList.grid_slaves(row=row_num):
                        row.grid_forget()
                        row.destroy()

                    self.matchframeupdate(match_list, row_num)
                    self.frame_matchList.update_idletasks()

    def action_listPlayers ( self ) :
        """
            creates a new window to view player data.
        """
        print ( "Listing Players" )

        self.win_listPlayer = Tk ()
        self.win_listPlayer.title ( "Players Finder" )
        self.win_listPlayer.minsize ( 600, 300 )
        Label ( self.win_listPlayer, text = "Players Finder" ).pack ()

        frame_playerFind = Frame ( self.win_listPlayer )
        frame_playerFind.pack ( side = "top" )
        self.frame_playerList = Frame ( self.win_listPlayer )
        self.frame_playerList.pack ( expand = True, side = "left")
        frame_playerFooter = Frame ( self.win_listPlayer )
        frame_playerFooter.pack ( side = "right" )

        Label ( frame_playerFind, text = "Search For:" ).grid ( row = 0 )
        self.input_playerList_searchName = Entry ( frame_playerFind )
        self.input_playerList_searchName.grid ( row = 0, column = 1 )

        btn_playerFind_find = Button ( frame_playerFind, text = "Find", command = self.event_findPlayer ).grid ( row = 0, column = 2 )

        scroll_playerList = Scrollbar ( self.frame_playerList )
        scroll_playerList.pack ( side = "right", fill = "y" )

        self.list_playerList = Listbox ( self.frame_playerList, yscrollcommand = scroll_playerList.set, selectmode = "multiple" )
        self.list_playerList.config ( width = "95", font=self.fixed_font )
        self.list_playerList.pack ( side = "left", fill = "both" )

        scroll_playerList.config ( command = self.list_playerList.yview )

        playerList = tr_api.searchPlayers ( self.input_playerList_searchName.get () ) ['rows']

        # build the formatter string
        output =" {:>10} {:>30}"

        row_count = 1
        for player in playerList :
            entry = output.format(str ( player["id"] ), player["name"])
            self.list_playerList.insert ( END, entry )

        btn_addPlayer_add = Button ( frame_playerFooter, text = "Add to Active", command = self.event_addPlayer ).pack ()
        btn_addPlayer_cancel = Button ( frame_playerFooter, text = "Cancel", command = self.win_listPlayer.destroy ).pack ()

    def addtoplayerlist(self, playerList):
        output =" {:>10} {:>30} {:>3}"

        row_count = 1
        for player in playerList :
            entry = output.format(str ( player["id"] ), player["name"], player['standing'])
            self.list_activePlayerList.insert ( END, entry )

    def action_listActivePlayers ( self ) :
        """
            creates a new window to view active player data.
        """
        if self.activeTourn is None :
            messagebox.showerror (
                "Active Players",
                "Usage: active tournament must be selected "
            )
            print ( "error: invalid conditions" )
            return
        print ( "Listing Active Players" )

        self.win_listActivePlayers = Tk ()
        self.win_listActivePlayers.title ( "Players Viewer" )
        self.win_listActivePlayers.minsize ( 600, 200 )
        Label ( self.win_listActivePlayers, text = "Players Viewer" ).pack ()

        self.frame_activePlayerList = Frame ( self.win_listActivePlayers )
        self.frame_activePlayerList.pack ( expand = True, side = "left")
        frame_playerFooter = Frame ( self.win_listActivePlayers )
        frame_playerFooter.pack ( side = "right" )

        scroll_playerList = Scrollbar ( self.frame_activePlayerList )
        scroll_playerList.pack ( side = "right", fill = "y" )

        self.list_activePlayerList = Listbox ( self.frame_activePlayerList, yscrollcommand = scroll_playerList.set, selectmode = "multiple")
        self.list_activePlayerList.config ( width = "95", font=self.fixed_font )
        self.list_activePlayerList.pack ( side = "left", fill = "both" )

        scroll_playerList.config ( command = self.list_activePlayerList.yview )

        playerList = tr_api.listActiveTournamentPlayers ( self.activeTourn ) ['rows']
        # print ( playerList )

        self.addtoplayerlist(playerList)

        # playerList.update_idletasks ()

        Button ( frame_playerFooter, text = "Refresh Player List", command = self.event_refreshTournPlayer ).grid ( row = 0, column = 0 ) # create remove button
        Button ( frame_playerFooter, text = "Remove Player(s)", command = self.event_removeTournPlayer ).grid ( row = 1, column = 0 ) # create remove button
        Button ( frame_playerFooter, text = "Cancel", command = self.win_listActivePlayers.destroy ).grid ( row = 2, column = 0 ) # create cancel button

    def event_refreshTournPlayer(self):
        playerList = tr_api.listActiveTournamentPlayers ( self.activeTourn ) ['rows']
        # print ( playerList )

        self.list_activePlayerList.delete(0, END)

        self.addtoplayerlist(playerList)

        self.list_activePlayerList.update_idletasks()

    def action_createPlayer ( self ) :
        """
            creates a new window to submit new player data.
        """
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
        """
            used to handle creation of tournament
        """
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

    def event_findPlayer ( self ) :
        """
            create the findPlayer window
        """

        print ( "Finding player" )

        playerList = tr_api.searchPlayers ( self.input_playerList_searchName.get () ) ['rows']
        self.list_playerList.delete ( 0, END )
        for player in playerList :
            entry = str ( player["id"] ) + " " + player["name"]
            self.list_playerList.insert ( END, entry )

    def event_addPlayer ( self ) :
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
            e = e.split()
            result = tr_api.addPlayer ( int(e[0]),
                                        self.activeTourn )
            self.displayError(result, "Add Player")

        # once added, refresh the player list if it exists
        try:
            exists = self.list_activePlayerList
        except NameError:
            exists = True
        else:
            exists = False
        print(exists)

        if exists:
            self.event_refreshTournPlayer()

        self.list_playerList.selection_clear(0, END)


        # self.win_listPlayer.quit ( )

    def event_removeTournPlayer ( self ) :
        print ( "Removing selected players from tourn" )
        items = self.list_activePlayerList.curselection ( ) # returns a tuple
        selected = []

        for i in items :
            selected.append ( self.list_activePlayerList.get ( i ) )

        print ( selected )

        for e in selected :
            result = tr_api.removePlayer ( e.split ( )[0], self.activeTourn )
            self.displayError(result, "Remove Player")



    def action_match_results ( self, m_id , match) :
        """
            creates a new window to submit results of a match.
        """
        print ( "Match Results" )

        global input_player1Wins
        global input_player2Wins
        global input_matchDraws
        global win_matchResult

        global text_matchResult_failMsg

        self.activeMatch = m_id

        self.win_matchResult = Tk ()                   # create the new window
        self.win_matchResult.title ( "Match" )        # set the title of window
        self.win_matchResult.minsize ( 200, 100 )      # set the minimum (default) size
        Label ( self.win_matchResult, text="Input Match Results" ).pack ()

        frame_matchForm = Frame ( self.win_matchResult )   # create a frame
        frame_matchForm.pack ( side = "top" )               # and place it on the top

        # create the labels that define what each input box is used for, and align them
        Label ( frame_matchForm, text = "Player 1 wins:" ).grid ( row = 0, column = 0, sticky = W )
        Label ( frame_matchForm, text = "Draws:" ).grid ( row = 1, column = 0, sticky = W )
        Label ( frame_matchForm, text = "Player 2 Wins:" ).grid ( row = 2, column = 0, sticky = W )

        # create the entry boxes and align them
        self.input_player1Wins = Entry ( frame_matchForm )
        self.input_player1Wins.grid ( row = 0, column = 1 )
        self.input_matchDraws = Entry ( frame_matchForm )
        self.input_matchDraws.grid (row = 1, column = 1)
        self.input_player2Wins = Entry ( frame_matchForm )
        self.input_player2Wins.grid ( row = 2, column = 1 )

        # create the submit and cancel buttons
        btn_matchResult_submit = Button ( frame_matchForm, text = "Submit", command = lambda: self.event_matchResult_submit(match) ).grid ( row = 4, column = 0 )
        btn_matchResult_cancel = Button ( frame_matchForm, text = "Cancel", command = self.win_matchResult.destroy ).grid ( row = 4, column = 1 )

        # bind these keystrokes
        self.win_matchResult.bind ( '<Return>', lambda: self.event_matchResult_submit(match))
        self.win_matchResult.bind ( '<Escape>', self.win_matchResult.destroy )

        self.win_matchResult.mainloop ()

    def event_matchResult_submit ( self , match) :
        """
            used to submit match information
        """
        global input_player1Wins
        global input_player2Wins
        global input_matchDraws

        # get the input values
        player1Wins = self.input_player1Wins.get ( )
        player2Wins = self.input_player2Wins.get ( )
        draws       = self.input_matchDraws.get ( )

        if ( not player1Wins.isdigit ( ) or not player2Wins.isdigit ( ) or not draws.isdigit ( ) ) :
            messagebox.showerror ( "Match Results",
                                   "Invalid match result. Unrecognized input format" )
        elif ( int(player1Wins) > 2 or int(player2Wins) > 2 or (int(player1Wins) + int(player2Wins) + int(draws)) == 0 ) :
            messagebox.showerror ( "Match Results",
                                   "Invalid match result. Invalid number of games" )
        else :
            result = tr_api.setMatchResults ( self.activeMatch, player1Wins, player2Wins, draws )
            self.win_matchResult.destroy ( )    # destroy window on db submission
            self.displayError(result, "Submit Results")

            self.update_matches(match)


if ( __name__ == "__main__" ) :
    g_client = Tk ( )
    g_clientGUI = clientApp ( g_client )
    g_client.update ( )
    g_client.mainloop ()

from tkinter import *
import tr_api

class clientApp ( Tk ) :
    g_master = None
    g_menubar = None

    win_createTourn = None
    win_createPlayer = None

    input_tournName = None
    input_tournMaxRounds = None
    input_playerDCI = None
    input_playerName = None

    text_createTourn_failMsg = None
    text_createPlayer_failMsg = None

    def __init__  ( self, master ) :
        global g_master

        self.g_master = master
        self.g_master.title ( "Tournament Recorder" )

        self.label = Label ( self.g_master, text = "" )
        self.label.pack ()

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

        self.menu_file = Menu ( self.g_menubar )
        self.menu_file.add_command ( label = "Exit", command = self.g_master.quit )

        self.g_menubar.add_cascade ( label = "File", menu = self.menu_file )

    def create_menu_tourn ( self ):
        self.menu_tourn = Menu ( self.g_menubar )
        self.menu_tourn.add_command ( label = "List Tournament", command = self.action_listTournaments )
        self.menu_tourn.add_separator ()
        self.menu_tourn.add_command ( label = "Create Tournament", command = self.action_createTournament )

        self.topdict = tr_api.listTournaments(None,None)
        if ( self.topdict.keys() == True ) and ( self.topdict.get('rows')[0].get('num_players') != 0 ):
            self.menu_tourn.add_command ( label = "Start Tournament", command = self.action_startTournament )

        self.g_menubar.add_cascade ( label = "Tournaments", menu = self.menu_tourn )

    def create_menu_players ( self ) :
        self.menu_players = Menu ( self.g_menubar )
        self.menu_players.add_command ( label = "List Player", command = self.action_listPlayers )
        self.menu_players.add_separator ()
        self.menu_players.add_command ( label = "Create Player", command = self.action_createPlayer )
        self.menu_players.add_command ( label = "Add Player", command = self.action_addPlayer )

        self.g_menubar.add_cascade ( label = "Players", menu = self.menu_players )

    def action_listTournaments ( self ) :
        print ( "Listing Tournaments" )

    def action_startTournament ( self ) :
        print ( "Starting Tournament" )

    def action_createTournament ( self ) :
        '''
            creates a new to submit tournament data.
        '''
        print ( "Creating Tournament" )

        global input_tournName
        global input_tournMaxRounds
        global win_createTourn

        global text_createTourn_failMsg

        self.win_createTourn = Tk ()                            # create the new window
        self.win_createTourn.title ( "Tournament Creation" )    # set the title of window
        self.win_createTourn.minsize ( 200, 100 )               # set the minimum (default) size
        lbl_createTourn = Label ( self.win_createTourn, text="Create a new Tournament" ).pack ()

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

        # create the error message text label
        self.text_createTourn_failMsg = StringVar ()
        lbl_createTourn_fail = Label ( self.win_createTourn, textvariable = self.text_createTourn_failMsg ).pack ()

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

            self.win_createTourn.destroy ( )    # destroy window on db submission
        else : # values are not valid, check what failed
            print ( "create tournament failed" )
            if ( len ( tournName ) < 4 ) :
                self.text_createTourn_failMsg.set ( "tournament name length must be greater that 4" )
                print ( "Error: tournName length < 4" )

            if ( not tournMaxRounds.isdigit () ) :
                self.text_createTourn_failMsg.set ( "max rounds must be a number at least 1" )
                print ( "Error: tourn max rounds < 1" )

        print ( "tournName: " + tournName )
        print ( "tournMaxRounds: " + tournMaxRounds )

    def action_listPlayers ( self ) :
        print ( "Listing Players" )

    def action_createPlayer ( self ) :
        '''
            creates a new window to submit new player data.
        '''
        print ( "Creating Player" )


        global input_playerDCI
        global input_playerName
        global win_createPlayer

        global text_createPlayer_failMsg

        self.win_createPlayer = Tk ()                   # create the new window
        self.win_createPlayer.title ( "Player" )        # set the title of window
        self.win_createPlayer.minsize ( 200, 100 )      # set the minimum (default) size
        lbl_createPlayer = Label ( self.win_createPlayer, text="Create a new Player" ).pack ()

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

        # create the error message text label
        self.text_createPlayer_failMsg = StringVar ()
        lbl_createPlayer_fail = Label ( self.win_createPlayer, textvariable = self.text_createPlayer_failMsg ).pack ()

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


    def action_addPlayer ( self ) :
        self.menu_tourn.add_command ( label = "Start Tournament", command = self.action_startTournament )
        print ( "Adding Player" )

if ( __name__ == "__main__" ) :
    g_client = Tk ( )
    g_clientGUI = clientApp ( g_client )
    g_client.mainloop ()

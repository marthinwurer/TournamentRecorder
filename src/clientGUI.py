from tkinter import *
import tr_api

class clientApp ( Tk ) :
    g_master = None
    g_menubar = None

    win_createTourn = None

    input_tournName = None
    input_tournMaxRounds = None

    text_createTourn_failMsg = None

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

        self.win_createTourn = Tk ()
        self.win_createTourn.title ( "Tournament Creation" )
        self.win_createTourn.minsize ( 200, 100 )
        createTourn_label = Label ( self.win_createTourn, text="Create a new Tournament" )

        frame_tournForm = Frame ( self.win_createTourn )
        frame_tournForm.pack ( side = "top" )

        Label ( frame_tournForm, text = "Tournament Name" ).grid ( row = 0, sticky = W )
        Label ( frame_tournForm, text = "Max Rounds" ).grid ( row = 1, sticky = W )
        self.input_tournName = Entry ( frame_tournForm )
        self.input_tournName.grid ( row = 0, column = 1)
        self.input_tournMaxRounds = Entry ( frame_tournForm )
        self.input_tournMaxRounds.grid ( row = 1, column = 1)

        btn_createTourn_submit = Button ( frame_tournForm, text = "Submit", command = self.event_createTourn_submit )
        btn_createTourn_cancel = Button ( frame_tournForm, text = "Cancel", command = self.win_createTourn.destroy )

        btn_createTourn_submit.grid ( row = 2, column = 0 )
        btn_createTourn_cancel.grid ( row = 2, column = 1 )

        self.text_createTourn_failMsg = StringVar ()
        lbl_createTourn_fail = Label ( self.win_createTourn, textvariable = self.text_createTourn_failMsg ).pack ()

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

        tournName = self.input_tournName.get ( )
        tournMaxRounds = self.input_tournMaxRounds.get ( )

        if ( len ( tournName ) >= 4 and tournMaxRounds.isdigit () ) :
            print ( "create tournament success" )

            self.win_createTourn.destroy ( )
        else :
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

        self.

    def action_addPlayer ( self ) :
        self.menu_tourn.add_command ( label = "Start Tournament", command = self.action_startTournament )
        print ( "Adding Player" )

if ( __name__ == "__main__" ) :
    g_client = Tk ( )
    g_clientGUI = clientApp ( g_client )
    g_client.mainloop ()

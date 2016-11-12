from tkinter import *
import tr_api

class clientApp ( Tk ) :
    g_master = None
    g_menubar = None
    input_tournName = None
    input_tournMaxRounds = None

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
        print ( "Creating Tournament" )

        global input_tournName
        global input_tournMaxRounds

        win_createTourn = Tk ()
        win_createTourn.title ( "Tournament Creation" )
        win_createTourn.minsize ( 200, 100 )
        createTourn_label = Label ( win_createTourn, text="Create a new Tournament" )

        frame_tournForm = Frame ( win_createTourn )
        frame_tournForm.pack ( side = "top" )

        Label ( frame_tournForm, text = "Tournament Name" ).grid ( row = 0, sticky = W )
        Label ( frame_tournForm, text = "Max Rounds" ).grid ( row = 1, sticky = W )
        input_tournName = Entry ( frame_tournForm )
        input_tournName.grid ( row = 0, column = 1)
        input_tournMaxRounds = Entry ( frame_tournForm )
        input_tournMaxRounds.grid ( row = 1, column = 1)

        btn_createTourn_submit = Button ( frame_tournForm, text = "Submit", command = self.event_createTourn_submit ( input_tournName.get (), input_tournMaxRounds.get () ) )
        btn_createTourn_submit.grid ( row = 2, column = 0 )
        btn_createTourn_cancel = Button ( frame_tournForm, text = "Cancel", command = win_createTourn.destroy )
        btn_createTourn_cancel.grid ( row = 2, column = 1 )

    def event_createTourn_submit ( self, tournName, tournMaxRounds ) :
        global input_tournName
        global input_tournMaxRounds

        print ( "tournName: " + tournName )
        print ( "tournMaxRounds: " + tournMaxRounds )

    def action_listPlayers ( self ) :
        print ( "Listing Players" )

    def action_createPlayer ( self ) :
        print ( "Creating Player" )

    def action_addPlayer ( self ) :
        self.menu_tourn.add_command ( label = "Start Tournament", command = self.action_startTournament )
        print ( "Adding Player" )

if ( __name__ == "__main__" ) :
    g_client = Tk ( )
    g_clientGUI = clientApp ( g_client )
    g_client.mainloop ()

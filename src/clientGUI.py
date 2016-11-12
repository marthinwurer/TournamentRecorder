from tkinter import *
from tr_api import listPlayers

class clientApp ( Tk ) :
    g_master = None
    g_menubar = None

    def __init__  ( self, master ) :

        self.g_master = master
        self.g_master.title ( "Tournament Recorder" )

        self.label = Label ( self.g_master, text = "" )
        self.label.pack ()

        self.g_master.minsize ( 500,500 )

        self.g_menubar = Menu (self. g_master )

        self.g_master.config ( menu = self.g_menubar )

        self.action_createMenu ()

    def action_createMenu ( self ) :
        self.menu_file = Menu ( self.g_menubar )
        self.menu_file.add_command ( label = "Exit", command = self.g_master.quit )

        self.menu_tourn = Menu ( self.g_menubar )
        self.menu_tourn.add_command ( label = "List Tournament", command = self.action_listTournaments )
        self.menu_tourn.add_separator ()
        self.menu_tourn.add_command ( label = "Create Tournament", command = self.action_createTournament )
        self.menu_tourn.add_command ( label = "Start Tournament", command = self.action_startTournament )

        self.menu_players = Menu ( self.g_menubar )
        self.menu_players.add_command ( label = "List Players", command = self.action_listPlayers )
        self.menu_players.add_separator ()
        self.menu_players.add_command ( label = "Create Players", command = self.action_createPlayer )

        self.g_menubar.add_cascade ( label = "File", menu = self.menu_file )
        self.g_menubar.add_cascade ( label = "Tournaments", menu = self.menu_tourn )
        # self.g_memubar.add_cascade ( label = "Players", menu = self.menu_players )

    def action_listTournaments ( self ) :
        print ( "Listing Tournaments" )

    def action_startTournament ( self ) :
        print ( "Starting Tournament" )

    def action_createTournament ( self ) :
        print ( "Creating Tournament" )

    def action_listPlayers ( self ) :
        print ( "Listing Players" )

    def action_createPlayer ( self ) :
        print ( "Creating Player")


if ( __name__ == "__main__" ) :
    g_client = Tk ( )
    g_clientGUI = clientApp ( g_client )
    g_client.mainloop ()

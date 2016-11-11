from tkinter import *
from tr_api import listPlayers

g_clientRoot = None

menubar_clientRoot = None
menu_Config = None

def action_startClient () :
    global g_clientRoot

    g_clientRoot = Tk( ) # create the window
    g_clientRoot.minsize ( 500, 500 )
    g_clientRoot.geometry ( "500x500")
    g_clientRoot.title ( "Tournament Recorder" )

    lbl_clientRoot = Label ( g_clientRoot, text = "Recorder Menu" )
    lbl_clientRoot.pack ()

    menubar_clientRoot = Menu ( g_clientRoot )

    menu_Config = Menu ( menubar_clientRoot )
    menu_Config.add_command ( label = "Exit", command = action_exit )

    menu_tourn = Menu ( menubar_clientRoot )
    # menu_tourn.add_command ( label = "Create Tournament", command = action_createTournament )
    menu_tourn.add_command ( label = "Create Tournament" )

    menubar_clientRoot.add_cascade ( label = "Config", menu = menu_Config )
    menubar_clientRoot.add_cascade ( label = "Tournaments", menu = menu_tourn )
    menubar_clientRoot.add_cascade ( label = "Players" )

    g_clientRoot.config ( menu = menubar_clientRoot)

    g_clientRoot.mainloop()

'''
    action_exitClient ()
    exits and kills
'''
def action_exit ( ) :
    global g_clientRoot

    g_clientRoot.destroy ()
    print ( "Exiting client" )

action_startClient ()

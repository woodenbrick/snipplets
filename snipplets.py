# snipplets.py
#
# Copyright 2009 Daniel Woodhouse
#
#This file is part of snipplets.
#
#snipplets is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#snipplets is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with snipplets.  If not, see http://www.gnu.org/licenses/

import os
import gtk
import pygtk
pygtk.require("2.0")
import gtk.glade

from mainsnipplet import MainSnippletHandler
from createnewsnipplet import CreateNewSnippletHandler
import dbsnipplet
import syntaxhighlight

class RunSnipplets(object):

    def __init__(self):
        self.GLADE_DIR = "ui/glade/"
        self.HOME_DIR = os.path.join(os.environ['HOME'], ".snipplets" + os.sep)
        try:
            os.mkdir(self.HOME_DIR)
        except:
            pass
        
        self.db = dbsnipplet.DbSnipplet(self.HOME_DIR + "snippletsDB")
        #define codecompletion object here for use by all children
        self.code_syntax = syntaxhighlight.HighLighter(self.db)
        self.create_main_window()
        
        self.tray_icon = gtk.StatusIcon()
        self.tray_icon.set_from_file("ui/images/user_male.png")
        self.tray_icon.connect("activate", self.activate_menu, None)
        self.tray_icon.connect("popup-menu", self.popup_menu, None)
        
        self.wTree_menu = gtk.glade.XML(self.GLADE_DIR + "notification_menu")
        self.wTree_menu.signal_autoconnect(self)
        self.right_click_menu = self.wTree_menu.get_widget("status_menu")

    def activate_menu(self, *args):
        if self.main_window.window.props.visible:
            self.main_window.window.hide()
        else:
            self.main_window.window.show()
        
    def popup_menu(self, *args):
        self.right_click_menu.popup(parent_menu_shell=None, parent_menu_item=None,
                                    func=gtk.status_icon_position_menu,
                                        button=args[1], activate_time=args[2],
                                        data=self.tray_icon)

    def on_show_snipplets_activate(self, widget):
        self.main_window.window.present()
    
    def create_main_window(self):
        self.main_window = MainSnippletHandler(self, "snipplets.glade")

    def gtk_main_quit(self, widget=None):
        gtk.main_quit()
    
    def update_selection_view(self, data, id):
        self.main_window.update_selection_view(data, id)
        

    def create_new_snipplet_window(self, widget=None, id=None):
        self.create_new_window = CreateNewSnippletHandler(self, "create_new_snipplet.glade", id=id)

    


if __name__ == '__main__':
    RunSnipplets()
    gtk.main()

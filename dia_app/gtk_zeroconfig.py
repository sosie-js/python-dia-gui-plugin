from  logging import warnings
import sys, os

GTK_SOS_VERSION="1.0"

from version_info import *

#######  ENVIRON DETECTION for Python and Dia ########

# NOTE: All this stuff is linux specific and can be comppleted for other platforms
#  we assume the configuration
# given on https://sosie-js.github.io/python-dia/
# all started with a big discussion on "generate_run_with_dia_env.sh" script usage
# https://gitlab.gnome.org/GNOME/dia/-/issues/512

if "linux" in sys.platform :
    
    # 
    # PYTHON
    #
    python_prefix="/usr"

    python_version_info.limit=2
    if python2:
        PYTHONPATH=python_prefix+"/local/lib/python"+str(python_version_info)+"/dist-packages:/usr/lib/python"+str(python_version_info)+"/dist-packages"
    if python3:
        PYTHONPATH=python_prefix+"/local/lib/python"+str(python_version_info)+"/site-packages:/usr/lib/python"+str(python_version_info)+"/dist-packages"

    python_version_info.limit=3 #get rid of extra releaselevel and serial

    # 
    # DIA
    #
    dia_prefix="/opt"

    if python2 :
        dia_prefix=python_prefix 
    elif not python3 :
        raise(Exception("Unsupported python version"))
        
    DIA_BIN_PATH=dia_prefix+"/bin/dia"
    DIA_LIB_PATH=dia_prefix+"/lib/x86_64-linux-gnu/dia"
    DIA_BASE_PATH=dia_prefix+"/share/dia"
###########################

import warnings

#NOTE, As Namespace Gtk is already loaded with version 2.0, 
#for dia 0.97.2, we cannot choose 3.0
gtk_ver= "2.0" #PyGTK is only for gtk2.0 and python2 due to error on import gi: When using gi.repository you must not import static modules like "gobject"
gtk_ver ="3.0gi" #outdated in python3, that recommends 3.0gi

#Autodetect which python GTK+ gas factory to use, works for python2/3

"""
    if(python2 and  (not "gi" in gtk_ver)):
        gtk_ver="2.0" 
        raise(Exception("pyGtk is the standard for gtk2.0, gi is for now in fact not supported on python2"))    
"""
    

gtk_support="pyGObject"
gtk_ver=gtk_ver.replace("gi","")

import gi

try:    
    gi.require_version('Pango', '1.0')
    gi.require_version('Gtk', gtk_ver)
    gi.require_version('GdkPixbuf', '2.0')

    try:
        gtks=True
        gi.require_version('GtkSource', gtk_ver)  #http://lazka.github.io/pgi-docs/#GtkSource-4
    except:
        gtks=False
   
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        from gi.repository import Pango, Gtk, Gdk, GdkPixbuf
        from gi.repository import GLib as GObject #PyGIDeprecationWarning: GObject.timeout_add is deprecated; use GLib.timeout_add instead
        from gi.repository import Gio #to build menus with Model
        if gtks:
            from gi.repository import GtkSource as gtksourceview
            buf = gtksourceview.Buffer()
    gtk_version_info = VersionInfo(gi.version_info)
    
except Exception as e:
    print(e)
    import pygtk
    gtk_support="pyGTK"
    pygtk.require(gtk_ver)

    #Because Gtk 2.0 was not designed for use with introspection some of the interfaces 
    #and API will fail.  As such this is not supported by the pygobject development team 
    #and we encourage you to port your app to Gtk 3 or greater. 
    import gtk as Gtk
    try:
        import gtk.keysyms
    except:
        # FIXME : Weird error: sys.path must be a list of directory names
        pass
    import gobject as GObject
    gtk_version_info =VersionInfo(getattr(GObject, 'pygobject_version', {}))
   
if gtk_ver == "3.0":
    
    ui_support=gtk_support
    ui_lib="gtk+"
    ui_lib_version_info=gtk_version_info   
    
else:
   
    #if   gtk_support == "pyGTK"
    #or  (gtk_support=="pyGObject" and  gtk_ver == "2.0"):
    #then Houston we have a problem, Gtk2.0 crashed easily..
    #so we set the MacGyver rescue mode by
    #We cloaking Tkinter as Gtk
    del globals()["Gtk"]
   
    if  python2 :
        import Tkinter as tk
        import tkFont
    else :
        import tkinter as tk
        import tkinter.font as tkFont
        
    ## Using tkinter to mock AboutDialog ui as replacement
    ##############################

    class _Gtk_AboutDialog:
        
        version=""
        program_name=""
        background='#F0F0F0'
        comments=""
        website=""
        website_label=""
        authors=[]
        copyright=""

        @staticmethod
        def set_program_name(name):
            Gtk.AboutDialog.program_name= name

        @staticmethod
        def set_version(version):
            Gtk.AboutDialog.version= version
        
        @staticmethod
        def set_comments(comments):
            Gtk.AboutDialog.comments=comments

        @staticmethod
        def set_website(website):
            Gtk.AboutDialog.website=website
            
        @staticmethod
        def set_website_label(label):
            Gtk.AboutDialog.website_label=label
            
        @staticmethod
        def set_authors(authors):
            Gtk.AboutDialog.authors=authors
        
        @staticmethod
        def set_copyright(copyright):
            Gtk.AboutDialog.copyright=copyright
        
        @staticmethod
        def show_all():
            
            ## Using tkinter to mock AboutDialog ui as replacement
            ##############################
            background='#F0F0F0'
            root = tk.Tk()
            
            root.title("About "+PROGRAM_NAME)
            root.geometry('680x350')
            root.configure(background=background)
            root.resizable(False, False)
            #root.iconbitmap('./assets/pythontutorial.ico')
            
            def credits():
            
                fenetre0 =tk.Toplevel()
                fenetre0.title("Credits")
                fenetre0.geometry('350x250+50+50')
                fenetre0.configure(background=background)
                fenetre0.resizable(False, False)
               
                cadre0 =tk.Frame(fenetre0)
               
                tab0 =tk.Text(cadre0)
                tab0.config(font ="sans 12", width =10, height =1)
                tab0.insert("end", "Written by")
                tab0.config(state =tk.DISABLED)
                tab0.pack() #FIXME  did not manage to align this on left..
                
                texte0 =tk.Text(cadre0)
                texte0.config(font ="sans 12", width =25, height =6)
                
                ret=""
                for author in AUTHORS:
                    texte0.insert("end", ret+author)
                    ret="\n"
                    
                texte0.config(state =tk.DISABLED)
                texte0.pack()
             
                bouton1 =tk.Button(cadre0, text ="Close", command =fenetre0.destroy)
                bouton1.pack(side =tk.RIGHT)
                
                cadre0.pack(padx=3,side="left")
                cadre0.configure(background=background)
        
        
            root.aspect(3, 2, 5, 3)
            
            cadre0 =tk.Frame(root)

            sep0 = tk.Label(cadre0, text="")
            sep0.pack()
            sep0.configure(background=background) 
            
            title = tk.Label(cadre0, text=PROGRAM_NAME+" " +VERSION, font ="sans 16 bold")
            title.configure(background=background)   
            title.pack()

            comments = tk.Label(cadre0, text=COMMENTS)
            comments.configure(background=background)
            comments.pack()
            
            copyright= tk.Label(cadre0, text=COPYRIGHT)
            copyright.configure(background=background)
            copyright.pack()
            
            #Creates the website link
            
            def callback(url):
                import webbrowser
                webbrowser.open_new(url)

            website = tk.Label(cadre0, text=WEBSITE,  fg="blue", cursor="hand2")
            website.pack()
            website.bind("<Button-1>", lambda e: callback(WEBSITE))

            # clone the font, set the underline attribute,
            # and assign it to our widget
            f = tkFont.Font(website, website.cget("font"))
            f.configure(underline = True)
            website.configure(font=f,background=background)

            #separator
            sep1 = tk.Label(cadre0, text="")
            sep1.pack()
            sep1.configure(background=background) 
            
            bouton0 =tk.Button(cadre0,text ="Credits", command =credits)
            bouton0.pack(side =tk.LEFT)
            
            bouton1 =tk.Button(cadre0, text ="Close", command =root.destroy)
            bouton1.pack(side =tk.RIGHT)
            
            cadre0.pack(padx=10)
            cadre0.configure(background= background)

   
    class _Gtk_StatusBar(tk.Frame):   
                
        def set_message(self,message):
            self.variable.set(message)
            
        def show_mouse_coords(self):    
            self.set_message(str(get_mouse_position()))
            
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            self.variable=tk.StringVar()        
            self.label=tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                               textvariable=self.variable,
                               font=('arial',16,'normal'))
            self.set_message('Ready')
            self.label.pack(fill=tk.X, expand=1)        
            self.pack(side="left")
            setattr(self,"manager",self)
                   
        def install_mouse_coords_watcher(self,polling):
            self.pt=pt=RepeatTimer(polling,self.show_mouse_coords)
            pt.start()
            
        def uninstall(self):
            self.pt.stop()
   
   
    class _Gtk_DiaMockWindow:
        
        background='#d5d5d5'
        menubar=None
        menus={}
        root= tk.Tk()
        width=637
        height=304
        title="DiaMock"
        bodyimage=r"diamock.png"
      
        @staticmethod
        def load_menubar(menus):
           
            root=Gtk.DiaMockWindow.root
            
            menubar =tk.Menu(root) 
            Gtk.DiaMockWindow.menubar= (menubar,menus)

        @staticmethod
        def add_menu(menu_label):
            
            menubar=Gtk.DiaMockWindow.menubar[0]
            
            menu =tk.Menu(menubar, tearoff ="0") 
            menubar.add_cascade(label = menu_label, menu =menu)
            
            Gtk.DiaMockWindow.menus[menu_label]=(menu,[])

        @staticmethod
        def get_menu(menu_label):
            
            return Gtk.DiaMockWindow.menus[menu_label][0]

        @staticmethod
        def add_menuitem(menu_label, item_label, item_cmd):
            
            menu= Gtk.DiaMockWindow.get_menu(menu_label)
            
            menuitem=menu.add_command(label = item_label,  command =item_cmd)
            
            Gtk.DiaMockWindow.menus[menu_label][1].append(menuitem)
        
        @staticmethod
        def show_all():
            
            root=Gtk.DiaMockWindow.root
            background=Gtk.DiaMockWindow.background
          
            # This is the section of code which creates the main window
            root.geometry(str(Gtk.DiaMockWindow.width)+'x'+str(Gtk.DiaMockWindow.height))
            root.configure(background=background)
            root.title(Gtk.DiaMockWindow.title)
            
            (sysdemenu0,menus) = Gtk.DiaMockWindow.menubar
    
            division0 =tk.PanedWindow(orient =tk.VERTICAL)
            division0.pack(expand ="yes", fill ="both")

            for d in menus:
            
                menu_label=d[0]
                items= d[1] 
            
                #choix0 =tk.StringVar(); choix0.set("Rouge")
                #option0 =tk.OptionMenu(menubar, choix0, "Rouge", "Vert", "Bleu", command =ecran)
                #option0.pack()
               
                #Gtk.DiaMockWindow.menus[menu_label]=(menu,[])
                Gtk.DiaMockWindow.add_menu(menu_label)

                # addition des deux items pour le premier menu et leur commande associee
                for i in items:
                    item_label=i[0]
                    item_cmd=i[1]
                    #menuitem=menu.add_command(label = item_name,  command =item_cmd)
                    #Gtk.DiaMockWindow.menus[menu_label][1].append(menuitem)
                    Gtk.DiaMockWindow.add_menuitem(menu_label, item_label, item_cmd)
                    
            #division0.add(sysdemenu0)
            
            # ---- Add image as low panel
            
            import os
            script_dir = os.path.dirname(__file__)
            rel_path = Gtk.DiaMockWindow.bodyimage
            abs_path = os.path.join(script_dir, rel_path)
            
            photo0 =tk.PhotoImage(file =abs_path) 
            largeur =photo0.width(); hauteur =photo0.height() 
            
            startframe = tk.Frame(root)
            startframe.configure(background=background)
            
            fond0 =tk.Canvas(startframe, bg= 'grey')
            startframe.pack(side="left", fill="both", expand=1)
            fond0.pack(side="left", fill="both", expand=1)
            
            root.photo0 = photo0  # to prevent the image garbage collected.
            fond0.create_image((0,0), image=photo0, anchor='nw')
            
            division0.add(startframe)
            
           
            #Add the Status bar
            d=_Gtk_StatusBar(root)
            d.set_message('Ready...')
            d.install_mouse_coords_watcher(0.25)
            
            #division0.configure(background=background)
            
            root.geometry(str(largeur+2)+"x"+str(hauteur+10+2))
            root.config(menu =sysdemenu0)
            root.configure(background=background)
            
            #return MockGtk(root)
            root.mainloop()
       
    class _Gtk_Builder:
    
        def add_from_file(self, file_path):
            pass
            
        def get_object(self,id):
            pass
            
    #New G(TK)
    class Gtk:
        Builder=_Gtk_Builder
        AboutDialog=_Gtk_AboutDialog
        DiaMockWindow = _Gtk_DiaMockWindow
    
    #================================
   
    ui_support="gtk-sos "+GTK_SOS_VERSION
    ui_lib="Tcl/Tkinter"
    tcl = tk.Tcl()
    ui_lib_version_info=tcl.call("info", "patchlevel")
    


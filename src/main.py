# Load Gtk
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

from apps import *

# When the application is launched…
def on_activate(app):
    # … create a new window…
    win = Gtk.ApplicationWindow(application=app)
    # … with a button in it…
    #btn = Gtk.Button(label='Hello, World!')
    # … which closes the window when clicked
    #btn.connect('clicked', lambda x: win.close())
    #win.set_child(btn)

    label = Gtk.Label(label="Hello, GTK4!")
    win.set_child(label)

    win.set_default_size(400, 400)
    css = b"""
    #my-window {
        background-color: #ca1dc2;
    }
    
    .custom-box {
        background-color: #ca1dc2;
    }
    """
    provider = Gtk.CssProvider()
    provider.load_from_data(css)
    display = Gdk.Display.get_default()
    Gtk.StyleContext.add_provider_for_display(
        display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    box = Gtk.Box()
    box.set_css_classes(["custom-box"])
    win.set_child(box)

    win.present()

# Create a new application
app = Gtk.Application(application_id='com.example.GtkApplication')
app.connect('activate', on_activate)

# Run the application
app.run(None)

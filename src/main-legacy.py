import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_default_size(1300, 700)
        # self.set_decorated(False)
        # self.set_css_classes(["my-window"])

        # button = Gtk.Button(label="Hello, GTK4!")
        # button.set_css_classes(["my-button"])
        # self.set_child(button)

        label = Gtk.Label(label="Hello, GTK4!")
        label.set_css_classes(["my-label"])
        label.set_wrap(False)
        label.set_size_request(500, 500)
        self.set_child(label)


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.GtkApp")

    def do_activate(self):
        self.load_css()
        win = MyWindow(self)
        win.present()

    def load_css(self):
        css = b"""
        .my-window {
            background-color: #ca1dc200;
        }

        .my-label {
            color: #ca1dc2ff;
            min-width: 500px;
            min-height: 500px;
            max-width: 500px;
            max-height: 500px;
            padding: 0;
            margin: 0;
            border: 3px solid #ca1dc2ff;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


app = MyApp()
app.run(None)
import gi
import math
gi.require_version('Gtk', '4.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, Rsvg
import cairo

from random import randint

class AppLauncher(Gtk.Window):
    def __init__(self, app: Gtk.Application):
        super().__init__(title="App Launcher", application=app)
        self.app = app

        # Window setup
        #self.set_default_size(1920, 1080)
        self.set_default_size(960, 540)
        #self.fullscreen() #enable later
        self.set_decorated(False)
        self.maximize()
        self.set_css_classes(["my-window"])

        self.box1 = Gtk.Box()
        self.box1.set_css_classes(["my-box"])
        self.set_child(self.box1)

        # Drawing area (where the magic happens)
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_hexpand(True)
        self.drawing_area.set_vexpand(True)

        # Instead, If we didn't want it to fill the available space but wanted a fixed size
        # self.dw.set_content_width(100)
        # self.dw.set_content_height(100)

        self.drawing_area.set_draw_func(self.on_draw, None)
        self.box1.append(self.drawing_area)


        # Circle motion parameters
        self.angle = 0
        self.radius = 200
        self.icons = self.get_app_icons()  # Get app icons
        self.icons = self.icons[:10]  # Limit to 10 icons for now
        self.offsets = []

        for i in range(len(self.icons)):
            self.offsets.append(randint(-180, 180))

        # Timer for animation
        GLib.timeout_add(1000 // 60, self.on_timeout)  # 60 FPS

    def on_timeout(self):
        # Update angle for animation
        #self.angle += 0.05
        self.angle += 0.02
        if self.angle >= 2 * math.pi:
            self.angle = 0
        self.drawing_area.queue_draw()  # Trigger redraw
        return True

    def on_draw(self, area, c: cairo.Context , width, height, data):
        center_x, center_y = width / 2, height / 2

        # Draw icons in a circle
        num_icons = len(self.icons)
        for i, icon in enumerate(self.icons):
            angle = self.angle + (i * 2 * math.pi / num_icons) + self.offsets[i]
            x = center_x + (self.radius +  i * 30) * math.cos(angle)
            y = center_y + (self.radius +  i * 30) * math.sin(angle)

            # Load and draw icon
            icon_width = 128
            icon_height = 128
            Gdk.cairo_set_source_pixbuf(c, icon,  x - icon_width / 2, y - icon_height / 2)
            c.paint()

    def get_app_icons(self):
        # Fetch icons from desktop applications (using .desktop files)
        apps = Gio.AppInfo.get_all()
        icons = []

        icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())

        for app in apps:
            icon = app.get_icon()
            if icon:
                icon_image = icon_theme.lookup_icon(icon.to_string(), None, 128, 128, Gtk.TextDirection.LTR, Gtk.IconLookupFlags.FORCE_REGULAR)
                if icon_image:
                    icon_file: Gio.File = icon_image.get_file()
                    icon_path = icon_file.get_path()
                    pixbuf = None
                    if icon_path:
                        #print(icon_path)
                        if icon_path.endswith(".png"):
                            surface = cairo.ImageSurface.create_from_png(icon_path)
                            pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, surface.get_width(), surface.get_height())
                        elif icon_path.endswith(".svg"):
                            #icons.append(cairo.SVGSurface(icon_path, 128, 128)) # WRITE ONLY
                            try:
                                handle = Rsvg.Handle.new_from_file(icon_path)
                                pixbuf = handle.get_pixbuf()
                            except:
                                pass
                        else:
                            # Handle other formats if needed
                            pass
                        if pixbuf is not None:
                            pixbuf = pixbuf.scale_simple(128, 128, GdkPixbuf.InterpType.BILINEAR)
                            icons.append(pixbuf)


        return icons

class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.GtkApp")

    def do_activate(self):
        self.load_css()
        win = AppLauncher(self)
        win.present()

    def load_css(self):
        css = b"""
        .my-window {
            background-color: #ca1dc200;
        }

        .my-box {
            background-color: #ca1dc200;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

# Run the application
if __name__ == "__main__":
    app = MyApp()
    app.run(None)
    #app.connect("destroy", Gtk.main_quit)
    #app.show_all()
    #Gtk.main()

import gi
import math
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Gio
import cairo

class AppLauncher(Gtk.Window):
    def __init__(self, app: Gtk.Application):
        super().__init__(title="App Launcher", application=app)
        self.app = app

        # Window setup
        self.set_default_size(400, 400)
        #self.set_border_width(0)
        self.set_resizable(False)

        self.box1 = Gtk.Box()
        self.set_child(self.box1)

        # Centering the window
        #screen = self.get_screen()
        #self.set_position(Gtk.WindowPosition.CENTER)

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
        self.radius = 120
        self.icons = self.get_app_icons()  # Get app icons

        # Timer for animation
        GLib.timeout_add(1000 // 60, self.on_timeout)  # 60 FPS

    def on_timeout(self):
        # Update angle for animation
        self.angle += 0.05
        if self.angle >= 2 * math.pi:
            self.angle = 0
        self.drawing_area.queue_draw()  # Trigger redraw
        return True

    def on_draw(self, area, c, w, h, data):
        width = area.get_allocated_width()
        height = area.get_allocated_height()
        center_x, center_y = width / 2, height / 2

        # Clear the drawing area
        c.set_source_rgb(0, 0, 0)  # Black background
        c.rectangle(0, 0, width, height)
        c.fill()

        # Draw icons in a circle
        num_icons = len(self.icons)
        for i, icon in enumerate(self.icons):
            # angle = self.angle + (i * 2 * math.pi / num_icons)
            # x = center_x + self.radius * math.cos(angle)
            # y = center_y + self.radius * math.sin(angle)

            # Load and draw icon
            icon_width = 128
            icon_height = 128
            # c.set_source_surface(icon, x - icon_width / 2, y - icon_height / 2)
            c.set_source_surface(icon, 0, 0)
            c.paint()

    def get_app_icons(self):
        # Fetch icons from desktop applications (using .desktop files)
        apps = Gio.AppInfo.get_all()
        icons = []

        #icon_theme = Gio.ThemedIcon.get_default()
        #icon_theme = Gtk.IconTheme.get_default()
        icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())

        for app in apps:
            icon = app.get_icon()
            if icon:
                icon_image = icon_theme.lookup_icon(icon.to_string(), None, 128, 128, Gtk.TextDirection.LTR, Gtk.IconLookupFlags.FORCE_REGULAR)
                if icon_image:
                    icon_file: Gio.File = icon_image.get_file()
                    icon_path = icon_file.get_path()
                    icon_path = "test/org.gnome.Weather.svg"
                    if icon_path.endswith(".png"):
                        icons.append(cairo.ImageSurface.create_from_png(icon_path))
                    elif icon_path.endswith(".svg"):
                        #icons.append(cairo.SVGSurface(icon_path, icon_image.get_intrinsic_width(), icon_image.get_intrinsic_height()))
                        icons.append(cairo.SVGSurface(icon_path, 128, 128))
                    else:
                        # Handle other formats if needed
                        pass


        return icons

class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.GtkApp")

    def do_activate(self):
        win = AppLauncher(self)
        win.present()

# Run the application
if __name__ == "__main__":
    app = MyApp()
    app.run(None)
    #app.connect("destroy", Gtk.main_quit)
    #app.show_all()
    #Gtk.main()

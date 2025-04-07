import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gdk, GLib, GObject

import OpenGL.GL as gl

class OpenGLWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_default_size(400, 300)
        self.set_title("GTK4 OpenGL Example")

        self.gl_area = Gtk.GLArea()
        self.gl_area.set_auto_render(True)
        self.gl_area.connect("realize", self.on_realize)
        self.gl_area.connect("render", self.on_render)
        self.gl_area.set_required_version(3, 3)

        self.set_child(self.gl_area)

    def on_realize(self, area):
        context = self.gl_area.get_context()
        if not context:
            print("Failed to get GL context")
            return
        print("OpenGL context realized")

    def on_render(self, area, context):
        gl.glClearColor(0.3, 0.0, 0.0, 1.0)  # Dark red
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        return True


class OpenGLApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.OpenGLApp")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = OpenGLWindow(self)
        win.present()


if __name__ == "__main__":
    app = OpenGLApp()
    app.run(None)
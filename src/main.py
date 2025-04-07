import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gdk, GLib, GObject

from OpenGL.GL import *

class OpenGLWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_default_size(400, 300)
        self.set_title("GTK4 OpenGL Example")

        self.gl_area = Gtk.GLArea()
        #self.gl_area.set_auto_render(True)
        self.gl_area.connect("realize", self.on_realize)
        self.gl_area.connect("render", self.on_render)
        #self.gl_area.set_required_version(3, 3)

        self.set_child(self.gl_area)

    def on_render(self, area: Gtk.GLArea, context: Gdk.GLContext):
        area.make_current()

        #w = area.get_allocated_width()
        w = area.get_width()
        #h = area.get_allocated_height()
        h = area.get_height()
        glViewport(0, 0, w, h)

        # inside this function it's safe to use GL; the given
        # Gdk.GLContext has been made current to the drawable
        # surface used by the Gtk.GLArea and the viewport has
        # already been set to be the size of the allocation
        # we can start by clearing the buffer
        glClearColor(1, 1, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT)

        # draw your object
        glColor3f(0, 0, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f ( 0.0, 1.0, 0.0)
        glVertex3f (-1.0,-1.0, 0.0)
        glVertex3f ( 1.0,-1.0, 0.0)
        glEnd()

        # we completed our drawing; the draw commands will be
        # flushed at the end of the signal emission chain, and
        # the buffers will be drawn on the window
        return True

    def on_realize(self, area: Gtk.GLArea):
        # We need to make the context current if we want to
        # call GL API
        area.make_current()

        # If there were errors during the initialization or
        # when trying to make the context current, this
        # function will return a Gio.Error for you to catch
        if area.get_error() is not None:
          return

        #self.init_buffers()
        #self.init_shaders()


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
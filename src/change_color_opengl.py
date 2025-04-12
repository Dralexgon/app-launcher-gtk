import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

import time
import OpenGL.GL as gl

class OpenGLWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_default_size(600, 400)
        self.set_title("OpenGL Triangle")

        self.gl_area = Gtk.GLArea()
        self.gl_area.set_auto_render(True)
        self.gl_area.set_required_version(3, 2)
        self.gl_area.connect("realize", self.on_realize)
        self.gl_area.connect("render", self.on_render)

        self.set_child(self.gl_area)

        self.fps_count = 0
        self.fps_timer = time.time()

        GLib.timeout_add(1000 // 60, self.update_frame)

    def update_frame(self):
        self.gl_area.queue_render()
        return True

    def on_realize(self, area: Gtk.GLArea):
        area.make_current()

    def get_val(self, t, n):
        if t <= n and t >= n - 1:
            return t - n + 1
        elif t > n and t < n + 1:
            return n + 1 - t
        else:
            return 0


    def on_render(self, area: Gtk.GLArea, context):
        r = self.get_val((time.time() % 6), 1)
        g = self.get_val((time.time() % 6), 3)
        b = self.get_val((time.time() % 6), 5)
        gl.glClearColor(r, g, b, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        self.fps_count += 1
        if time.time() - self.fps_timer >= 1:
            print(f"FPS: {self.fps_count}")
            self.fps_count = 0
            self.fps_timer = time.time()

        return True


class OpenGLApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.opengl.triangle")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = OpenGLWindow(self)
        win.present()


if __name__ == "__main__":
    app = OpenGLApp()
    app.run()

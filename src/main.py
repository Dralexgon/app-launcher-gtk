import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

import time
import OpenGL.GL as gl
import numpy as np

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

        self.vao = None

        self.fps_count = 0
        self.fps_timer = time.time()

        GLib.timeout_add(1000 // 60, self.test)

    def test(self):
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
        # Triangle data (3 vertices, 2D positions + RGB colors)
        vertices = np.array([
            # Position    # Color
            -0.5, -0.5,   1.0, 0.0, 0.0,  # Bottom left, red
             0.5, -0.5,   0.0, 1.0, 0.0,  # Bottom right, green
             0.0,  0.5,   0.0, 0.0, 1.0,  # Top center, blue
        ], dtype=np.float32)

        self.vao = gl.glGenVertexArrays(1)
        vbo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

        # position attribute
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, False, 20, gl.ctypes.c_void_p(0))
        # color attribute
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, 20, gl.ctypes.c_void_p(8))

        gl.glBindVertexArray(0)

        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        gl.glBindVertexArray(0)

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

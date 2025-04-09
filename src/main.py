import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from math import sqrt, sin, cos, pi

import time
import OpenGL.GL as gl
import numpy as np

VERTEX_SHADER_SRC = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
};
"""

FRAGMENT_SHADER_SRC = """
#version 330
in vec3 v_color;
out vec4 frag_color;
void main() {
    frag_color = vec4(v_color, 1.0);
}
"""

VERTICES = [
    -0.5, -0.5 * sqrt(3) / 3, 0.0,
    0.5, -0.5 * sqrt(3) / 3, 0.0,
    0.0, 0.5 * sqrt(3) * 2 / 3, 0.0,
]

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

        self.last_time = time.time()

        #GLib.timeout_add(1000 // 60, self.test)
        GLib.timeout_add(1000 // 60, self.test)

    def test(self):
        #self.gl_area.queue_draw()
        self.gl_area.queue_render()
        return True

    def on_realize(self, area: Gtk.GLArea):
        area.make_current()
        # vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        # gl.glShaderSource(vertex_shader, VERTEX_SHADER_SRC)
        # gl.glCompileShader(vertex_shader)
        #assert gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS)

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

        print(round(1 / (time.time() - self.last_time)))
        self.last_time = time.time()

        gl.glFlush()
        self.gl_area.queue_draw()
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

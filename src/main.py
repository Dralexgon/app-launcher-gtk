import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from math import sqrt, sin, cos, pi

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
        #self.gl_area.set_required_version(3, 2) work but not sure
        self.gl_area.set_required_version(3, 1)
        self.gl_area.connect("realize", self.on_realize)
        self.gl_area.connect("render", self.on_render)

        self.set_child(self.gl_area)

    def on_realize(self, area: Gtk.GLArea):
        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex_shader, VERTEX_SHADER_SRC)
        gl.glCompileShader(vertex_shader)
        #assert gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS)

    def on_render(self, area, context):
        #gl.glViewport(0, 0, 800, 600)

        gl.glClearColor(0.1, 0.7, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

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

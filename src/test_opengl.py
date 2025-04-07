import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import OpenGL.GL as gl
import numpy as np

VERTEX_SHADER_SRC = """
#version 330
layout(location = 0) in vec2 position;
layout(location = 1) in vec3 color;
out vec3 v_color;
void main() {
    v_color = color;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

FRAGMENT_SHADER_SRC = """
#version 330
in vec3 v_color;
out vec4 frag_color;
void main() {
    frag_color = vec4(v_color, 1.0);
}
"""

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

        # OpenGL objects
        self.program = None
        self.vao = None

    def on_realize(self, area):
        area.make_current()

        # Compile shaders
        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex_shader, VERTEX_SHADER_SRC)
        gl.glCompileShader(vertex_shader)
        # assert gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS)

        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragment_shader, FRAGMENT_SHADER_SRC)
        gl.glCompileShader(fragment_shader)
        # assert gl.glGetShaderiv(fragment_shader, gl.GL_COMPILE_STATUS)

        # Create program
        self.program = gl.glCreateProgram()
        gl.glAttachShader(self.program, vertex_shader)
        gl.glAttachShader(self.program, fragment_shader)
        gl.glLinkProgram(self.program)
        # assert gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)

        # Clean up shaders (they're linked now)
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

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

    def on_render(self, area, context):
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        #gl.glUseProgram(self.program)
        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        gl.glBindVertexArray(0)

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

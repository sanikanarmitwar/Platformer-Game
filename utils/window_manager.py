  
import glfw
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer

class Window:
    def __init__(self, height, width):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        
        self.windowHeight = height
        self.windowWidth = width
        self.window = glfw.create_window(width, height, "Demo", None, None)

        if not self.window:
            glfw.terminate()
            print("Glfw window can't be created")
            exit()

        glfw.set_window_pos(self.window, 500, 100) 
        glfw.make_context_current(self.window)

        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS) 
       
        glViewport(0, 0, self.windowWidth, self.windowHeight)

        self.prevTime = glfw.get_time()

    def Close(self):
        self.impl.shutdown()
        glfw.terminate()
    
    def IsOpen(self):
        return not glfw.window_should_close(self.window)

    def StartFrame(self, c0, c1, c2, c3):
        currentTime = glfw.get_time()
        deltaTime = currentTime - self.prevTime
        self.prevTime = currentTime
        time = {"currentTime": currentTime, "deltaTime": deltaTime}

        glfw.poll_events()
        
        self.impl.process_inputs()
        imgui.new_frame()
        
        inputs = []
        if glfw.get_key(self.window, glfw.KEY_1) == glfw.PRESS:
            inputs.append("1")
        if glfw.get_key(self.window, glfw.KEY_2) == glfw.PRESS:
            inputs.append("2")
        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            inputs.append("W")
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            inputs.append("A")
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            inputs.append("S")
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            inputs.append("D")
        if glfw.get_key(self.window, glfw.KEY_SPACE) == glfw.PRESS:
            inputs.append("SPACE")

        glClearColor(c0, c1, c2, c3)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        return inputs, time
    
    def EndFrame(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
        
        glfw.swap_buffers(self.window)
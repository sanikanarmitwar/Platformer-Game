
import imgui
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
import assets.objects.objects as ob

class Key:
    def __init__(self, shader, x, y):
        from assets.objects.objects import keyProps 
        self.object = Object(shader, keyProps)
        self.object.properties["position"] = np.array([x, y, 0], dtype=np.float32)
        self.collected = False

class Game:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = -1 
        self.level = 0 
        self.camera = Camera(height, width)
        self.shaders = [Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])]
        self.lives = 3 
        self.invulnerable_timer = 0  
        self.menu_background = Object(self.shaders[0], ob.backgroundPropsmenu)
        self.load_level(self.level)
        self.aliens = [] 

        self.keys_collected = 0
        self.total_keys = 3  
        self.keys = []
        self.game_completed = False

        self.gravity = -500.0
        self.jump_velocity = 300.0
        self.is_jumping = False
        self.velocity_y = 0.0
        self.ground_level = -150 

       

    def check_crocodile_collision(self):
        player_pos = self.objects[0].properties["position"][:2]  
        player_radius = 30 

       
        if self.level == 0:
            
            croc_positions = [
                        [300, 10, 0.0], 
                        [-200, -200, 0.0], 
                        [-50, 300, 0.0],
                        [-350, 0, 0.0],
                        [50, -50, 0.0],
                        [200, -300, 0.0],
                        [200, 200, 0.0],
                        [-200, 200, 0.0]
        
            ]
            
           
            for croc_pos in croc_positions:
                
                dx = player_pos[0] - croc_pos[0]
                dy = player_pos[1] - croc_pos[1]
                distance = np.sqrt(dx*dx + dy*dy)
                
                if distance < (player_radius + 40): 
                    return True
            
        return False
    
    def check_level_complete(self):
       
        if self.level == 0 or self.level==1:  
            player_pos_x = self.objects[0].properties["position"][0]
            if self.keys_collected == self.level + 1 :
                self.level += 1
                self.load_level(self.level)
                
                self.objects[0].properties["position"] = np.array([-450, 0, 0], dtype=np.float32)


    def load_level(self, level):
       
        """Load objects and background based on the current level"""
        if level == 0:
            self.objects = [Object(self.shaders[0], ob.playerProps), 
                          Object(self.shaders[0], ob.backgroundProps)]
            self.keys = [Key(self.shaders[0], 450, 0)]

        elif level == 1:
            
            self.objects = [Object(self.shaders[0], ob.playerProps), 
                          Object(self.shaders[0], ob.backgroundProps2)]
            
            self.keys = [Key(self.shaders[0], 450, 0)]
            
          
            alien_positions = [
                [-350, 300, 0],
                [0, 100, 0],
                [300, -400, 0]
            ]
            
            self.aliens = []
            for pos in alien_positions:
                alien = Object(self.shaders[0], ob.alienProps.copy())
                alien.properties['position'] = np.array(pos, dtype=np.float32)
                self.objects.append(alien)
                self.aliens.append(alien)

        elif level == 2:
            self.objects = [Object(self.shaders[0], ob.playerProps), 
                          Object(self.shaders[0], ob.backgroundProps3)]
            self.keys = [Key(self.shaders[0], 450, -150)]
            self.aliens = []
            self.objects = [Object(self.shaders[0], ob.playerProps), 
                          Object(self.shaders[0], ob.backgroundProps3)]
            
           
            rock_positions = [
                [100, self.ground_level, 0],
                [350, self.ground_level, 0],
                [-150, self.ground_level, 0]
            ]
            
            self.rocks = []
            for pos in rock_positions:
                rock = Object(self.shaders[0], ob.rockProps.copy())
                rock.properties['position'] = np.array(pos, dtype=np.float32)
                self.objects.append(rock)
                self.rocks.append(rock)

    def check_key_collision(self):
        player_pos = self.objects[0].properties["position"][:2]
        player_radius = 30

        for key in self.keys:
            if not key.collected:
                key_pos = key.object.properties["position"][:2]
                dx = player_pos[0] - key_pos[0]
                dy = player_pos[1] - key_pos[1]
                distance = np.sqrt(dx*dx + dy*dy)
                
                if distance < (player_radius + 20):  
                    key.collected = True
                    self.keys_collected += 1
                    return True
        return False
    
    def DrawWinScreen(self):
        for shader in self.shaders:
            self.camera.Update(shader)
        
        self.menu_background.Draw()

        imgui.set_next_window_size(400, 200)
        imgui.set_next_window_position(self.width / 2 - 200, self.height / 2 - 100)
        
        imgui.begin("Victory!", flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE |
                    imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR)

        imgui.text("Congratulations! You've collected all the keys!")
        imgui.spacing()

        button_width = 200
        button_x = (imgui.get_window_width() - button_width) / 2

        imgui.set_cursor_pos_x(button_x)
        if imgui.button("New Game", width=button_width, height=40):
            self.reset_game()
            self.screen = 0

        imgui.set_cursor_pos_x(button_x)
        if imgui.button("Main Menu", width=button_width, height=40):
            self.reset_game()
            self.screen = -1

        imgui.end()

    def reset_game(self):
        self.level = 0
        self.keys_collected = 0
        self.game_completed = False
        self.lives = 3
        self.load_level(self.level)


    def check_rock_collision(self):
        if self.level == 2:
            player_pos = self.objects[0].properties["position"][:2]
            player_radius = 30 

            for rock in self.rocks:
                rock_pos = rock.properties["position"][:2]
                dx = player_pos[0] - rock_pos[0]
                dy = player_pos[1] - rock_pos[1]
                distance = np.sqrt(dx*dx + dy*dy)
                
                if distance < (player_radius + 20):  
                    return True
        return False

    def update_player_physics(self, time):
        if self.level == 2:
            player = self.objects[0]
            
            self.velocity_y += self.gravity * time["deltaTime"]
            player.properties["position"][1] += self.velocity_y * time["deltaTime"]
            
            
            if player.properties["position"][1] < self.ground_level:
                player.properties["position"][1] = self.ground_level
                self.velocity_y = 0
                self.is_jumping = False

    def update_aliens(self, time):
        if self.level == 1: 
            for alien in self.aliens:
                
                movement = alien.properties['movement_speed'] * alien.properties['movement_direction'] * time['deltaTime']
                alien.properties['position'][1] += movement

                
                if alien.properties['position'][1] > 300:
                    alien.properties['movement_direction'] = -1
                elif alien.properties['position'][1] < -300:
                    alien.properties['movement_direction'] = 1

    def check_alien_collision(self):
        if self.level == 1:  
            player_pos = self.objects[0].properties["position"][:2]
            player_radius = 30 

            for alien in self.aliens:
                alien_pos = alien.properties["position"][:2]
                dx = player_pos[0] - alien_pos[0]
                dy = player_pos[1] - alien_pos[1]
                distance = np.sqrt(dx*dx + dy*dy)
                
                if distance < (player_radius + 30):  
                    return True
        return False


    def DrawMenu(self):
        for shader in self.shaders:
            self.camera.Update(shader)
        
        self.menu_background.Draw()

        imgui.set_next_window_size(400, 200)
        imgui.set_next_window_position(self.width / 2 - 200, self.height / 2 - 150)
        
        imgui.begin("Main Menu", flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE |
                    imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR)

        imgui.text("Welcome to the Game")
        imgui.spacing()

        button_width = 200
        button_x = (imgui.get_window_width() - button_width) / 2

        imgui.set_cursor_pos_x(button_x)
        if imgui.button("Start Game", width=button_width, height=40):
            self.level = 0
            self.screen = 0
            self.load_level(self.level)

        imgui.set_cursor_pos_x(button_x)
        if imgui.button("Quit", width=button_width, height=40):
            exit(0)

        imgui.end()


    def DrawLevelMenu(self):
        """Displays a small in-game menu at the top with level-specific information"""
        imgui.set_next_window_size(400, 100) 
        imgui.set_next_window_position(self.width / 2 - 200, 10)

        imgui.begin("Level Menu", flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE |
                    imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR)

        if self.level == 0:
            biome = "River Biome"
            objective = "Avoid the crocodiles!"
        elif self.level == 1:
            biome = "Space Biome"
            objective = "Watch out for Aliens!"
        else:
            biome = "Field Biome"
            objective = "Beware of Rocks!"

        imgui.text(f"Level {self.level + 1} - {biome}")
        imgui.text(f"Objective: {objective}")
        imgui.text(f"Lives: {self.lives}  Keys: {self.keys_collected}")

        if imgui.button("Next Level", width=140, height=30) and self.level < 2:
            self.level += 1
            self.load_level(self.level)

        imgui.same_line()
        if imgui.button("Main Menu", width=140, height=30):
            self.screen = -1

        imgui.end()
        


    def InitScreen(self):
        if self.screen == 0:
            self.show_menu = False
            pass
        if self.screen == 1:
            pass
        if self.screen == 2:
            pass


    def ProcessFrame(self, inputs, time):
        if self.screen == -1:
            self.DrawMenu()
            return
        
        if self.game_completed:
            self.DrawWinScreen()
            return
        
        self.DrawLevelMenu()

        if self.check_key_collision():
            if self.keys_collected == self.total_keys:
                self.game_completed = True
                return

    
        for key in self.keys:
            if not key.collected:
                key.object.Draw()

       
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= time["deltaTime"]

        if self.level == 2:
            if "SPACE" in inputs and not self.is_jumping:
                self.velocity_y = self.jump_velocity
                self.is_jumping = True

        self.update_aliens(time)


        self.objects[0].properties["velocity"] = np.array([0,0,0], dtype=np.float32)
        if "W" in inputs:
            self.objects[0].properties["velocity"][1] = self.objects[0].properties["sens"]
        if "S" in inputs:
            self.objects[0].properties["velocity"][1] = -self.objects[0].properties["sens"]
        if "A" in inputs:
            self.objects[0].properties["velocity"][0] = -self.objects[0].properties["sens"]
        if "D" in inputs:
            self.objects[0].properties["velocity"][0] = self.objects[0].properties["sens"]
        
        self.objects[0].properties["position"] += self.objects[0].properties["velocity"] * time["deltaTime"]

        self.check_level_complete()

        self.update_player_physics(time)

      
        if self.invulnerable_timer <= 0 and self.check_crocodile_collision():
            self.lives -= 1
            self.invulnerable_timer = 2.0  
            
           
            self.objects[0].properties["position"] = np.array([-450, 0, 0], dtype=np.float32)
            

            if self.lives <= 0:
                self.screen = -1
                self.keys_collected=0
                self.level = 0 
                self.lives = 3  

        if self.invulnerable_timer <= 0:
            if self.check_alien_collision():
                self.lives -= 1
                self.invulnerable_timer = 2.0
                self.objects[0].properties["position"] = np.array([-450, 0, 0], dtype=np.float32)
                
                if self.lives <= 0:
                    self.screen = -1
                    self.level = 0 
                    self.keys_collected=0
                    self.lives = 3

        if self.invulnerable_timer <= 0:
            if self.check_rock_collision():
                self.lives -= 1
                self.invulnerable_timer = 2.0
                self.objects[0].properties["position"] = np.array([-450, self.ground_level, 0], dtype=np.float32)
                self.velocity_y = 0
                self.is_jumping = False
                
                if self.lives <= 0:
                    self.screen = -1
                    self.keys_collected=0
                    self.level = 0 
                    self.lives = 3

        for shader in self.shaders:
            self.camera.Update(shader)


        for obj in self.objects:
            obj.Draw()

    def DrawText(self):
        if self.screen == 0:
            pass  
        if self.screen == 1:
           pass
        if self.screen == 2:
           pass

    def UpdateScene(self, inputs, time):
        if self.screen == 0:
            pass
        if self.screen == 1:
            pass
            
    def DrawScene(self):
        if self.screen == 1:
            for shader in self.shaders:
                self.camera.Update(shader)
 
            for obj in self.objects:
                obj.Draw()

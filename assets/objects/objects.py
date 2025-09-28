import numpy as np
import random

def CreateCircle(center, radius, colour, points = 10, offset = 0, semi = False):
    vertices = [center[0], center[1], center[2], colour[0], colour[1], colour[2]]
    indices = []

    if semi == True:
        for i in range(points+1):
            vertices += [
                center[0] + radius * np.cos(float(i * np.pi)/points),
                center[1] + radius * np.sin(float(i * np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]
    else:
        for i in range(points):
            vertices += [
                center[0] + radius * np.cos(float(i * 2* np.pi)/points),
                center[1] + radius * np.sin(float(i * 2* np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points-1 else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]

    return (vertices, indices)    

def CreatePlayer():

    vertices, indices = CreateCircle([0.0, 0.0, 0.03], 1.0, [220/255, 183/255, 139/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices


def CreateTriangleCrocodile(position):
    crocodileColor = [0.000, 0.392, 0.000]  
    
    # Triangle body vertices
    body_verts = [
        position[0], position[1] + 40, position[2], crocodileColor[0], crocodileColor[1], crocodileColor[2],
        position[0] - 40, position[1] - 40, position[2], crocodileColor[0], crocodileColor[1], crocodileColor[2],
        position[0] + 40, position[1] - 40, position[2], crocodileColor[0], crocodileColor[1], crocodileColor[2]
    ]
    
    # Eye and pupil vertices
    eye_left_verts = [
        position[0] - 16, position[1] + 10, position[2] + 0.001, 1, 1, 1,  
        position[0] - 22, position[1], position[2] + 0.001, 1, 1, 1,     
        position[0] - 10, position[1], position[2] + 0.001, 1, 1, 1      
    ]
    
    eye_right_verts = [
        position[0] + 16, position[1] + 10, position[2] + 0.001, 1, 1, 1,  
        position[0] + 10, position[1], position[2] + 0.001, 1, 1, 1,     
        position[0] + 22, position[1], position[2] + 0.001, 1, 1, 1      
    ]
    
    pupil_left_verts = [
        position[0] - 16, position[1] + 8, position[2] + 0.002, 0, 0, 0,  
        position[0] - 20, position[1] + 2, position[2] + 0.002, 0, 0, 0, 
        position[0] - 12, position[1] + 2, position[2] + 0.002, 0, 0, 0  
    ]
    
    pupil_right_verts = [
        position[0] + 16, position[1] + 8, position[2] + 0.002, 0, 0, 0,  
        position[0] + 12, position[1] + 2, position[2] + 0.002, 0, 0, 0, 
        position[0] + 20, position[1] + 2, position[2] + 0.002, 0, 0, 0  
    ]

    all_verts = body_verts + eye_left_verts + eye_right_verts + pupil_left_verts + pupil_right_verts
    return all_verts 


def CreateBackground():
    grassColour = [0.824, 0.412, 0.118]
    waterColour = [0.125, 0.698, 0.667]

    vertices = [
        -500.0, 500.0, -1.0, *grassColour,
        -400.0, 500.0, -1.0, *grassColour,
        -400.0, -500.0, -1.0, *grassColour,
        -500.0, -500.0, -1.0, *grassColour,

        500.0, 500.0, -1.0, *grassColour,
        400.0, 500.0, -1.0, *grassColour,
        400.0, -500.0, -1.0, *grassColour,
        500.0, -500.0, -1.0, *grassColour,

        -400.0, 500.0, -1.0, *waterColour,
        400.0, 500.0, -1.0, *waterColour,
        400.0, -500.0, -1.0, *waterColour,
        -400.0, -500.0, -1.0, *waterColour,
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]

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

    for pos in croc_positions:
        croc_verts = CreateTriangleCrocodile(pos)
        vertex_offset = len(vertices) // 6 
        body_inds = [vertex_offset, vertex_offset + 1, vertex_offset + 2]
        eye_indices = [
            vertex_offset + 3, vertex_offset + 4, vertex_offset + 5,
            vertex_offset + 6, vertex_offset + 7, vertex_offset + 8,
            vertex_offset + 9, vertex_offset + 10, vertex_offset + 11,
            vertex_offset + 12, vertex_offset + 13, vertex_offset + 14
        ]
        
        vertices += croc_verts
        indices += body_inds + eye_indices 

    return vertices, indices




def CreateBackground2(num_stars=30):
    spaceColour = [0.0, 0.0, 0.1] 
    starColour = [1.0, 1.0, 1.0]  
    starColour1 = [1.0, 0.71, 0.76]
    starColour2 = [0.5, 0.0, 0.5]
    ufo = [0.294, 0.000, 0.510]

    
    vertices = [
        -500.0, 500.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2],
        500.0, 500.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2],
        500.0, -500.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2],
        -500.0, -500.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2],
        230,300,-0.05,ufo[0],ufo[1],ufo[2],
        370,300,-0.05,ufo[0],ufo[1],ufo[2],
        150,250,-0.05,ufo[0],ufo[1],ufo[2],
        450,250,-0.05,ufo[0],ufo[1],ufo[2],
    ]

    indices = [
        0, 1, 2,  0, 3, 2, 
        4, 5, 7,  4, 7, 6,
    ]

    sun_verts1, sun_inds1 = CreateCircle([300,300, -0.05], 70, [0.561, 0.737, 0.561], 20, len(vertices)/6,True)

    vertices += sun_verts1
    indices += sun_inds1

    sun_verts2, sun_inds2 = CreateCircle([230,275, -0.03], 10, [1.000, 1.000, 0.000], 20, len(vertices)/6)

    vertices += sun_verts2
    indices += sun_inds2

    sun_verts3, sun_inds3 = CreateCircle([370,275, -0.03], 10, [1.000, 1.000, 0.000], 20, len(vertices)/6)

    vertices += sun_verts3
    indices += sun_inds3

    sun_verts4, sun_inds4 = CreateCircle([300,275, -0.03], 10, [1.000, 1.000, 0.000], 20, len(vertices)/6)

    vertices += sun_verts4
    indices += sun_inds4

    
    star_size = 2.0  
    start_index = len(vertices) // 6 

    for _ in range(num_stars):
        x = random.uniform(-500, 500)  
        y = random.uniform(-500, 500)  
        z = -0.8 

       
        vertices.extend([
            x - star_size, y + star_size, z, starColour[0], starColour[1], starColour[2],
            x + star_size, y + star_size, z, starColour[0], starColour[1], starColour[2],
            x + star_size, y - star_size, z, starColour[0], starColour[1], starColour[2],
            x - star_size, y - star_size, z, starColour[0], starColour[1], starColour[2],
        ])

        indices.extend([
            start_index, start_index + 1, start_index + 2,
            start_index, start_index + 3, start_index + 2,
        ])

        start_index += 4 

    for _ in range(num_stars):
        x = random.uniform(-500, 500) 
        y = random.uniform(-500, 500) 
        z = -0.8 

       
        vertices.extend([
            x - star_size, y + star_size, z, starColour1[0], starColour1[1], starColour1[2],
            x + star_size, y + star_size, z, starColour1[0], starColour1[1], starColour1[2],
            x + star_size, y - star_size, z, starColour1[0], starColour1[1], starColour1[2],
            x - star_size, y - star_size, z, starColour1[0], starColour1[1], starColour1[2],
        ])

        indices.extend([
            start_index, start_index + 1, start_index + 2,
            start_index, start_index + 3, start_index + 2,
        ])

        start_index += 4  

    for _ in range(num_stars):
        x = random.uniform(-500, 500)  
        y = random.uniform(-500, 500) 
        z = -0.8  

        
        vertices.extend([
            x - star_size, y + star_size, z, starColour2[0], starColour2[1], starColour2[2],
            x + star_size, y + star_size, z, starColour2[0], starColour2[1], starColour2[2],
            x + star_size, y - star_size, z, starColour2[0], starColour2[1], starColour2[2],
            x - star_size, y - star_size, z, starColour2[0], starColour2[1], starColour2[2],
        ])

        indices.extend([
            start_index, start_index + 1, start_index + 2,
            start_index, start_index + 3, start_index + 2,
        ])

        start_index += 4  

    return vertices, indices


def CreateBackground3():
    skyColor = [0.184, 0.310, 0.310]   # Light blue sky
    groundColor = [0.5, 0.25, 0.0]  # Brown ground
    grassColor = [0.0, 0.5, 0.0]  # Green grass

    vertices = [
        # Sky
        -500.0, 500.0, -0.9, skyColor[0], skyColor[1], skyColor[2],
        500.0, 500.0, -0.9, skyColor[0], skyColor[1], skyColor[2],
        500.0, -150.0, -0.9, skyColor[0], skyColor[1], skyColor[2],
        -500.0, -150.0, -0.9, skyColor[0], skyColor[1], skyColor[2],

        # Ground 
        -500.0, -200.0, -0.9, groundColor[0], groundColor[1], groundColor[2],
        500.0, -200.0, -0.9, groundColor[0], groundColor[1], groundColor[2],
        500.0, -500.0, -0.9, groundColor[0], groundColor[1], groundColor[2],
        -500.0, -500.0, -0.9, groundColor[0], groundColor[1], groundColor[2],

        # Grass layer
        -500.0, -200.0, -0.85, grassColor[0], grassColor[1], grassColor[2],
        500.0, -200.0, -0.85, grassColor[0], grassColor[1], grassColor[2],
        500.0, -150.0, -0.85, grassColor[0], grassColor[1], grassColor[2],
        -500.0, -150.0, -0.85, grassColor[0], grassColor[1], grassColor[2],
    ]

    indices = [
        # Sky
        0, 1, 2,  0, 3, 2,
        # Ground
        4, 5, 6,  4, 7, 6,
        # Grass layer
        8, 9, 10,  8, 11, 10,
    ]
    sun_verts1, sun_inds1 = CreateCircle([-300,300, 0.05], 70, [0.827, 0.827, 0.827], 20, len(vertices)/6)

    vertices += sun_verts1
    indices += sun_inds1

    sun_verts2, sun_inds2 = CreateCircle([-270,315, 0.06], 10, [0.663, 0.663, 0.663], 20, len(vertices)/6)

    vertices += sun_verts2
    indices += sun_inds2

    sun_verts3, sun_inds3 = CreateCircle([-280,335, 0.06], 10, [0.663, 0.663, 0.663], 20, len(vertices)/6)

    vertices += sun_verts3
    indices += sun_inds3


    return vertices, indices

def CreateBackgroundmenu():
    skyColor = [0.3, 0.6, 1.0]   # Light blue sky
    groundColor = [0.5, 0.25, 0.0]  # Brown ground
    grassColor = [0.0, 0.5, 0.0]  # Green grass

    vertices = [
        # Sky 
        -500.0, 500.0, -0.9, skyColor[0], skyColor[1], skyColor[2],
        500.0, 500.0, -0.9, skyColor[0], skyColor[1], skyColor[2],
        500.0, -150.0, -0.9, skyColor[0], skyColor[1], skyColor[2],
        -500.0, -150.0, -0.9, skyColor[0], skyColor[1], skyColor[2],

        # Ground 
        -500.0, -200.0, -0.9, groundColor[0], groundColor[1], groundColor[2],
        500.0, -200.0, -0.9, groundColor[0], groundColor[1], groundColor[2],
        500.0, -500.0, -0.9, groundColor[0], groundColor[1], groundColor[2],
        -500.0, -500.0, -0.9, groundColor[0], groundColor[1], groundColor[2],

        # Grass layer 
        -500.0, -200.0, -0.85, grassColor[0], grassColor[1], grassColor[2],
        500.0, -200.0, -0.85, grassColor[0], grassColor[1], grassColor[2],
        500.0, -150.0, -0.85, grassColor[0], grassColor[1], grassColor[2],
        -500.0, -150.0, -0.85, grassColor[0], grassColor[1], grassColor[2],
    ]

    indices = [
        # Sky
        0, 1, 2,  0, 3, 2,
        # Ground
        4, 5, 6,  4, 7, 6,
        # Grass layer
        8, 9, 10,  8, 11, 10,
    ]
    sun_verts1, sun_inds1 = CreateCircle([-300,300, 0.05], 70, [1.0, 0.6, 0.0], 20, len(vertices)/6)

    vertices += sun_verts1
    indices += sun_inds1

    sun_verts4, sun_inds4 = CreateCircle([240,300, 0.05], 70, [0.827, 0.827, 0.827], 20, len(vertices)/6)

    vertices += sun_verts4
    indices += sun_inds4

    sun_verts2, sun_inds2 = CreateCircle([340,315, 0.06], 50, [0.827, 0.827, 0.827], 20, len(vertices)/6)

    vertices += sun_verts2
    indices += sun_inds2

    sun_verts3, sun_inds3 = CreateCircle([310,265, 0.06], 60, [0.827, 0.827, 0.827], 20, len(vertices)/6)

    vertices += sun_verts3
    indices += sun_inds3

    sun_verts5, sun_inds5 = CreateCircle([400,305, 0.06], 60, [0.827, 0.827, 0.827], 20, len(vertices)/6)

    vertices += sun_verts5
    indices += sun_inds5


    return vertices, indices



def CreateAlien():
    vertices = []
    indices = []
    
    # Body
    body_verts, body_inds = CreateCircle([0.0, 0.0, 0.0], 1.0, [0, 1, 0], 20, 0)
    vertices.extend(body_verts)
    indices.extend(body_inds)
    
    # Eyes 
    eye_size = 0.2
    left_eye = [
        -0.4, 0.2, 0.1, 1.0, 1.0, 1.0,  # Top left
        -0.4 + eye_size, 0.2, 0.1, 1.0, 1.0, 1.0,  # Top right
        -0.4 + eye_size, 0.2 - eye_size, 0.1, 1.0, 1.0, 1.0,  # Bottom right
        -0.4, 0.2 - eye_size, 0.1, 1.0, 1.0, 1.0,  # Bottom left
    ]
    
    right_eye = [
        0.2, 0.2, 0.1, 1.0, 1.0, 1.0,  # Top left
        0.2 + eye_size, 0.2, 0.1, 1.0, 1.0, 1.0,  # Top right
        0.2 + eye_size, 0.2 - eye_size, 0.1, 1.0, 1.0, 1.0,  # Bottom right
        0.2, 0.2 - eye_size, 0.1, 1.0, 1.0, 1.0,  # Bottom left
    ]
    
    # Add eye vertices
    start_idx = len(vertices) // 6
    vertices.extend(left_eye)
    vertices.extend(right_eye)
    
    # Add eye indices
    indices.extend([
        start_idx, start_idx + 1, start_idx + 2,  # Left eye triangle 1
        start_idx, start_idx + 2, start_idx + 3,  # Left eye triangle 2
        start_idx + 4, start_idx + 5, start_idx + 6,  # Right eye triangle 1
        start_idx + 4, start_idx + 6, start_idx + 7,  # Right eye triangle 2
    ])
    
    return vertices, indices

def CreateRock():
    vertices = []
    indices = []
    

    rock_color = [0.5, 0.5, 0.5]  # Gray color
    rock_verts = [
        0.0, 1.0, 0.0, *rock_color,    # Top
        -0.8, 0.3, 0.0, *rock_color,   # Upper left
        -0.5, -1.0, 0.0, *rock_color,  # Bottom left
        0.5, -1.0, 0.0, *rock_color,   # Bottom right
        0.8, 0.3, 0.0, *rock_color,    # Upper right
    ]
    
    rock_indices = [
        0, 1, 4,  # Top triangle
        1, 2, 3,  # Bottom left triangle
        1, 3, 4,  # Bottom right triangle
    ]
    
    vertices.extend(rock_verts)
    indices.extend(rock_indices)
    
    return vertices, indices

def Createkey():
    vertices = []
    indices = []
    
  
    vertices = [
       
        -15, -15, 0.0, 1.0, 0.84, 0.0,
        15, -15, 0.0, 1.0, 0.84, 0.0,
        15, 15, 0.0, 1.0, 0.84, 0.0,
        -15, 15, 0.0, 1.0, 0.84, 0.0,
        -5, -15, 0.0, 1.0, 0.84, 0.0,
         5, -15, 0.0, 1.0, 0.84, 0.0,
        5, -55, 0.0, 1.0, 0.84, 0.0,
        -5, -55, 0.0, 1.0, 0.84, 0.0,
        

    ]
    indices = [0, 1, 2, 0, 2, 3,4,5,6,4,6,7]
    
    
    return vertices, indices


rockVerts, rockInds = CreateRock()
rockProps = {
    'vertices': np.array(rockVerts, dtype=np.float32),
    'indices': np.array(rockInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([40, 40, 1], dtype=np.float32),
}


alienVerts, alienInds = CreateAlien()
alienProps = {
    'vertices': np.array(alienVerts, dtype=np.float32),
    'indices': np.array(alienInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([30, 30, 1], dtype=np.float32),  
    'movement_speed': 200.0,
    'movement_direction': 1
}



playerVerts, playerInds = CreatePlayer()
playerProps = {
    'vertices' : np.array(playerVerts, dtype = np.float32),
    
    'indices' : np.array(playerInds, dtype = np.uint32),

    'position' : np.array([-450, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32)
}

backgroundVerts, backgroundInds = CreateBackground()
backgroundProps = {
    'vertices' : np.array(backgroundVerts, dtype = np.float32),
    
    'indices' : np.array(backgroundInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0]
}

backgroundVerts2, backgroundInds2 = CreateBackground2()
backgroundProps2 = {
    'vertices' : np.array(backgroundVerts2, dtype = np.float32),
    'indices' : np.array(backgroundInds2, dtype = np.uint32),
    'position' : np.array([0, 0, 0], dtype = np.float32),
    'rotation_z' : 0.0,
    'scale' : np.array([1, 1, 1], dtype = np.float32),
    'boundary' : [500.0, -500.0, 500.0, 500.0],
    'river_banks': [-400.0, 400.0]
}

backgroundVerts3, backgroundInds3 = CreateBackground3()
backgroundProps3 = {
    'vertices' : np.array(backgroundVerts3, dtype = np.float32),
    'indices' : np.array(backgroundInds3, dtype = np.uint32),
    'position' : np.array([0, 0, 0], dtype = np.float32),
    'rotation_z' : 0.0,
    'scale' : np.array([1, 1, 1], dtype = np.float32),
    'boundary' : [500.0, -500.0, 500.0, 500.0],
    'river_banks': [-400.0, 400.0]
}

backgroundVerts0, backgroundInds0 = CreateBackgroundmenu()
backgroundPropsmenu = {
    'vertices' : np.array(backgroundVerts0, dtype = np.float32),
    'indices' : np.array(backgroundInds0, dtype = np.uint32),
    'position' : np.array([0, 0, 0], dtype = np.float32),
    'rotation_z' : 0.0,
    'scale' : np.array([1, 1, 1], dtype = np.float32),
    'boundary' : [500.0, -500.0, 500.0, 500.0],
    'river_banks': [-400.0, 400.0]
}

keyVerts, keyInds = Createkey()
keyProps = {
    'vertices': np.array(keyVerts, dtype=np.float32),
    'indices': np.array(keyInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
}

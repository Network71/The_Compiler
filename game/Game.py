# from ursina import *

# app = Ursina()

# camera.orthographic = True
# camera.fov = 20

# score = 0

# score_text = Text(
#     text=f"Score: {score}",
#     position =(-0.7, 0.45),
#     scale = 2
# )

# player = Entity(
#     model='cube',
#     color=color.orange,
#     scale=(1, 1, 1),
#     position=(0, 1, 0),
#     collider='box'
# )
# # ground = Entity(
# #     model='cube',
# #     color=color.green,
# #     scale=(100, 1, 0),
# #     position=(0, -10, 0),
# #     collider='box'
# # )
# # #another block 
# # blockLeft = Entity(
# #     model='cube',
# #     color=color.black,
# #     scale=(10, 1, 0),
# #     position=(-10, -6.5, 0),
# #     collider='box'    
# # )
# # blockRight = Entity(
# #     model='cube',
# #     color=color.black,
# #     scale=(10, 1, 0),
# #     position=(10, -6.5, 0),
# #     collider='box'
# # )
# # middleBox = Entity(
# #     model='cube',
# #     color=color.black,
# #     scale=(10, 1, 0),
# #     position=(0, -3, 0),
# #     collider='box'
# # )
# # TopRightBox = Entity(
# #     model='cube',
# #     color=color.black,
# #     scale=(10, 1, 0),
# #     position=(-10, 1, 0),
# #     collider='box'
# # )

# # TopLeftBox = Entity(
# #     model='cube',
# #     color=color.black,
# #     scale=(10, 1, 0),
# #     position=(-10, 1, 0),
# #     collider='box'
# # )

# # TopRightBox = Entity(
# #     model='cube',
# #     color=color.black,
# #     scale=(10, 1, 0),
# #     position=(10, 1, 0),
# #     collider='box'
# # )

# # TopMiddleBox = Entity(
# #     model='cube',
# #     color=color.black,
# #     scale=(10, 1, 0),
# #     position=(0, 5, 0),
# #     collider='box'
# # )


# # collectibles = [Entity(
# #     model='cube',
# #     color=color.yellow,
# #     scale=(0.5, 0.5, 0),
# #     position=(2, 1, 0),
# #     collider='box'
# # ), 

# ground = Entity(model='cube', color=color.green, scale=(100, 1, 0), position=(0, -10, 0), collider='box')
# blockLeft = Entity(model='cube', color=color.black, scale=(10, 1, 0), position=(-10, -6.5, 0), collider='box')
# blockRight = Entity(model='cube', color=color.black, scale=(10, 1, 0), position=(10, -6.5, 0), collider='box')
# middleBox = Entity(model='cube', color=color.black, scale=(10, 1, 0), position=(0, -3, 0), collider='box')
# topLeftBox = Entity(model='cube', color=color.black, scale=(10, 1, 0), position=(-10, 1, 0), collider='box')
# topRightBox = Entity(model='cube', color=color.black, scale=(10, 1, 0), position=(10, 1, 0), collider='box')
# topMiddleBox = Entity(model='cube', color=color.black, scale=(10, 1, 0), position=(0, 5, 0), collider='box')

# platforms = [ground, blockLeft, blockRight, middleBox, topLeftBox, topRightBox, topMiddleBox]


# collectibles = [
#     Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 1), position=(2, 1, 0), collider='box'),
#     Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 1), position=(10, -5, 0), collider='box'),
#     Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 1), position=(-10, -5.5, 0), collider='box'),
#     Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 1), position=(-10, 5.5, 0), collider='box'),
#     Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 1), position=(0, 7, 0), collider='box'),
#     Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 1), position=(10, 5.5, 0), collider='box'),
# ]

# # Entity( # Middle
# #     model='cube',
# #     color=color.yellow, scale=(0.5, 0.5, 0),
# #     position=(10,-5,0),
# #     collider='box'
# # ),
# # Entity( # bottom left
# #     model='cube',
# #     color=color.yellow, scale=(0.5, 0.5, 0),
# #     position=(-10,-5.5,0),
# #     collider='box'
# # ),

# # Entity( # Bottom right 
# #     model='cube',
# #     color=color.yellow, scale=(0.5, 0.5, 0),
# #     position=(-10,5.5,0),
# #     collider='box'
# # ),
# # Entity( # Middle Top
# #     model='cube',
# #     color=color.yellow, scale=(0.5, 0.5, 0),
# #     position=(0,7,0),
# #     collider='box'
# # ),
# # Entity(
# #     model='cube',
# #     color=color.yellow, scale=(0.5, 0.5, 0),
# #     position=(10,5.5,0),
# #     collider='box'
# # )


# velocity_y = 0
# gravity = 30
# jump_force = 12
# speed = 5
# grounded = False

# def update():
#     global velocity_y, grounded, score

#     player.x += held_keys['d'] * time.dt * speed
#     player.x -= held_keys['a'] * time.dt * speed

#     velocity_y -= gravity * time.dt
#     player.y += velocity_y

#     grounded = False
#     for plat in platforms:
#         hit_info = player.intersects(plat)
#         if hit_info.hit:
#             if velocity_y <= 0:
#                 grounded = True
#                 player.y = plat.world_y + plat.scale_y / 2 + player.scale_y / 2
#                 velocity_y = 0
#                 grounded = True
#             else:
#                 player.y = plat.y - plat.scale_y / 2 - player.scale_y / 2

#     #collectible collision
#     for c in collectibles:
#         if c.enabled and player.intersects(c).hit:
#             c.disable()
#             score += 1
#             score_text.text = f"Score: {score}"

    
# print(player.position)
# def input(key):
#     global velocity_y
#     if key == 'space' and grounded:
#         velocity_y = jump_force

# app.run()


from ursina import *

app = Ursina()

camera.orthographic = True
camera.fov = 20

score = 0
game_over = False

game_over_text = Text(text="GAME OVER", origin=(0,0), scale=3, color=color.red, enabled=False)
quit_text =Text(text="Press Q to quit", origin=(0, -2), scale=1.5, color=color.white, enabled=False)

score_text = Text(
    text=f"Score: {score}",
    position=(-0.7, 0.45),
    scale=2
)

#Enemy Test
enemy_one = Entity(model="quad", color=color.red, scale=(1,1,1), position=(0, -9, 0), collider='box')
enemy_two = Entity(model="quad", color=color.red, scale=(1,1,1), position=(-10, -5.5, 0), collider='box')
enemy_three = Entity(model="quad", color=color.red, scale=(1,1,1), position=(0, 6, 0), collider='box')
enemy_four = Entity(model="quad", color=color.red, scale=(1,1,1), position=(10, 2, 0), collider='box')

enemies = [enemy_one, enemy_two, enemy_three, enemy_four]       
        
for enemy in enemies:
    enemy.start_x = enemy.x
    enemy.range = 3
    enemy.direction = 1
    enemy.speed = 2

enemy_three.direction = -1
enemy_four.directtion = -1


# PLAYER
player = Entity(
    model='cube',
    color=color.orange,
    scale=(1, 1, 1),
    position=(0, 2, 0),
    collider='box'
)

# PLATFORMS (FIXED SCALE Z = 1)
ground = Entity(model='cube', color=color.green, scale=(100, 1, 1), position=(0, -10, 0), collider='box')
blockLeft = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(-10, -6.5, 0), collider='box')
blockRight = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(10, -6.5, 0), collider='box')
middleBox = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(0, -3, 0), collider='box')
topLeftBox = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(-10, 1, 0), collider='box')
topRightBox = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(10, 1, 0), collider='box')
topMiddleBox = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(0, 5, 0), collider='box')

platforms = [ground, blockLeft, blockRight, middleBox, topLeftBox, topRightBox, topMiddleBox]

# COLLECTIBLES (FIXED SCALE Z)
collectibles = [
    Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 0.5), position=(2, 1, 0), collider='box'),
    Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 0.5), position=(10, -5, 0), collider='box'),
    Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 0.5), position=(-10, -5.5, 0), collider='box'),
    Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 0.5), position=(-10, 5.5, 0), collider='box'),
    Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 0.5), position=(0, 7, 0), collider='box'),
    Entity(model='cube', color=color.yellow, scale=(0.5, 0.5, 0.5), position=(10, 5.5, 0), collider='box'),
]

# PHYSICS
velocity_y = 0
gravity = 1
jump_force = 0.40
speed = 5
grounded = False

def enemy_movement(enemy):    
    enemy.x += enemy.direction * enemy.speed * time.dt
    if enemy.x > enemy.start_x + enemy.range:
        enemy.direction = -1
    if enemy.x < enemy.start_x - enemy.range:
        enemy.direction = 1


def update():
    global velocity_y, grounded, score, game_over, enemy_direction

    if not game_over:
        for enemy in enemies:
            enemy_movement(enemy)

    if game_over:
        return

    # movement
    player.x += (held_keys['d'] - held_keys['a']) * time.dt * speed

    # gravity
    velocity_y -= gravity * time.dt
    player.y += velocity_y

    grounded = False

    # COLLISION (FIXED)
    for plat in platforms:
        hit = player.intersects(plat)

        if hit.hit:
            # only land if falling
            if velocity_y <= 0:
                grounded = True
                player.y = plat.y + plat.scale_y / 2 + player.scale_y / 2
                velocity_y = 0
                break  # IMPORTANT: stop after first valid platform


    # collectibles
    for c in collectibles:
        if c.enabled and player.intersects(c).hit:
            c.disable()
            score += 1
            score_text.text = f"Score: {score}"


    # safety reset (prevents “lost player”)
    if player.y < -50:
        player.position = (0, 5, 0)
        velocity_y = 0

    #Enemy collision 
    for enemy in enemies:
        if player.intersects(enemy).hit:
            game_over = True
            score_text.text = "GAME OVER"
            player.color = color.gray
            game_over_text.enabled = True
            quit_text.enabled = True

def input(key):
    global velocity_y

    if game_over:
        if key == 'q':
            application.quit()

    if key == 'w' and grounded:
        velocity_y = jump_force


app.run()
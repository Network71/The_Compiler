from ursina import *
import sys
import subprocess
#Add coin sprite as texture to collectables

app = Ursina()

camera.orthographic = True
camera.fov = 20

score = 0
game_over = False

game_over_text = Text(text="GAME OVER", origin=(0,0), scale=3, color=color.red, font="ARCADECLASSIC.TTF", enabled=False)
quit_text =Text(text="Press Q to quit", origin=(0, -2), scale=1.5, color=color.white, font="ARCADECLASSIC.TTF", enabled=False)

#background image
background = Entity(
    model="quad",
    texture="Background2.png",
    scale=(35,25),
    z=1
)


score_text = Text(
    text=f"Score  { score}",
    position=(-0.7, 0.45),
    scale=2,
    font="ARCADECLASSIC.TTF"
)

win_text = Text(
    text=f"", #runs at the beginning of the program
    origin=(0,0), 
    scale=3,
    color=color.green,
    enabled = False,
    font="ARCADECLASSIC.TTF"
)

#Enemies
#position=(-12, 1, 0)
enemy_one = Entity(model="quad", texture="Enemy.png", scale=(2.5,2.5,2.5), position=(3, -5.3, 0), collider='box')
enemy_two = Entity(model="quad", texture="Enemy.png", scale=(2.5,2.5,2.5), position=(0, 0.3, 0), collider='box')
enemy_three = Entity(model="quad", texture="Enemy.png", scale=(2.5,2.5,2.5), position=(0, 6.3, 0), collider='box')
enemy_four = Entity(model="quad", texture="Enemy.png", scale=(2.5,2.5,2.5), position=(-12, 2.2, 0), collider='box')

enemies = [enemy_three, enemy_one, enemy_two, enemy_four]
        
for enemy in enemies:
    enemy.start_x = enemy.x
    enemy.range = 3
    enemy.direction = 1
    enemy.speed = 2

enemy_three.direction = -1
# enemy_four.direction = -1


for enemy in enemies:
    enemy.collider = BoxCollider(enemy, size=(0.5, 0.8, 1))

player = Entity(
    position=(-15, -9.2, 0),
    collider='box'
)

player.collider = BoxCollider(player, size=(1, 1.6, 1))


# VISUAL (this is what you SEE)
player_visual = Entity(
    parent=player,
    model='quad',
    texture="ByteRider2.png",
    scale=(2.7, 2.7, 2.7),
    y=0.1   
)


#adjusted hit box
# player.collider.scale = (0.8,0.9, 1)

# PLATFORMS (FIXED SCALE Z = 1)
startingblockLeft = Entity(model='quad', color=color.black, scale=(7, 1, 1), position=(-14, -9.3, 0), collider='box')
longMiddleBlock = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(3, -6.5, 0), collider='box')
bottommiddleBox = Entity(model='cube', color=color.black, scale=(3, 1, 1), position=(-4.7, -8.4, 0), collider='box')
topleftcorner = Entity(model='quad', color=color.black, scale=(7, 1, 1), position=(-12, 1, 0), collider='box')
centermiddlebox = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(0, -1, 0), collider='box')
middlerightbox = Entity(model='cube', color=color.black, scale=(4, 1, 1), position=(11, -3, 0), collider='box')
topMiddleBox = Entity(model='cube', color=color.black, scale=(10, 1, 1), position=(0, 5, 0), collider='box')

platforms = [startingblockLeft, longMiddleBlock, bottommiddleBox, centermiddlebox, middlerightbox, topMiddleBox, topleftcorner] 

# COLLECTIBLES (FIXED SCALE Z)
collectibles = [
    Entity(model='cube', texture="Collectable.png", scale=(1.5, 1.5, 1), position=(3, -5, 0), collider='box'),
    Entity(model='cube', texture="Collectable.png", scale=(1.5, 1.5, 1), position=(-12, -7, 0), collider='box'),
    Entity(model='cube', texture="Collectable.png", scale=(1.5, 1.5, 1), position=(11, -1, 0), collider='box'),
    Entity(model='cube', texture="Collectable.png", scale=(1.5, 1.5, 1), position=(-3.5, 1, 0), collider='box'),
    Entity(model='cube', texture="Collectable.png", scale=(1.5, 1.5, 1), position=(0.5, 1, 0), collider='box'),
    Entity(model='cube', texture="Collectable.png", scale=(1.5, 1.5, 1), position=(4.5, 1, 0), collider='box'),
    Entity(model='cube', texture="Collectable.png", scale=(1.5, 1.5, 1), position=(-12, 2.5, 0), collider='box'),
    Entity(model='cube', texture="Collectable.png", scale=(1.5, 1.5, 1), position=(0, 6.5, 0), collider='box')
]

# PHYSICS
velocity_y = 0
gravity = 1
jump_force = 0.38
speed = 5
grounded = False


#Testing HitBox 
# enemy.collider.visible = True
# player.collider.visible = True

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
    if held_keys['a']:
        player_visual.texture = "ByteRiderL.png"
    else:
        player_visual.texture = "ByteRider2.png"
    # move = held_keys['d'] - held_keys['a']
    # player.x += move + time.dt * speed

    # if move > 0:
    #     player_visual.scale_x = abs(player.scale_x)
    # elif move < 0:
    #     player_visual.scale_x = -abs(player_visual.scale_x)

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
                player.y = plat.y + plat.scale_y / 2 + player.collider.size[1] / 2
                velocity_y = 0
                break  # IMPORTANT: stop after first valid platform


    # collectibles
    for c in collectibles:
        if c.enabled and player.intersects(c).hit:
            c.disable()
            score += 1
            score_text.text = f"Score { score}"

    #win condition 
    if score >= 8:
        game_over = True
        score_text.text = "YOU WIN"
        win_text.text = f"YOU WIN   Score { score}"
        win_text.enabled = True
        quit_text.enabled = True
        player.color=color.green

        print("opening second level")
        subprocess.Popen([sys.executable, r"C:\Users\aidan\OneDrive\Documents\UNI WORK\Bartek Git\The_Compiler\debugging_code_2.py"])
        print("passed Popen")
        application.quit()



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
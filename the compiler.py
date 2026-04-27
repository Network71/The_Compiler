#the compiler!
print("Welcome to the compiler")

from ursina import *
import random

app = Ursina()

# --- Player ---
player = Entity(
    model='cube',
    color=color.azure,
    scale=(1,2,1),
    position=(0,1,0),
    collider='box'
)

player.speed = 5
player.jump_height = 6
player.gravity = 1
player.velocity_y = 0
player.grounded = False

# --- Ground ---
ground = Entity(
    model='cube',
    scale=(20,1,10),
    position=(0,0,0),
    color=color.gray,
    collider='box'
)

# --- Platform ---
platform = Entity(
    model='cube',
    scale=(5,1,5),
    position=(5,3,0),
    color=color.dark_gray,
    collider='box'
)

# --- Collectible (Data Bit) ---
bit = Entity(
    model='sphere',
    color=color.yellow,
    position=(5,5,0),
    scale=0.5,
    collider='box'
)

score = 0

# --- Enemy (simple guard) ---
enemy = Entity(
    model='cube',
    color=color.red,
    position=(8,1,0),
    scale=(1,2,1),
    collider='box'
)

enemy.direction = 1

# --- UI ---
score_text = Text(text='Bits: 0', position=(-0.85, 0.45), scale=2)

# --- Update loop ---
def update():
    global score

    # --- Movement ---
    if held_keys['a']:
        player.x -= player.speed * time.dt
    if held_keys['d']:
        player.x += player.speed * time.dt

    # --- Gravity ---
    player.y -= player.velocity_y * time.dt
    player.velocity_y += player.gravity * time.dt

    # --- Ground check ---
    hit_info = raycast(player.world_position, Vec3(0,-1,0), distance=1.1, ignore=(player,))
    if hit_info.hit:
        player.grounded = True
        player.velocity_y = 0
        player.y = hit_info.world_point.y + 1
    else:
        player.grounded = False

    # --- Jump ---
    if held_keys['space'] and player.grounded:
        player.velocity_y = -player.jump_height

    # --- Collect bit ---
    if player.intersects(bit).hit:
        score += 1
        score_text.text = f'Bits: {score}'
        bit.position = (random.randint(-5,5), 5, 0)

    # --- Enemy patrol ---
    enemy.x += enemy.direction * 2 * time.dt
    if enemy.x > 10 or enemy.x < 5:
        enemy.direction *= -1

    # --- Stealth detection ---
    if distance(player.position, enemy.position) < 2:
        print("DETECTED! Mission failed")
        application.quit()

app.run()
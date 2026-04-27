"""
CYBER_BREACH - A Cybersecurity Platformer built with Ursina Engine
=================================================================
Install dependencies:
    pip install ursina
 
Run:
    python cyber_breach.py
 
Controls:
    A / D       - Move left / right
    Space       - Jump
    E           - Launch attack (when fully charged)
    R           - Restart (after game over / win)
    Escape      - Quit
"""
 
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import sys
 
app = Ursina()
 
# ── Colour palette ────────────────────────────────────────────────────────────
COL_BG          = color.rgb(10,  10,  26)
COL_PLATFORM    = color.rgb(20,  40,  80)
COL_PLATFORM_LT = color.rgb(26,  58, 100)
COL_PLAYER      = color.rgb(0,  136, 255)
COL_PLAYER_GLOW = color.rgb(0,  200, 255)
COL_BIT         = color.rgb(0,  255, 170)
COL_ENEMY       = color.rgb(220,  30,  60)
COL_ENEMY_EYE   = color.rgb(255, 100, 120)
COL_TEXT        = color.rgb(0,  255, 170)
COL_WARN        = color.rgb(255,  60,  80)
COL_GOLD        = color.rgb(255, 200,  50)
 
# ── Window & camera setup ─────────────────────────────────────────────────────
window.title        = '// CYBER_BREACH v1.0'
window.borderless   = False
window.fullscreen   = False
window.size         = (1024, 640)
window.color        = COL_BG
 
camera.orthographic = True
camera.fov          = 14          # world units visible vertically
camera.position     = (0, 4, -50)
 
# ── Global state ──────────────────────────────────────────────────────────────
GRAVITY        = -28
JUMP_FORCE     = 11
MOVE_SPEED     = 7
MAX_HP         = 3
INVINCIBLE_DUR = 1.5   # seconds of invincibility after hit
 
game_state     = 'menu'   # 'menu' | 'playing' | 'dead' | 'win'
 
# ── Entity containers (cleared on restart) ────────────────────────────────────
platforms = []
bit_entities = []
enemy_entities = []
particle_pool = []
ui_elements = []
 
player_ent       = None
vy               = 0
on_ground        = False
hp               = MAX_HP
bits_collected   = 0
invincible_timer = 0
flash_timer      = 0
 
# ══════════════════════════════════════════════════════════════════════════════
# Level definition  (x, y, width, height)  — all in world units
# ══════════════════════════════════════════════════════════════════════════════
LEVEL = {
    'platforms': [
        # Ground
        ( 0,  0,  28, 0.6),
        # Mid platforms
        (-9,  2.5, 4, 0.4),
        (-2,  4,   4, 0.4),
        ( 5,  2.5, 4, 0.4),
        # Upper platforms
        (-8,  5.5, 3, 0.4),
        ( 0,  6.5, 4, 0.4),
        ( 7,  5.5, 3, 0.4),
        # High platforms
        (-5,  8.5, 3, 0.4),
        ( 4,  8.5, 3, 0.4),
        # Top
        (-1, 10.5, 5, 0.4),
    ],
 
    # (x, y)  — centre of each data bit
    'bits': [
        (-9,  3.4),
        (-2,  4.9),
        ( 5,  3.4),
        (-8,  6.4),
        ( 0,  7.4),
        ( 7,  6.4),
        (-5,  9.4),
        ( 4,  9.4),
        (-1, 11.4),
        ( 2,  1.0),   # bonus on ground level
    ],
 
    # (x, y, patrol_min_x, patrol_max_x)
    'enemies': [
        (-7,  0.7, -13,  -2),
        ( 6,  0.7,   2,  12),
        (-2,  4.7,  -5,   1),
        ( 0,  7.2,  -2,   3),
        (-5,  9.2,  -7,  -3),
    ],
}
 
# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════
 
def clear_scene():
    for lst in (platforms, bit_entities, enemy_entities, particle_pool, ui_elements):
        for e in lst:
            destroy(e)
        lst.clear()
 
def make_text(txt, pos, scale=1, col=None, parent=camera.ui):
    t = Text(txt, position=pos, scale=scale,
             color=col or COL_TEXT, font='VeraMono.ttf',
             origin=(-.5, .5), parent=parent)
    ui_elements.append(t)
    return t
 
# ══════════════════════════════════════════════════════════════════════════════
# Platform class
# ══════════════════════════════════════════════════════════════════════════════
 
class Platform(Entity):
    def __init__(self, x, y, w, h):
        super().__init__(
            model='cube',
            color=COL_PLATFORM,
            position=(x, y, 0),
            scale=(w, h, 1),
            collider=None,   # manual collision
        )
        # Top-edge glow strip
        self.glow = Entity(
            model='cube',
            color=color.rgb(0, 200, 120),
            position=(x, y + h/2 + 0.04, 0),
            scale=(w, 0.08, 0.5),
            parent=scene,
        )
        platforms.append(self)
 
    def cleanup(self):
        destroy(self.glow)
        destroy(self)
 
# ══════════════════════════════════════════════════════════════════════════════
# Data Bit (collectible)
# ══════════════════════════════════════════════════════════════════════════════
 
class DataBit(Entity):
    def __init__(self, x, y):
        super().__init__(
            model='cube',
            color=COL_BIT,
            position=(x, y, 0),
            scale=(0.4, 0.4, 0.4),
        )
        self.collected = False
        self._t = random.uniform(0, 6.28)
        self.origin_y = y
        self.label = Text(
            'BIT',
            position=self.world_position + Vec3(0, 0.35, 0),
            scale=50,
            color=COL_BIT,
            origin=(0, 0),
            parent=scene,
            billboard=True,
        )
        bit_entities.append(self)
 
    def update(self):
        if self.collected:
            return
        self._t += time.dt * 3
        self.y = self.origin_y + math.sin(self._t) * 0.15
        self.label.world_position = self.world_position + Vec3(0, 0.4, 0)
        self.rotation_y += 80 * time.dt
 
    def collect(self):
        self.collected = True
        spawn_particles(self.world_position, COL_BIT, 12)
        self.label.enabled = False
        self.enabled = False
 
# ══════════════════════════════════════════════════════════════════════════════
# Security Drone (enemy)
# ══════════════════════════════════════════════════════════════════════════════
 
class Drone(Entity):
    def __init__(self, x, y, pmin, pmax):
        super().__init__(
            model='cube',
            color=COL_ENEMY,
            position=(x, y, 0),
            scale=(0.7, 0.5, 0.5),
        )
        self.pmin   = pmin
        self.pmax   = pmax
        self.speed  = random.uniform(2.5, 4.0)
        self.dir    = 1
        # Eyes
        self.eye_l = Entity(model='sphere', color=COL_ENEMY_EYE,
                            scale=0.18, position=(-0.15, 0.08, -0.28), parent=self)
        self.eye_r = Entity(model='sphere', color=COL_ENEMY_EYE,
                            scale=0.18, position=( 0.15, 0.08, -0.28), parent=self)
        self._t = 0
        self.origin_y = y
        enemy_entities.append(self)
 
    def update(self):
        self._t += time.dt * 4
        self.y = self.origin_y + math.sin(self._t) * 0.2   # hover bob
        self.x += self.speed * self.dir * time.dt
        if self.x > self.pmax:
            self.x = self.pmax; self.dir = -1
        if self.x < self.pmin:
            self.x = self.pmin; self.dir = 1
        self.scale_x = abs(self.scale_x) * self.dir   # flip sprite
 
# ══════════════════════════════════════════════════════════════════════════════
# Particles
# ══════════════════════════════════════════════════════════════════════════════
 
class Particle(Entity):
    def __init__(self, pos, col):
        super().__init__(
            model='sphere',
            color=col,
            position=pos,
            scale=random.uniform(0.06, 0.16),
        )
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(1, 5)
        self.life = random.uniform(0.4, 0.8)
        particle_pool.append(self)
 
    def update(self):
        self.x += self.vx * time.dt
        self.y += self.vy * time.dt
        self.vy -= 12 * time.dt
        self.life -= time.dt
        self.color = Color(self.color.r, self.color.g, self.color.b,
                           max(0, self.life))
        if self.life <= 0:
            particle_pool.remove(self)
            destroy(self)
 
 
def spawn_particles(pos, col, n=8):
    for _ in range(n):
        Particle(pos, col)
 
# ══════════════════════════════════════════════════════════════════════════════
# HUD
# ══════════════════════════════════════════════════════════════════════════════
 
hud_bits   = None
hud_charge = None
hud_hp     = None
hud_status = None
hud_msg    = None
overlay    = None   # full-screen menu/win/dead overlay
 
def build_hud():
    global hud_bits, hud_charge, hud_hp, hud_status, hud_msg
    hud_bits   = Text('', position=(-0.85,  0.48), scale=1.1, color=COL_TEXT,
                      font='VeraMono.ttf', parent=camera.ui)
    hud_charge = Text('', position=(-0.85,  0.43), scale=1.1, color=COL_TEXT,
                      font='VeraMono.ttf', parent=camera.ui)
    hud_hp     = Text('', position=(-0.85,  0.38), scale=1.1, color=COL_WARN,
                      font='VeraMono.ttf', parent=camera.ui)
    hud_status = Text('', position=( 0.35,  0.48), scale=1.1, color=COL_WARN,
                      font='VeraMono.ttf', parent=camera.ui)
    hud_msg    = Text('', position=(-0.85, -0.46), scale=1.0, color=color.cyan,
                      font='VeraMono.ttf', parent=camera.ui)
 
def update_hud():
    if hud_bits is None:
        return
    total   = len(LEVEL['bits'])
    charged = bits_collected >= total
    hud_bits.text   = f'BITS: {bits_collected}/{total}'
    hud_charge.text = f'CHARGE: {int(bits_collected/total*100)}%'
    hud_hp.text     = f'HP: {"■" * hp}{"□" * (MAX_HP - hp)}'
    if charged:
        hud_status.text  = '[ ATTACK READY — press E ]'
        hud_status.color = COL_BIT
    else:
        hud_status.text  = '[ ATTACK OFFLINE ]'
        hud_status.color = COL_WARN
 
def set_msg(txt, col=None):
    if hud_msg:
        hud_msg.text  = f'>> {txt}'
        hud_msg.color = col or color.cyan
 
def destroy_hud():
    for widget in (hud_bits, hud_charge, hud_hp, hud_status, hud_msg):
        if widget:
            destroy(widget)
 
# ══════════════════════════════════════════════════════════════════════════════
# Overlay screens
# ══════════════════════════════════════════════════════════════════════════════
 
def show_overlay(title, subtitle, hint, title_col=None):
    global overlay
    if overlay:
        destroy(overlay)
    overlay = Entity(parent=camera.ui, model='quad',
                     color=color.rgba(5, 5, 20, 220),
                     scale=(2, 1), z=-1)
    Text(title,    parent=overlay, y= 0.25, scale=3.5,
         color=title_col or COL_BIT, origin=(0,0), font='VeraMono.ttf')
    Text(subtitle, parent=overlay, y= 0.05, scale=1.2,
         color=color.rgb(100, 180, 255), origin=(0,0), font='VeraMono.ttf')
    Text(hint,     parent=overlay, y=-0.12, scale=1.0,
         color=color.rgb(80, 120, 160), origin=(0,0), font='VeraMono.ttf')
 
def hide_overlay():
    global overlay
    if overlay:
        destroy(overlay)
        overlay = None
 
# ══════════════════════════════════════════════════════════════════════════════
# Game lifecycle
# ══════════════════════════════════════════════════════════════════════════════
 
def start_game():
    global player_ent, vy, on_ground, hp, bits_collected
    global invincible_timer, flash_timer, game_state
 
    clear_scene()
    destroy_hud()
    hide_overlay()
 
    # Build level
    for (x, y, w, h) in LEVEL['platforms']:
        Platform(x, y, w, h)
 
    for (bx, by) in LEVEL['bits']:
        DataBit(bx, by)
 
    for (ex, ey, pmn, pmx) in LEVEL['enemies']:
        Drone(ex, ey, pmn, pmx)
 
    # Background grid lines (decorative)
    for i in range(-14, 15, 2):
        e = Entity(model='cube', color=color.rgba(0, 60, 120, 30),
                   scale=(0.02, 14, 0.1), position=(i, 5, 1))
        platforms.append(e)   # reuse list for cleanup
 
    # Player
    player_ent = Entity(
        model='cube',
        color=COL_PLAYER,
        position=(-12, 1.2, 0),
        scale=(0.55, 0.8, 0.5),
    )
 
    vy               = 0
    on_ground        = False
    hp               = MAX_HP
    bits_collected   = 0
    invincible_timer = 0
    flash_timer      = 0
    game_state       = 'playing'
 
    build_hud()
    update_hud()
    set_msg('Collect all DATA BITS to charge the attack...')
 
    camera.position = Vec3(player_ent.x, player_ent.y + 2, -50)
 
 
def trigger_death():
    global game_state
    game_state = 'dead'
    spawn_particles(player_ent.world_position, COL_WARN, 20)
    player_ent.enabled = False
    show_overlay(
        '// CONNECTION LOST',
        'Security system detected the intrusion.',
        'Press  R  to retry',
        title_col=COL_WARN,
    )
 
 
def trigger_win():
    global game_state
    game_state = 'win'
    spawn_particles(player_ent.world_position, COL_BIT, 30)
    spawn_particles(player_ent.world_position + Vec3(1,0,0), COL_GOLD, 20)
    show_overlay(
        '// ATTACK LAUNCHED',
        f'System compromised. All {len(LEVEL["bits"])} bits collected.',
        'Press  R  for next breach',
    )
 
 
# ══════════════════════════════════════════════════════════════════════════════
# AABB collision helpers
# ══════════════════════════════════════════════════════════════════════════════
 
def player_aabb():
    hw = player_ent.scale_x / 2
    hh = player_ent.scale_y / 2
    return (player_ent.x - hw, player_ent.y - hh,
            player_ent.x + hw, player_ent.y + hh)
 
def platform_aabb(p):
    hw = p.scale_x / 2
    hh = p.scale_y / 2
    return (p.x - hw, p.y - hh, p.x + hw, p.y + hh)
 
def overlaps(ax1,ay1,ax2,ay2, bx1,by1,bx2,by2):
    return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1
 
 
# ══════════════════════════════════════════════════════════════════════════════
# Main update loop
# ══════════════════════════════════════════════════════════════════════════════
 
def update():
    global vy, on_ground, hp, bits_collected
    global invincible_timer, flash_timer, game_state
 
    if game_state == 'menu':
        return
 
    if game_state in ('dead', 'win'):
        if held_keys['r']:
            start_game()
        return
 
    # ── Input ────────────────────────────────────────────────────────────────
    dx = 0
    if held_keys['a'] or held_keys['left arrow']:  dx = -1
    if held_keys['d'] or held_keys['right arrow']: dx =  1
 
    player_ent.x += dx * MOVE_SPEED * time.dt
 
    if (held_keys['space'] or held_keys['up arrow']) and on_ground:
        vy        = JUMP_FORCE
        on_ground = False
 
    # ── Launch attack ────────────────────────────────────────────────────────
    if held_keys['e'] and bits_collected >= len(LEVEL['bits']):
        trigger_win()
        return
 
    # ── Gravity ──────────────────────────────────────────────────────────────
    vy += GRAVITY * time.dt
    player_ent.y += vy * time.dt
 
    # ── Platform collision ───────────────────────────────────────────────────
    on_ground = False
    px1,py1,px2,py2 = player_aabb()
 
    for plat in platforms:
        if not hasattr(plat, 'scale_x'):
            continue   # decorative entities without proper scale
        try:
            tx1,ty1,tx2,ty2 = platform_aabb(plat)
        except Exception:
            continue
 
        if px1 < tx2 and px2 > tx1:
            # Landing on top
            if py1 < ty2 and py2 > ty1 and vy <= 0:
                # check player was above last frame
                if player_ent.y - player_ent.scale_y/2 >= ty1 - 0.15:
                    player_ent.y = ty2 + player_ent.scale_y / 2
                    vy           = 0
                    on_ground    = True
 
    # Clamp below floor
    if player_ent.y < -3:
        hp = 0
        trigger_death()
        return
 
    # ── Bit collection ───────────────────────────────────────────────────────
    for bit in bit_entities:
        if bit.collected:
            continue
        dist = (Vec2(player_ent.x, player_ent.y) -
                Vec2(bit.x, bit.y)).length()
        if dist < 0.55:
            bit.collect()
            bits_collected += 1
            update_hud()
            total = len(LEVEL['bits'])
            if bits_collected == total:
                set_msg('FULL CHARGE! Press E to launch the attack!', COL_BIT)
            else:
                set_msg(f'BIT acquired [{bits_collected}/{total}] — keep going!')
 
    # ── Enemy collision ──────────────────────────────────────────────────────
    if invincible_timer > 0:
        invincible_timer -= time.dt
        # Flash player
        flash_timer += time.dt
        player_ent.enabled = (int(flash_timer * 10) % 2 == 0)
    else:
        player_ent.enabled = True
        for drone in enemy_entities:
            dist = (Vec2(player_ent.x, player_ent.y) -
                    Vec2(drone.x, drone.y)).length()
            if dist < 0.65:
                hp -= 1
                invincible_timer = INVINCIBLE_DUR
                flash_timer      = 0
                spawn_particles(player_ent.world_position, COL_WARN, 10)
                update_hud()
                set_msg('SECURITY ALERT! Hull breach detected!', COL_WARN)
                if hp <= 0:
                    trigger_death()
                    return
                break
 
    # ── Camera follow ────────────────────────────────────────────────────────
    cam_target = Vec3(player_ent.x, player_ent.y + 2, -50)
    camera.position = lerp(camera.position, cam_target, time.dt * 5)
    # Clamp camera X so we don't go off-level
    camera.x = clamp(camera.x, -8, 8)
    camera.y = clamp(camera.y, 3,  12)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# Input events
# ══════════════════════════════════════════════════════════════════════════════
 
def input(key):
    if key == 'escape':
        application.quit()
    if key == 'r' and game_state in ('dead', 'win'):
        start_game()
 
 
# ══════════════════════════════════════════════════════════════════════════════
# Entry point — show menu, then let player press Enter
# ══════════════════════════════════════════════════════════════════════════════
 
game_state = 'menu'
show_overlay(
    '// CYBER_BREACH v1.0',
    'Collect DATA BITS to charge the system attack.\nAvoid security drones. Reach full charge, then press E.',
    'Press  ENTER  to begin',
)
 
def input(key):
    global game_state
    if key == 'escape':
        application.quit()
    if key == 'enter' and game_state == 'menu':
        start_game()
    if key == 'r' and game_state in ('dead', 'win'):
        start_game()
 
 
app.run()
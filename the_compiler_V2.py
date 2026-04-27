from ursina import * # This imports Entity, color, and other core tools
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

app = Ursina()

player = PlatformerController2d(y=1, z=.01, scale_y=1, max_jumps=2)

# Now 'Entity' and 'color' will be recognized
ground = Entity(model='quad', scale_x=10, collider='box', color=color.black)

app.run()



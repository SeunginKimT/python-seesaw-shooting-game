# python-seesaw-shooting-game
A simple two stage object-oriented Python shooting game with seesaw physics and shooting mechanics.

## Gameplay Overview
### **Level 1**
- Control a character using the **left** and **right** arrow keys.
- Use the **seesaw** to launch the second character into the air.
- The goal is the **land on the seesaw**.
- If the character **misses the seesaw**, or **land on the right side of the seesaw**, it's **Game Over**.

### **Level 2**
- **Clouds** and **raindrops** fall from the top, and **moles** pop up from the bottom.
- Avoid **raindrops** -each hit decreases your **life (starts at 10)**.
- Press **Space bar** to **shoot bullets**.
- Hitting **clouds** with bullets removes them.
- **Moles and Clouds** don't cause damage but must be dodged.
- The game continues until your **life reaches 0**.

## Controls
- **Arrow keys**: Move character left and right
- **Space bar**: Shoot bullets
- **Seesaw physics**: Automatically triggered

## Features
- **Two-level gameplay** with simple mechanics and challenges  
- **Seesaw physics**: One character launches the other into the air  
- **Collision logic**: Land back on the seesaw to stay alive  
- **Falling obstacles**: Clouds, raindrops, and moles increase difficulty in Level 2  
- **Life system**: 10 lives total; raindrop collisions reduce life  
- **Shooting mechanic**: Use space bar to shoot and eliminate clouds  
- **Continuous gameplay**: Game runs until all lives are lost  
- **Keyboard controls** for movement and actions (← → and Space bar)

## Tech Stack
- **Language**: Python 3.11.9
- **Library**: Pygame
- **IDE**: PyCharm

## Author
- Created by Seungin Kim T  
GitHub: [SeunginKimT](https://github.com/SeunginKimT)

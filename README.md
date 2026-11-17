# ren.py - A Game Framework

A modular Python game framework with Three.js web integration for browser-based games.

## Features

- **Modular Architecture**: Separate modules for player, enemies, and terrain management
- **Procedural Terrain**: Algorithmically generated terrain layers with tile effects
- **Enemy AI**: Simple chase behavior with multiple enemy types (Slime, Brute, Sprinter)
- **Three.js Integration**: WebGL rendering for smooth browser gameplay
- **Wave System**: Progressive difficulty scaling

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ren-game
```

2. Install requirements (if any):
```bash
pip install -r requirements.txt
```

3. Run the game server:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:8000`

## Project Structure

```
ren-game/
├── game.py              # Main game engine and loop
├── modules/
│   ├── player.py        # Player stats, movement, and XP system
│   ├── enemies.py       # Enemy types, factory, and AI
│   └── terrain.py       # Procedural terrain generation
├── public/
│   └── index.html       # Three.js web interface
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Controls

| Key | Action |
|-----|--------|
| W / ↑ | Move Up |
| S / ↓ | Move Down |
| A / ← | Move Left |
| D / → | Move Right |
| Click | Attack |

## Game Mechanics

### Player
- Start with 100 HP and level 1 stats
- Gain XP from defeating enemies
- Level up to increase max health and damage

### Enemies
- **Slime**: Balanced health, speed, and damage (Green)
- **Brute**: High health, slow, moderate damage (Brown)
- **Sprinter**: Low health, fast, low damage (Orange)

### Terrain
- **Grass**: Normal movement speed
- **Water**: Slower movement (0.5x)
- **Lava**: Faster but damages enemies
- **Crystal**: Slight damage over time

### Fog System
- Fog creeps up from the bottom over time
- Reaching fog levels below 50 results in death
- Visual feedback shows current height percentage

## Extending the Game

### Adding New Enemy Types

Edit `modules/enemies.py` and add to `EnemyFactory.ENEMY_TYPES`:

```python
"new_enemy": {
    "health_base": 10,
    "speed_base": 1.0,
    "damage_base": 5,
    "color": "#FF0000",
    "xp_base": 15
}
```

### Adding New Terrain Types

Edit `modules/terrain.py` and add to `TerrainConfig.TILE_TYPES`:

```python
"new_terrain": {
    "color": "#XXXXXX",
    "speed_mod": 1.0,
    "damage": 0
}
```

## Development Notes

This is a foundational project for building animated visual novels and coloring book content. The current implementation provides:

- Core game loop architecture
- Modular component design
- Three.js rendering integration path
- Procedural generation framework

Future iterations will add:
- Story-driven narrative elements
- Coloring mode for artistic exploration
- More complex enemy behaviors
- Terrain customization options

## License

MIT License - Feel free to use and modify.

---

**Built with ❤️ using Python + Three.js**

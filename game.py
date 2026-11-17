"""Main game engine for ren.py."""

import asyncio
from typing import Dict

from modules.player import Player, PlayerInput
from modules.enemies import EnemyFactory, EnemyAI, Enemy
from modules.terrain import TerrainManager, ProceduralTerrain, TerrainLayer


class GameEngine:
    """Main game loop and state management."""
    
    def __init__(self):
        self.player = Player()
        self.enemies: Dict[str, Enemy] = {}
        self.enemy_id_counter = 0
        self.terrain = TerrainManager(initial_height=200)
        self.input = PlayerInput()
        self.is_running = False
        self.score = 0
        self.wave = 1
        
    def spawn_enemy(self) -> None:
        """Spawn a new enemy."""
        enemy = EnemyFactory.spawn_random(wave_multiplier=self.wave * 0.5)
        enemy_id = f"enemy_{self.enemy_id_counter}"
        self.enemies[enemy_id] = enemy
        self.enemy_id_counter += 1
        
    def update_player(self, input_data: PlayerInput) -> None:
        """Update player position based on input."""
        speed = 3.0
        
        dx = 0
        dy = 0
        
        if input_data.left:
            dx -= speed * self.terrain.calculate_height_percent()
            
        if input_data.right:
            dx += speed * self.terrain.calculate_height_percent()
            
        if input_data.up:
            dy -= speed
            
        if input_data.down:
            dy += speed
        
        # Apply terrain effects
        terrain_speed = self.terrain.calculate_height_percent()
        if terrain_speed > 0:
            dx *= terrain_speed
            
        self.player.move(dx, dy)
        
    def update_enemies(self) -> None:
        """Update all enemy positions."""
        alive_enemy_ids = [
            eid for eid, enemy in self.enemies.items() 
            if not enemy.is_dead()
        ]
        
        if alive_enemy_ids:
            EnemyAI.update_enemies(
                [self.enemies[eid] for eid in alive_enemy_ids],
                self.player.x,
                self.player.y
            )
        
    def check_collisions(self) -> None:
        """Check player-enemy and enemy-terrain collisions."""
        terrain_speed = self.terrain.calculate_height_percent()
        
        for enemy_id, enemy in list(self.enemies.items()):
            # Check if enemy hit player
            distance = ((self.player.x - enemy.x) ** 2 + 
                       (self.player.y - enemy.y) ** 2) ** 0.5
            
            if distance < 30:
                self.player.take_damage(enemy.damage)
                
            # Check enemy terrain effects
            tiles = ProceduralTerrain.generate_tile_grid(
                TerrainLayer(name="grass", y_position=self.terrain.current_height, width=200)
            )
            
            for tile in tiles:
                if tile.tile_type in ["lava", "water"]:
                    speed_mod = tile.tile_properties()["speed_mod"]
                    enemy.y += enemy.speed * speed_mod
                    
    def handle_input(self, input_data: PlayerInput) -> None:
        """Process player input."""
        self.update_player(input_data)
        
        # Auto-spawn enemies periodically
        if self.enemies and len([e for e in self.enemies.values() if not e.is_dead()]) < 5:
            if random.random() < 0.1:
                self.spawn_enemy()

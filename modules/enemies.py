"""Enemy management and AI for ren.py game."""

import random
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Enemy:
    """Enemy entity with position, type, and stats."""
    x: float
    y: float
    enemy_type: str
    health: int
    max_health: int
    speed: float
    damage: int
    xp_reward: int
    color: str = "#8B4513"  # Default brown
    
    def take_damage(self, damage: int) -> None:
        """Apply damage and return remaining health."""
        self.health -= damage
        
    def get_remaining_health(self) -> int:
        """Return current health."""
        return max(0, self.health)
    
    def is_dead(self) -> bool:
        """Check if enemy is dead."""
        return self.health <= 0
    
    def update_position(self, dx: float, dy: float) -> None:
        """Update enemy position."""
        self.x += dx
        self.y += dy


class EnemyFactory:
    """Factory for creating enemy instances."""
    
    ENEMY_TYPES = {
        "slime": {
            "health_mult": 1.0,
            "speed_mult": 0.8,
            "damage_mult": 1.0,
            "color": "#32CD32",  # Lime green
            "xp_base": 10,
        },
        "brute": {
            "health_mult": 2.5,
            "speed_mult": 0.6,
            "damage_mult": 1.5,
            "color": "#8B4513",  # Brown
            "xp_base": 25,
        },
        "sprinter": {
            "health_mult": 0.6,
            "speed_mult": 1.5,
            "damage_mult": 0.8,
            "color": "#FF4500",  # Orange red
            "xp_base": 12,
        },
    }
    
    @classmethod
    def create_enemy(
        cls,
        enemy_type: str,
        wave_multiplier: float = 1.0,
        position: tuple = (None, None)
    ) -> Enemy:
        """Create an enemy of the specified type.
        
        Args:
            enemy_type: One of "slime", "brute", or "sprinter"
            wave_multiplier: Scaling factor for stats based on wave number
            position: (x, y) coordinates, defaults to random
            
        Returns:
            Enemy instance with calculated stats
        """
        config = cls.ENEMY_TYPES.get(enemy_type.lower(), cls.ENEMY_TYPES["slime"])
        
        if position[0] is None:
            x = random.uniform(-300, 300)
            y = random.uniform(200, 350)  # Spawn near top of fog
        else:
            x, y = position
        
        wave_stats = {
            "health": config["health_base"] * wave_multiplier,
            "speed": config["speed_base"] * wave_multiplier,
            "damage": config["damage_base"] * wave_multiplier,
            "xp_reward": config["xp_base"] * (1 + wave_multiplier * 0.2),
        }
        
        return Enemy(
            x=x,
            y=y,
            enemy_type=enemy_type.lower(),
            health=int(wave_stats["health"]),
            max_health=int(wave_stats["health"]),
            speed=wave_stats["speed"],
            damage=int(wave_stats["damage"]),
            xp_reward=int(wave_stats["xp_reward"]),
            color=config["color"]
        )
    
    @classmethod
    def spawn_random(cls, wave_multiplier: float) -> Enemy:
        """Spawn a random enemy type."""
        types = list(cls.ENEMY_TYPES.keys())
        return cls.create_enemy(
            random.choice(types),
            wave_multiplier=wave_multiplier
        )


class EnemyAI:
    """Simple AI for enemy behavior."""
    
    @staticmethod
    def update_enemies(
        enemies: List[Enemy],
        player_x: float,
        player_y: float,
        bounds: tuple = (-400, -300, 600, 500)
    ) -> None:
        """Update all enemy positions towards player.
        
        Args:
            enemies: List of Enemy instances
            player_x: Player X coordinate
            player_y: Player Y coordinate
            bounds: (min_x, min_y, max_x, max_y) for movement limits
        """
        # Track if any enemies are alive
        alive_enemies = [e for e in enemies if not e.is_dead()]
        
        for enemy in alive_enemies:
            dx = player_x - enemy.x
            dy = player_y - enemy.y
            
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance > 1:
                move_x = dx / distance * enemy.speed
                move_y = dy / distance * enemy.speed
                
                # Clamp to bounds
                min_x, min_y, max_x, max_y = bounds
                enemy.x = max(min_x, min(max_x, enemy.x))
                enemy.y = max(min_y, min(max_y, enemy.y))
            else:
                # Already at player position
                enemy.x = player_x
                enemy.y = player_y

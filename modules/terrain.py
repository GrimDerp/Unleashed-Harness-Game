"""Terrain generation and management for ren.py game."""

import random
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class Tile:
    """A single terrain tile."""
    x: int
    y: int
    tile_type: str
    height_modifier: float = 0.0
    color: str = "#90EE90"  # Light green default


@dataclass
class TerrainLayer:
    """A layer of terrain (ground, water, fog)."""
    name: str
    y_position: float
    width: int = 120
    active: bool = True
    opacity: float = 0.8


class ProceduralTerrain:
    """Generate procedural terrain layers and tiles."""
    
    TILE_TYPES = {
        "grass": {"color": "#90EE90", "speed_mod": 1.0, "damage": 0},
        "water": {"color": "#1E90FF", "speed_mod": 0.5, "damage": 0},
        "lava": {"color": "#FF4500", "speed_mod": 1.2, "damage": 1},
        "crystal": {"color": "#DA70D6", "speed_mod": 1.0, "damage": 0.5},
    }
    
    @staticmethod
    def generate_terrain_layer(width: int = 120) -> TerrainLayer:
        """Generate a single terrain layer at specified y-position.
        
        Args:
            width: Width of the terrain in units
            
        Returns:
            TerrainLayer instance with generated position
        """
        terrain_type = random.choice(["grass", "water", "lava"])
        return TerrainLayer(
            name=terrain_type,
            y_position=random.uniform(150, 200),  # Base fog level
            width=width
        )
    
    @staticmethod
    def generate_tile_grid(
        layer: TerrainLayer,
        grid_size: int = 40
    ) -> List[Tile]:
        """Generate a grid of tiles for a terrain layer.
        
        Args:
            layer: The TerrainLayer to generate tiles for
            grid_size: Size of each tile in units
            
        Returns:
            List of Tile instances
        """
        tiles = []
        
        # Calculate grid dimensions
        cols = int(layer.width / grid_size) + 1
        rows = 3  # Vertical variation
        
        for row in range(rows):
            for col in range(cols):
                # Add some randomness to tile placement
                if random.random() > 0.7:
                    continue
                
                x = col * grid_size - layer.width / 2 + random.uniform(-10, 10)
                y = row * 30 + layer.y_position
                
                tile = Tile(
                    x=round(x, 1),
                    y=round(y, 1),
                    tile_type=layer.name,
                    color=TerrainConfig.TILE_TYPES[layer.name]["color"]
                )
                
                # Chance for special tiles (lava/crystal) on grass
                if layer.name == "grass" and random.random() < 0.3:
                    special = random.choice(["lava", "crystal"])
                    tile.tile_type = special
                    tile.color = TerrainConfig.TILE_TYPES[special]["color"]
                
                tiles.append(tile)
        
        return tiles


class TerrainManager:
    """Manage terrain state and interactions."""
    
    def __init__(self, initial_height: float = 200):
        self.current_height = initial_height
        self.original_height = initial_height
        self.tiles: List[Tile] = []
        self.fog_level: int = 0
        
    def update_fog(self) -> None:
        """Update fog level (creeps up from bottom)."""
        self.fog_level += 1
        
        if self.fog_level > 100:
            self.current_height -= 1
            if self.current_height < 50:
                self.current_height = 50  # Death threshold
    
    def is_fog_ended(self) -> bool:
        """Check if fog has fully covered the screen."""
        return self.fog_level >= 500 or self.current_height <= 0
    
    def calculate_height_percent(self) -> float:
        """Calculate current height as percentage (1.0 = full, 0.0 = dead)."""
        return max(0, min(1, self.current_height / self.original_height))
    
    def set_height(self, new_height: float) -> None:
        """Set terrain height directly."""
        self.current_height = max(50, min(self.original_height, new_height))


class TerrainConfig:
    """Constants and configuration for terrain."""
    
    TILE_TYPES = {
        "grass": {"color": "#90EE90", "speed_mod": 1.0, "damage": 0},
        "water": {"color": "#1E90FF", "speed_mod": 0.5, "damage": 0},
        "lava": {"color": "#FF4500", "speed_mod": 1.2, "damage": 1},
        "crystal": {"color": "#DA70D6", "speed_mod": 1.0, "damage": 0.5},
    }
    
    @classmethod
    def get_tile_properties(cls, tile_type: str) -> Dict:
        """Get properties for a tile type."""
        return cls.TILE_TYPES.get(tile_type.lower(), cls.TILE_TYPES["grass"])

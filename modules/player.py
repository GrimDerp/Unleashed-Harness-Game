#!/usr/bin/env python3
"""Player module for BASH & BLUDGEON."""

class Player:
    """Player character with stats and attack mechanics."""
    
    def __init__(self, x=None, y=None):
        self.x = x or 400
        self.y = y or 520
        self.hp = 100
        self.maxHp = 100
        self.lvl = 1
        self.xp = 0
        self.xpNext = 30
        self.atk = 10
        self.spd = 3.0
        self.score = 0
        self.invuln = 0
        self.attack_cooldown = 0
        
    def update(self, keys, mouse, dt=1):
        """Update player position based on input and terrain effects."""
        # Handle invulnerability timer
        if self.invuln > 0:
            self.invuln -= dt
            return
            
        # Calculate movement from WASD/arrows
        dx = 0
        dy = 0
        if keys.get('w') or keys.get('arrowup'):
            dy = -1
        if keys.get('s') or keys.get('arrowdown'):
            dy = 1
        if keys.get('a') or keys.get('arrowleft'):
            dx = -1
        if keys.get('d') or keys.get('arrowright'):
            dx = 1
            
        # Normalize diagonal movement
        if dx and dy:
            dx *= 0.707
            dy *= 0.707
            
        self.x += dx * self.spd
        self.y += dy * self.spd
        
        # Clamp to canvas boundaries
        self.x = max(10, min(800 - 10, self.x))
        self.y = max(10, min(600 - 10, self.y))
        
        # Handle attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
    def take_damage(self, amount):
        """Apply damage to player."""
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            return True  # Player dead
        return False
    
    def heal(self, amount):
        """Heal player by amount."""
        self.hp = min(self.maxHp, self.hp + amount)
    
    def level_up(self):
        """Level up with stat increases and full heal."""
        self.lvl += 1
        self.xpNext = int(self.xpNext * 1.4)
        self.maxHp += 15
        self.heal(self.maxHp)  # Full heal on level up
        self.atk += 3
        self.spd += 0.15
    
    def gain_xp(self, amount):
        """Gain XP and check for level up."""
        self.xp += amount
        if self.xp >= self.xpNext:
            self.level_up()

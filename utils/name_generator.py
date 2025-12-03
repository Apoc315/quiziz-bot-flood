import random

class NameGenerator:
    def __init__(self):
        self.adjectives = [
            'Cool', 'Smart', 'Quick', 'Epic', 'Mega', 'Super', 'Fast', 'Pro', 
            'Ultra', 'Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Omega',
            'Swift', 'Clever', 'Bright', 'Wise', 'Sharp', 'Keen', 'Nimble',
            'Mighty', 'Brave', 'Calm', 'Eager', 'Fair', 'Gentle', 'Happy',
            'Jolly', 'Kind', 'Lively', 'Nice', 'Proud', 'Silly', 'Witty'
        ]
        
        self.nouns = [
            'Player', 'Gamer', 'Student', 'Learner', 'Scholar', 'Brain', 
            'Mind', 'Genius', 'Master', 'Ninja', 'Warrior', 'Hunter', 
            'Knight', 'Wizard', 'Mage', 'Pro', 'Expert', 'Champ',
            'Hero', 'Legend', 'Star', 'King', 'Queen', 'Prince', 'Princess',
            'Tiger', 'Lion', 'Eagle', 'Hawk', 'Wolf', 'Fox', 'Bear'
        ]
        
        self.used_names = set()
    
    def generate(self):
        """Generate a unique bot name with multiple patterns"""
        patterns = [
            lambda: f"{random.choice(self.adjectives)}{random.choice(self.nouns)}{random.randint(100, 9999)}",
            lambda: f"{random.choice(self.adjectives)}_{random.choice(self.nouns)}_{random.randint(10, 99)}",
            lambda: f"{random.choice(self.nouns)}Of{random.choice(self.adjectives)}{random.randint(100, 999)}",
            lambda: f"The{random.choice(self.adjectives)}{random.choice(self.nouns)}",
            lambda: f"{random.choice(self.nouns)}{random.randint(1000, 9999)}"
        ]
        
        # Try multiple times to get a unique name
        for _ in range(10):
            name = random.choice(patterns)()
            if name not in self.used_names:
                self.used_names.add(name)
                return name
        
        # If all patterns are used, add more numbers
        return f"Player{random.randint(10000, 99999)}"

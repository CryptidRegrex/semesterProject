from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Character(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-Binary'),
        ('O', 'Other'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50, help_text="Character's race, e.g., Elf, Human, Dwarf")
    background = models.CharField(max_length=50, help_text="Character's background, e.g., Soldier, Noble")
    char_class = models.CharField(max_length=50, help_text="Character's class, e.g., Fighter, Wizard, Rogue")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, help_text="Gender identity of the character")

    # Core Attributes
    strength = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Strength (1-30)")
    dexterity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Dexterity (1-30)")
    constitution = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Constitution (1-30)")
    intelligence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Intelligence (1-30)")
    wisdom = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Wisdom (1-30)")
    charisma = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Charisma (1-30)")
    
    # Secondary Attributes
    # To add some more color these will be the attributes the DM will be using and or modifying during a campaign 
    # Special permissions will want to be used for something like this
    hit_points = models.IntegerField(validators=[MinValueValidator(0)], help_text="Current hit points")
    max_hit_points = models.IntegerField(validators=[MinValueValidator(1)], help_text="Maximum hit points")
    armor_class = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Armor Class (AC)")
    speed = models.IntegerField(validators=[MinValueValidator(1)], help_text="Movement speed in feet per round")
    proficiency_bonus = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], help_text="Proficiency bonus (1-6)")
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], help_text="Character level (1-20)")
    experience_points = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Experience points accumulated")
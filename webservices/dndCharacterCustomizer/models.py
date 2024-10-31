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
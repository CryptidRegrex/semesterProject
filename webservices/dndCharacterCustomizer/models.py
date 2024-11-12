from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractUser


# class User(AbstractUser):
#     # Add any additional fields if needed
#     pass

# #Found that django have a build in user model that i can extend.
# class CustomUserManager(BaseUserManager):
#     def createUser(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field is required")
#         email = self.email.lower()
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


class Campaign(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the campaign")
    characters = models.ManyToManyField('Character', related_name='campaigns', blank=True, help_text="Characters participating in this campaign")

    def __str__(self):
        return self.name


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
    charClass = models.CharField(max_length=50, help_text="Character's class, e.g., Fighter, Wizard, Rogue")
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
    hitPoints = models.IntegerField(validators=[MinValueValidator(0)], help_text="Current hit points")
    maxHitPoints = models.IntegerField(validators=[MinValueValidator(1)], help_text="Maximum hit points")
    armorClass = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Armor Class (AC)")
    speed = models.IntegerField(validators=[MinValueValidator(1)], help_text="Movement speed in feet per round")
    proficiencyBonus = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], help_text="Proficiency bonus (1-6)")
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], help_text="Character level (1-20)")
    experiencePoints = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Experience points accumulated")
    
    # Skills
    # In this case we are going to let the player mark if they have said skill or not. 
    # Using this later in the model to calculate the skil bonus like a +2 to athletics
    athletics = models.BooleanField(default=False, help_text="Proficient in Athletics (Strength-based)")
    #Dex based
    acrobatics = models.BooleanField(default=False, help_text="Proficient in Acrobatics (Dexterity-based)")
    sleightOfHand = models.BooleanField(default=False, help_text="Proficient in Sleight of Hand (Dexterity-based)")
    stealth = models.BooleanField(default=False, help_text="Proficient in Stealth (Dexterity-based)")
    #Intelligence based
    arcana = models.BooleanField(default=False, help_text="Proficient in Arcana (Intelligence-based)")
    history = models.BooleanField(default=False, help_text="Proficient in History (Intelligence-based)")
    investigation = models.BooleanField(default=False, help_text="Proficient in Investigation (Intelligence-based)")
    nature = models.BooleanField(default=False, help_text="Proficient in Nature (Intelligence-based)")
    religion = models.BooleanField(default=False, help_text="Proficient in Religion (Intelligence-based)")
    #Wisdom based
    animalHandling = models.BooleanField(default=False, help_text="Proficient in Animal Handling (Wisdom-based)")
    insight = models.BooleanField(default=False, help_text="Proficient in Insight (Wisdom-based)")
    medicine = models.BooleanField(default=False, help_text="Proficient in Medicine (Wisdom-based)")
    perception = models.BooleanField(default=False, help_text="Proficient in Perception (Wisdom-based)")
    survival = models.BooleanField(default=False, help_text="Proficient in Survival (Wisdom-based)")
    #Charisma based
    deception = models.BooleanField(default=False, help_text="Proficient in Deception (Charisma-based)")
    intimidation = models.BooleanField(default=False, help_text="Proficient in Intimidation (Charisma-based)")
    performance = models.BooleanField(default=False, help_text="Proficient in Performance (Charisma-based)")
    persuasion = models.BooleanField(default=False, help_text="Proficient in Persuasion (Charisma-based)")
    
    #Essentially, like in D&D take the score -10 and get the bonus from it
    #Better user experience so they don't have to calculate that
    def abilityModifier(self, score):
        """Calculate the ability modifier for a given ability score."""
        return (score - 10) // 2

    #So fo rthis one there's a lot going on
    def skillModifier(self, skill_name):
        """
        Calculate skill modifier based on proficiency and associated ability score.
        """
        #List of skills with the object's self value of the core stats in a key value pair
        skill_to_ability = {
            'athletics': self.strength,
            'acrobatics': self.dexterity,
            'sleightOfHand': self.dexterity,
            'stealth': self.dexterity,
            'arcana': self.intelligence,
            'history': self.intelligence,
            'investigation': self.intelligence,
            'nature': self.intelligence,
            'religion': self.intelligence,
            'animalHandling': self.wisdom,
            'insight': self.wisdom,
            'medicine': self.wisdom,
            'perception': self.wisdom,
            'survival': self.wisdom,
            'deception': self.charisma,
            'intimidation': self.charisma,
            'performance': self.charisma,
            'persuasion': self.charisma,
        }
        
        # Get base modifier based on associated ability and then we set the bonus based on the core stat bonus
        ability_score = skill_to_ability.get(skill_name)
        base_modifier = self.abilityModifier(ability_score)
        
        # Add proficiency bonus if proficient in skill. We'll only calcuate that of abilities the user has
        if getattr(self, skill_name):
            return base_modifier + self.proficiencyBonus
        return base_modifier
    
    # Thought returing some more information about the character would be neat.
    def __str__(self):
        return f"{self.name} - Level {self.level} {self.charClass} ({self.race})"
    
    
    
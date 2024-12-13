from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
#Using this for special access token to campaign
import uuid
import os

"""This stores additional information about the User record
   Using this as a detail object to store user types, relationships, and reset token which can be used for password resets
Returns:
    string: of user name and type of user
"""
class Profile(models.Model):
    # Link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Roles
    USER_TYPES = [
        ("ADMIN", "Admin"),
        ("AUTHORIZED", "Authorized"),
    ]
    type = models.CharField(max_length=10, choices=USER_TYPES, default="AUTHORIZED")
    
    #Just setting it here too. Maybe should remove later. 
    email = models.EmailField(unique=True, max_length=100)

    # Relationships to the Character model and the Campaign model. These should be default blank. 
    characters = models.ManyToManyField("Character", blank=True)
    campaigns = models.ManyToManyField("Campaign", related_name="profile_campaigns", blank=True)

    #Used for password resets
    reset_token = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"

"""Tracks campaign, user, and profile relationships
   Stores access token needed to join a campaign
Returns:
    string: of campaign name
"""
class Campaign(models.Model):
    userOwner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Name of the campaign")
    characters = models.ManyToManyField('Character', related_name='character_campaigns', blank=True, help_text="Characters participating in this campaign")
    profiles = models.ManyToManyField(Profile, related_name="campaign_profiles", blank=True)  
    #Access token for a campaign owner to pass to a player in their campaign
    access_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Auto-generated access token

    def __str__(self):
        return self.name

"""This tracks character informatoin.
   This model, models, a Dungeons & Dragons 5e character

Returns:
    string: Character name, level, class, and race
"""
class Character(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-Binary'),
        ('O', 'Other'),
    ]

    #ChatGPT helped in the creation of this definition
    def user_directory_path(instance, filename):

        # Extract file extension
        ext = filename.split('.')[-1]

        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}.{ext}"

        # Construct file path
        return os.path.join(f"characters/user_{instance.profiles.first().user.id}", unique_filename)

    # Many-to-many relationship to Profile (for the owners of this character)
    profiles = models.ManyToManyField('Profile', related_name='owners', blank=True)

    #Campagin
    campaigns = models.ManyToManyField('Campaign', related_name='campaign_characters', blank=True)
    
    #image for the player to upload something to the site - Help from ChatGPT to create this. 
    #calling a new defintion that will ensure image is of certain type and size
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

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
    hitPoints = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], help_text="Current hit points")
    maxHitPoints = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)], help_text="Maximum hit points")
    armorClass = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], help_text="Armor Class (AC)")
    speed = models.IntegerField(validators=[MinValueValidator(1), (MaxValueValidator(10000))], help_text="Movement speed in feet per round")
    proficiencyBonus = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], help_text="Proficiency bonus (1-6)")
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], help_text="Character level (1-20)")
    experiencePoints = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)], help_text="Experience points accumulated")
    
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
    
    
    """Essentially, like in D&D take the score -10 and get the bonus from it
       Better user experience so they don't have to calculate that
    """
    def abilityModifier(self, score):
        """Calculate the ability modifier for a given ability score."""
        return (score - 10) // 2

    """tracks the skill modifiers based on selection of which skills are selected
    """
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
    
    
    
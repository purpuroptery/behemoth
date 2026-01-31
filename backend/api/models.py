from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from shortuuidfield import ShortUUIDField

"""
common abstract base classes
"""

class BaseModel(models.Model):
    pk = ShortUUIDField(primary_key=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
    def get_name(self):
        return getattr(self, "name", None) or getattr(self, "username", None) or "(no name)"
        
    def __str__(self):
        return f"{type(self).__name__}<{self.get_name()}> ({self.pk})"

class NamedModel(BaseModel):
    name = models.CharField(max_length=63)

    class Meta(BaseModel.Meta):
        abstract = True

class UsernamedModel(BaseModel):
    username = models.CharField(
        max_length=32,
        unique=True,
        validators=[RegexValidator(
            regex=r"^[a-z0-9]+$",
            message="username must be alphanumeric and lowercase",
        )]
    )
    
    class Meta(BaseModel.Meta):
        abstract = True
        
class NamedOwnedModel(NamedModel):
    creator = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta(NamedModel.Meta):
        abstract = True
        unique_together = ("creator", "name")
        
        
"""
application models
"""
    
class User(UsernamedModel):
    verified = models.BooleanField(default=False)
    trusted = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    
    """
    insert google login stuff
    """
        
        
class Game(NamedModel):
    pass
    
"""
1. assigns orders to holes
e.g. on Lakeside/Resort, 1=L1, 2=L2... 10=R1...

2. defines wind speeds available on course
"""
class Course(NamedModel):
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="courses")
    
    holes = models.JSONField(default=list, blank=True) # list of hole IDs in the order they appear
    
    wind_speeds = models.JSONField(default=list, blank=True) # list of int wind speeds
    
    def get_name(self):
        return f"{self.game.name} ({self.name})"

class Hole(NamedModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="holes")
    pins = models.ManyToManyField("Pin", blank=True)
    
class Pin(NamedModel):
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE, related_name="pins")
    
class Setup(NamedOwnedModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="setups")
    
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE, related_name="setups")
    wind_speed = models.IntegerField()
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    
    objective = models.CharField(choices=[("score", "Score"), ("speed", "Speed")], null=False, blank=False)
    
    text = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)  # time in ms

class SetupGroup(NamedOwnedModel): 
    setups = models.ManyToManyField(Setup, related_name="groups", blank=True)
    
class SetupSheet(NamedOwnedModel):
    
    class SetupSheetLayer(BaseModel):
        sheet = models.ForeignKey("SetupSheet", on_delete=models.CASCADE, related_name="layers")
        group = models.ForeignKey(SetupGroup, on_delete=models.CASCADE)
        enabled = models.BooleanField(default=True)

    layers = models.JSONField(default=list, blank=True)  # list of layer ids in order
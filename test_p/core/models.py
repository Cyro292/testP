from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Client(models.Model):
    
    class Meta:
        abstract = True
        
class UserClient(Client):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(self.user)
    
class AnonymousClient(Client):
    username = models.CharField(max_length=64)
    
    def __str__(self) -> str:
        return self.username
    
class Board(models.Model):
    name = models.CharField(max_length=64)
    creation_date = models.DateTimeField(default=datetime.now())
    clients = models.ManyToManyField(to=UserClient, related_name="boards", through="Participation")
    
class Participation(models.Model):
    OWNER = "owner"
    ADMIN = "admin"
    WRITER = "writer"
    READER = "reader"
    
    permissions = [
        (OWNER, "Owner"),
        (ADMIN, "Admin"),
        (WRITER, "Writer"),
        (READER, "Reader"),
    ]
    
    client = models.ForeignKey(UserClient, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    join_date = models.DateTimeField(default=datetime.now())
    permission = models.CharField(choices=permissions, default=READER, max_length=64)
    
    class Meta:
        unique_together = [["client", "board"]]

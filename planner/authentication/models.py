from django.db import models

import uuid

from django.shortcuts import render

# Create your models here.

from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):

  ADMIN = 'Admin','Admin'

  COORDINATOR = 'Project Coordinator','Project Coordinator'

  DEVELOPER = 'Developer', 'Developer'

class TechChoices(models.TextChoices):

  BACKEND = 'Backend Developer', 'Backend Developer'

  FRONTEND = 'Frontend Developer', 'Frontend Developer'

  FULLSTACK = 'Fullstack Developer', 'Fullstack Developer'

  UI_UX = 'UI/UX Designer', 'UI/UX Designer'

  TESTER = 'Software Tester', 'Software Tester'

  NOT_APPLICABLE = 'N/A', 'Not applicable'

class Profile(AbstractUser):

  role = models.CharField(max_length=20,choices=RoleChoices.choices)

  tech = models.CharField(max_length=30, choices=TechChoices.choices)

  class Meta:

    verbose_name = 'Profiles'

    verbose_name_plural = 'Profiles'

  def __str__(self):
    
    return f'{self.first_name}-{self.tech}'
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    
    def _str_(self):
        return self.name

    class Meta:
        ordering = ['id']
    
    

class FormData(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,default=None)
    
    #project_name = models.CharField(max_length=255, default="empty")
    form_key = models.CharField(max_length=100, default="empty")
    forms_name = models.CharField(max_length=255, default="value")
    Rediretpath_name = models.CharField(max_length=100, default="value")

    def _str_(self):
        return f"{self.forms_name}"
    def save(self, *args, **kwargs):
        if self.project:
            self.project_name = self.project.name
        super(FormData, self).save(*args, **kwargs)
        
class FieldData(models.Model):
    #form_data = models.ForeignKey(FormData, on_delete=models.CASCADE, default=None)
    form_id = models.IntegerField()  # Add a field to store the form ID
    
    field_key = models.CharField(max_length=100, default="empty")
    field_value = models.CharField(max_length=255, default="value")
    selection_value = models.CharField(max_length=100, default="value")
    required = models.BooleanField(default=None, null=True)
    readable = models.BooleanField(default=None, null=True)
    #project_name = models.CharField(max_length=255, default="empty")
    project = models.ForeignKey(Project, on_delete=models.CASCADE,default=None)
    def _str_(self):
        return f"{self.field_key}"




class User(models.Model):
    name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100, unique=True)
    #project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=200, blank=True)
    
    def save(self, *args, **kwargs):
        self.username = f"{self.name}@{self.project_name}"
        super(User, self).save(*args, **kwargs)
       
    # def save(self, *args, **kwargs):
    #     existing_project = Project.objects.filter(name=self.project_name).first()
    #     if existing_project:
    #         self.project_name = existing_project
    #     else:
    #         new_project = Project.objects.create(name=self.project_name)
    #         self.project_name = new_project
    #     self.username = f"{self.name}@{self.project_name}"
    #     super(User, self).save(*args, **kwargs)


# class User(models.Model):
#     name = models.CharField(max_length=100)
#     projects = models.ManyToManyField(Project)

#     # Other fields
#     password = models.CharField(max_length=100)
#     username = models.CharField(max_length=200, blank=True)
    
#     def save(self, *args, **kwargs):
#         # Update username based on the first project (assuming each user has at least one project)
#         if self.projects.exists():
#             self.username = f"{self.name}@{self.projects.first().name}"
#         super(User, self).save(*args, **kwargs)
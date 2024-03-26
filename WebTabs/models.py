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
       

class DraggableData(models.Model):
    forms_name = models.CharField(max_length=100, null=True, blank=True)
    x_axis = models.CharField(max_length=255, default=None)
    y_axis = models.CharField(max_length=255, default=None)
    color = models.CharField(max_length=50, default="value")
    padding_size = models.CharField(max_length=255, default=None)
    #formid = models.CharField(max_length=100, null=True, blank=True)
    #fieldid = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE ,default=1)

    def __str__(self):
        return f"{self.forms_name} - {self.project.name}"

    
    def save(self, *args, **kwargs):
        if not self.forms_name:
            self.forms_name = 'null'
        # if not self.field_name:
        #     self.field_name = 'null'
        # if not self.field_type:
        #     self.field_type = 'null'
        if not self.x_axis:
            self.x_axis = 'null'
        if not self.y_axis:
            self.y_axis = 'null'
        if not self.padding_size:
            self.padding_size = 'null'
        super(DraggableData, self).save(*args, **kwargs)
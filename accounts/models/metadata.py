from django.db import models
import uuid
# Create your models here.

def generate_uuid_hex():
    return uuid.uuid4().hex


class Objects(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=generate_uuid_hex, editable=False)
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    table_name = models.CharField(max_length=255)
    deleted = models.CharField(max_length=1, default='0')

    def logic_delete(self):
        self.deleted = '1'
        self.save()

        for field in self.fields.all():
            field.logic_delete()

    def __str__(self):
        return self.name
    

class PageLists(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=generate_uuid_hex, editable=False)
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    deleted = models.CharField(max_length=1, default='0')

    def logic_delete(self):
        self.deleted = '1'
        self.save()

        for field in self.fields.all():
            field.logic_delete()

        for layout in self.layouts.all():
            layout.logic_delete()

    def __str__(self):
        return self.name


class ObjectFields(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=generate_uuid_hex, editable=False)
    object_id = models.ForeignKey(Objects, on_delete=models.SET_NULL, null=True, related_name='fields')
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    deleted = models.CharField(max_length=1, default='0')

    def logic_delete(self):
        self.deleted = '1'
        self.save()

        for page_list_field in self.page_list_fileds.all():
            page_list_field.logic_delete()

    def __str__(self):
        return self.name


class PageListFields(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=generate_uuid_hex, editable=False)
    object_field_id = models.ForeignKey(ObjectFields, on_delete=models.SET_NULL, null=True, related_name='page_list_fields')
    page_list_id = models.ForeignKey(PageLists, on_delete=models.SET_NULL, null=True, related_name='fields')
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    hidden = models.CharField(max_length=1, default="0")
    type = models.CharField(max_length=255)
    deleted = models.CharField(max_length=1, default='0')

    def logic_delete(self):
        self.deleted = '1'
        self.save()

    def __str__(self):
        return self.name
    

class PageLayouts(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=generate_uuid_hex, editable=False)
    name = models.CharField(max_length=255)
    page_list_id = models.ForeignKey(PageLists, on_delete=models.SET_NULL, null=True, related_name='layouts')
    deleted = models.CharField(max_length=1, default='0')

    def logic_delete(self):
        self.deleted = '1'
        self.save()

        for field in self.fields.all():
            field.logic_delete()

    def __str__(self):
        return self.name


class PageLayoutFields(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=generate_uuid_hex, editable=False)
    page_layout_id = models.ForeignKey(PageLayouts, on_delete=models.SET_NULL, null=True, related_name='fields')
    object_field_id = models.ForeignKey(ObjectFields, on_delete=models.SET_NULL, null=True, related_name='layout_fields')
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    deleted = models.CharField(max_length=1, default='0')

    def logic_delete(self):
        self.deleted = '1'
        self.save()

    def __str__(self):
        return self.name
    


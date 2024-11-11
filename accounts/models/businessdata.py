from django.db import models
import uuid

def generate_uuid_hex():
    return uuid.uuid4().hex


class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=generate_uuid_hex, editable=False)
    account_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.account_name
    

# class AccountLog(models.Model):
#     OPERATION_TYPE = [
#         ('CREATE', 'Create'),
#         ('UPDATE', 'Update'),
#         ('DELETE', 'Delete'),
#     ]
#     id = models.BigAutoField(primary_key=True)
#     account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='logs')
#     operation_type = models.CharField(max_length=10, choices=OPERATION_TYPE)
#     operator = models.CharField(max_length=255, null=True, blank=True)
#     operation_time = models.DateTimeField(auto_now_add=True)
#     details = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.operation_type} by {self.operator} on {self.account.account_name}"
    

# class BatchOperation(models.Model):
#     OPERATION_TYPES = [
#         ('IMPORT', 'Import'),
#         ('EXPORT', 'Export'),
#     ]
#     id = models.BigAutoField(primary_key=True)
#     operation_type = models.CharField(max_length=10, choices=OPERATION_TYPES)
#     file_path = models.CharField(max_length=255, null=True, blank=True)
#     operator = models.CharField(max_length=255, null=True, blank=True)
#     operation_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.operation_type} by {self.operator}"


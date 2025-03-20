from django.db import models
import time
# Create your models here.
class MpesaAccessToken(models.Model):
    token = models.CharField(max_length=500)#store the actual access token
    expiry_time = models.FloatField() #store the expiry time  
    
    def is_token_valid(self):
        """Check if the token is still valid.
        """
        return time.time() > self.expiry_time
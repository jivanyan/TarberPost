from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User

class Patron(models.Model):
        user            = models.OneToOneField(User, related_name='patron')

        picture         = models.ImageField(upload_to = 'profile_pictures',
                                      blank = True)

        # Leave phone field for PhoneNumberField in the future.
        raw_phone       = models.CharField(verbose_name='Raw phone',
                                     max_length=1024,
                                     null=True,
                                     blank=True)
	

class Bid(models.Model):
	patron 		= models.ForeignKey(Patron, related_name = 'all_bids')
	title		= models.CharField(verbose_name = 'Title', max_length = 128)
	startpoint 	= models.CharField(verbose_name = 'Starting Point',
						max_length = 128)
	exacttime	= models.DateTimeField(verbose_name = 'Time', null = True, blank = True)
	begin		= models.DateTimeField(verbose_name = 'From', null = True, blank = True)
	end	 	= models.DateTimeField(verbose_name = 'To', null = True, blank = True)
		
        endpoint        = models.CharField(verbose_name = 'End Point',
                                                max_length = 128,
                                                null = True,
                                                blank = True)

	description 	= models.CharField(verbose_name = 'Description',
						max_length = 1024,
						null = True,
						blank = True)
	status		= models.IntegerField(verbose_name = 'Status')
							

from django.db import models
from common import model_utils
# Create your models here.

class User (model_utils.BaseModel):
	user_id = models.BigIntegerField(primary_key=True)
	username = models.CharField(max_length=36, unique=True)
	password = models.CharField(max_length=32)
	email = models.CharField(max_length=50)
	photo_url = models.CharField(max_length=200)
	create_time = models.IntegerField()
	update_time = models.IntegerField()

	class Meta:
		db_table = 'user_tab'
		app_label = 'activitylib'


class ActivityPicture(model_utils.BaseModel):
	id = models.BigIntegerField(primary_key=True)
	activity_id = models.BigIntegerField()
	picture_url = models.CharField(max_length=200)
	#activity = models.ForeignKey('Activity')

	class Meta:
		db_table = 'activity_picture_tab'
		app_label = 'activitylib'


class Activity (model_utils.BaseModel):
	id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	channel_id = models.BigIntegerField()
	desc = models.CharField(max_length=500)
	detail = models.TextField()
	location = models.CharField(max_length=200)
	admin_id = models.BigIntegerField()
	begin_time = models.IntegerField()
	end_time = models.IntegerField()
	create_time = models.IntegerField()
	update_time = models.IntegerField()
	#activity_pictures = models.ManyToManyField(ActivityPicture, related_name="activity_id")

	class Meta:
		db_table = 'activity_tab'
		app_label = 'activitylib'


class Admin (model_utils.BaseModel):
	admin_id = models.BigIntegerField(primary_key=True)
	username = models.CharField(max_length=36, unique=True)
	password = models.CharField(max_length=32)
	photo_url = models.CharField(max_length=200)
	create_time = models.IntegerField()
	update_time = models.IntegerField()

	class Meta:
		db_table = 'admin_tab'
		app_label = 'activitylib'


class ActivityChannel (model_utils.BaseModel):
	id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length=100, unique=True)
	admin_id = models.BigIntegerField(default=0)
	create_time = models.IntegerField(default=0)
	update_time = models.IntegerField(default=0)

	class Meta:
		db_table = 'activity_channel_tab'
		app_label = 'activitylib'


class Comment (model_utils.BaseModel):
	id = models.BigIntegerField(primary_key=True)
	activity_id = models.BigIntegerField()
	user_id = models.BigIntegerField()
	refer_id = models.BigIntegerField()
	content = models.CharField(max_length=400)
	comment_time = models.IntegerField(default=0)
	username = None

	class Meta:
		db_table = 'comment_tab'
		app_label = 'activitylib'


class Participate (model_utils.BaseModel):
	id = models.BigIntegerField(primary_key=True)
	activity_id = models.BigIntegerField()
	user_id = models.BigIntegerField()
	is_join = models.BooleanField(default=True)
	create_time = models.IntegerField()
	update_time = models.IntegerField()

	class Meta:
		db_table = 'participate_tab'
		app_label = 'activitylib'
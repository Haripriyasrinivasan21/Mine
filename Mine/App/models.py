from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
	img= models.ImageField(upload_to='Profiles/',default="profile.png")
	dob=models.DateField(null=True,blank=True)
	g=[('Male','Male'),('Female','Female')]
	gender=models.CharField(max_length=10,choices=g,null=True,blank=True)
	ph_no=models.CharField(max_length=10)
	pan_no=models.CharField(max_length=10,null=True,blank=True)
	address=models.CharField(max_length=100)
	postal_code=models.CharField(max_length=7)
	city=models.CharField(max_length=20)
	state=models.CharField(max_length=20,default='Andhra Pradesh')
	country=models.CharField(max_length=20,default='India')
	idgen = models.TextField(blank=True)
	p=[(1,'Donor'),(2,'Organisation'),(3,'Guest')]
	role=models.IntegerField(choices=p,default=3)

class Rolrq(models.Model):
	r = [(1,'Donor'),(2,'Organisation')]
	uname = models.CharField(max_length=50)
	roltype = models.IntegerField(choices=r,default=0)
	random_id=models.CharField(max_length=20)
	is_checked = models.BooleanField(default=0)
	ud = models.OneToOneField(User,on_delete=models.CASCADE)

class Orgdetails(models.Model):
	org_name=models.CharField(max_length=50,default="Organisation Name")
	org_email=models.EmailField(max_length=50)
	found_name=models.CharField(max_length=50,default="Founder Name")
	est_date=models.DateField(null=True)
	no_of_childrens=models.IntegerField(default=0)
	us=models.OneToOneField(User,on_delete=models.CASCADE)

class Donate(models.Model):
	d=[('Select',"Select"),('Yearly',"Yearly Once"),('Monthly',"Monthly Once"),('Quarterly',"Quarterly Once"),('One Time',"One time donation")]
	s=[('Select',"Select"),('Food',"Food"),('Clothes',"Clothes"),('Money',"Money")]
	username=models.CharField(max_length=50)
	email=models.EmailField(max_length=50)
	ways_to_donate=models.CharField(max_length=50,choices=d,default='Select')
	donating_to=models.CharField(max_length=50)
	sponsor_way=models.CharField(max_length=50,choices=s,default='Select')
	donating_date=models.DateField()
	uid=models.ForeignKey(User,on_delete=models.CASCADE)

class OccDonate(models.Model):
	s=[('Select',"Select"),('Food',"Food"),('Clothes',"Clothes"),('Money',"Money")]
	username=models.CharField(max_length=50)
	email=models.EmailField(max_length=50)
	donating_way=models.CharField(max_length=50,default='On Occasion')
	occ_name=models.CharField(max_length=100)
	donating_to=models.CharField(max_length=50)
	sponsor_way=models.CharField(max_length=50,choices=s,default='Select')
	donating_on=models.DateField()
	uid=models.ForeignKey(User,on_delete=models.CASCADE)

class Child_details(models.Model):
	child_name = models.CharField(max_length=50)
	c=[('Female','Female'),('Male','Male'),('Select','Select Your Gender')]
	child_gen=models.CharField(max_length=10,choices=c,default='Select')
	child_dob=models.DateField(null=True)
	child_age = models.CharField(max_length=10)
	joining_date = models.DateField(null=True)
	yrs_stayed = models.CharField(max_length=30)
	exit_date = models.CharField(max_length=50,default="Not Yet Exited")
	chimg= models.ImageField(upload_to='Children_profiles/',default="profile.png")
	about = models.CharField(max_length=500)
	ch = models.ForeignKey(User,on_delete=models.CASCADE)

class Worker_details(models.Model):
	worker_name = models.CharField(max_length=50)
	w=[('Female','Female'),('Male','Male'),('Select','Select Your Gender')]
	worker_gen=models.CharField(max_length=10,choices=w,default='Select')
	worker_dob=models.DateField(null=True)
	worker_age = models.CharField(max_length=10)
	worker_ph=models.CharField(max_length=20)
	worker_add=models.CharField(max_length=100)
	working_as = models.CharField(max_length=100)
	joining_date = models.DateField(null=True)
	yrs_worked = models.CharField(max_length=30)
	exit_date = models.CharField(max_length=50,default="Not Yet Exited")
	worimg= models.ImageField(upload_to='Worker_profiles/',default="profile.png")
	salary = models.CharField(max_length=100)
	wor = models.ForeignKey(User,on_delete=models.CASCADE)

class Donor_info(models.Model):
	donor_name = models.CharField(max_length=50)
	donor_email=models.EmailField(max_length=50)
	donated_thing = models.CharField(max_length=100)
	donated_on = models.DateField(null=True)
	used_for = models.CharField(max_length=200)
	rep= models.ImageField(upload_to='Receipts/',default="receipt.png")
	don = models.ForeignKey(User,on_delete=models.CASCADE)


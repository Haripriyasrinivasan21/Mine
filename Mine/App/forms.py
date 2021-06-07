from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django import forms
from App.models import User,Rolrq,Orgdetails,Donate,OccDonate,Child_details,Worker_details,Donor_info

class UsrReg(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control-plaintext my-2","placeholder":"Password"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control-plaintext my-2","placeholder":"Confirm Password"}))	
	class Meta:
		model = User
		fields = ["username","email"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control-plaintext my-2",
			"placeholder":"Username",
			}),
		"email":forms.EmailInput(attrs={
			"class":"form-control-plaintext my-2",
			"placeholder":"Email Id",
			}),
		}

class PrfUpd(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username","email","dob","gender","ph_no","pan_no","address","city","postal_code","state","country","img"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"readOnly":True,
			}),
		"email":forms.EmailInput(attrs={
			"class":"form-control my-2",
			}),
		"dob":forms.DateInput(attrs={
			"class":"form-control my-2",
			"type":"date",
			"placeholder":"select Your Date of Birth",
			}),
		"gender":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"ph_no":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Update Phone number",
			}),
		"pan_no":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Update Pan Number",
			}),
		"address":forms.Textarea(attrs={
			"class":"form-control my-2",
			"placeholder":"Update Address",
			"rows":5,
			}),
		"city":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Update City",
			}),
		"state":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Update State",
			}),
		"postal_code":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Update Postal Code",
			}),
		"country":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Update Country",
			}),
		}

class RolerqForm(forms.ModelForm):
	class Meta:
		model = Rolrq
		fields = ["uname","roltype","random_id"]
		widgets = {
		"uname":forms.TextInput(attrs={
			"class":"form-control my-2",
			"readOnly":True,
			}),
		"roltype":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"random_id":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter the id received in ur mail",
			}),
		}

class GvForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username","role"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"readOnly":True,
			}),
		"role":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		}
class OrgForm(forms.ModelForm):
	class Meta:
		model = Orgdetails
		fields = ["org_name","found_name","est_date","no_of_childrens"]
		widgets = {
		"org_name":forms.TextInput(attrs={
			"class":"form-control my-2",
			}),
		"found_name":forms.TextInput(attrs={
			"class":"form-control my-2",
			}),
		"est_date":forms.DateInput(attrs={
			"class":"form-control my-2",
			"type":"date",
			}),
		"no_of_childrens":forms.NumberInput(attrs={
			"class":"form-control",
			}),
		}

class DonateForm(forms.ModelForm):
	class Meta:
		model=Donate
		fields=["ways_to_donate","donating_to","sponsor_way","donating_date"]
		widgets={
		"ways_to_donate":forms.Select(attrs={
			"class":"form-control",
			}),
		"donating_to":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Organisation Name",
			}),
		"sponsor_way":forms.Select(attrs={
			"class":"form-control",
			}),
		"donating_date":forms.DateInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the date of donation",
			}),
		}

class OccDonateForm(forms.ModelForm):
	class Meta:
		model=OccDonate
		fields=["occ_name","donating_to","sponsor_way","donating_on"]
		widgets={
		"occ_name":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Occasion Name",
			"required":True,
			}),
		"donating_to":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Organisation Name",
			"required":True,
			}),
		"sponsor_way":forms.Select(attrs={
			"class":"form-control",
			"required":True,
			}),
		"donating_on":forms.DateInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the date of donation",
			"required":True,
			}),
		}


class Childform(forms.ModelForm):
	class Meta:
		model = Child_details
		fields = ["child_name","child_gen","child_dob","child_age","joining_date","yrs_stayed","exit_date","about","chimg"]
		widgets = {
		"child_name":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter child name",
			}),
		"child_gen":forms.Select(attrs={
			"class":"form-control",
			}),
		"child_dob":forms.DateInput(attrs={
			"class":"form-control",
			"placeholder":"DOB of the child",
			}),
		"child_age":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter child's age",
			}),
		"joining_date":forms.DateInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the joining date of the child",
			}),
		"yrs_stayed":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the no.of.yrs child stayed"
			}),
		"exit_date":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the date the child exited",
			}),
		"about":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter any infomation of the child",
			}),
		}


class Workerform(forms.ModelForm):
	class Meta:
		model = Worker_details
		fields = ["worker_name","worker_gen","worker_dob","worker_age","worker_ph","worker_add","working_as","joining_date","yrs_worked","exit_date","salary","worimg"]
		widgets = {
		"worker_name":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter worker name",
			}),
		"worker_gen":forms.Select(attrs={
			"class":"form-control",
			}),
		"worker_dob":forms.DateInput(attrs={
			"class":"form-control",
			"placeholder":"DOB of the worker",
			}),
		"worker_age":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter worker's age",
			}),
		"worker_ph":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the ph.no of the worker"
			}),
		"worker_add":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the address of the worker"
			}),
		"working_as":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter worker occupation",
			}),
		"joining_date":forms.DateInput(attrs={
			"class":"form-control",
			"placeholder":"Joining date of the worker",
			}),
		"yrs_worked":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"No.of.yrs worker worked"
			}),
		"exit_date":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the date the worker exited",
			}),
		"salary":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter any salary of the worker",
			}),
		}

class Donorinfoform(forms.ModelForm):
	class Meta:
		model = Donor_info
		fields = ["donor_name","donor_email","donated_thing","donated_on","used_for"]
		widgets = {
		"donor_name":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter donor name",
			}),
		"donor_email":forms.EmailInput(attrs={
			"class":"form-control",
			"placeholder":"Enter donor's Email Id",
			}),
		"donated_thing":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the donated value",
			}),
		"donated_on":forms.DateInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the date of donation",
			}),
		"used_for":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter the usage",
			}),
		}

class ChpasForm(PasswordChangeForm):
	old_password=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control",
		"placeholder":"Enter Old password"
		}))
	new_password1=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control",
		"placeholder":"Enter New password"
		}))
	new_password2=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control",
		"placeholder":"Confirm New password"
		}))

	class Meta:
		model=User
		fields=['oldpassword','newpassword','confirmpassword']



from django.shortcuts import render,redirect
from App.forms import UsrReg,PrfUpd,RolerqForm,GvForm,OrgForm,DonateForm,OccDonateForm,ChpasForm,Childform,Workerform
from App.models import User,Rolrq,Orgdetails,Donate,OccDonate,Child_details,Worker_details
from django.core.mail import send_mail
from Hari import settings
import secrets
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib import messages
# Create your views here.

def home(request):
	return render(request,'html/home.html')

def register(request):
	if request.method == "POST":
		k = UsrReg(request.POST)
		if k.is_valid():
			m = k.save(commit=False)
			m.idgen = secrets.token_hex(3)
			sb = "Registration Confirmation Email"
			mg = "Hi Welcome {}. You have successfully registered in Children Welfare Portal.Your ID is {}, You can use this ID during your Role Request.".format(m.username,m.idgen)
			sd = settings.EMAIL_HOST_USER
			snt = send_mail(sb,mg,sd,[m.email])
			if snt == 1:
				m.save()
				return redirect('/lgi')
			else:
				return redirect('/')
		password1=request.POST.get('password1')
		password2=request.POST.get('password2')

		user=authenticate(request,password1=password1,password2=password2)
		if not user:
			messages.add_message(request,messages.WARNING,'Passwords are not matching, Please Enter the Passwords Correctly...')
			return render(request,'html/register.html',{'f':k})
	k = UsrReg()
	return render(request,'html/register.html',{'f':k})

def mainpage(request):
	h=Donate.objects.filter(uid_id=request.user.id)
	o=OccDonate.objects.filter(uid_id=request.user.id)
	ru=User.objects.all()
	t = Orgdetails.objects.filter(us_id=request.user.id)
	y = Donate.objects.all()
	p = []
	for b in y:
		p.append(b.uid_id)
	m = {}
	for n in h:
		if n.uid_id in p:
			m[n.id] = n.id,n.username,n.donating_to,n.uid_id
	z = {}
	tr = User.objects.all()
	for j in tr:
		for c in m.values():
			if j.id == c[3]:
				z[j.id]=c[1],c[2],j.img.url
	rk = Orgdetails.objects.all()
	p = []
	for b in rk:
		p.append(b.us_id)
	m = {}
	for n in t:
		if n.us_id in p:
			m[n.id] = n.id,n.org_name,n.us_id
	x = {}
	tr = User.objects.all()
	for j in tr:
		for c in m.values():
			if j.id == c[2]:
				x[j.id]=c[1],j.img.url
	return render(request,'html/main.html',{'h':h,'o':o,'ru':ru,'s':z.values(),'b':x.values()})

def visible(request):
	t = Orgdetails.objects.get(us_id=request.user.id)
	s = Donate.objects.filter(donating_to=t.org_name)
	y = Donate.objects.all()
	p = []
	for b in y:
		p.append(b.uid_id)
	m = {}
	for n in s:
		if n.uid_id in p:
			m[n.id] = n.id,n.username,n.donating_to,n.uid_id
	z = {}
	tr = User.objects.all()
	for j in tr:
		for c in m.values():
			if j.id == c[3]:
				z[j.id]=c[1],c[2],j.img.url
	oc= OccDonate.objects.filter(donating_to=t.org_name)
	q = OccDonate.objects.all()
	p = []
	for b in q:
		p.append(b.uid_id)
	m = {}
	for n in oc:
		if n.uid_id in p:
			m[n.id] = n.id,n.username,n.donating_to,n.uid_id
	h = {}
	ab = User.objects.all()
	for i in ab:
		for c in m.values():
			if i.id == c[3]:
				h[i.id]=c[1],c[2],i.img.url
	# print(z)
	return render(request,'html/main.html',{'s':s,'oc':oc,'t':z.values(),'h':h.values()})

def profile(request):
	return render(request,'html/profile.html')

def updpfle(request):
	f = User.objects.get(id=request.user.id)
	v = Orgdetails.objects.get(us_id=request.user.id)
	if request.method == "POST":
		z = PrfUpd(request.POST,request.FILES,instance=f)
		s = OrgForm(request.POST,instance=v)
		if z.is_valid() or s.is_valid():
			z.save()
			s.save()
			return redirect('/pfe')
	z = PrfUpd(instance=f)
	s = OrgForm(instance=v)
	return render(request,'html/updpfle.html',{'x':z,'k':s})


def rolereq(request):
	if request.method == "POST":
		m = RolerqForm(request.POST)
		if m.is_valid():
			z=m.save(commit=False)
			z.ud_id = request.user.id
			if z.roltype == 1:
				r="Donor"
			else:
				r="Organisation"
			sb = "Role Request Confirmation"
			mg = "Hi Welcome {}, You have requested for the role {}, You will be assigned your requested role ASAP. Till then Stay Tuned :)".format(z.uname,r)
			sd = settings.EMAIL_HOST_USER
			snt = send_mail(sb,mg,sd,[request.user.email,settings.ADMINS[0][1]])
			if snt == 1:
				z.save()
				return redirect('/main')
			else:
				return redirect('/')
	m = RolerqForm()
	return render(request,'html/rolereq.html',{'n':m})

def gvper(request):
	m = User.objects.all()
	n = Rolrq.objects.all()
	p,s = [],{}
	for i in m:
		p.append(i.id)
	for j in m:
		if j.id not in p or j.is_superuser:
			continue
		else:
			q = Rolrq.objects.get(ud_id=j.id)
			s[j.id] = j.username,q.roltype,q.random_id,j.role,j.id
	return render(request,'html/giveperm.html',{'v':s.values()})

def aprvrl(request,t):
	s = User.objects.get(id=t)
	h = Rolrq.objects.get(ud_id=t)
	if request.method == "POST":
		y = GvForm(request.POST,instance=s)
		if y.is_valid():
			h.is_checked = 1
			h.save()
			a=y.save(commit=False)
			if a.role == 1:
				r="Donor"
			elif a.role == 3:
				r="Guest"
			else:
				r="Organisation"
			sb = "Requested Role Assigned"
			mg = "Hi {}, You have been assigned the role {}, You can Login now to avail Services, Thank you :)".format(a.username,r)
			sd = settings.EMAIL_HOST_USER
			snt = send_mail(sb,mg,sd,[s.email,settings.ADMINS[0][1]])
			if snt == 1:
				a.save()
				return redirect('/gvperm')
			else:
				return redirect('/')
	y = GvForm(instance=s)
	return render(request,'html/aprorl.html',{'a':y})

def orgform(request):
	if request.method == "POST":
		k = OrgForm(request.POST)
		if k.is_valid():
			n = k.save(commit=False)
			n.us_id = request.user.id
			n.save()
			return redirect('/pfe')
	k = OrgForm()
	return render(request,'html/orgentry.html',{'g':k})

def dnrpfle(request):
	f = User.objects.get(id=request.user.id)
	if request.method == "POST":
		z = PrfUpd(request.POST,request.FILES,instance=f)
		if z.is_valid():
			z.save()
			messages.success(request,"Profile updated Successfully")
			return redirect('/pfe')
	z = PrfUpd(instance=f)
	return render(request,'html/dnrpfle.html',{'x':z})


def donate(request):
	if request.method == "POST":
		e=DonateForm(request.POST)
		f=OccDonateForm(request.POST)
		if e.is_valid():
			t=e.save(commit=False) 
			t.username=request.user.username
			t.email=request.user.email
			t.uid_id=request.user.id
			t.save()
			return redirect('/main')
		elif f.is_valid():
			r=f.save(commit=False)
			r.username=request.user.username
			r.email=request.user.email
			r.uid_id=request.user.id
			r.save() 
			return redirect('/main')    
	e=DonateForm()
	f=OccDonateForm()
	return render(request,'html/donate.html',{'a':e,'b':f})

def update(request,a):
	u=Donate.objects.get(id=a)
	if request.method == "POST":
		v=DonateForm(request.POST,instance=u)
		if v.is_valid():
			v.save()
			return redirect('/dontab1')
	z=DonateForm(instance=u)
	return render(request,'html/update.html',{'p':z})

def delete(request,b):
	c=Donate.objects.get(id=b)
	if request.method == "POST":
		c.delete()
		return redirect('/main')
	return render(request,'html/userdelete.html',{'d':c})

def message(request,m):
	s=Donate.objects.get(id=m)
	return render(request,'html/message.html',{'q':s})

def occdetails(request,bi):
	o=OccDonate.objects.get(id=bi)
	if request.method == "POST":
		p=OccDonateForm(request.POST,instance=o)
		if p.is_valid():
			p.save()
			return redirect('/dontab2')
	q=OccDonateForm(instance=o)
	return render(request,'html/occdetails.html',{'q':q})

def occdelete(request,ai):
	d=OccDonate.objects.get(id=ai)
	if request.method == "POST":
		d.delete()
		return redirect('/main')
	return render(request,'html/userdelete.html',{'d':d})

def occmsg(request,om):
	m=OccDonate.objects.get(id=om)
	return render(request,'html/occmessage.html',{'o':m})

def details(request):
	q=Orgdetails.objects.all()
	return render(request,'html/details.html',{'q':q})

def joinus(request):
	if request.method=="POST":
		u=request.POST.get('uname')
		e=request.POST.get('email')
		p=request.POST.get('ph')
		ms=request.POST.get('msg')
		o=request.POST.get('oname')
		oe=request.POST.get('oemail')
		a="Hi "+o+",""<br/>" "The user "+u+", wanted to join your organisation.""<br/>"" Their Email ID is "+e+ " and their Phone Number is "+p+"<br/>""They have also sent you a message..."+ms+"<br/>"" Please get back to them ASAP :)" 
		t = EmailMessage("Joining us",a,settings.EMAIL_HOST_USER,[oe])
		t.content_subtype='html'
		t.send()
		if t==1:
			return redirect('/jmsg')
		else:
			return redirect('/jmsg')
	return render(request,'html/joinus.html')

def joinmsg(request):
	return render(request,'html/joinmsg.html')

def childinfo(request):
	if request.method == "POST":
		c=Childform(request.POST,request.FILES)
		if c.is_valid():
			l=c.save(commit=False)
			l.username=request.user.username
			l.email=request.user.email
			l.ch_id=request.user.id
			l.save()
			return redirect('/dash')
	c=Childform()
	return render(request,'html/childinfo.html',{'c':c})

def childtable(request):
	h = Child_details.objects.filter(ch_id=request.user.id)
	return render(request,'html/childtable.html',{'h':h})


def childupdate(request,cu):
	ch=Child_details.objects.get(id=cu)
	if request.method == "POST":
		x=Childform(request.POST,instance=ch)
		if x.is_valid():
			x.save()
			return redirect('/dash')
	c=Childform(instance=ch)
	return render(request,'html/chupdate.html',{'c':c})

def childdelete(request,cd):
	d=Child_details.objects.get(id=cd)
	if request.method == "POST":
		d.delete()
		return redirect('/dash')
	return render(request,'html/orgdelete.html',{'d':d})

def childview(request,cv):
	shu=Child_details.objects.get(id=cv)
	return render(request,'html/childview.html',{'sh':shu})

def workerview(request,wv):
	dha=Worker_details.objects.get(id=wv)
	return render(request,'html/workerview.html',{'dh':dha})

def workerinfo(request):
	if request.method == "POST":
		w=Workerform(request.POST,request.FILES)
		if w.is_valid():
			k=w.save(commit=False)
			k.username=request.user.username
			k.email=request.user.email
			k.wor_id=request.user.id
			k.save()
			return redirect('/dash')
	w=Workerform()
	return render(request,'html/workerinfo.html',{'w':w})

def workertable(request):
	r = Worker_details.objects.filter(wor_id=request.user.id)
	return render(request,'html/workertable.html',{'r':r})

def workerupdate(request,wu):
	wo=Worker_details.objects.get(id=wu)
	if request.method == "POST":
		y=Workerform(request.POST,instance=wo)
		if y.is_valid():
			y.save()
			return redirect('/dash')
	w=Workerform(instance=wo)
	return render(request,'html/worupdate.html',{'w':w})

def workerdelete(request,wd):
	d=Worker_details.objects.get(id=wd)
	if request.method == "POST":
		d.delete()
		return redirect('/dash')
	return render(request,'html/orgdelete.html',{'d':d})

def donorinfo(request):
	if request.method == "POST":
		u=request.POST.get('uname')
		e=request.POST.get('email')
		d=request.POST.get('dtype')
		da=request.POST.get('ddate')
		us=request.POST.get('usage')
		f=request.FILES['fe']
		a="Hi " +u+"," "<br/>" "First of all we wanted to Thankyou on behalf of our Organisation for your generosity in donating "+d+" to our Organisation on "+da+".""<br/>""We just wanted to let you know how much help did your donation made...""<br/>""Usage of you Donation: "+us+".""<br/>""Here we are attesting you the 'TAX EXEMPTIONABLE RECEIPT'""<br/>""We appreciate your support...THANK YOU :)"
		t = EmailMessage("Donation Usage and Invoice",a,settings.EMAIL_HOST_USER,[settings.ADMINS[0][1],e,request.user.email])
		t.content_subtype='html'
		t.attach(f.name,f.read(),f.content_type)
		t.send()
		if t==1:
			return redirect('/vis')
		else:
			return redirect('/vis')
	return render(request,'html/donorinfo.html')

def change(request):
	if request.method == "POST":
		g=ChpasForm(user=request.user,data=request.POST)
		if g.is_valid():
			g.save()
			return redirect('/lgi')
	g=ChpasForm(user=request)
	return render(request,'html/changepassword.html',{'c':g})

def dashboard(request):
	ch=Child_details.objects.filter(ch_id=request.user.id)
	wor=Worker_details.objects.filter(wor_id=request.user.id)
	return render(request,'html/dashboard.html',{'ch':ch,'wor':wor})

def donationtable1(request):
	w=Donate.objects.filter(uid_id=request.user.id)
	return render(request,'html/dontab1.html',{'x':w})


def donationtable2(request):
	z=OccDonate.objects.filter(uid_id=request.user.id)
	return render(request,'html/dontab2.html',{'h':z})

def orgtable1(request):
	od = Donate.objects.filter(uid_id=request.user.id)
	g = Donate.objects.all()
	k={}
	for m in g:
		k[m.id]=m.id,m.username,m.ways_to_donate,m.donating_to,m.sponsor_way,m.donating_date
	f=k.values() 
	return render(request,'html/orgtab1.html',{'f':f})


def orgtable2(request):
	oo=OccDonate.objects.filter(uid_id=request.user.id)
	h =OccDonate.objects.all()
	k={}
	for m in h:
		k[m.id]=m.id,m.username,m.donating_way,m.occ_name,m.donating_to,m.sponsor_way,m.donating_on
	i=k.values() 
	return render(request,'html/orgtab2.html',{'i':i})


def information(request):
	d=Donate.objects.all()
	o=OccDonate.objects.all()
	return render(request,'html/information.html',{'d':d,'o':o})

def contactus(request):
	if request.method=="POST":
		u=request.POST.get('uname')
		e=request.POST.get('email')
		ms=request.POST.get('msg')
		a="Hi Organiser,""<br/>" "I "+u+" wanted to know about "+ms+".""<br/>" "Please let me know the details soon..!!" 
		t = EmailMessage("Contacting Us",a,settings.EMAIL_HOST_USER,[settings.ADMINS[0][1],e])
		t.content_subtype='html'
		t.send()
		if t==1:
			return redirect('/main')
		else:
			return redirect('/main')
	return render(request,'html/contactus.html')

def aboutus(request):
	return render(request,'html/aboutus.html')

def paymentdon(request,pd):
	d=Donate.objects.get(id=pd)
	if request.method == "POST":
		v=DonateForm(request.POST,instance=d)
		if v.is_valid():
			v.save()
			return redirect('/pm')
	p=DonateForm(instance=d)
	return render(request,'html/paymentdon.html',{'p':p})

def paymentocc(request,po):
	s=OccDonate.objects.get(id=po)
	if request.method == "POST":
		c=OccDonateForm(request.POST,instance=s)
		if c.is_valid():
			c.save()
			return redirect('/pm')
	o=OccDonateForm(instance=s)
	return render(request,'html/paymentocc.html',{'o':o})


def Login_valid(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(request,username=username,password=password)

		if not user:
			messages.add_message(request,messages.INFO,'Invalid Credentials, Please Enter the valid Details...')
			return render(request,'html/login.html')
		else:
			login(request,user)
			messages.add_message(request,messages.SUCCESS,f'Welcome {user.username}, Have a good time :)')
			return redirect('/main')
	return render(request,'html/login.html')

def feedback(request):
	if request.method=="POST":
		u=request.POST.get('uname')
		e=request.POST.get('email')
		msg=request.POST.get('ms')
		a="User "+u+", bearing Email ID "+e+".""<br/>" "Has sent you a Feedback as "+msg+"." "<br/>" "Hope this helps...!!!" 
		t = EmailMessage("Feedback",a,settings.EMAIL_HOST_USER,[settings.ADMINS[0][1],e])
		t.content_subtype='html'
		t.send()
		if t==1:
			return redirect('/tq')
		else:
			return redirect('/tq')
	return render(request,'html/feedback.html')

def thankyou(request):
	return render(request,'html/thankyou.html')

def paymsg(request):
	return render(request,'html/paymsg.html')
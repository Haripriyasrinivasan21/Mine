from django.shortcuts import render,redirect
from App.forms import UsrReg,PrfUpd,RolerqForm,GvForm,OrgForm,DonateForm,OccDonateForm,ChpasForm,Childform,Workerform,Donorinfoform
from App.models import User,Rolrq,Orgdetails,Donate,OccDonate,Child_details,Worker_details,Donor_info
from django.core.mail import send_mail
from Hari import settings
import secrets
from django.core.mail import EmailMessage
from django.http import HttpResponse
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
	k = UsrReg()
	return render(request,'html/register.html',{'f':k})

def mainpage(request):
	h=Donate.objects.filter(uid_id=request.user.id)
	o=OccDonate.objects.filter(uid_id=request.user.id)
	return render(request,'html/main.html',{'h':h,'o':o})


def visible(request):
	t = Orgdetails.objects.get(us_id=request.user.id)
	s = Donate.objects.filter(donating_to=t.org_name)
	oc= OccDonate.objects.filter(donating_to=t.org_name)
	return render(request,'html/main.html',{'s':s,'oc':oc})

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
			y.save()
			return redirect('/gvperm')
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
			return redirect('/don')
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
			return redirect('/don')
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
		a="Hi "+u+",""<br/>" "You requested to join the organisation "+o+".""<br/>" "They will get back to you shortly..!!" 
		t = EmailMessage("Joining us",a,settings.EMAIL_HOST_USER,[settings.ADMINS[0][1],e])
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
	n=Donor_info.objects.filter(don_id=request.user.id)
	if request.method == "POST":
		d=Donorinfoform(request.POST)
		if d.is_valid():
			o=d.save(commit=False)
			o.username=request.user.username
			o.email=request.user.email
			o.don_id=request.user.id
			o.save()
			return redirect('/doninfo')
	d=Donorinfoform()
	return render(request,'html/donorinfo.html',{'d':d,'n':n})

def donorinfoupdate(request,du):
	do=Donor_info.objects.get(id=du)
	if request.method == "POST":
		z=Donorinfoform(request.POST,instance=do)
		if z.is_valid():
			z.save()
			return redirect('/doninfo')
	p=Donorinfoform(instance=do)
	return render(request,'html/donorinfoupdate.html',{'p':p})

def donorinfodelete(request,dd):
	d=Donor_info.objects.get(id=dd)
	if request.method == "POST":
		d.delete()
		return redirect('/doninfo')
	return render(request,'html/orgdelete.html',{'d':d})


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
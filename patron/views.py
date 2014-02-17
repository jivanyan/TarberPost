
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from patron.forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


def main(request):
	context = RequestContext(request)
	uf = UserForm()
        pf = PatronForm()
	uc = Patron.objects.all().count()
	bc = Bid.objects.all().count()
	return render_to_response('main.html',{'uf':uf, 'pf':pf,'uc':uc, 'bc':bc},context)

#login_required
def homepage(request):
	context = RequestContext(request)
        p = Patron.objects.get(user = request.user)
	all_bids = []
	if request.method == 'POST':
		bf = BidForm(request.POST)
		if bf.is_valid():
			bid = bf.save(commit = False)
			bid.patron = p
			bid.status = 0
			bid.save()	
		else:
			print bf.errors
	else:
		bf = BidForm()
	all_bids = p.all_bids.all() #Bid.objects.filter(patron = p)
	return render_to_response('patron/profile.html',{'bid_form':bf, 'bids':all_bids},context)

def signup(request):
	context = RequestContext(request)
	registered = False
	print ".............{0}".format(request.method)
	if request.method == 'POST':	
		uf = UserForm(data = request.POST)
		pf = PatronForm(data = request.POST)
		print request.POST
		if uf.is_valid() and pf.is_valid():
			user = uf.save(commit = False)
			user.set_password(user.password)
			user.save()
			profile = pf.save(commit = False)
			profile.user = user
			profile.save()
			registered = True
                	print ">>>>>>>>>{0}-{1}".format(user.username,user.password)
			return HttpResponseRedirect(reverse('homepage'))
		else:
			return HttpResponse("{0},{1}".format(uf.errors, pf.errors))
	else:
		return HttpResponse("Something wrong has happened")

def login(request):
	context = RequestContext(request)
	next1 = ""
	print ">>>>>>>>>>>>>>>"
	if request.GET:
		next1 = request.GET['next']
	if request.method == 'POST':
		print ">>>>>>>>>>>>>>>{0}".format(request.POST)
		#next = request.['next']
		username = request.POST['username']
		password = request.POST['password']
		print ">>>>>>>>>{0}-{1}".format(username, password)
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				print ">>>>>>>>>>>>> Loged"
				return HttpResponseRedirect(reverse('homepage'))
			else:
				return HttpResponse("Your account is disabled")		
		else:
			return HttpResponse("Invalid Login details {0}, {1}".format(username, password))
	else:
		print next1
		return HttpResponseRedirect(next1)	
	
@login_required
def logout(request):
    # Since we know the user is logged in, we can now just log them out.
    auth_logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


def search_bids(sp = '', ep = ''):
	kwargs = {}	
	if sp:
		kwargs['startpoint__startswith'] = sp
	if ep:
		kwargs['endpoint__startswith'] = ep
	bids = Bid.objects.filter( **kwargs )
	return bids	 

def suggest_bids(request):
	context = RequestContext(request)
	print ">>>>> Called"
	bids = []
	sp, ep = '',''
	if request.is_ajax():
		print ">>>AJAX>>>"
	if request.method == 'GET':
		sp = request.GET['sp']
		ep = request.GET['ep']
	print "---{0}---{1}---".format(sp,ep)
	bids = search_bids(sp, ep)
	print "-----------BIDS"
	x = render_to_response('bids.html', {'tbids':bids},context)
	print x
	return x
		

import email
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import News
from datetime import datetime, date, timedelta
from .dataInserter import insertNewsData

# Create your views here.
def loginUser(request):
    """
    This function is for authenticating users to access data
    """
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('notification-dashboard', pk=1)
        else:
            print("Wrong Credentials")
            return render(request, "login.html")
    else:
        print("final else block working")
        if request.user.is_authenticated:
            return redirect('notification-dashboard', pk=1)

        else:
            return render(request, "login.html")

    
def dashboard(request, pk):
    """
    This function for notification dashboard
    """
    # insertNewsData()
    # print(pk)
    if request.user.is_anonymous:
        return redirect('login')
    else:
        totalNewsData = News.objects.all()
        if pk==1:
            newsData = totalNewsData.filter(reportedAt__date=date.today())
        else:
            newsData = totalNewsData.filter(reportedAt__date=date.today()- timedelta(days = pk - 1))
        pages = [i for i in range(1,15)]

        newsWebsites = []
        for j in totalNewsData:
            if j.source not in newsWebsites:
                newsWebsites.append(j.source)

        print(newsWebsites)

        return render(request, "home.html", {"data": newsData, "currentPath": request.path.rsplit("/", 2)[0], "pages": pages, "currentPage": pk, "newsWebsites": newsWebsites})


def logoutUser(request):
    """
    This function is for logging out user
    """
    logout(request)
    return redirect("login")


def searchDashboard(request):
    """
    This function is for providing search functionality in dashboard
    """
    if request.user.is_anonymous:
        return redirect('login')
    else:
        totalNewsData = News.objects.all()
        newsWebsites = []
        for j in totalNewsData:
            if j.source not in newsWebsites:
                newsWebsites.append(j.source)

        searchedText = request.GET.get("search_query")
        print(type(searchedText))
        newsData = News.objects.filter(Q(source__icontains=searchedText) | Q(headline__icontains=searchedText)
                                | Q(reportedAt__icontains=searchedText) )

        # from textblob import TextBlob
        # data = []
        # for i in newsData:
        #     blob = TextBlob(i.headline)
        #     if searchedText in blob.noun_phrases:
        #         print(i.id, i.headline)
        #         data.append(i)
        # print(data)
        return render(request, "search.html", {"data": newsData, "newsWebsites": newsWebsites})
    

def filteredDashboard(request, pk, website):
    """
    This function is for showing filtered data on dashboard for a specific source
    """
    # print(pk, website)
    if request.user.is_anonymous:
        return redirect('login')
    else:
        totalNewsData = News.objects.all()
        data = totalNewsData.filter(source=website)
        print(data)
        if pk==1:
            newsData = data.filter(reportedAt__date=date.today())
        else:
            newsData = data.filter(reportedAt__date=date.today()- timedelta(days = pk - 1))
        pages = [i for i in range(1,15)]

        newsWebsites = []
        for j in totalNewsData:
            if j.source not in newsWebsites:
                newsWebsites.append(j.source)

        print(request.path.rsplit("/", 2)[0])
        return render(request, "home.html", {"data": newsData, "currentPath": request.path.rsplit("/", 2)[0], "pages": pages, "currentPage": pk, "newsWebsites": newsWebsites})
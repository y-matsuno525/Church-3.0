from django.shortcuts import render

#メニューを表示するだけ
def menu(request):

    return render(request,"menu/menu.html")
from django.shortcuts import render
from .models import Bible,Book,Chapter,Verse
from django.http import JsonResponse
from django.template.loader import render_to_string

#メニューを表示するだけ
def menu(request):

    #左側メニュー
    #欲しいクエリセットを取得
    bible = Bible.objects.filter(version="JCO").first()
    books = Book.objects.filter(bible=bible)

    params = {
        "books" : books
    }
    

    return render(request,"menu/menu.html",params)

#ajaxによる聖書のverse取得
def get_verses(request):

    book_id = request.GET.get("book_id")
    book = Book.objects.filter(id=book_id)
    chapters = Chapter.objects.filter(book=book)
    
    # 各Chapterに関連するVerseを取得し、テキストをまとめる
    chapter_data = []
    for chapter in chapters:
        verses = Verse.objects.filter(chapter=chapter).order_by('verse_number')
        chapter_data.append({
            "chapter_number": chapter.chapter_number,
            "verses": [{"verse_number": v.verse_number, "text": v.text} for v in verses]
        })
    
    # HTMLテンプレートをレンダリングして返す
    html = render_to_string("menu/menu.html", {
        "book": book,
        "chapter_data": chapter_data,
    })

    return JsonResponse({"html": html})
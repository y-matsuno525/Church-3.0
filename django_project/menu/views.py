from django.shortcuts import render
from .models import Bible,Book,Chapter,Verse,ForumPost
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

# Ajaxによる聖書のVerse取得
def get_verses(request):
    # book_idを取得
    book_id = request.GET.get("book_id")

    if not book_id:  # book_idが指定されていない場合
        return JsonResponse({"error": "Book ID is required"}, status=400)

    try:
        # Bookの取得
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:  # 存在しない場合のエラーハンドリング
        return JsonResponse({"error": "Book not found"}, status=404)

    # Chapterおよび関連するVerseの取得
    chapters = Chapter.objects.filter(book=book).order_by('chapter_number')
    chapter_data = []

    for chapter in chapters:
        verses = Verse.objects.filter(chapter=chapter).order_by('verse_number')
        chapter_data.append({
            "chapter_number": chapter.chapter_number,
            "verses": [{"verse_number": v.verse_number, "text": v.text} for v in verses]
        })

    # HTMLテンプレートをレンダリングして返す
    html = render_to_string("menu/content.html", { #ajaxレスポンス用のhtml(content.html)を別で作ればいい。面白い！
        "book": book,
        "chapter_data": chapter_data,
    })

    return JsonResponse({"html": html})

def get_forum_posts(request):
    verse_id = request.GET.get("verse_id")

    if not verse_id:  # Verse IDが指定されていない場合
        return JsonResponse({"error": "Verse ID is required"}, status=400)

    try:
        # Verseを取得
        verse = Verse.objects.get(id=verse_id)
    except Verse.DoesNotExist:  # 該当するVerseが存在しない場合
        return JsonResponse({"error": "Verse not found"}, status=404)

    # Verseに関連する掲示板投稿を取得
    forum_posts = ForumPost.objects.filter(verse=verse).order_by("-created_at")

    # 掲示板内容をレンダリング
    html = render_to_string("menu/forum_posts.html", {
        "verse": verse,
        "forum_posts": forum_posts,
    })

    return JsonResponse({"html": html})
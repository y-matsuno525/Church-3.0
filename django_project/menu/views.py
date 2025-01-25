from django.shortcuts import render,get_object_or_404
from .models import Bible,Book,Chapter,Verse,VerseAnnotation,VerseAnnotationFavorite,VerseFavorite,VerseQuestion,VerseAnswer,VerseAnswerFavorite
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import AnnotationForm,VerseQuestionForm,VerseAnswerForm

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
            "verses": [{"verse_number": v.verse_number, "text": v.text, "id": v.id} for v in verses]
        })

    # HTMLテンプレートをレンダリングして返す
    html = render_to_string("menu/content.html", { #ajaxレスポンス用のhtml(content.html)を別で作ればいい。面白い！
        "book": book,
        "chapter_data": chapter_data,
    })

    return JsonResponse({"html": html})



def get_verse_annotations(request):
    try:
        verse_id = request.GET.get("verse_id")
        print(type(verse_id))
        if not verse_id:
            return JsonResponse({"error": "invalid Verse ID"}, status=400)
        verse_id = int(verse_id)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid Verse ID"}, status=400)

    if not verse_id:  # Verse IDが指定されていない場合
        return JsonResponse({"error": "Verse ID is required"}, status=400)

    try:
        #Verseを取得
        verse = Verse.objects.get(id=verse_id)
    except Verse.DoesNotExist:  # 該当するVerseが存在しない場合
        return JsonResponse({"error": "Verse not found"}, status=404)

    # Verseに関連する注釈を取得
    annotations = VerseAnnotation.objects.filter(verse=verse).order_by("-created_at")

    # 掲示板内容をレンダリング
    html = render_to_string("menu/verse_annotations.html", {
        "verse": verse,
        "annotations": annotations,
        "form" : AnnotationForm(),
    }, request=request)

    return JsonResponse({"html": html})



def add_verse_annotation(request):

    if request.method == "POST":

        form = AnnotationForm(request.POST)
        
        if form.is_valid():

            #DBに作成されたannotationを格納

            verse_id = int(request.POST.get("verse_id"))
            content = request.POST.get("content")
            public = request.POST.get("public")
            if public == "on":
                public = True
            else:
                public = False            
            verse = get_object_or_404(Verse, id=verse_id)

            annotation = VerseAnnotation(
                verse=verse,
                user=request.user,
                content=content,
                public=public
            )
            annotation.save()

            #更新するためにもう一度レンダリング(get_verse_annotationsと同じロジック)
            annotations = VerseAnnotation.objects.filter(verse=verse).order_by("-created_at")
            print(annotations)
            html = render_to_string("menu/update_verse_annotations.html", {
                "verse": verse,
                "annotations": annotations,
                "form" : AnnotationForm(),
            }, request=request)

            print(html)

            return JsonResponse({
                "success": True,
                "html": html 
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "フォームにエラーがあります。",
                "errors": form.errors
            })
    return JsonResponse({
        "success": False,
        "message": "無効なリクエストです。"
    })

def verse_questions(request):
    verse_id = request.GET["id"]
    verse = get_object_or_404(Verse, id=verse_id)
    questions = VerseQuestion.objects.filter(verse=verse)

    params = {
        "verse" : verse,
        "questions" : questions,
    }
    return render(request,"menu/verse_questions.html",params)

def create_verse_question(request):

    verse_id = request.GET["verse_id"]
    verse = get_object_or_404(Verse, id=verse_id)

    html = render_to_string("menu/create_verse_question.html", {
        "verse": verse,
        "form" : VerseQuestionForm(),
    }, request=request)

    return JsonResponse({"html": html})

def register_verse_question(request):

    if request.method == "POST":
        try:
            verse_id = int(request.POST.get("verse_id"))
            verse = get_object_or_404(Verse, id=verse_id)
            content = request.POST.get("content")

            verse_question = VerseQuestion(
                    verse=verse,
                    user=request.user,
                    content=content,
                )
            
            verse_question.save()
            print("保存成功")
        except Exception as e:
            # 保存エラー時のログ
            print(f"Error saving VerseQuestion: {e}")

        return JsonResponse({"success": True, "message": "質問が保存されました。"})
    print("POSTじゃない")
    return JsonResponse({"success": False, "message": "無効なリクエストです。"})



#ある質問に紐付いた回答一覧を表示(あとで関数名変える。名前意味不明)
#verse_questions.htmlから来て、ある質問に対する回答一覧を生成し、verse_questions.htmlへ送り返す
def answer_verse_question(request):
    question_id = request.GET.get("question_id")
    question_id = int(question_id)

    question = get_object_or_404(VerseQuestion, id=question_id)
    answers = VerseAnswer.objects.filter(question=question)

    # 掲示板内容をレンダリング
    html = render_to_string("menu/verse_answers.html", {
        "question": question,
        "answers": answers,
        "form" : VerseAnswerForm(),
    }, request=request)

    return JsonResponse({"html": html})



#verse_answers.htmlで作成された回答を受取りDBに格納。verse_answers.htmlにJSONでsuccess:Trueを返したらサブウィンドウが閉じて、親ウィンドウは自動更新。
def add_verse_answer(request):

    if request.method == "POST":

        form = VerseAnswerForm(request.POST)
        
        if form.is_valid():

            #作成されたanswerをDBに格納

            question_id = int(request.POST.get("question_id"))
            content = request.POST.get("content")          
            question = get_object_or_404(VerseQuestion, id=question_id)

            #質問者と回答者が同じだったら保存しない
            if question.user == request.user:
                return JsonResponse({
                    "success": False,
                    "message": "質問者は回答できません"
                })

            verse_answer = VerseAnswer(
                question=question,
                user=request.user,
                content=content,
            )
            verse_answer.save()

            #更新するためにもう一度レンダリング(answer_verse_questionと同じロジック)
            answers = VerseAnswer.objects.filter(question=question).order_by("-created_at")
            html = render_to_string("menu/update_verse_questions.html", {
                "question": question,
                "answers": answers,
                "form" : VerseAnswerForm(),
            }, request=request)

            return JsonResponse({
                "success": True,
                "html": html 
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "フォームにエラーがあります。",
                "errors": form.errors
            })
    return JsonResponse({
        "success": False,
        "message": "無効なリクエストです。"
    })
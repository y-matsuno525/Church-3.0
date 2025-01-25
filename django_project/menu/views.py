from django.shortcuts import render,get_object_or_404
from .models import Bible,Book,Chapter,Verse,VerseAnnotation,VerseAnnotationFavorite,VerseFavorite,VerseQuestion,VerseAnswer,VerseAnswerFavorite
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import AnnotationForm,VerseQuestionForm,VerseAnswerForm

#メニューを表示するだけ
def menu(request):

    #左側メニューを生成
    #諸書のクエリセットを取得
    #TODO:versionを左側メニューのセレクトボックスから選べるようにする(ajax)
    bible = Bible.objects.filter(version="JCO").first()
    books = Book.objects.filter(bible=bible)

    params = {
        "books" : books
    }
    

    return render(request,"menu/menu.html",params)



# 選択した書のVerseを取得(TODO:書の章ごとのページネーションをしたい)
#menu.html から ,book_content.htmlを挿入
def get_verses(request):
    # book_idを取得
    book_id = request.GET.get("book_id")

    try:
        # Bookの取得
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:  # 存在しない場合のエラーハンドリング
        return JsonResponse({"error": "書を取得できませんでした"}, status=404)

    # ChapterとVerseの取得
    chapters = Chapter.objects.filter(book=book).order_by('chapter_number')
    chapter_data = []

    for chapter in chapters:
        verses = Verse.objects.filter(chapter=chapter).order_by('verse_number')
        chapter_data.append({
            "chapter_number": chapter.chapter_number,
            #フィールドを選んで取得している。章を取得していないことに注意。（すべてのビューでこのように必要な情報を受け取るだけにしたほうがいい？）
            "verses": [{"verse_number": v.verse_number, "text": v.text, "id": v.id} for v in verses]
        })

    # HTMLをレンダリングして返す
    html = render_to_string("menu/book_content.html", { #ajaxレスポンス用のhtml(book_content.html)を別で作ればいい。面白い！
        "book": book,
        "chapter_data": chapter_data,
    })

    return JsonResponse({"html": html})



#ある節の注釈を取得(TODO:プライベートな注釈が表示されないようにする)(TODO:エラーハンドリングいる？)
#book_content.htmlから,verse_annotations.htmlをサブウィンドウで開く
def get_verse_annotations(request):
    
    #節を取得
    verse_id = request.GET.get("verse_id")
    verse = Verse.objects.get(id=int(verse_id))

    #節に紐付いた注釈を取得（多分ここでプライベートな注釈をはじく）
    annotations = VerseAnnotation.objects.filter(verse=verse).order_by("-created_at")

    html = render_to_string("menu/verse_annotations.html", {
        "verse": verse,
        "annotations": annotations,
        "form" : AnnotationForm(),
    }, request=request)

    return JsonResponse({"html": html})



#注釈を追加
#verse_annotations.htmlから, 格納に成功したらサブウィンドウを閉じる
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
            html = render_to_string("menu/update_verse_annotations.html", {
                "verse": verse,
                "annotations": annotations,
                "form" : AnnotationForm(),
            }, request=request)

            return JsonResponse({
                "success": True,
                "html": html 
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "フォームがおかしい",
                "errors": form.errors
            })
    return JsonResponse({
        "success": False,
        "message": "リクエストがおかしい"
    })



#ある節に紐付けられた質問を取得(verse_questions.htmlに表示（新しいタブで開く）)
#book_content.htmlから
def get_verse_questions(request):
    verse_id = request.GET["id"]
    verse = get_object_or_404(Verse, id=verse_id)
    questions = VerseQuestion.objects.filter(verse=verse)

    params = {
        "verse" : verse,
        "questions" : questions,
    }
    return render(request,"menu/verse_questions.html",params)



#質問作成サブウィンドウに表示させるHTML(create_verse_question.html)を作成
#verse_questions.htmlから, 
def create_verse_question(request):

    verse_id = request.GET["verse_id"]
    verse = get_object_or_404(Verse, id=verse_id)

    html = render_to_string("menu/create_verse_question.html", {
        "verse": verse,
        "form" : VerseQuestionForm(),
    }, request=request)

    return JsonResponse({"html": html})



#作成した質問をDBに格納
#create_verse_question.htmlから
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
def verse_answers(request):
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
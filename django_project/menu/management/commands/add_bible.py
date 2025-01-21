from django.core.management.base import BaseCommand
import os
from menu.models import Bible,Book,Chapter,Verse

class Command(BaseCommand):
    help = "聖書をDBへ追加"

    def handle(self, *args, **options):

        #聖書のパスを指定 
        directory = "media/bible/JCO.txt"

        try:
            with open(directory, "r", encoding="utf-8") as file:

                for line in file:

                    #聖句じゃない行は無視する            
                    if not ":" in line:
                        continue

                    else:

                        content = line.split(" ")
                        chapter_and_verse = content[1].split(":")
                        #print(f"{content[2]}の{chapter_and_verse[0]}章{chapter_and_verse[1]}節は「{content[-2]}」です。")

                        #聖書のバージョン指定(例.JCO)
                        version = "JCO"
                        #聖書の言語指定(model.pyのLANGUAGE_CHOICES参照)
                        language = "ja"
                        #書の名前（例.創世記）
                        name = content[2]
                        chapter_number = chapter_and_verse[0]
                        verse_number = chapter_and_verse[1]
                        text = content[-2]
                        #DBへ格納
                        bible,_ = Bible.objects.get_or_create(version=version,language=language)
                        book, _ = Book.objects.get_or_create(bible=bible,name=name)
                        chapter, _ = Chapter.objects.get_or_create(book=book, chapter_number=chapter_number)
                        verse, _ = Verse.objects.get_or_create(chapter=chapter, verse_number=verse_number, text=text)


        except FileNotFoundError:
            print(f"{directory}が見つかりません")

from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):

        #読み込みたいファイルのあるディレクトリを指定 
        directory = "media/bible/books.txt"

        try:
            with open(directory, "r", encoding="utf-8") as file:

                c = 0
        
                for line in file:
            
                    if not ":" in line:

                        continue

                    else:

                        content = line.split(" ")
                        #print(content)
                        #print(content[1])
                        #print(content[1].split(":"))
                        chapter_and_verse = content[1].split(":")
                        #print(chapter_and_verse)
                        print(f"{content[2]}の{chapter_and_verse[0]}章{chapter_and_verse[1]}節は「{content[-2]}」です。")

                    c += 1
                    if c == 2000:
                        break
        except FileNotFoundError:
            print(f"{directory}が見つかりません")

from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):

        #読み込みたいファイルのあるディレクトリを指定 
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
                        print(f"{content[2]}の{chapter_and_verse[0]}章{chapter_and_verse[1]}節は「{content[-2]}」です。")

        except FileNotFoundError:
            print(f"{directory}が見つかりません")

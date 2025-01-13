#dockerhubにあるベースイメージを指定
FROM python:3.13
#基準となるコンテナ内ディレクトリの指定
WORKDIR /usr/src/app
#Python用環境変数の指定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#PostgreSQLに必要なパッケージをインストール(これでいいのかわからない)
RUN apt update && apt install postgresql-dev gcc python3-dev musl-dev
#pipアップグレード
RUN pip install --upgrade pip
#dockerディレクトリからrequirements.txtを探し、コンテナ内カレントディレクトリ（/usr/src/app）へコピー
COPY ./requirements.txt . 
#requirements.txtに書かれたライブラリをpipインストール
RUN pip install -r requirements.txt
#dockerディレクトリをコンテナ内カレントディレクトリへコピー（下でentrypoint.shを実行するために必要）
COPY . .
#/usr/src/app/entrypoint.shを実行
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
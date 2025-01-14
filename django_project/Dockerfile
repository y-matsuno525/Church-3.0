#BUILDER#

#dockerhubにあるベースイメージを指定(同時にAlpine LinuxがOSイメージとして指定される)。as builderは後で参照するための命名
FROM python:3.13-alpine AS builder
#基準となるコンテナ内ディレクトリの指定
WORKDIR /usr/src/app
#Python用環境変数の指定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#PostgreSQLに必要なパッケージをインストール(これでいいのか要確認)
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
#pipアップグレード
RUN pip install --upgrade pip
#pythonコードのスタイルチェック（PEP8に従っているかなど）ライブラリのインストール（必須か？）
RUN pip install flake8
#dockerディレクトリを/usr/src/appへコピー（必要なファイルがちゃんとコピーされるか要確認）
COPY . .
#dockerディレクトリからrequirements.txtを探し、コンテナ内カレントディレクトリ（/usr/src/app）へコピー
COPY ./requirements.txt . 
#requirements.txtに書かれたライブラリをwheel形式（zip形式）で取得
#--no-cache-dir : キャッシュ無効化（たまに問題あるキャッシュがあるから。あまり推奨されてないらしい）
#--no-deps : 依存関係をダウンロードしない（なぜ？）
#--wheel-dir : 後ろに書かれたディレクトリへダウンロード
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#FINAL#  builderステージで作ったものを利用する

FROM python:3.13-alpine
#pオプションは途中のディレクトリも含めて作成
RUN mkdir -p /home/app
#appグループとappユーザーを作り、appユーザーをappグループに入れる
RUN addgroup -S app && adduser -S app -G app
#パス設定とディレクトリ設定
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
#パッケージリストを更新し、PostgreSQL用ライブラリをインストール
RUN apk update && apk add libpq
#builderステージからwheelファイルを/wheelsへコピー
COPY --from=builder /usr/src/app/wheels /wheels
#builderステージからrequirements.txtをカレントディレクトリ(WORKDIRで指定したディレクトリである/home/app/web)へコピー
COPY --from=builder /usr/src/app/requirements.txt .
#wheel形式のライブラリをインストール
RUN pip install --no-cache /wheels/*
COPY ./entrypoint.sh $APP_HOME
#dockerディレクトリを/home/app/webへコピー（必要なファイルがちゃんとコピーされるか要確認）
COPY . $APP_HOME
#/home/app/webの所有者をappグループ,appユーザーへ変更
RUN chown -R app:app $APP_HOME
#以降のコマンドはappユーザーの権限で実行
USER app
#entrypoint.shを実行
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

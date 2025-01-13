#PostgreSQLが利用可能になるまで待機
if [ "$DATABASE" = "postgres" ]
then
   echo "Waiting for postgres..."
   #ポートが開いてるか確認
   while ! nc -z $SQL_HOST $SQL_PORT; do
     sleep 0.1
   done
   echo "PostgreSQL started"
fi
#よくわからない
exec "$@"
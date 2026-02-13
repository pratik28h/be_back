@echo off
echo Testing Upload...
curl -X POST -F "file=@test.csv" http://127.0.0.1:8000/upload
echo.
echo Testing Chat (Remove Nulls)...
curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"remove nulls\"}" http://127.0.0.1:8000/chat
echo.
echo Testing Chat (Drop Column)...
curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"drop column city\"}" http://127.0.0.1:8000/chat
echo.

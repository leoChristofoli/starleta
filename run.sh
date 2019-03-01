clear
echo Starting server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b :8003 --log-level debug starleta:app
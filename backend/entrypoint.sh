#!/bin/sh
if [ "$APP_ENV" = "development" ]; then
  exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
else
  exec uvicorn app.main:app --host 0.0.0.0 --port 8080
fi
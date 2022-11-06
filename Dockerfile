FROM python:3.9 

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 80
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]

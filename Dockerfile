# ---- Base Image ----
FROM python:3.11-slim

# ---- Set Work Directory ----
WORKDIR /app

# ---- Install Dependencies ----
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy Project Files ----
COPY . .

# ---- Expose Flask Port ----
EXPOSE 5000

# ---- Run Flask App ----
CMD ["python", "app.py"]

pip3 install --no-cache-dir -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate 


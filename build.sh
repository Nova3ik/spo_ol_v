pip3 install --no-cache-dir -r requirements.txt
python manage.py collectstatic --no-input
mkdir -p staticfiles_build
cp -R staticfiles staticfiles_build/static
python manage.py migrate

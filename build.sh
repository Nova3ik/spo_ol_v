python -m venv .vercel-venv
. .vercel-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt
python manage.py collectstatic --no-input
mkdir -p staticfiles_build
cp -R staticfiles staticfiles_build/static
python manage.py migrate

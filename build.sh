set -e

python -m venv .vercel-venv
. .vercel-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt
python manage.py collectstatic --no-input

if [ -d staticfiles/admin ]; then
  cp -R staticfiles/admin static/
fi

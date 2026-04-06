set -e

python -m venv .vercel-venv
. .vercel-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt
python manage.py collectstatic --no-input

rm -rf staticfiles_build
mkdir -p staticfiles_build/static

if [ -d static ]; then
  cp -R static/. staticfiles_build/static/
fi

if [ -d staticfiles/admin ]; then
  mkdir -p staticfiles_build/static/admin
  cp -R staticfiles/admin/. staticfiles_build/static/admin/
fi

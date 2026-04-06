# Teacher Portfolio Django Project

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run development server:
   ```bash
   python manage.py runserver
   ```

`manage.py` is configured to use `config.settings`.

## Notes

- Project uses sqlite by default for Django system apps.
- No business-domain models or database integrations are implemented.
- Environment variables can be configured with `.env` (see `.env.example`).


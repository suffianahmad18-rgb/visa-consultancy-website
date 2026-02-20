# Create build.sh
@"
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
"@ | Out-File -FilePath build.sh -Encoding utf8
# backup_data.py
import json
import os
import sys

import django
from django.core import serializers
from django.db import connection

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visa_consultancy.settings")
django.setup()

# Get all models
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

from accounts.models import ClientProfile, StaffProfile
from applications.models import Application, Document
from messaging.models import Message
from study_destinations.models import (
    DestinationSection,
    IntakeTable,
    PostStudyWork,
    Scholarship,
    StudyDestination,
    TuitionTable,
    VisaRequirement,
)

# List all models to export
models_to_export = [
    User,
    ClientProfile,
    StaffProfile,
    StudyDestination,
    DestinationSection,
    TuitionTable,
    IntakeTable,
    Scholarship,
    VisaRequirement,
    PostStudyWork,
    Application,
    Document,
    Message,
]

# Collect data
all_data = []

for model in models_to_export:
    try:
        queryset = model.objects.all()
        if queryset.exists():
            print(f"Exporting {model.__name__}: {queryset.count()} records")
            data = serializers.serialize("json", queryset, indent=2)
            all_data.extend(json.loads(data))
    except Exception as e:
        print(f"Error exporting {model.__name__}: {e}")

# Save to file with UTF-8 encoding
with open("datadump.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Data exported successfully to datadump.json")
print(f"Total records: {len(all_data)}")

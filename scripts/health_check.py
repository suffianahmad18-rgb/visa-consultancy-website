#!/usr/bin/env python
"""Health check script for monitoring the application."""

import os
import sys
import requests
import django
from django.db import connection
from django.core.management import call_command

def check_database():
    """Check database connection."""
    try:
        connection.ensure_connection()
        print("✅ Database: Connected")
        return True
    except Exception as e:
        print(f"❌ Database: {str(e)}")
        return False

def check_migrations():
    """Check if all migrations are applied."""
    try:
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if not plan:
            print("✅ Migrations: All applied")
            return True
        else:
            print(f"❌ Migrations: {len(plan)} pending")
            return False
    except Exception as e:
        print(f"❌ Migrations: {str(e)}")
        return False

def check_static_files():
    """Check if static files exist."""
    from django.conf import settings
    static_root = settings.STATIC_ROOT
    if os.path.exists(static_root) and os.listdir(static_root):
        print(f"✅ Static files: Found in {static_root}")
        return True
    else:
        print(f"❌ Static files: Missing in {static_root}")
        return False

def check_media_files():
    """Check if media directory is writable."""
    from django.conf import settings
    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root):
        test_file = os.path.join(media_root, 'health_check.txt')
        try:
            with open(test_file, 'w') as f:
                f.write('health check')
            os.remove(test_file)
            print(f"✅ Media directory: Writable at {media_root}")
            return True
        except Exception as e:
            print(f"❌ Media directory: Not writable - {str(e)}")
            return False
    else:
        print(f"❌ Media directory: Missing at {media_root}")
        return False

def check_http_endpoint():
    """Check if website is accessible."""
    base_url = os.getenv('BASE_URL', 'http://localhost:8000')
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print(f"✅ HTTP: Website accessible at {base_url}")
            return True
        else:
            print(f"❌ HTTP: Returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HTTP: {str(e)}")
        return False

def check_disk_space():
    """Check available disk space."""
    import shutil
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb > 5:
        print(f"✅ Disk space: {free_gb}GB free")
        return True
    else:
        print(f"❌ Disk space: Only {free_gb}GB free")
        return False

def check_memory():
    """Check available memory."""
    import psutil
    memory = psutil.virtual_memory()
    if memory.available > 500 * 1024 * 1024:  # 500MB
        print(f"✅ Memory: {memory.available / (1024**2):.0f}MB available")
        return True
    else:
        print(f"❌ Memory: Only {memory.available / (1024**2):.0f}MB available")
        return False

def main():
    """Run all health checks."""
    print("\n" + "="*50)
    print("HEALTH CHECK REPORT")
    print("="*50 + "\n")
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visa_consultancy.settings')
    django.setup()
    
    checks = [
        ("Database Connection", check_database),
        ("Migrations Status", check_migrations),
        ("Static Files", check_static_files),
        ("Media Files", check_media_files),
        ("HTTP Endpoint", check_http_endpoint),
        ("Disk Space", check_disk_space),
        ("Memory", check_memory),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        results.append(check_func())
    
    print("\n" + "="*50)
    total_passed = sum(results)
    total_checks = len(checks)
    
    if total_passed == total_checks:
        print(f"\n✅ ALL CHECKS PASSED ({total_passed}/{total_checks})")
        return 0
    else:
        print(f"\n❌ {total_passed}/{total_checks} checks passed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
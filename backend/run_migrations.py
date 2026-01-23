#!/usr/bin/env python3
"""
Migration runner that handles existing databases without alembic_version table.

For databases created before alembic was introduced, this script will:
1. Check if alembic_version table exists
2. If not, stamp the database with the baseline revision
3. Then run all pending migrations
"""
import subprocess
import sys

print("=== Migration Runner Started ===", flush=True)

try:
    from sqlalchemy import create_engine, text
    from config import settings
    print(f"Database URL configured: {settings.DATABASE_URL[:20]}...", flush=True)
except Exception as e:
    print(f"Error importing modules: {e}", flush=True)
    sys.exit(1)

def main():
    try:
        engine = create_engine(settings.DATABASE_URL)
        print("Database engine created", flush=True)

        with engine.connect() as conn:
            # Check if alembic_version table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'alembic_version'
                )
            """))
            alembic_exists = result.scalar()
            print(f"alembic_version table exists: {alembic_exists}", flush=True)

            # Check if users table exists (to determine if this is an existing database)
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'users'
                )
            """))
            users_exists = result.scalar()
            print(f"users table exists: {users_exists}", flush=True)

        if not alembic_exists and users_exists:
            # Existing database without alembic - stamp with baseline
            print("Existing database detected without alembic_version table.", flush=True)
            print("Stamping database with baseline revision...", flush=True)
            result = subprocess.run(["alembic", "stamp", "000_baseline"], capture_output=True, text=True)
            print(f"Stamp stdout: {result.stdout}", flush=True)
            print(f"Stamp stderr: {result.stderr}", flush=True)
            if result.returncode != 0:
                print(f"Stamp failed with code {result.returncode}", flush=True)
                sys.exit(result.returncode)
            print("Database stamped with baseline.", flush=True)

        # Run migrations
        print("Running alembic upgrade head...", flush=True)
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        print(f"Upgrade stdout: {result.stdout}", flush=True)
        print(f"Upgrade stderr: {result.stderr}", flush=True)

        if result.returncode != 0:
            print(f"Migration failed with code {result.returncode}", flush=True)
        else:
            print("=== Migrations completed successfully ===", flush=True)

        sys.exit(result.returncode)

    except Exception as e:
        print(f"Error during migration: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

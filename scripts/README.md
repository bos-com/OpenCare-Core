# Scripts

This folder contains utility scripts for the OpenCare-Africa project.

## seed_data.py

Populates the database with realistic sample data for development and testing.

### Usage

```bash
# Local development
python manage.py shell < scripts/seed_data.py

# With Docker
docker-compose exec web python manage.py shell < scripts/seed_data.py
```

### What it seeds
- 5 sample health facilities (clinics, hospitals)
- 10 sample patients with Ugandan names and demographics
- 5 sample health workers (doctors and nurses)

### Notes
- Safe to run multiple times (uses get_or_create)
- Only for development — never run on production
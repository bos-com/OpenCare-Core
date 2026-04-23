-- Database initialization script for OpenCare-Africa
-- This script sets up the initial database structure and sample data

-- Create database if it doesn't exist
-- Note: This should be run as a superuser or the database should be created manually

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create custom types if needed
-- (Django will handle most type creation)

-- Set timezone
SET timezone = 'UTC';

-- Create indexes for better performance
-- (Django will create most indexes automatically)

-- Sample data for locations (optional - can be added through Django admin)
-- INSERT INTO core_location (name, location_type, parent_id, latitude, longitude) VALUES
-- ('Kenya', 'country', NULL, -1.2921, 36.8219),
-- ('Nairobi', 'region', 1, -1.2921, 36.8219),
-- ('Nairobi County', 'district', 2, -1.2921, 36.8219);

-- Sample data for health facilities (optional - can be added through Django admin)
-- INSERT INTO core_healthfacility (name, facility_type, location_id, address, phone_number, contact_person_name, contact_person_phone) VALUES
-- ('Kenyatta National Hospital', 'hospital', 3, 'Hospital Road, Nairobi', '+254-20-2726300', 'Dr. John Doe', '+254-700-000000');

-- Create a superuser account (optional - can be created through Django management command)
-- Note: This is just a template - actual passwords should be set securely
-- INSERT INTO auth_user (username, password, first_name, last_name, email, is_staff, is_superuser, is_active, date_joined) VALUES
-- ('admin', 'pbkdf2_sha256$600000$...', 'Admin', 'User', 'admin@opencare-africa.com', true, true, true, NOW());

-- Grant necessary permissions
-- (Django will handle most permission setup)

-- Set up database configuration
ALTER DATABASE opencare_africa SET timezone TO 'UTC';
ALTER DATABASE opencare_africa SET datestyle TO 'ISO, MDY';

-- Create a read-only user for reporting (optional)
-- CREATE USER opencare_readonly WITH PASSWORD 'secure_password_here';
-- GRANT CONNECT ON DATABASE opencare_africa TO opencare_readonly;
-- GRANT USAGE ON SCHEMA public TO opencare_readonly;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO opencare_readonly;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO opencare_readonly;

-- Create a backup user (optional)
-- CREATE USER opencare_backup WITH PASSWORD 'secure_password_here';
-- GRANT CONNECT ON DATABASE opencare_africa TO opencare_backup;
-- GRANT USAGE ON SCHEMA public TO opencare_backup;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO opencare_backup;

-- Set up connection limits
ALTER USER opencare_user CONNECTION LIMIT 100;
-- ALTER USER opencare_readonly CONNECTION LIMIT 50;
-- ALTER USER opencare_backup CONNECTION LIMIT 10;

-- Create tablespace for better performance (optional)
-- CREATE TABLESPACE opencare_data LOCATION '/var/lib/postgresql/data/opencare_data';
-- CREATE TABLESPACE opencare_index LOCATION '/var/lib/postgresql/data/opencare_index';

-- Set default tablespace for new tables (optional)
-- SET default_tablespace = 'opencare_data';

-- Optimize database settings for health care applications
-- These settings can be adjusted based on server resources
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Reload configuration
SELECT pg_reload_conf();

-- Create initial audit trail entry
-- INSERT INTO core_audittrail (user_id, action, model_name, object_id, changes, timestamp) VALUES
-- (1, 'create', 'database', 'initialization', '{"message": "Database initialized successfully"}', NOW());

-- Set up monitoring and logging
-- Enable pg_stat_statements for query monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Create views for common queries (optional)
-- CREATE VIEW patient_summary AS
-- SELECT 
--     p.id,
--     p.patient_id,
--     p.first_name,
--     p.last_name,
--     p.gender,
--     p.date_of_birth,
--     p.phone_number,
--     l.name as location_name,
--     hf.name as facility_name,
--     COUNT(pv.id) as visit_count
-- FROM patients_patient p
-- LEFT JOIN core_location l ON p.location_id = l.id
-- LEFT JOIN core_healthfacility hf ON p.registered_facility_id = hf.id
-- LEFT JOIN patients_patientvisit pv ON p.id = pv.patient_id
-- GROUP BY p.id, p.patient_id, p.first_name, p.last_name, p.gender, p.date_of_birth, p.phone_number, l.name, hf.name;

-- Grant access to views
-- GRANT SELECT ON patient_summary TO opencare_user;
-- GRANT SELECT ON patient_summary TO opencare_readonly;

-- Set up partitioning for large tables (optional - for future scalability)
-- This can be implemented later when the system grows

-- Create indexes for common search patterns
-- These will be created automatically by Django, but can be optimized here if needed

-- Set up full-text search (optional)
-- ALTER TABLE patients_patient ADD COLUMN search_vector tsvector;
-- CREATE INDEX patient_search_idx ON patients_patient USING gin(search_vector);
-- CREATE TRIGGER patient_search_update BEFORE INSERT OR UPDATE ON patients_patient
--     FOR EACH ROW EXECUTE FUNCTION tsvector_update_trigger(search_vector, 'pg_catalog.english', first_name, last_name, notes);

-- Final setup
-- Update statistics
ANALYZE;

-- Create a completion message
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully!';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Run Django migrations: python manage.py migrate';
    RAISE NOTICE '2. Create superuser: python manage.py createsuperuser';
    RAISE NOTICE '3. Load initial data: python manage.py loaddata initial_data';
    RAISE NOTICE '4. Start the application: python manage.py runserver';
END $$;

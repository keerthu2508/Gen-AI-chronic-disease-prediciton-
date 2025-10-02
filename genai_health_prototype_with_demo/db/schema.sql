-- PostgreSQL schema for encrypted patient data using pgcrypto
-- Assumes extension: CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE patients (
    patient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT,
    dob DATE,
    phone BYTEA, -- encrypted
    email BYTEA, -- encrypted
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE vitals (
    id BIGSERIAL PRIMARY KEY,
    patient_id UUID REFERENCES patients(patient_id),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    heart_rate INTEGER,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    spo2 INTEGER,
    glucose_mg_dl INTEGER,
    notes TEXT
);

-- Example inserting encrypted phone/email:
-- INSERT INTO patients(name, dob, phone, email) VALUES(
--   'Test', '1980-01-01',
--   pgp_sym_encrypt('9999999999', 'your_sym_key'),
--   pgp_sym_encrypt('test@example.com', 'your_sym_key')
-- );

-- To read encrypted values:
-- SELECT name, pgp_sym_decrypt(phone, 'your_sym_key') AS phone FROM patients;

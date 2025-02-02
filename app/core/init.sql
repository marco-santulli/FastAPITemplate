-- Following the naming conventions from the guidelines
-- T_ prefix for transactional tables
-- L_ prefix for log tables

-- Create user table
CREATE TABLE t_user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create audit log table
CREATE TABLE l_user_audit (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    cod_evento VARCHAR(10) NOT NULL CHECK (cod_evento IN ('insert', 'update', 'delete')),
    old_data JSONB,
    new_data JSONB,
    data_aggiornamento TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    utente_aggiornamento VARCHAR(255)
);

-- Create index on email for faster lookups
CREATE INDEX idx_t_user_email ON t_user(email);

-- Create trigger function for audit logging
CREATE OR REPLACE FUNCTION f_user_audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO l_user_audit (user_id, cod_evento, old_data, new_data, utente_aggiornamento)
        VALUES (NEW.id, 'insert', NULL, row_to_json(NEW), current_user);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO l_user_audit (user_id, cod_evento, old_data, new_data, utente_aggiornamento)
        VALUES (NEW.id, 'update', row_to_json(OLD), row_to_json(NEW), current_user);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO l_user_audit (user_id, cod_evento, old_data, new_data, utente_aggiornamento)
        VALUES (OLD.id, 'delete', row_to_json(OLD), NULL, current_user);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER tr_user_audit
AFTER INSERT OR UPDATE OR DELETE ON t_user
FOR EACH ROW EXECUTE FUNCTION f_user_audit_trigger();

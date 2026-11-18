CREATE TABLE IF NOT EXISTS parents (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS students (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    birth_date DATE NOT NULL,
    parent_id BIGINT NOT NULL REFERENCES parents(id)
);

CREATE TABLE IF NOT EXISTS programs (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    min_age SMALLINT NOT NULL CHECK (min_age >= 0),
    max_age SMALLINT NOT NULL CHECK (max_age >= min_age),
    duration_hours INTEGER NOT NULL CHECK (duration_hours > 0),
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS study_groups (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    program_id BIGINT NOT NULL REFERENCES programs(id),
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    enrollment_open BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS applications (
    id BIGSERIAL PRIMARY KEY,
    parent_id BIGINT NOT NULL REFERENCES parents(id),
    student_id BIGINT NOT NULL REFERENCES students(id),
    program_id BIGINT NOT NULL REFERENCES programs(id),
    preferred_group_id BIGINT REFERENCES study_groups(id),
    status VARCHAR(30) NOT NULL DEFAULT 'new'
        CHECK (status IN ('new', 'under_review', 'approved', 'rejected', 'enrolled')),
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

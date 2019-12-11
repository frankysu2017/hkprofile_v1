
DROP TABLE IF EXISTS person;
 
CREATE TABLE person(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cn_name TEXT,
    en_name TEXT,
    picture BLOB,
    gender TEXT,
    birthdate DATE,
    id_num TEXT,
    permit_num TEXT,
    passort TEXT,
    home_address TEXT,
    post_address TEXT,
    company_address TEXT,
    party TEXT,
    occupation TEXT,
    private_phone TEXT,
    company_phone TEXT,
    fax TEXT,
    email TEXT,
    internet_account TEXT,
    homepage TEXT,
    bank_account TEXT,
    other_number TEXT,
    family TEXT,
    hobby TEXT,
    experience TEXT,
    event TEXT,
    stain TEXT
);
 
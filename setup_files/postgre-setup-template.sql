CREATE DATABASE portfoliosite;
CREATE USER portfolioadmin WITH PASSWORD 'temppass';
ALTER ROLE portfolioadmin SET client_encoding TO 'utf8';
ALTER ROLE portfolioadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE portfolioadmin SET timezone TO 'EST';
GRANT ALL PRIVILEGES ON DATABASE portfoliosite TO portfolioadmin;

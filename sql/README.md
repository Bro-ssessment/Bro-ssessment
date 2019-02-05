# Postgres DB

DB migration scripts

## Naming Convention

### Name

- Table name should be plural instead of singular
- Column name should be sanke case all lower case

### Filename

`_<sequence>_<migration_name>.sql`

## How to run

`psql postgres://<username>:<password>@<hostname>:<port>/<database_name> -f <migration_script_pathname>`

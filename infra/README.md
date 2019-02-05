# Infrastructure

Spin up a Postgres DB like a lightsaber on butter.

## Deployment

```bash
# Create env file for specific environment
$ cp .env.example prod.env

# Edit env var as needed
$ vim prod.env

# Start production database instance
$ env $(cat prod.env) docker-compose -f docker-compose.yml -p <project_name> up -d
```

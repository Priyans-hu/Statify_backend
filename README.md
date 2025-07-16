# Statify_backend

to run:

```
- using docker-cli:
    - docker build -t statify-backend .
    - docker run -p 5000:5000 statify-backend

- using docker compose:
    - docker-compose up --build
```

```
tables:

- Organizations
- Services/applications (fk - org)
- Users (role based, fk - org)
- Status master (option for status)
- Incident/Maintenance logs (fk - org, app, timestamp, status)

routes:
- /login or /register
- /org/status - public route
- /org/services (add new service, view all service)

models/schema:
- Organizations
	{
		int auto-inc Id,
		String Name,
		dateTime created_at,
		dateTime updted_at,
		boolean is_deleted
	}

- services
	{
		int auto-inc Id,
		String service_name,
		int org_id (fk),
		int Status_code,
		String/Text domain,
		dateTime created_at,
		dateTime updted_at,
		boolean is_deleted
	}

- users
	{
		uuid user_id,
		String username,
		int org_id,
		String role (admin/viewer),
		varchar(128) password_hash,
		String email (optional, default - null),
		dateTime created_at,
		dateTime updted_at,
		boolean is_deleted
	}

- Status_Master
	{
		int id {code},
		String status
	}

- Incident/Maintenance logs
	{
		int log_id,
		int org_id,
		int service_id,
		dateTime timestamp,
		int status_code,
		json details (err msg, maintaince duration)
	}
```

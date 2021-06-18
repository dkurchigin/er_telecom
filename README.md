# er_telecom

1) Need Redis for the server
2) Need Celery. Run as:
	celery -A server.celery worker --loglevel=info --concurrency=4 -P gevent
	gevent - for Windows only
broker_url = 'redis://localhost:6379/0'  # Using Redis as a message broker
result_backend = 'redis://localhost:6379/0'  # Store task results in Redis
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

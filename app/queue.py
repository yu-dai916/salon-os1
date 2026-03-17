from redis import Redis
from rq import Queue

# Docker Compose内は service名 "redis" で到達できる
redis_conn = Redis(host="redis", port=6379, db=0)

# Queue名は "gbp" に統一
queue = Queue("gbp", connection=redis_conn)
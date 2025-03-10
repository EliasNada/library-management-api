import os

from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from fastapi import FastAPI
import redis

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

load_dotenv()

# Initialize the rate limiter
limiter = Limiter(
    key_func=get_remote_address,  # Use the client's IP address for rate limiting
    storage_uri=os.getenv('REDIS_URL') + '/0',  # Use Redis for storing request counts
)


# Apply rate limiting to the FastAPI app
def apply_rate_limiting(app: FastAPI):
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

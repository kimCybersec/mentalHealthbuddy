from flask import request, jsonify 
from functools import wraps
import time

rate_limit_window = 60 # seconds 
max_requests = 30 
request_log = {}

def limiter(func): 
    @wraps(func) 
    def wrapper(*args, **kwargs): 
        ip = request.remote_addr 
        now = time.time()

        if ip not in request_log:
            request_log[ip] = []
        request_log[ip] = [t for t in request_log[ip] if now - t < rate_limit_window]

        if len(request_log[ip]) >= max_requests:
            return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

        request_log[ip].append(now)
        return func(*args, **kwargs)
    return wrapper
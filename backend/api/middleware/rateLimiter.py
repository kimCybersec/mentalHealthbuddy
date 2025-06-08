from flask import request, jsonify
from time import time
from functools import wraper

RATELIMIT = 10
TIMEWINDOW = 60  
rateData = {}

def rateLimiter(func):
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        now = time()
        windowData = rateData.get(ip, [])
        windowData = [t for t in windowData if now - t < TIMEWINDOW]
        if len(windowData) >= RATELIMIT:
            return jsonify({"error": "Rate limit exceeded. Give me a minute to cool down."}), 429
        windowData.append(now)
        rateData[ip] = windowData
        return func(*args, **kwargs)
    return wrapper
   
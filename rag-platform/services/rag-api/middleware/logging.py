import time

async def log_request(request, call_next):

    start = time.time()

    response = await call_next(request)

    latency = time.time() - start

    print("Request latency:", latency)

    return response
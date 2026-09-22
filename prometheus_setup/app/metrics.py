from prometheus_client import Counter,Gauge,Histogram

#--------------------
# Counter 1: Total HTTP Request
#--------------------

REQUEST_COUNT = Counter(
    name="http_request_total",
    documentation="Total to number of http requests received",
    labelnames=["method","endpoint","status_code"],
) #Red method

#------------------
# Counter 2: Request latency in seconds
#------------------

REQUEST_LATENCY = Histogram(
    name="http_request_duration_seconds",
    documentation="HTTP request duration in seconds",
    labelnames=["method","endpoint"],
    # `buckets` define the ranges for percentile calculation.
    buckets=(0.005,0.01,0.025,0.05,0.1,0.25,0.5,1.0,2.5,5.0),
)

#----------------
# Counter 3: Number of tasks currently in memory (business metric)
#----------------
TASKS_IN_PROGRESS = Gauge(
    name="tasks_in_progress",
    documentation="Number of tasks currently in memory",
)

#-----------------
# Counter 4: Business metric: total task created
#-----------------
TASKS_CREATED_TOTAL = Counter(
    name="tasks_created_total",
    documentation="Total number of tasks created via the API",
)

# ---------------------------------------------------------------
# COUNTER 5: Errors, labeled by type
# ---------------------------------------------------------------
ERROR_COUNT = Counter(
    name="app_errors_total",
    documentation="Total number of application errors",
    labelnames=["error_type"],
)
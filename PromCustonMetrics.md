
We integrated custom metrics into our Python application to monitor its performance and track key application events. Here’s a breakdown of the process:

### 1. **Installing Prometheus Client Library**
We began by installing the `prometheus_client` Python library, which is the official client for exposing metrics to Prometheus. This library provides a straightforward API to create, collect, and expose metrics.

```bash
pip install prometheus_client
```

### 2. **Defining Custom Metrics**
Next, we identified the key metrics we wanted to monitor. For our application, these included:
   - **Request Latency**: The time taken to process incoming requests.
   - **Request Count**: A counter for the number of requests processed.
   - **Errors**: A counter for the number of errors encountered.

We used Prometheus' metric types to expose these metrics:
   - **Counter**: Used for request count and error tracking.
   - **Histogram**: Used to measure request latency.

Here’s a sample of how we implemented these metrics in the code:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Define a Counter for the number of requests
REQUEST_COUNT = Counter('app_request_count', 'Total number of requests received')

# Define a Histogram for request latency
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Latency in seconds for each request')

# Define a Counter for errors
ERROR_COUNT = Counter('app_error_count', 'Total number of errors encountered')
```

### 3. **Recording Metrics in Application Code**
Once we defined the metrics, we integrated them into the core functions of the application. For example, each time a new request was handled, we incremented the `REQUEST_COUNT`, and for each error, we incremented the `ERROR_COUNT`. To track latency, we used the histogram's `observe()` method to record the time taken to process requests.

Here’s how it was integrated within a typical request handler:

```python
import time

@app.route('/process')
def process_data():
    start_time = time.time()  # Record start time
    REQUEST_COUNT.inc()  # Increment request count

    try:
        # Business logic goes here
        result = handle_request()

        latency = time.time() - start_time  # Calculate latency
        REQUEST_LATENCY.observe(latency)  # Record latency in the histogram

        return result

    except Exception as e:
        ERROR_COUNT.inc()  # Increment error count
        return str(e), 500
```

### 4. **Exposing Metrics to Prometheus**
We needed to expose these metrics so that Prometheus could scrape them. The `prometheus_client` library provides an endpoint to serve the metrics over HTTP. We created a `/metrics` endpoint in our Flask app where Prometheus could fetch the metrics data.

```python
from flask import Flask, Response

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```

### 5. **Configuring Prometheus**
With the application exposing metrics at `/metrics`, we added the service as a target in our Prometheus configuration. This ensures Prometheus periodically scrapes the metrics.

In the `prometheus.yml` configuration file, we added:

```promql
# Global config  
global:  
  scrape_interval: 15s   # Scrape metrics every 15 seconds  
  evaluation_interval: 15s  # Evaluate rules every 15 seconds

# Scrape configuration for Prometheus itself:  
scrape_configs:  
  - job_name: "prometheus"  
    static_configs:  
      - targets: ["localhost:9090"]  # Scraping Prometheus' own metrics

  # Scrape configuration for your Flask application  
  - job_name: "scockulator_metrics"  
    static_configs:  
      - targets: ["aa0e69998eed3498fba3076d247c5dcd-669029395.us-east-1.elb.amazonaws.com:80"]
```

This configuration tells Prometheus to scrape the `/metrics` endpoint of the Python application running on port 5000.

### 6. **Verifying Metrics in Prometheus**
Once the configuration was set, we restarted Prometheus and the Python application. Prometheus began scraping the custom metrics, which we could then query and visualize through Prometheus’ UI.

For instance, we queried the total request count with:

```promql
app_request_count_total
```

Similarly, we visualized latency trends by querying the histogram data:

```promql
histogram_quantile(0.95, sum(rate(app_request_latency_seconds_bucket[5m])) by (le))
```

### 7. **Alerting and Dashboards**
Finally, we integrated Prometheus with Grafana to visualize these metrics on a dashboard and set up alerts based on thresholds. For example, if request latency exceeded a certain threshold, an alert would notify the team, helping us maintain the application’s performance and reliability.

---

This process allowed us to monitor key aspects of our Python application in real-time, providing insights into its performance and helping us proactively address any issues. By adding custom metrics, we were able to better understand how our application behaves under different conditions, and Prometheus provided a robust solution for tracking these metrics and setting up alerts.

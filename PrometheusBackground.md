## Installation
Here’s a **Prometheus installation guide** for setting up Prometheus **locally** in **Markdown format**:

```markdown
# Prometheus Installation on Local Machine

This guide will walk you through the process of installing Prometheus on a local machine.

## Prerequisites
Ensure you have the following prerequisites before proceeding with the installation:

- **Operating System**: Linux, macOS, or Windows.
- **Docker** (optional): If you prefer to run Prometheus in a Docker container.
- **Admin/Sudo Access**: You will need administrative rights to install software packages.

---

## Option 1: Installing Prometheus Locally (Direct Install)

### 1. Download Prometheus
Visit the official [Prometheus download page](https://prometheus.io/download/) and download the appropriate version for your operating system. 

Alternatively, you can use the following command to download the latest version (Linux/macOS example):

```bash
curl -LO https://github.com/prometheus/prometheus/releases/download/v2.46.0/prometheus-2.46.0.linux-amd64.tar.gz
```

### 2. Extract the Prometheus Archive
Extract the downloaded archive:

```bash
tar -xvf prometheus-*.tar.gz
```

### 3. Move the Binary Files
Move the Prometheus binary files to a suitable location:

```bash
sudo mv prometheus-2.46.0.linux-amd64/prometheus /usr/local/bin/
sudo mv prometheus-2.46.0.linux-amd64/promtool /usr/local/bin/
```

### 4. Configure Prometheus
Create a configuration file named `prometheus.yml` in a directory (e.g., `/etc/prometheus/`) with the following content:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

Move the configuration file to the desired directory:

```bash
sudo mkdir -p /etc/prometheus
sudo mv prometheus-2.46.0.linux-amd64/prometheus.yml /etc/prometheus/
```

### 5. Start Prometheus
Run Prometheus using the following command:

```bash
prometheus --config.file=/etc/prometheus/prometheus.yml
```

Prometheus will now start, and you can access the web interface at `http://localhost:9090`.

---

## Option 2: Running Prometheus in Docker

### 1. Install Docker (If Not Installed)
If you haven't installed Docker yet, install it from the official Docker website: [Docker Installation Guide](https://docs.docker.com/get-docker/).

### 2. Pull the Prometheus Docker Image
You can pull the official Prometheus image from Docker Hub:

```bash
docker pull prom/prometheus
```

### 3. Run Prometheus in a Container
Run Prometheus in a Docker container with a basic configuration:

```bash
docker run -d \
    --name prometheus \
    -p 9090:9090 \
    -v /path/to/your/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```

Make sure to replace `/path/to/your/prometheus.yml` with the actual path to your `prometheus.yml` file on your local machine.

### 4. Access Prometheus Web UI
Once the container is running, Prometheus will be accessible on `http://localhost:9090`.

---

## Verifying Prometheus Installation

### 1. Access the Prometheus Web UI
You can access Prometheus by opening your browser and navigating to:

```bash
http://localhost:9090
```

### 2. Test a Query
Once Prometheus is up and running, you can execute basic queries in the Prometheus web UI.

For example, enter the following query to check Prometheus uptime:

```promql
up
```

You should see metrics indicating whether Prometheus is up and running.

---

## Managing Prometheus

### Starting Prometheus Automatically
To make Prometheus start automatically on boot, you can create a systemd service file on Linux. Here’s an example:

```bash
sudo nano /etc/systemd/system/prometheus.service
```

Add the following content:

```ini
[Unit]
Description=Prometheus Service
After=network.target

[Service]
User=prometheus
ExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Reload the systemd configuration:

```bash
sudo systemctl daemon-reload
sudo systemctl enable prometheus
```

Now, Prometheus will start automatically on boot.

---

## Conclusion
You have successfully installed and started Prometheus locally. You can now configure additional scrape targets, set up alerts, and use the Prometheus web interface for monitoring. Explore more about Prometheus through [official documentation](https://prometheus.io/docs/).
```

### Key Points:
- **Option 1**: Direct installation of Prometheus on a local machine.
- **Option 2**: Running Prometheus in a Docker container for simplicity and isolation.
- **Accessing Prometheus**: Prometheus is available at `http://localhost:9090` by default.
- **Managing Prometheus**: If using a local installation, Prometheus can be set up as a service for automatic startup.

This Markdown guide can be easily shared or uploaded for use in documentation platforms.

## Architecture 
![[Pasted image 20240905154733.png]]


## How to take a sample from an identifier
![[Pasted image 20240905160413.png]]
### PromQL examples
#### Example 1
```
	sum by(path) (rate(http_requests_total[status="500}[5m]))
```
This query is used to calculate the rate of HTTP requests resulting in a '500' status code over the last 5 minutes, grouped by request path. It is particularly useful in identifying problematic paths in a web application that might be returning many 500 errors, which can help with debugging or monitoring server health
**Breakdown:**
1. !`http_requests_total{status="500"}!`:
	- This selects the metric ``http_requests_total`` which tracks the total number of HTTP requests.
	- The filter ``{status="500"}`` narrows down the selection to only those requests that returned an ``HTTP 500`` status code (typically representing an internal server error).
1. ``rate(...[5m])``:
	- The ``rate()`` function calculates the rate(per unit second) of increase for the selected metric over the specified time window.
	- In this case, ``rate(http_requests_total{status="500"}[5m])`` calculates the rate of HTTP 500 errors over the past 5 minutes. This helps in smoothing out the data to show trends rather than instantaneous counts.
1. ``sum by(path)``:
	- The ``sum by(path)`` groups the results by the label `path`.
	- It sums up the HTTP 500 error rates for each distinct path, allowing you to see which request paths are experiencing 500 errors and at what rate.
  **Use case:**
  If you're monitoring several APIs or web endpoints, this query will return something like:
- ``/api/v1/users` → 0.05 errors per second``
- ``/api/v1/orders` → 0.02 errors per second``
#### Example 2
```
	sum by(path) (rate(http_requests_total{status="500"}[5m]))
	/
	sum by(path) (rate(http_requsets_total[5m]))
	* 100
	> 5
```
This PromQL query is used to calculate the HTTP 500 error rate as a percentage of total HTTP requests over the past 5 minutes and then filters the path to only show where the error percentage exceeds 5%.

**Breakdown:**
1. ``sum by(path) (rate(http_requests_total{status="500"}[5m]))``:
	- Described previously.
1. ``sum by(path) (rate(http_requests_total[5m]))``:
	- Calculates the total rate of all HTTP requests (regardless of status code) over the past 5 minutes, grouped by the `path`.
	- ``rate(http_requests_total[5m])`` gives the rate of all requests over the past 5 minutes.
	- ``sum by(path)`` groups this data by ``path``, meaning you'll get the total request rate for each endpoint or URL.
3.`` /``:
	- The query divides the HTTP 500 error rate by the total request rate for each `path`, effectively calculating error rate of requests that resulted in a 500 error.
	- This gives the error rate of total requests for each `path`.
1. ``* 100``:
	- The result of the division is multiplied by 100 to convert the error rate into a percentage.
1. ``> 5``:
	- Finally, the query filters the results to only show `path` values where the 500 error rate is greater than 5%.
	- This allows identifying paths where more than 5% of the total requests are resulting in HTTP 500 errors.
   
**Use case:**
This query is useful in identifying problematic paths that are returning a significant number of server errors, helping narrow down focus to problematic endpoints.

---
## Making Alerts
In this description the above query is used to build an alert.
```
alert: Many500Errors
expr: |
	(
		sum by(path) (rate(http_requests_total{status="500"}[5m]))
		/
		sum by(path) (rate(http_requsets_total[5m]))
	) * 100
	>5
for: 5m
labels: 
	severity: "critical"
annotations:
	summary: "Many 500 errors for path {{$lables.path}} ({{$value}}%)"
```
**Breakdown**:
1. ``alert: Many500Errors``:
	- This defines the name of the alert. Here, it's called ``Many500Errors``, indicating that this alert will trigger when a high percentage of HTTP 500 errors is detected.
2. ``expr``:
	- This specifies the actual PromQL (Prometheus Query Language) expression to evaluate. The expression calculates the percentage of HTTP 500 errors relative to all HTTP requests over the last 5 minutes.
	- Expression Breakdown:
	 - `sum by(path) (rate(http_requests_total{status="500"}[5m]))`: Calculates the rate of HTTP 500 errors over the past 5 minutes, grouped by the `path`.
	 - ``sum by(path) (rate(http_requests_total[5m]))``: 
	 - ``* 100``: Multiplies the result by 100 to convert it into a percentage.
	 - ``> 5``: The alert will trigger if the HTTP 500 error rate exceeds 5% of the total requests for any path.
3. ``for: 5m``:
	- This indicates that the condition (HTTP 500 error rate > 5%) needs to be true for at least 5 minutes before the alert is triggered. This avoids false positives due to brief spikes in errors.
4. ``labels``:
	- ``severity: "critical"``: Labels are used to categorize the alert. In this case, the severity is set to "critical," indicating a severe issue that requires immediate attention.
5. ``annotations``: ``summary: "Many 500 errors for path {{$labels.path} ({{$value}}%)"``:
	- Annotations provide additional information about the alert. In this case:  
		 - The `path` where the errors are occurring is inserted using ``{{$labels.path}}``.
		 - The actual percentage of 500 errors is included using ``{{$value}}%``, which represents the calculated percentage from the expression.
		- This annotation will help when the alert is fired, providing clear context on which path is experiencing the issue and the percentage of errors.
**Use case:**
If the `/api/orders` path has an HTTP 500 error rate of 10% (greater than the 5% threshold) over a 5-minute period, this alert will trigger. The alert message will include something like:
```
	Many 500 errors for path /api/orders (10%)
```
This helps pinpoint the problematic path and allows for quick troubleshooting.

---
## Core Concepts
### Vector Selectors 
#### Instant Vector Selectors
***Instant Vector***t:  A single data point (sample) per time series at a specific moment in time.
***Instant Vector Selectors***: Used to select and return a set of time series(***instant vectors***) at a specific timestamp.
**Example**:
```
	http_requests_total
```
This query returns the current value of the `http_requests_total` metric across all series (e.g., for different `instance` and `job` labels) at the moment of query execution.
#### Range Vector Selector
***Range Vector*** : A range of data points over a period of time for each time series.
***Range vectors*** : Used to analyze time-series data over a defined time range (e.g., last 5 minutes).
**Example**:
```
	http_requests_total[5m]
```
This returns all samples for `http_requests_total` over the last 5 minutes.
### 5m Lookback Delta
***Lookback delta***: The default window of time that Prometheus uses to "look back" when querying metrics if data points are missing.

By default, Prometheus uses a 5-minute lookback window, meaning if a metric has no recent value within the last 5 minutes, it is treated as stale.

This is important for avoiding gaps in data when some scrapes are missed due to network issues or other temporary problems.
### Staleness Handling:
***Staleness*** : how the system deals with missing or outdated data points.

Metrics are automatically marked as stale if there are no updates within the lookback window (e.g., 5 minutes by default).

Stale data is essential to prevent misleading results in queries, especially when calculating rates or aggregations. Missing values are replaced with `NaN` (Not a Number) when data is stale.
### Relative Offsets:
***Offsets*** allow you to shift the time window of a query by a specified duration into the past.
***Relative offsets*** enable you to compare current data with past data by adjusting the time range.
**Example:**
```
	http_requests_total[5m] offset 1h
```

This query fetches data from 1 hour ago, looking at a 5-minute window starting from 1 hour ago. This is useful for comparisons like analyzing metrics at the same time yesterday or last week.
### Absolute Timestamps:
Instead of querying for data at the current time or relative times, you can query Prometheus data using ***absolute timestamps***.
This allows you to precisely specify the start and end time for your query.
**Example:**
```
http_requests_total @ 1631025600
```
This query fetches the value of `http_requests_total` at the specific Unix timestamp (e.g., September 7, 2021).

### Summary
***Instant Vector Selectors*** allow you to look at the current state of a metric, while ***Range Vector Selectors*** help you analyze data over time (e.g., for rate calculations or trends).

The ***5-minute lookback delta*** and ***staleness handling*** prevent gaps in your data by ensuring that outdated data is marked as stale rather than missing, helping to avoid misinterpretation.

***Offsets*** and ***absolute timestamps*** give you flexibility in querying past data, whether you need to look back a specific amount of time (relative offsets) or query exact historical data (absolute timestamps).

These concepts are core to querying, analyzing, and interpreting time-series data, especially when dealing with complex monitoring and alerting use cases.

---
## Metric Types

### Counters
Counters are a metric that can only increase and never decreases unless reset.
#### Methods
```
	var counterName = prometheus.NewCounter(
	    prometheus.CounterOpts{
	        Name: "counter_metric_name",
	        Help: "Total number of  something.",
	    },
	)
	counterName.Add(x)
	counterName.Inc()
```
**``counterName.Inc()``**
- **``Inc()``** increments the value of the counter by 1. This method is helpful when you're observing something that increases, such as counting the number of requests
**``counterName.Add(x)``**
- **``Add()``** increases the counter by a specified amount (in this case, x). This is useful when you want to increase the counter by more than 1 in a single operation.
#### Example
Here’s a breakdown of how you would use counters in practical situations:
1. **Tracking Total Requests**
	If you are monitoring the total number of requests handled by your web application, a counter is ideal since requests can only be added, never removed. Each time a new request is processed, you call `.Inc()` to add one to the total.

   ```
	   requestCounter.Inc() // Every time a request is received
   ```
2. **Tracking Total Errors**
   When tracking the number of errors or failures, you can increment the counter every time an error happens.
  ```
	 errorCounter.Inc()   // Increases every time an error occurs
```
3. **Tracking Processed Data**
   You can use a counter to measure cumulative data processed over time, for example, the total number of bytes transferred.
```
	bytesTransferred.Add(2048)  // Adds 2048 bytes to the total counter
```
#### Special Application
Rate calculation: Counters are often used in combination with Prometheus functions like `rate()` or `irate()` to calculate the rate of change (e.g., requests per second) over time.
```
	rate(counter_metric_name[2h])
```
 
##### Example:
```
	rate(counter_metric_name[5m])
```
This would show the per-second rate of HTTP requests over the last 5 minutes by using a counter that stores the total number of requests.
### Gauges
Gauges are a metric used to track metrics that are not monotonically increasing (i.e., they can go up or down). 
#### Methods

```
	var (
	    gaugeName = prometheus.NewGauge(prometheus.GaugeOpts{
        Name: "gauge_metric_name",
        Help: "Current something in the somewhere.",
    })
	)
	gaugeName.Set(0)
	gaugeName.Inc() 
	gaugeName.Dec() 
	gaugeName.Add(x)
	gaugeName.Sub(2x)
	myTimestamp.SetToCurrentTime()
```
##### Breakdown 
**``gaugeName.Set(0)``**
- ``Set()`` is used when you know the exact value of the metric, and you're updating it directly. In this case, the gauge ``gaugeName`` is being set to 0, which might represent an empty queue.
- Use this method when you want to set the gauge to a specific value based on some external information or calculation.
**``gaugeName.Inc()``**
- **``Inc()``** increments the value of the gauge by 1. This method is helpful when you're directly observing something that increases, such as adding an item to a queue.
**``gaugeName.Dec()``**
- **``Dec()``** decrements the value of the gauge by 1. This is used to represent a decrease in value, such as removing an item from a queue.
**``gaugeName.Add(x)``**
- **``Add()``** increases the gauge by a specified amount (in this case, x). This is useful when you want to increase the gauge by more than 1 in a single operation.
**``gaugeName.Sub(2x)``**
- **``Sub()``** decreases the gauge by a specified amount (in this case, 2x). This is used when you want to decrease the gauge by more than 1.
**``myTimestamp.SetToCurrentTime()``**
- This last line suggests setting a timestamp (perhaps another type of gauge or time-based metric) to the current time. This could be used to track when a particular event occurred, for example, when the last update to the gauge happened.
#### Summary
- **Set()**: Assigns a specific value to the gauge.
- **Inc()**: Increases the gauge by 1.
- **Dec()**: Decreases the gauge by 1.
- **Add(x)**: Increases the gauge by a specified value x.
- **Sub(x)**: Decreases the gauge by a specified value x.
These methods are commonly used in scenarios where the current state of a system needs to be measured and tracked over time. Gauges are well-suited for these dynamic metrics that can fluctuate up and down.
#### Application
```
package main

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "net/http"
)

var (
    temperatureGauge = prometheus.NewGauge(prometheus.GaugeOpts{
        Name: "server_room_temperature_celsius",
        Help: "Current temperature in the server room.",
    })
)

func init() {
    // Register the gauge with Prometheus
    prometheus.MustRegister(temperatureGauge)
}

func main() {
    // Simulating temperature updates
    go func() {
        for {
            // Set the temperature to a random value (for example purposes)
            temperatureGauge.Set(22.5)
        }
    }()

    // Expose metrics at the /metrics endpoint
    http.Handle("/metrics", promhttp.Handler())
    http.ListenAndServe(":8080", nil)
}
)
```

In this example, a **gauge** is created to track the temperature of a server room (``server_room_temperature_celsius``). The value of the gauge is periodically updated with the ``Set`` method.

#### Queries
You can query gauge metrics using PromQL. For eg. to query a gauge metric named ``server_room_temperature_celsius``, you can use:
```
	server_room_temperature_celsius
```
returning the current temperature value of the gauge.

### Gauges vs Counters
| **Gauge**                                     | **Counter**                                      |
|-----------------------------------------------|--------------------------------------------------|
| Can increase, decrease, or remain constant    | Only increases or resets to zero                 |
| Used for values that go up and down (e.g., memory, temperature) | Used for counting events like requests or errors |
| Represents the current value/state            | Represents cumulative totals over time           |
### Summary Metrics
A metric type that tracks the size of observed events, providing quantiles (e.g., 95th percentile) and total counts, which is useful for measuring request durations or sizes.
**Tracking Latency:** By tracking different percentiles, you get a more complete picture of how most requests are performing (e.g., the median), as well as insights into the slower requests (e.g., the 90th and 99th percentiles).
**Quantiles vs Percentiles:** A quantile represents a specific point in the distribution of a dataset. For example, the 0.5 quantile is the same as the 50th percentile, which divides the dataset into two halves. A 0.99 quantile represents the 99th percentile, meaning only 1% of the data points are higher than this value.
#### Methods
```
	summaryName := prometheus.NewSummary(prometheus.SummaryOpts{
		Name : "summary_metric_name",
		Help: "A summary of the something measured in sometypes",
		Objectivs: map[float64]float64{
			0.5: 0.05,
			0.9: 0.01,
			0.99: 0.001,
		},
	})
```
#### Breakdown:
**``prometheus.NewSummary()``**:
	This is the function that creates a new Summary metric.
**``SummaryOpts``**:
	These are the options passed to the summary metric that define its behavior.
 **``Name and Help``**:
	 "``summary_metric_name``": This is the name of the metric, and it is meant to track the duration of HTTP requests in seconds.
	"``A summary of the HTTP something durations in seconds.``": A description of the metric, which is helpful for understanding what this metric tracks.
 **``Objectives: map[float64]float64``:**
	 This map defines the **quantiles** and their allowed **absolute error margins**. The quantile represents a specific percentile of the observed data, and the error margin defines how much deviation from the true quantile is acceptable.
##### Use Case:
This is a typical setup to monitor the latency of HTTP requests in a web service. By analyzing the 50th, 90th, and 99th percentiles, you can get a good understanding of how your service is performing:
- The **50th percentile** gives a median view of the latencies.
- The **90th percentile** helps identify if certain requests are taking more time than average.
- The **99th percentile** allows you to track outliers and performance bottlenecks that might affect only a small portion of your traffic but still need attention.

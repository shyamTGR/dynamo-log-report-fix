The file /app/access.log is an Apache-style access log with one request per line. Parse it and write a summary report to /app/report.json. Do not modify /app/access.log.

Success criteria:

1. /app/report.json exists and contains a single valid JSON object.
2. The object has exactly three keys: "total_requests", "unique_ips", and "top_path".
3. "total_requests" is an integer: the total number of request lines in /app/access.log.
4. "unique_ips" is an integer: the number of distinct client IP addresses (the first field of each line).
5. "top_path" is a string: the request path (e.g. "/index.html") that appears in the most requests. The log has a single most-requested path, so no tie-breaking rule is needed.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.

FreeCodeCamp Flask Tutorial: https://www.youtube.com/watch?v=Z1RJmh_OqeA

Multi threading tutorial: https://www.youtube.com/watch?v=3dEPY3HiPtI 

Multi processing tutorial: https://www.youtube.com/watch?v=YOhrIov7PZA 

REST API tutorial: https://realpython.com/api-integration-in-python/ 

OpenTelemetry in Flask tutorial: 
- https://opentelemetry.io/docs/languages/python/getting-started/
- https://scoutapm.com/blog/configuring-opentelemetry-python

Run this command in terminal to see spans printed in console
```shell
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name dice-server \
    flask run 
```

Run this command to start the OpenTelemetry collector in docker
```shell
docker run --name flask-otel-collector -d -p 4317:4317 \
    -v ./otel/otel-collector-config.yml:/etc/otel-collector-config.yml \
    otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yml 
```

Run the application, but don't export to console
```shell
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument --logs_exporter otlp flask run
```

Send traces from otel collector to Jaeger: 
- https://www.aspecto.io/blog/opentelemetry-collector-guide/
- https://www.youtube.com/watch?v=ThCoFDA9XuI
- https://middlewaretechnologies.in/2023/12/how-to-send-opentelemetry-data-to-otlp-collector-and-jaeger-tracing.html

Jaeger UI URL: localhost:16686

Run docker-compose
```shell
docker-compose up -d
```
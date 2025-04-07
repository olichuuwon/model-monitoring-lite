# Setting up Facebook OPT-125M on Triton Inference Server using vLLM (CPU-only)

This guide will help you deploy the facebook/opt-125m model via Triton Inference Server with vLLM backend, with monitoring through Prometheus and Grafana.

## 1. Directory Structure

Create the following directory structure:

```
triton-opt-deployment/
├── docker-compose.yml
├── model_repository/
│   └── opt/
│       ├── config.pbtxt
│       └── 1/
│           └── model.py  # Optional, as the model is downloaded automatically
├── prometheus/
│   └── prometheus.yml
└── grafana/
    ├── dashboards/
    │   └── triton-opt-dashboard.json
    └── provisioning/
        └── datasources/
            └── prometheus.yml
```

## 2. Model Repository Setup

The vLLM backend will automatically download the model from Hugging Face. You just need to set up the proper config.pbtxt file in the opt directory.

- Place the provided `config.pbtxt` file in the `model_repository/opt/` directory
- Create an empty `1` directory inside `model_repository/opt/`

## 3. Prometheus Configuration

Create a `prometheus.yml` file in the prometheus directory:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "triton"
    scrape_interval: 5s
    static_configs:
      - targets: ["triton:8002"]
    metrics_path: /metrics

  - job_name: "prometheus"
    scrape_interval: 10s
    static_configs:
      - targets: ["localhost:9090"]
```

## 4. Grafana Configuration

Create a datasource configuration in `grafana/provisioning/datasources/prometheus.yml`:

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

## 5. Deployment Instructions

1. **Start the Services**:

   ```bash
   cd triton-opt-deployment
   docker-compose up -d
   ```

2. **Check Status**:

   ```bash
   docker-compose logs -f triton
   ```

   Wait until you see logs indicating the model is loaded successfully.

3. **Test the Model**:
   ```bash
   curl -X POST http://localhost:8000/v2/models/opt/generate -d '{
     "text_input": "Once upon a time",
     "max_tokens": 50,
     "temperature": 0.7
   }'
   ```

## 6. Performance Considerations (CPU-only)

For CPU-only deployment of OPT-125M:

1. **Memory Requirements**:

   - Ensure your system has at least 4GB of available RAM
   - The model requires approximately 2-3GB of memory

2. **Performance Expectations**:

   - On CPU, inference will be significantly slower than on GPU
   - Expect token generation speeds of around 1-5 tokens per second
   - Batch processing will be limited due to memory constraints

3. **Configuration Optimization**:
   - Lower `max_model_len` if you run into memory issues
   - Set a reasonable batch size (1-2) for CPU processing

## 7. Monitoring

1. **Access Grafana**:

   - Open http://localhost:3000 in your browser
   - Login with admin/admin
   - Navigate to the Dashboards section to find the Triton dashboard

2. **Key Metrics to Monitor**:
   - Request latency (will be higher on CPU)
   - Memory usage (important for LLM deployment)
   - Inference count and success rate
   - CPU utilization

## Troubleshooting

If you encounter issues:

1. **Memory Errors**:

   - Reduce the model's config parameters (max_model_len, batch size)
   - Consider using quantized versions (but this requires additional setup)

2. **Slow Performance**:

   - This is expected for CPU-only deployment of a transformer model
   - Limit concurrent requests to prevent overloading
   - Consider using a smaller model if possible

3. **Model Loading Failures**:
   - Check internet connectivity as the model is downloaded from HuggingFace
   - Verify disk space for model storage

## Additional Resources

- [vLLM Documentation](https://docs.vllm.ai/)
- [Triton vLLM Backend](https://github.com/triton-inference-server/vllm_backend)
- [OPT Model Documentation](https://huggingface.co/facebook/opt-125m)

needa use gpu ~ from online ~

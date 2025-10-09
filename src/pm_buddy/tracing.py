"""Tracing configuration for PM Buddy application."""

import os
from typing import Optional
from agent_framework.observability import setup_observability
from opentelemetry import trace

def initialize_tracing(
    otlp_endpoint: Optional[str] = None,
    enable_sensitive_data: bool = True,
    service_name: str = "pm-buddy"
) -> None:
    """Initialize OpenTelemetry tracing for the PM Buddy application.
    
    Args:
        otlp_endpoint: OTLP endpoint URL. Defaults to AI Toolkit's gRPC endpoint.
        enable_sensitive_data: Whether to capture prompts and completions in traces.
        service_name: Name of the service for tracing identification.
    """
    if otlp_endpoint is None:
        # Use AI Toolkit's default gRPC endpoint
        otlp_endpoint = "http://localhost:4317"

    # Set service name as environment variable for OpenTelemetry
    os.environ.setdefault("OTEL_SERVICE_NAME", service_name)

    # Initialize tracing using agent-framework's built-in observability setup
    setup_observability(
        otlp_endpoint=otlp_endpoint,
        enable_sensitive_data=enable_sensitive_data
    )

    print(f"✅ Tracing initialized - Service: {service_name}, Endpoint: {otlp_endpoint}")


def get_tracer(name: str = "pm-buddy"):
    """Get a tracer instance for manual instrumentation.
    
    Args:
        name: The name of the tracer
        
    Returns:
        OpenTelemetry tracer instance
    """
    return trace.get_tracer(name)

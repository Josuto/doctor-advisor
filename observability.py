from pydantic_ai import Agent


def init_telemetry(
    project_name: str | None = None,
    endpoint: str = "http://127.0.0.1:6006",
    enrich_spans: bool = True,
) -> None:
    """Initialize OpenTelemetry tracing for Phoenix.

    Args:
        project_name: Project name shown in Phoenix UI.
        endpoint: Phoenix server base URL.
        enrich_spans: If True, add OpenInference span enrichment for richer
            Phoenix visualizations. If False, use standard OTel format.
    """
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor

    # Create and register a TracerProvider (Phoenix uses this attribute for project routing)
    resource = (
        Resource.create({"openinference.project.name": project_name})
        if project_name
        else None
    )
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Optionally enrich spans with OpenInference attributes (must be added before exporter)
    if enrich_spans:
        from openinference.instrumentation.pydantic_ai import OpenInferenceSpanProcessor

        tracer_provider.add_span_processor(OpenInferenceSpanProcessor())

    # Export spans to Phoenix
    tracer_provider.add_span_processor(
        SimpleSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces"))
    )

    # Enable PydanticAI instrumentation
    Agent.instrument_all()
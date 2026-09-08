# Deployment

Deployment configuration will be added after the existing CHOP VM is redeployed and its CPU,
memory, Docker, Neo4j, DDKG release, networking, and authentication settings are recorded.

The initial deployment will be CPU-only and will keep Ollama and Neo4j on internal Docker
networks. Only the browser application will be eligible for DMZ exposure.

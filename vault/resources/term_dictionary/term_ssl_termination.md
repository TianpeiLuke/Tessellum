---
tags:
  - resource
  - terminology
  - networking
  - security
  - infrastructure
keywords:
  - SSL termination
  - TLS termination
  - TLS offloading
  - SSL offloading
  - reverse proxy SSL
  - load balancer TLS
  - certificate management
  - SSL passthrough
  - SSL bridging
  - SSL re-encryption
  - HTTPS offloading
  - TLS handshake
  - X.509 certificate
  - SNI (Server Name Indication)
topics:
  - Networking
  - Security
  - Infrastructure
  - Distributed Systems
  - Web Architecture
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: SSL Termination

## Definition

**SSL Termination** (also called **TLS termination** or **TLS/SSL offloading**) is the practice of decrypting TLS-encrypted traffic at a network boundary device — typically a load balancer, reverse proxy, or application delivery controller (ADC) — so that backend servers receive and process only plaintext HTTP. The termination point holds the server's X.509 certificate and private key, performs the TLS handshake with clients, and forwards decrypted requests over an internal network to origin servers.

Because TLS handshakes are CPU-intensive (asymmetric key exchange, symmetric cipher negotiation, certificate verification), offloading this work to a dedicated edge device frees backend application servers to focus on business logic, improving throughput and simplifying horizontal scaling. Certificates are managed in a single location rather than distributed across every backend instance.

## Context

SSL termination is a foundational pattern in modern web infrastructure. Nearly every production deployment of web services routes traffic through a termination point — whether an NGINX or HAProxy reverse proxy, a cloud provider's managed load balancer (AWS ALB/NLB, GCP Cloud Load Balancing, Azure Application Gateway), or a CDN edge node (CloudFront, Cloudflare). In abuse-detection and fraud-prevention systems, SSL termination is operationally significant because it is the point where encrypted traffic becomes inspectable, enabling Layer 7 analysis, request logging, DDoS mitigation on decrypted payloads, and injection of security headers or rate-limiting signals before traffic reaches application services.

## Key Characteristics

### Three TLS Handling Modes

| Mode | How It Works | Encryption on Internal Network | Layer 7 Inspection | Certificate Location |
|------|-------------|-------------------------------|--------------------|--------------------|
| **SSL Termination (Offloading)** | Edge device decrypts; forwards plaintext HTTP to backends | None | Yes | Edge only |
| **SSL Passthrough** | Edge device forwards encrypted traffic untouched; backend decrypts | End-to-end TLS | No | Backend servers |
| **SSL Bridging (Re-encryption)** | Edge device decrypts, inspects, then re-encrypts with a separate TLS session to the backend | Re-encrypted TLS | Yes | Edge + Backend |

### Performance Benefits

- **CPU offloading**: TLS handshakes add 20-30% CPU overhead on servers; termination moves this cost to purpose-built edge infrastructure (often with hardware TLS acceleration).
- **Connection reuse**: The termination point can maintain persistent connections to backends (HTTP keep-alive, connection pooling) while handling thousands of short-lived client TLS sessions.
- **Caching enablement**: Decrypted traffic at the edge allows HTTP caching, reducing backend load by 40-60% for cacheable content.
- **Simplified scaling**: New backend instances require no certificate installation; horizontal scaling becomes a matter of adding compute without cryptographic configuration.

### Certificate Management

- **Centralized certificates**: A single edge device (or a small cluster) holds the X.509 certificate and private key, reducing the blast radius of key compromise and simplifying renewal workflows.
- **Automated renewal**: Tools like Let's Encrypt / ACME protocol integrate with edge devices for zero-downtime certificate rotation.
- **SNI (Server Name Indication)**: The termination point can use SNI to serve multiple domains from a single IP address, selecting the correct certificate based on the client's requested hostname during the TLS ClientHello.
- **Wildcard and SAN certificates**: Edge devices can manage wildcard (`*.example.com`) or Subject Alternative Name certificates to cover many services behind a single termination point.

### Security Trade-offs

**Advantages of termination:**
- Enables Layer 7 inspection: WAF rules, bot detection, abuse signal extraction, and request logging all require access to decrypted HTTP payloads.
- Simplifies DDoS mitigation by allowing pattern analysis on plaintext traffic.
- Single point of certificate management reduces the probability of misconfigured or expired certificates.
- Enables HTTP header injection (e.g., `X-Forwarded-For`, `X-Request-ID`) for traceability.

**Risks of termination:**
- **Plaintext internal traffic**: Data between the termination point and backends is unencrypted. Mitigations include network segmentation (private VLANs), mTLS for internal traffic (SSL bridging), and ensuring the internal network is not reachable from untrusted zones.
- **Single point of compromise**: If the termination device is breached, the attacker gains access to all decrypted traffic and the private key. Mitigations include HSMs (Hardware Security Modules) for key storage, strict access controls, and regular key rotation.
- **Compliance considerations**: Regulations like PCI DSS and HIPAA may require end-to-end encryption, making SSL passthrough or SSL bridging mandatory for certain data flows.

### When to Use Each Mode

- **SSL Termination**: Best for most web applications where internal networks are trusted, Layer 7 routing is needed, and performance is a priority. Suitable for abuse-detection pipelines that need to inspect request payloads.
- **SSL Passthrough**: Required for zero-trust architectures, end-to-end encryption mandates, or when the edge device should not have access to plaintext data (e.g., healthcare, financial PII).
- **SSL Bridging**: Compromise approach — enables inspection at the edge while maintaining encryption on the internal network. Higher CPU cost due to double encrypt/decrypt but satisfies both inspection and encryption requirements.

## Related Terms

- **[Self-Supervised Learning (SSL)](term_ssl.md)**: Shares the SSL acronym but refers to a machine learning paradigm; SSL termination is a networking concept
- **[Proxy Pattern](term_proxy_pattern.md)**: Reverse proxies performing SSL termination are a concrete instance of the proxy structural pattern, interposing decryption logic before forwarding to the real subject
- **[Load Balancing Loss](term_load_balancing_loss.md)**: While load balancing loss is an ML concept (mixture-of-experts), SSL termination is commonly deployed on load balancers that distribute traffic across backend servers
- **[Microservices Architecture](term_microservices_architecture.md)**: SSL termination at an API gateway or ingress controller is a standard pattern in microservices deployments, centralizing TLS handling for many small services
- **[Layered Architecture](term_layered_architecture.md)**: SSL termination embodies the layered principle — the TLS layer is handled at the edge, cleanly separated from application logic layers
- **[IPS Attack Vectors and Infrastructure](term_ips_attack_vectors_and_infrastructure.md)**: SSL termination enables inspection of decrypted traffic for impersonation and phishing attack signatures
- **[SMS Technology and Infrastructure](term_sms_technology_and_infrastructure.md)**: Infrastructure-level concept paralleling SSL termination in providing foundational transport capabilities for abuse-detection systems
- **[GDPR](term_gdpr.md)**: Data protection regulations may impose constraints on where SSL termination occurs and who can access decrypted traffic
- **[Phishing](term_phishing.md)**: SSL termination points can inspect decrypted traffic for phishing indicators, malicious payloads, and suspicious request patterns
- **[Traffic Stream](term_traffic_stream.md)**: SSL termination is the entry point where encrypted traffic streams are decrypted and become available for downstream analysis and routing
- **[CSMO Technology and Performance](term_csmo_technology_and_performance.md)**: Performance optimization through SSL offloading parallels CSMO's technology-driven performance considerations
- **[API Gateway](term_api_gateway.md)**: SSL/TLS termination is a core responsibility of API Gateways, which handle encryption at the edge so internal service-to-service traffic can use lighter protocols
- **[HAProxy](term_haproxy.md)**: HAProxy supports SSL termination, SSL passthrough, and SSL re-encryption modes, serving as a dedicated TLS offloading layer in front of backend servers
- **[NGINX](term_nginx.md)**: NGINX handles TLS termination at the edge with support for TLS 1.2/1.3, OCSP stapling, and session resumption, centralizing certificate management for backend services
- **[Reverse Proxy](term_reverse_proxy.md)**: SSL termination is a core function of reverse proxies -- the reverse proxy decrypts TLS traffic at the edge and forwards plaintext requests to backend servers over a trusted internal network

## References

### External Sources
- [What is SSL/TLS Termination? — HAProxy](https://www.haproxy.com/glossary/what-is-ssl-tls-termination)
- [SSL Termination — GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/ssl-termination/)
- [TLS/SSL Offloading — CyberArk](https://www.cyberark.com/what-is/tls-ssl-offloading/)
- [SSL Offloading/Termination vs SSL Passthrough vs SSL Bridging — CodeNx](https://medium.com/codenx/ssl-offloading-termination-vs-ssl-passthrough-vs-ssl-bridging-a34962e0cb70)
- [SSL Termination in Load Balancers: Risks and Benefits — OptiBlack](https://optiblack.com/insights/ssl-termination-in-load-balancers-risks-and-benefits)
- [HAProxy SSL Termination in 5 Simple Steps — HAProxy](https://www.haproxy.com/blog/haproxy-ssl-termination)
- [The Pros and Cons of Offloading TLS/SSL to Your ADC — Loadbalancer.org](https://www.loadbalancer.org/blog/the-pros-and-cons-of-offloading-ssl-decryption-encryption-to-your-adcs/)

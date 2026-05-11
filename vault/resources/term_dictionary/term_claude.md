---
tags:
  - resource
  - terminology
  - llm
  - foundation_model
  - anthropic
keywords:
  - Claude
  - Anthropic Claude
  - Claude LLM
  - foundation model
  - large language model
  - Bedrock integration
  - investigation automation
  - return abuse prevention
topics:
  - foundation models
  - large language models
  - investigation automation
  - fraud detection
language: markdown
date of note: 2026-02-20
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Projects/Interns/Shengjie/Guardian/
related_sfsc_wiki: https://w.amazon.com/bin/view/SFSC/managed-services/Professional-Service-App-Central/GenAI-For-Salesforce-Bedrock/
related_llm_wiki: https://w.amazon.com/bin/view/LLMs/
---

# Claude - Anthropic's Large Language Model Family

## Definition

**Claude** is Anthropic's family of advanced Large Language Models (LLMs) available through Amazon Bedrock, comprising multiple variants (Haiku, Sonnet, Opus) optimized for different use cases ranging from fast, cost-effective interactions to sophisticated reasoning and complex analysis. At Amazon, Claude serves as a critical foundation model powering buyer abuse prevention through applications like Guardian (unified multimodal LLM outperforming Claude 3 Sonnet on return abuse prevention tasks), GreenTEA (BAP's first agentic AI using Claude Sonnet 4 for investigation automation achieving +9% AUC improvement), and AutoSignality (Phase II implementation using Claude 3 with RAG for payment fraud automation targeting $27MM savings). Claude models provide enterprise-grade reasoning capabilities, context understanding up to 200K tokens, and multimodal processing enabling Amazon's investigation automation, customer service enhancement, and fraud detection systems to achieve human-level decision-making accuracy while maintaining scalability and cost efficiency.

## Purpose

Claude serves multiple critical functions in Amazon's AI and investigation automation ecosystem:

1. **Investigation Automation**: Power fraud detection and abuse prevention through sophisticated reasoning capabilities
2. **Multi-Modal Analysis**: Process text, images, and tabular data for comprehensive fraud analysis
3. **SOP Compliance**: Enable automated decision-making following Standard Operating Procedures
4. **Complex Reasoning**: Handle sophisticated analysis requiring deep contextual understanding
5. **Agentic AI**: Support multi-agent frameworks and complex workflow orchestration
6. **Enterprise Applications**: Provide reliable, scalable AI for business-critical applications

## Technical Architecture

### Claude Model Variants

**Claude 3.5/4.5 Haiku**:
- **Use Case**: Near-instant responsiveness for simple queries and live interactions
- **Strengths**: Fastest, most compact model with low latency
- **Applications**: Quick support, translations, content moderation, logistics optimization
- **Cost**: Most economical option for high-volume, simple tasks

**Claude 3.5/4.5 Sonnet**:
- **Use Case**: Ideal balance between intelligence and speed for enterprise workloads
- **Strengths**: Maximum utility, dependable for scaled AI deployments
- **Applications**: RAG systems, search & retrieval, product recommendations, code generation
- **Amazon Usage**: GreenTEA production model, Guardian comparison baseline

**Claude 3.5 Opus**:
- **Use Case**: Highest intelligence for most complex tasks requiring deep reasoning
- **Strengths**: Superior performance on sophisticated analysis and creative tasks
- **Applications**: Complex reasoning, detailed analysis, advanced problem-solving
- **Enterprise**: Premium model for most demanding use cases

**Claude Instant**:
- **Use Case**: Faster, lower-priced model for casual interactions
- **Strengths**: Cost-effective with good capability for standard tasks
- **Applications**: Casual dialogue, text analysis, summarization, document comprehension

### Model Capabilities

**Context and Memory**:
- **Context Window**: Up to 200K tokens (Claude 2.1+) enabling long document analysis
- **Reduced Hallucination**: Improved accuracy and reliability over long contexts
- **Document Analysis**: Excellent performance on multi-document comparison and analysis
- **Memory Management**: Efficient handling of large contexts for complex reasoning

**Advanced Features**:
- **Tool Use**: Function calling and API integration capabilities
- **Code Generation**: Advanced programming assistance and code analysis
- **Multimodal**: Vision capabilities for image analysis and document processing
- **Reasoning**: Sophisticated logical reasoning and complex problem-solving

## Amazon Applications

### Buyer Abuse Prevention

**Guardian (Unified Multimodal LLM)**:
- **Architecture**: 8B Idefics2 vision-language model with Sparse Mixture of Experts projector
- **Training Data**: Synthetic dialogue pipeline using Claude 3 Sonnet from 71 active BAP SOPs
- **Performance**: Outperforms Claude 3 Sonnet on return abuse prevention tasks
- **Capabilities**: Return risk classification, customer risk classification, enforcement action determination
- **Multimodal**: Processes SOPs as vision input, tabular data, embeddings directly without text conversion

**GreenTEA (BAP's First Agentic AI)**:
- **Production Model**: Claude Sonnet 4 on Bedrock for optimal performance
- **Multi-Agent Framework**: Predictor + Error Analyzer + Prompt Generator agents
- **Business Impact**: +9% AUC improvement, PFW automation 15%→50% (NA), 60%→80% (EU)
- **Cost Efficiency**: LPA $1.63 vs Human $3.72, expanding across multiple abuse vectors
- **Genetic Algorithm**: Uses Claude for prompt evolution and optimization

**AutoSignality (Payment Risk Automation)**:
- **Phase II Architecture**: Claude 3 with RAG, few-shot prompting, Chain-of-SOPs
- **Multi-Agent**: Claude 3 deliberation for complex investigation scenarios
- **Business Target**: $27MM total savings (Phase II expansion)
- **Integration**: Handles DeepCARE residual volume with superior performance

### Enterprise and Customer Service

**Amazon Business (SFSC Applications)**:
- **CS Agent Support**: Claude models for Salesforce customer service automation
- **Model Recommendation**: Claude 3 variants show best overall results in enterprise testing
- **Integration**: Bedrock Knowledge Bases with RAG for accurate, grounded responses
- **Use Cases**: Question answering, summarization, content generation, code analysis

**Development and Productivity**:
- **Claude CLI**: AI peer-programmer for developers with file editing and bug fixing
- **Code Analysis**: Answers questions about architecture and logic
- **Test Execution**: Fixes tests, resolves merge conflicts, terminal integration
- **Local Environment**: Works directly with development environment and codebase

**Cartesio (Amazon Business)**:
- **BP LLM for CS Agents**: Customer service automation for business prime customers
- **Knowledge Base**: RAG implementation with OpenSearch Serverless vector database
- **Model Selection**: Claude 3 Haiku recommended for cost-effective enterprise deployment
- **Integration**: API Gateway + Lambda architecture for CS agent interface

### Technical Implementation

**Bedrock Integration**:
- **Managed Service**: Claude models hosted on Amazon Bedrock infrastructure
- **API Access**: RESTful APIs through Bedrock service endpoints
- **Messages API**: Anthropic Claude Messages API for advanced conversation management
- **Enterprise Features**: Security, compliance, governance through Bedrock platform

**RAG and Knowledge Integration**:
- **Bedrock Knowledge Bases**: Claude models with OpenSearch vector database backend
- **Document Processing**: Automatic chunking, embedding generation, context retrieval
- **Source Attribution**: Grounded responses with document citations
- **Multi-Document Analysis**: Superior performance on complex document comparison tasks

## Business Impact

### Investigation Automation Achievements

**Return Abuse Prevention**:
- **Guardian Performance**: Outperforms Claude 3 Sonnet baseline on three key tasks
- **Multimodal Efficiency**: Avoids SOP rewriting and text conversion requirements
- **Automation Accuracy**: Maintains high accuracy while reducing manual investigation burden
- **Cost Optimization**: Balanced performance-cost trade-offs for enterprise deployment

**Fraud Detection Enhancement**:
- **GreenTEA Success**: +9% AUC improvement over manual prompts (0.736→0.803)
- **Automation Scale**: PFW automation 15%→50% (NA), 60%→80% (EU)
- **Cost Reduction**: LPA $1.63 vs Human $3.72 through automated decision-making
- **Multi-Vector Expansion**: Successful deployment across multiple abuse detection scenarios

### Enterprise Productivity

**Development Acceleration**:
- **Claude CLI**: AI-assisted programming with codebase integration
- **Documentation**: Automated generation and maintenance of technical documentation
- **Code Quality**: Bug detection, test automation, merge conflict resolution
- **Architecture Analysis**: Deep understanding of complex codebases and logic

**Customer Service Enhancement**:
- **CS Agent Support**: AI-powered assistance for customer service representatives
- **Knowledge Retrieval**: Accurate, grounded responses through RAG systems
- **Multi-Language**: Global customer service with Claude's language capabilities
- **Context Understanding**: Superior performance on long, complex customer interactions

## Regional Context

### Amazon Global Deployment

**Buyer Abuse Prevention**:
- **GreenTEA Global**: Investigation automation across worldwide abuse prevention operations
- **AutoSignality**: Payment risk automation expanding to global markets
- **Guardian Research**: Return abuse prevention with multimodal capabilities
- **Enterprise Integration**: SFSC, Amazon Business, customer service applications

**Model Availability**:
- **Bedrock Regions**: Claude models available across major AWS regions
- **Enterprise Support**: Global deployment with enterprise SLAs and support
- **Cost Optimization**: Regional pricing optimization and volume discounts
- **Compliance**: Data residency and privacy compliance across regions

### Performance and Scaling

**Production Deployments**:
- **High-Volume Processing**: Scalable through Bedrock managed infrastructure
- **Cost Management**: Pay-per-use pricing with model-specific optimization
- **Reliability**: Enterprise-grade availability and performance guarantees
- **Integration**: Native AWS service integration across the stack

## Documentation References

### Internal Amazon Documentation

**Buyer Abuse Prevention Applications**:
- **[Guardian Multimodal LLM](https://w.amazon.com/bin/view/CTPS/BuyerAbuse/BuyerAbuseML/Projects/Interns/Shengjie/Guardian/)** - Unified multimodal LLM using Claude for return abuse prevention
- **[SFSC Salesforce GenAI](https://w.amazon.com/bin/view/SFSC/managed-services/Professional-Service-App-Central/GenAI-For-Salesforce-Bedrock/)** - Claude integration for customer service automation
- **[LLM Working Session](https://w.amazon.com/bin/view/LLMs/)** - Claude CLI and development tools for Amazon builders

**Technical Implementation**:
- **[Cartesio BP LLM](https://w.amazon.com/bin/view/B2B/Fallout/Sandia/Cartesio/Design/)** - Claude implementation for Amazon Business customer service agents
- **[AWS Bedrock Claude Pattern](https://apg-library.amazonaws.com/content/c10ea405-7eda-470f-a13c-b2a576358741)** - Anthropic Claude Messages API and Bedrock integration

### Project Documentation

**Investigation Automation**:
- **[Project: Guardian](../../projects/project_guardian.md)** - Multimodal return abuse prevention using Claude *(if exists)*
- **[Project: GreenTEA](../../projects/project_greentea.md)** - Agentic AI using Claude Sonnet 4 *(if exists)*

## Related Systems

### Foundation Model Platforms

- **[Bedrock](term_bedrock.md)** - AWS managed platform hosting Claude models
- **[LLM](term_llm.md)** - Large Language Models category including Claude *(if exists)*
- **[Foundation Models](term_foundation_models.md)** - Enterprise foundation model ecosystem *(if exists)*
- **[Anthropic](term_anthropic.md)** - Model provider company *(if exists)*

### Amazon AI Applications

- **[GreenTEA](term_greentea.md)** - Agentic AI using Claude Sonnet 4 for investigation automation *(if exists)*
- **[AutoSignality](term_autosignality.md)** - Payment risk automation using Claude 3 with RAG *(if exists)*
- **[Guardian](term_guardian.md)** - Multimodal return abuse prevention system *(if exists)*
- **[Amazon Q](term_amazon_q.md)** - Enterprise AI assistant platform with Claude integration

### AWS Integration

- **[RAG](term_rag.md)** - Retrieval-Augmented Generation systems using Claude *(if exists)*
- **[OpenSearch](term_opensearch.md)** - Default vector database for Claude-powered RAG systems
- **[SageMaker](term_sagemaker.md)** - ML platform with Claude integration capabilities
- **[Lambda](term_lambda.md)** - Serverless deployment for Claude applications *(if exists)*

## Technical Specifications

### Model Specifications

**Claude 3.5/4.5 Model Family**:
- **Parameters**: Ranging from compact (Haiku) to large (Opus) architectures
- **Context Window**: Up to 200K tokens for long document analysis
- **Multimodal**: Vision capabilities for image and document processing
- **Languages**: Multilingual support for global applications

**Performance Characteristics**:
- **Reasoning**: Advanced logical reasoning and complex problem-solving
- **Accuracy**: Reduced hallucination rates and improved factual accuracy
- **Speed**: Variable latency based on model variant and task complexity
- **Reliability**: Consistent performance across different input types and domains

### Integration Capabilities

**Bedrock Platform**:
- **Managed Infrastructure**: Fully managed deployment and scaling
- **Enterprise Security**: VPC endpoints, encryption, compliance certifications
- **Cost Control**: Pay-per-use pricing with token-based billing
- **API Access**: RESTful APIs and SDK integration across programming languages

**Advanced Features**:
- **Function Calling**: Tool use and API integration capabilities
- **RAG Integration**: Seamless knowledge base connectivity through Bedrock
- **Fine-Tuning**: Custom model training on domain-specific data
- **Multi-Agent**: Support for complex agent frameworks and orchestration

## Summary

**Claude Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Claude (Anthropic's Large Language Model Family) |
| **Variants** | Haiku (fast), Sonnet (balanced), Opus (sophisticated) |
| **Provider** | Anthropic (available through Amazon Bedrock) |
| **Context Window** | Up to 200K tokens for long document analysis |
| **Key Features** | Advanced reasoning, multimodal, reduced hallucination, function calling |
| **Amazon Applications** | Guardian (return abuse), GreenTEA (investigation), AutoSignality (fraud) |
| **BAP Impact** | +9% AUC (GreenTEA), outperforms baseline (Guardian), $27MM target (AutoSignality) |
| **Best For** | Complex reasoning, investigation automation, enterprise AI applications |

**Key Insight**: Claude represents the state-of-the-art in foundation models for Amazon's buyer abuse prevention and investigation automation, where its advanced reasoning capabilities, reduced hallucination rates, and sophisticated contextual understanding enable applications like GreenTEA to achieve superior performance over manual investigation processes while maintaining the reliability and accuracy required for enforcement actions. The model family's design for enterprise workloads—balancing intelligence, speed, and cost across variants—enables Amazon teams to optimize for specific use cases from high-volume customer service interactions (Haiku) to complex multi-step fraud investigations (Sonnet/Opus). For buyer abuse prevention, Claude's ability to process Standard Operating Procedures, understand complex customer scenarios, and generate reliable enforcement recommendations transforms traditional manual investigation workflows into scalable, automated systems that preserve investigator expertise while dramatically increasing processing capacity and consistency.

---

**Last Updated**: February 20, 2026  
**Status**: Active - Primary LLM for Amazon's investigation automation and fraud detection applications  
**Domain**: Foundation Models, Large Language Models, Investigation Automation, Fraud Detection
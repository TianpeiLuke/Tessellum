---
tags:
  - resource
  - terminology
  - machine_learning
  - computer_vision
  - vision_transformer
  - document_classification
keywords:
  - SWIN Transformer
  - Shifted Windows
  - Vision Transformer
  - Document Classification
  - Computer Vision
  - Hierarchical Vision Transformer
topics:
  - buyer risk prevention
  - machine learning
  - computer vision
  - document verification
  - fraud detection
  - deep learning
language: markdown
date of note: 2026-02-17
status: active
building_block: concept
related_wiki: https://w.amazon.com/bin/view/Users/disuna/SPAM_PR/
---

# SWIN Transformer - Shifted Window Transformer

## Definition

**SWIN Transformer** stands for **Shifted Window Transformer**. It is a hierarchical vision transformer that uses shifted windows for efficient visual feature representation, designed as a general-purpose backbone for computer vision tasks. At Amazon/BRP, SWIN Transformer is deployed for document classification in abuse prevention workflows, specifically for detecting invalid police report submissions in buyer abuse cases through automated document verification.

**Key Function**: Process images using hierarchical attention mechanisms to classify documents and detect visual patterns, enabling automated verification of customer-submitted evidence documents.

## Full Name

**Shifted Window Transformer** (Hierarchical Vision Transformer using Shifted Windows)

**Synonyms & Related Terms**:
- **Vision Transformer (ViT)**: Broader category of transformer models for computer vision
- **Hierarchical Vision Transformer**: Architecture type that builds multi-scale feature representations
- **Document Classifier**: Downstream application for document type detection
- **Window-based Attention**: Core mechanism for computational efficiency

## How SWIN Transformer Works

### Architecture Foundation

```
┌─────────────────────────────────────────────────────────────────┐
│                    SWIN Transformer Architecture                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         Hierarchical Feature Extraction                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │ Patch       │→ │ Window      │→ │ Shifted     │     │   │
│  │  │ Partition   │  │ Attention   │  │ Windows     │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                Multi-Scale Feature Maps                         │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ Stage 1: 56×56      │  │ Stage 2: 28×28      │              │
│  │ Small receptive     │  │ Medium receptive    │              │
│  │ field               │  │ field               │              │
│  └─────────────────────┘  └─────────────────────┘              │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ Stage 3: 14×14      │  │ Stage 4: 7×7        │              │
│  │ Large receptive     │  │ Global receptive    │              │
│  │ field               │  │ field               │              │
│  └─────────────────────┘  └─────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                Document Classification                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Feature     │  │ Global      │  │ Class       │             │
│  │ Pooling     │  │ Average     │  │ Prediction  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### Key Innovations

**1. Shifted Window Mechanism**
- **Regular Windows**: Self-attention computed within fixed 7×7 windows
- **Shifted Windows**: Windows moved by (⌊M/2⌋, ⌊M/2⌋) pixels between layers
- **Cross-window Connections**: Enable information flow across window boundaries
- **Computational Efficiency**: Linear complexity O(HW) vs quadratic O(H²W²)

**2. Hierarchical Feature Representation**
- **Patch Merging**: Reduces resolution while increasing channel dimensions
- **Multi-Scale Features**: Different stages capture fine to coarse patterns
- **CNN-like Inductive Bias**: Better for dense prediction tasks than flat ViT

**3. Model Variants**

| Variant | Layers | Channels | Window Size | Parameters |
|---------|--------|----------|-------------|------------|
| SWIN-T (Tiny) | [2,2,6,2] | 96 | 7×7 | 29M |
| SWIN-S (Small) | [2,2,18,2] | 96 | 7×7 | 50M |
| SWIN-B (Base) | [2,2,18,2] | 128 | 7×7 | 88M |
| SWIN-L (Large) | [2,2,18,2] | 192 | 7×7 | 197M |

## SWIN Transformer at Amazon/BRP

### Production Models

#### Police Report SPAM Detection (Primary Use Case)
**Purpose**: Automatically identify invalid police report submissions in buyer abuse cases
**Architecture**: SWIN Transformer fine-tuned for document classification
**Data Source**: S3-stored police reports (PDF/image format) from customer concession requests
**Performance**:
  - **96% Precision** at threshold 0.01 (minimizes false positives)
  - **60% Recall** (catches majority of invalid submissions)
  - **93% Accuracy** overall
  - **9.6% Filtered Volume** (105/1,094 contacts automated)
**Training Data**: 77K police reports across 15 months (US, CA, UK)
**Launch**: January 2026 (Model: checkpoint-2829)
**Contributor**: @disuna
**Wiki**: [SPAM Detection by SWIN Transformer](https://w.amazon.com/bin/view/Users/disuna/SPAM_PR/)

#### Document Types Detected
```
Valid Police Reports:
├── Documents with police department logos
├── Case IDs and incident narratives  
├── Official report formats
└── Law enforcement letterheads

Invalid Submissions (Filtered):
├── Screenshots of web pages
├── Contact cards or business cards
├── Title pages only (no content)
├── Unrelated documents
└── Generic forms without police headers
```

### Technical Implementation

#### Model Training Pipeline
```python
# SWIN Transformer fine-tuning for document classification
from transformers import AutoModelForImageClassification, AutoFeatureExtractor

# Load pre-trained SWIN model
model_name = "microsoft/swin-tiny-patch4-window7-224"
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(
    model_name,
    num_labels=2,  # Binary: valid_police_report/invalid
    ignore_mismatched_sizes=True
)

# Data preparation
def prepare_document_image(image_path):
    """Convert PDF/image to model input format"""
    # Convert PDF pages to images if needed
    # Resize to 224×224 (SWIN standard input)
    return feature_extractor(image, return_tensors="pt")

# Training configuration
training_args = {
    "learning_rate": 1e-5,
    "batch_size": 2,
    "num_train_epochs": 10,
    "selected_checkpoint": "checkpoint-2829"
}
```

#### Deployment Architecture
```
Customer Submission → S3 Storage → PDF→Image Conversion → 
SWIN Transformer (MIMS) → Classification Score → 
Threshold (0.01) → Auto-filter/Human Review
```

### Performance Comparison

| Approach | Precision | Recall | Accuracy | Use Case |
|----------|-----------|--------|----------|----------|
| **SWIN Transformer** | **96%** | **60%** | **93%** | **Document classification** |
| Claude 3.7 Sonnet | 91% | 91% | 87% | LLM-based labeling |
| Manual Review | ~98% | 100% | ~98% | Human baseline |
| OCR + Keywords | Variable | Low | Variable | Text-based detection |

### Integration with BRP Workflow

#### SPAM Detection Pipeline
1. **Document Submission**: Customer uploads police report for concession request
2. **Preprocessing**: PDF converted to images, stored in S3
3. **SWIN Classification**: Model scores document validity (0-1)
4. **Threshold Decision**: Score > 0.01 → Flag as invalid SPAM
5. **Action**: Invalid documents filtered out, valid ones proceed to human review
6. **Quality Control**: 5% sample maintained for continuous validation

#### Related Systems Integration
- **VISTA**: Handles duplicate detection and metadata extraction
- **CAP**: Addresses GenAI-modified images (future enhancement)
- **AMES**: Model endpoint serving infrastructure
- **MIMS**: Model registration and versioning

## SWIN vs Other Vision Models

### SWIN vs Vision Transformer (ViT)

| Aspect | SWIN Transformer | Vision Transformer (ViT) |
|--------|------------------|---------------------------|
| **Attention** | Window-based (7×7) | Global (full image) |
| **Complexity** | O(HW) - Linear | O(H²W²) - Quadratic |
| **Features** | Hierarchical multi-scale | Single-scale |
| **Inductive Bias** | CNN-like local connectivity | Minimal assumptions |
| **Performance** | Better for dense tasks | Better with large datasets |
| **BRP Use** | Document classification | Not deployed |

### SWIN vs CNN Models

| Aspect | SWIN Transformer | CNN (ResNet/EfficientNet) |
|--------|------------------|---------------------------|
| **Receptive Field** | Global through attention | Limited by kernel size |
| **Long-range Dependencies** | Direct modeling | Requires deep stacking |
| **Feature Learning** | Self-supervised attention | Convolution + pooling |
| **Data Efficiency** | Requires more data | Better with limited data |
| **Interpretability** | Attention maps | Activation maps |

### When to Use SWIN at BRP

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Document classification | ✅ SWIN | Global context + local details |
| Image-based fraud detection | ✅ SWIN | Multi-scale pattern recognition |
| Real-time inference (<10ms) | ❌ CNN/BERT | Lower latency requirements |
| Small datasets (<1K images) | ❌ CNN | Data efficiency |
| Video analysis | ⚠️ Video SWIN | Temporal modeling needed |

## Computer Vision Applications at Amazon

### Current Deployments

```
Document Verification:
├── Police Report SPAM Detection (BRP - SWIN)
├── Object Detection (Robotics - SWIN backbone)
└── Scene Change Detection (Video - Video SWIN roadmap)

Quality Assessment:
├── Avedon Quality Scoring (SWIN_TRANSFORMER model)
└── Product Image Classification
```

### Evolution & Roadmap

```
2021: SWIN Transformer paper published (Microsoft Research)
2021: First Amazon adoptions (Robotics, Video services)
2022-2024: Gradual expansion across computer vision use cases
2025: BRP SPAM Detection deployment
2026: Potential expansion to return item verification, document forgery detection
Future: Integration with multimodal LLMs for enhanced document understanding
```

## Related Terms

### Vision & Transformers
- **[Vision Transformer (ViT)](term_vit.md)**: Original transformer for computer vision
- **[Transformer](term_transformer.md)**: Foundational attention-based architecture
- **[CV (Computer Vision)](term_computer_vision.md)**: Broad field encompassing image understanding

### Document Processing
- **[OCR](term_ocr.md)**: Text extraction from documents (complementary to SWIN)
- **[Document Classification](term_document_classification.md)**: Task of categorizing document types
- **[VLM](term_vlm.md)**: Vision Language Models for multimodal understanding

### BRP Applications
- **[SPAM Detection](term_spam_detection.md)**: Invalid document filtering workflow
- **[Document Verification](term_document_verification.md)**: Evidence validation process
- **[VISTA](term_vista.md)**: Document processing system integration
- **[CAP](term_cap.md)**: Customer Abuse Prevention workflow

### Infrastructure
- **[MIMS](term_mims.md)**: Model Inference Management System
- **[AMES](term_ames.md)**: Model endpoint serving platform
- **[SageMaker](term_sagemaker.md)**: ML training and deployment service

## Performance & Benchmarks

### Academic Benchmarks
- **ImageNet-1K**: 87.3% top-1 accuracy (SWIN-B)
- **COCO Object Detection**: 58.7 box AP (better than ViT)
- **ADE20K Segmentation**: 53.5 mIoU
- **Computational Efficiency**: 4.5× faster than ViT for same accuracy

### BRP Production Metrics
- **Document Classification**: 96% precision, 60% recall
- **Inference Latency**: ~100ms per document image
- **Throughput**: Processes thousands of documents daily
- **Error Rate**: <4% false positive rate in production

## References

### Amazon Internal
- **SPAM Detection Wiki**: https://w.amazon.com/bin/view/Users/disuna/SPAM_PR/
- **Robotics Object Detection**: https://w.amazon.com/bin/view/WW_Ops_Robotics/Robotics_AI/Helios/Science/ObjectDetectionBenchmarkPipelineResult/
- **Video Scene Change**: https://w.amazon.com/bin/view/Amazon_Video/Digital_Video_Supply_Chain/DME/MediaSciences/SceneChangeDetection/ModelDataSharing/
- **Avedon Quality Scoring**: https://w.amazon.com/bin/view/Kahlo/Runbooks/AQS/

### External Resources  
- **Original Paper**: [SWIN Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030)
- **Microsoft GitHub**: https://github.com/microsoft/Swin-Transformer
- **HuggingFace Models**: https://huggingface.co/microsoft/swin-tiny-patch4-window7-224

## Summary

**SWIN Transformer Quick Reference**:

| Aspect | Details |
|--------|---------|
| **Full Name** | Shifted Window Transformer |
| **Architecture** | Hierarchical Vision Transformer with window-based attention |
| **Key Innovation** | Shifted windows for cross-window connections + linear complexity |
| **BRP Application** | Police Report SPAM Detection (document classification) |
| **Performance** | 96% precision, 60% recall, 93% accuracy |
| **Deployment** | MIMS endpoint, SageMaker infrastructure |
| **Model Size** | 29M (Tiny) to 197M (Large) parameters |
| **Input Format** | 224×224 RGB images (documents converted from PDF) |
| **Best For** | Document classification, object detection, image analysis |

**Key Insight**: SWIN Transformer brings **hierarchical attention** to document understanding at BRP, enabling automated filtering of invalid police report submissions with high precision (96%). Unlike flat Vision Transformers, SWIN's **multi-scale feature extraction** captures both fine-grained text details and global document structure, making it ideal for **document authenticity verification**. The shifted window mechanism provides **computational efficiency** for processing large document images while maintaining the **global context** needed to distinguish legitimate police reports from screenshots, contact cards, and other invalid submissions. As Amazon expands computer vision applications in fraud prevention, SWIN Transformer represents a **scalable foundation** for automated document verification workflows across buyer abuse prevention systems.

---

**Last Updated**: February 17, 2026  
**Status**: Active - deployed for police report SPAM detection in buyer abuse prevention
# System Improvement Plan & Future Roadmap

## 1. Current System Analysis

### 1.1 Architecture Overview
The current system (`animal_fresh`) utilizes a robust, two-stage classical Machine Learning approach:
*   **Core Engine**: XGBoost Classifiers (Stage 1: Category, Stage 2: Disease).
*   **Data Source**: 4,000+ synthetic samples covering 20 species.
*   **Validation**: Rule-based `biological_validation` module ensuring species-disease compatibility.
*   **Interface**: FastAPI (REST) and Streamlit (Web UI).

### 1.2 Identified Weaknesses & Opportunities
| Area | Weakness | Opportunity |
|------|----------|-------------|
| **Data Modality** | Restricted to tabular data (blood values, symptoms). | **Multi-modal Learning**: Integrate medical images (X-rays, skin lesions) and clinical notes. |
| **Feature Representation** | Simple One-Hot Encoding for species/breeds creates sparse vectors. | **Learned Embeddings**: Use neural embeddings to capture biological relationships between species. |
| **Generalization** | Trained on synthetic distributions. | **Transfer Learning**: Fine-tune on small subsets of real-world clinical data. |
| **Explainability** | XGBoost offers feature importance, but lacks local instance explanation. | **SHAP/LIME Integration**: Provide "Why this prediction?" explanations for vets. |

---

## 2. Deep Learning Neural Network Plan ("VetNet")

We propose transitioning from isolated XGBoost models to a unified Deep Learning architecture to handle complex, non-linear relationships and multi-modal data.

### 2.1 Proposed Architecture
**Hybrid Multi-Branch Network:**

1.  **Structured Branch (Dense Layers)**
    *   Input: Blood values (WBC, RBC, etc.), Vitals.
    *   Structure: Feed-forward dense layers with Batch Normalization and ReLU.

2.  **Categorical Branch (Embedding Layers)**
    *   Input: Species, Breed, Gender.
    *   Mechanism: Learn dense vector representations (e.g., `Species` -> 32-dim vector) to capture latent biological similarities (e.g., Cat is closer to Dog than to Chicken).

3.  **Future Expansion: Visual Branch (CNN)**
    *   Input: Images of skin lesions or X-rays.
    *   Model: Pre-trained ResNet50 or EfficientNet backbone.

4.  **Fusion Layer**
    *   Concatenates outputs from all branches.
    *   Passes through final Classification Head (Softmax over 400 classes).

### 2.2 Technology Stack
*   **Framework**: PyTorch or TensorFlow/Keras.
*   **Training**: GPU-accelerated training.
*   **Serving**: ONNX Runtime for high-performance CPU inference in the API.

---

## 3. Advanced AI Dashboard Plan

Transform the current simple UI into a comprehensive **Veterinary Command Center**.

### 3.1 Key Features

#### 🧠 Explainable AI (XAI) Panel
*   **What it does**: Visualizes why a diagnosis was made.
*   **Visualization**: Waterfall charts showing how each symptom contributed (e.g., "+30% prob due to High WBC", "-10% prob due to Normal Glucose").

#### 🌍 Real-Time Outbreak Monitoring
*   **Geospatial View**: Heatmap of predicted diseases by region (mocked location data).
*   **Trend Analysis**: Time-series graphs showing spikes in specific diseases (e.g., "Flu Season Alert").

#### 🛡️ Model Drift & Health
*   **Confidence Calibration**: Histogram of prediction confidence scores.
*   **Drift Detection**: Alerts if input data deviates from training distribution (e.g., sudden influx of new unknown symptoms).

---

## 4. Prioritized Implementation Roadmap

### Phase 1: Deep Learning Foundation (High Impact)
*   **Goal**: Replace XGBoost with a Neural Network capable of learning embeddings.
*   **Tasks**:
    1.  Design `VetNet` architecture in PyTorch.
    2.  Implement Entity Embeddings for `Animal` and `Category`.
    3.  Train and benchmark against current XGBoost baseline.

### Phase 2: Advanced Dashboarding (High Visibility)
*   **Goal**: Improve trust and usability for veterinarians.
*   **Tasks**:
    1.  Integrate `SHAP` library for model explainability.
    2.  Build "Drift Monitor" page in Streamlit.
    3.  Add PDF Report Generation for diagnosis.

### Phase 3: Data Quality & MLOps (Long-term Stability)
*   **Goal**: Ensure system reliability.
*   **Tasks**:
    1.  Implement `Great Expectations` for data validation.
    2.  Set up automated retraining pipelines (active learning).

### Phase 4: Multi-Modal Expansion (Innovation)
*   **Goal**: State-of-the-art diagnostic capability.
*   **Tasks**:
    1.  Collect open-source veterinary image datasets.
    2.  Add CNN branch to `VetNet`.

## 5. Next Steps
1.  **Approve** this plan.
2.  **Execute Phase 1**: logic to build the Neural Network training pipeline (`src/train_nn.py`).

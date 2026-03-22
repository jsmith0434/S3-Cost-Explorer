
# ☁️ S3 Cost & Usage Explorer

### 📊 Project Overview
This tool automates the retrieval, transformation, and visualization of Amazon S3 usage data. By interfacing directly with the **AWS Cost Explorer API**, it provides stakeholders with clear visibility into storage trends, helping to identify cost-saving opportunities and monitor budget adherence.

The application converts complex JSON responses from AWS into structured tabular data, making it easy to perform time-series analysis on monthly S3 expenditures.

---

### 🏗️ Architecture & Workflow



1.  **Extraction**: `main.py` authenticates via IAM and pulls raw cost data.
2.  **Transformation**: `converter.py` flattens nested JSON responses into clean CSV formats.
3.  **Visualization**: Generates time-series plots (e.g., `usage.jpg`) to track cost fluctuations.
4.  **Scaling**: Designed to be hosted on **Amazon EC2** for scheduled automated reporting.

---

### 📂 Repository Structure

| File | Description |
| :--- | :--- |
| **`main.py`** | The primary entry point; handles AWS API authentication and data orchestration. |
| **`converter.py`** | Helper library for JSON-to-tabular data conversion and cleaning. |
| **`usage.json` / `.csv`** | Examples of the raw API response and the post-processed structured data. |
| **`usage.jpg`** | Generated time-series visualization showing monthly S3 cost trends. |
| **`example_data/`** | A sandbox environment containing sample data to test functionality without an active AWS connection. |

---

### 🛠️ Setup & Requirements

**Prerequisites:**
* An active **AWS Account** with at least one S3 bucket.
* **IAM Credentials**: A user or role with `GetCostAndUsage`, `s3:ListBucket`, and `s3:GetObject` permissions.
* **AWS CLI**: Pre-configured profiles and access keys.

**Recommended Production Environment:**
* **Host on EC2**: Deploy on a Linux-based EC2 instance for 24/7 availability.
* **Security**: Implement rotating IAM access keys and secure SSH access for developers.
* **Persistence**: Store final model outputs and CSVs back in a centralized S3 bucket.
* **BI Integration**: Connect **Amazon QuickSight** to the S3 output folder to create automated executive dashboards.

---

### 🚀 Quick Start
1.  Clone the repository.
2.  Install dependencies: `pip install boto3 pandas matplotlib`.
3.  Ensure your AWS profile is active: `export AWS_PROFILE='your-profile'`.
4.  Run the explorer:
    ```bash
    python main.py
    ```

---

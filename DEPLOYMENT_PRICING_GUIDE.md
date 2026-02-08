# 🌐 Veterinary AI Suite - Deployment & Pricing Roadmap

This document provides a comparative analysis for deploying the **VetNet AI Suite** to the cloud. Given that the system uses **Deep Learning (PyTorch)** and **XGBoost**, it requires specific memory allocations (minimum 2GB RAM) for stable inference.

---

## 🚀 Option 1: Render.com (Easiest & Fastest)
*Best for: Rapid deployment, individual veterinarians, and small clinics.*

| Component | Tier Recommended | Estimated Price |
| :--- | :--- | :--- |
| **Web Service** | **Starter** (2 GB RAM, 1 CPU) | **$7.00 / month** |
| **Bandwidth** | 100 GB Included | $0.00 |
| **SSL (HTTPS)** | Automatic/Managed | $0.00 |
| **TOTAL** | | **~$7.00 / month** |

### ✅ Pros:
- **Zero Configuration**: Connect GitHub, select Docker, and it's live in 5 minutes.
- **Predictable Cost**: Fixed monthly price regardless of moderate traffic spikes.
- **Managed**: No need to worry about server security or OS updates.

### ❌ Cons:
- Limited geographical regions.
- Fewer options for complex database scaling.

---

## 🏗️ Option 2: AWS App Runner (Professional & Scalable)
*Best for: Enterprise applications, medical networks, and high-growth potential.*

| Component | Configuration | Estimated Price |
| :--- | :--- | :--- |
| **Compute** | 1 vCPU / 2 GB RAM | **~$15.00 / month** |
| **Provisioned Concurrency**| Keeps app warm 24/7 | Included in compute |
| **Data Transfer** | Standard Outbound | ~$0.09 per GB |
| **TOTAL** | | **~$15.00 - $20.00 / month** |

### ✅ Pros:
- **World-Class Infrastructure**: Extremely high reliability and global availability.
- **Scalability**: Can handle 1 user or 10,000 users with automatic scaling.
- **Health Checks**: Automatically restarts the container if the AI service crashes.

### ❌ Cons:
- **Complex Billing**: You pay for what you use, which can fluctuate.
- **Setup Overhead**: Requires configuring IAM roles and VPC settings.

---

## 💰 Option 3: AWS Lightsail (Budget Professional)
*Best for: Low-cost, dedicated performance on AWS infrastructure.*

| Component | Plan | Price |
| :--- | :--- | :--- |
| **Instance** | **2 GB RAM, 1 vCPU** | **$10.00 / month** |
| **Storage** | 60 GB SSD | Included |
| **Data Transfer** | 3 TB Included | Included |
| **TOTAL** | | **$10.00 / month** |

### ✅ Pros:
- Cheapest way to get on AWS with fixed pricing.
- Complete control over the server environment.

---

## 🧠 Deployment Summary for AI Features

| Feature | Requirement | Impact on Cloud Choice |
| :--- | :--- | :--- |
| **Document Parsing** | High CPU momentarily | Higher RAM tier required (>2GB) |
| **VetNet Inference** | High Memory (Neural Net) | Avoid AWS "micro" instances (only 1GB RAM) |
| **Real-time Map** | Google API Key | Requires Env Variable configuration |

### **Final Recommendation:**
- **Start with Render (Starter Hub)**: It is the most cost-effective way to host a Dockerized Streamlit app with PyTorch dependencies.
- **Migrate to AWS App Runner**: If you reach >1,000 active users or need specific compliance certifications.

---
**Created by Antigravity AI - 2026**

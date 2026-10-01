# 🔀 Smart LLM Cost Gateway & Multi-Model Router

![Uploading image.png…]()


**Live Demo:** [http://56.228.36.28:8501](http://56.228.36.28:8501) *(Running on AWS EC2)*

This project is an asynchronous GenAI gateway built in FastAPI that dynamically evaluates prompt complexity in milliseconds and routes the request to the most cost-effective open-weight LLM capable of answering it. Instead of sending every routine query to a massive, expensive foundation model, the gateway deflects standard traffic to a lighter model, dramatically reducing API inference costs without degrading user experience.

### 🚀 Key Achievements
* **Dynamic Routing:** Architected an intelligent gateway utilizing **MLflow** to track and serialize a Scikit-Learn Random Forest classifier that dynamically routes prompts across tiered open-weight LLMs (`gpt-oss-20b` vs. `gpt-oss-120b`).
* **Cost Optimization:** Deflected ~70% of traffic to the lighter 20B tier during a 50+ request live simulation, cutting routine inference costs by up to 50%.
* **Ultra-Low Latency:** Maintained a **~2.2ms steady-state routing overhead** (8.2ms mean, accounting for initial process warm-up).
* **Observability:** Built a real-time observability dashboard using Streamlit and SQLite to monitor live end-to-end latency, model distribution, and cumulative dollar savings.
* **Cloud Deployment:** Containerized the multi-service architecture with Docker Compose and deployed to an AWS EC2 micro-instance utilizing the AWS Free Tier.

---

## 🏗️ System Architecture

```text
[Client / User]
       │ (POST /v1/chat/completions)
       ▼
[ FastAPI Gateway ] ◄───── Loads ───── [ router.pkl (Random Forest) ]
       │
       ├─► Extracts Features (Word count, syntax, complexity markers)
       ├─► Predicts Tier (0: Easy, 1: Medium, 2: Hard)
       │
       ├───────────────(Tier 0 / 1)──────────────┐
       │                                         │
       ▼                                         ▼
[ gpt-oss-120b ] (Hard)                 [ gpt-oss-20b ] (Easy/Medium)
       │                                         │
       └───────────────(Response)────────────────┘
       │
       ▼
[ SQLite Database ] ◄───── Reads ───── [ Streamlit Dashboard ]
 (Logs latency, model used, cost)        (Live charts & metrics)

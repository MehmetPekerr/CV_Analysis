import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_REGULAR = "CVFont"
FONT_BOLD = "CVFont-Bold"


def register_fonts():
    font_paths = [
        (
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ),
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ),
        (
            "/Library/Fonts/Arial.ttf",
            "/Library/Fonts/Arial Bold.ttf",
        ),
    ]

    for regular_path, bold_path in font_paths:
        if os.path.exists(regular_path) and os.path.exists(bold_path):
            pdfmetrics.registerFont(TTFont(FONT_REGULAR, regular_path))
            pdfmetrics.registerFont(TTFont(FONT_BOLD, bold_path))
            pdfmetrics.registerFontFamily(
                FONT_REGULAR,
                normal=FONT_REGULAR,
                bold=FONT_BOLD,
                italic=FONT_REGULAR,
                boldItalic=FONT_BOLD,
            )
            return

    raise RuntimeError("A Unicode TrueType font is required to generate Turkish CV PDFs.")

CANDIDATES = [
    {
        "filename": "cv_metehan_yilmaz.pdf",
        "name": "Metehan Yılmaz",
        "email": "metehan.yilmaz@email.com",
        "phone": "+90 532 111 2233",
        "linkedin": "linkedin.com/in/metehanyilmaz",
        "github": "github.com/metehanyilmaz",
        "summary": (
            "Senior Full-Stack Software Engineer with 6 years of experience building "
            "scalable distributed systems and AI-integrated products. Passionate about "
            "clean architecture, LLM tooling, and open-source contributions."
        ),
        "education": [
            ("Middle East Technical University (METU)", "B.Sc. Computer Engineering", "2014 – 2018", "GPA: 3.71 / 4.00"),
        ],
        "languages": [
            ("English", "C2 — Proficient"),
            ("German", "B2 — Upper Intermediate"),
        ],
        "experience": [
            (
                "Senior Software Engineer",
                "Trendyol — Istanbul",
                "2021 – Present",
                "Led the design of a real-time recommendation engine (Python, Kafka, Redis) "
                "serving 40M+ users. Integrated OpenAI API for product description enrichment. "
                "Mentored a team of 5 junior engineers.",
            ),
            (
                "Software Engineer",
                "Getir — Istanbul",
                "2018 – 2021",
                "Built courier assignment microservice in Go. Reduced delivery ETA estimation "
                "error by 18% using ML-based route prediction (scikit-learn, XGBoost).",
            ),
        ],
        "projects": [
            ("LLM Document Analyzer", "FastAPI + LangChain + ChromaDB — RAG pipeline for legal document Q&A. 200+ GitHub stars."),
            ("OpenCV Face Attendance", "Real-time face recognition attendance system for university labs. PyTorch, MTCNN."),
            ("Distributed Task Queue", "Custom Celery-like task queue in Python supporting Redis and RabbitMQ backends."),
        ],
        "internships": [
            ("Software Development Intern", "Aselsan — Ankara", "Summer 2017", "Developed embedded C++ modules for radar signal processing unit."),
            ("Backend Intern", "Arçelik R&D", "Summer 2016", "Built REST APIs for IoT device management dashboard using Django."),
        ],
        "skills": "Python, Go, FastAPI, Docker, Kubernetes, Kafka, PostgreSQL, Redis, PyTorch, TensorFlow, LangChain, OpenAI API, AWS",
        "ai_section": (
            "AI & Machine Learning: Built production RAG pipeline with LangChain and ChromaDB. "
            "Fine-tuned BERT for Turkish NLP tasks. Completed Stanford ML Specialization (Coursera). "
            "Contributor to Hugging Face Transformers library (3 merged PRs). "
            "Experience with OpenAI, Anthropic, and self-hosted Ollama deployments."
        ),
    },
    {
        "filename": "cv_simge_aktas.pdf",
        "name": "Simge Aktaş",
        "email": "simge.aktas@protonmail.com",
        "phone": "+90 543 222 3344",
        "linkedin": "linkedin.com/in/simgeaktas",
        "github": "github.com/simgeaktas",
        "summary": (
            "Full-Stack Developer with 4 years of experience, specializing in backend systems "
            "and cloud infrastructure. Trilingual with strong international project exposure."
        ),
        "education": [
            ("Istanbul Technical University (ITU)", "B.Sc. Software Engineering", "2015 – 2019", "GPA: 3.52 / 4.00"),
        ],
        "languages": [
            ("English", "C1 — Advanced (IELTS 7.5)"),
            ("French", "B2 — Upper Intermediate (DELF B2)"),
            ("Spanish", "A2 — Elementary"),
        ],
        "experience": [
            (
                "Backend Engineer",
                "Peak Games — Istanbul",
                "2021 – Present",
                "Designed player matchmaking service in Node.js handling 500K concurrent sessions. "
                "Integrated AWS SageMaker for churn prediction model deployment.",
            ),
            (
                "Full-Stack Developer",
                "Logo Software",
                "2019 – 2021",
                "Developed ERP module extensions in Java Spring Boot and Angular. "
                "Automated CI/CD pipelines reducing deployment time from 4h to 20 min.",
            ),
        ],
        "projects": [
            ("MultiLang NLP Benchmark", "Benchmark suite comparing GPT-4, Claude, and Mistral on multilingual tasks. Published on arXiv."),
            ("E-Commerce Price Tracker", "Python scraper + FastAPI backend + React dashboard tracking 50K+ products."),
        ],
        "internships": [
            ("Cloud Infrastructure Intern", "Vodafone Turkey", "Summer 2018", "Automated VM provisioning scripts using Terraform and Ansible."),
            ("Backend Intern", "Insider", "Summer 2017", "Built A/B testing analytics dashboard with Python and Elasticsearch."),
            ("Data Intern", "TÜBİTAK BİLGEM", "Winter 2017", "Processed NLP datasets for Turkish government document classification."),
        ],
        "skills": "Node.js, Java, Spring Boot, Python, AWS, Terraform, Docker, PostgreSQL, Elasticsearch, Angular, React",
        "ai_section": (
            "AI: Deployed AWS SageMaker churn model. Published multilingual LLM benchmark paper. "
            "Familiar with Hugging Face pipelines and prompt engineering techniques."
        ),
    },
    {
        "filename": "cv_berk_kaya.pdf",
        "name": "Berk Kaya",
        "email": "berk.kaya@gmail.com",
        "phone": "+90 505 333 4455",
        "linkedin": "linkedin.com/in/berkkaya",
        "github": "github.com/berkkaya",
        "summary": (
            "AI-focused Software Engineer specializing in computer vision and generative AI. "
            "Graduated from Bilkent University with honors. 3 years of industry experience."
        ),
        "education": [
            ("Bilkent University", "B.Sc. Computer Engineering (Honors)", "2016 – 2020", "GPA: 3.89 / 4.00 — High Honors"),
        ],
        "languages": [
            ("English", "C1 — Advanced (TOEFL iBT 105)"),
            ("Japanese", "A2 — Elementary"),
        ],
        "experience": [
            (
                "Machine Learning Engineer",
                "Huawei R&D Center — Istanbul",
                "2022 – Present",
                "Developed on-device vision models (MobileNet variants) for smartphone cameras. "
                "Achieved 15% mAP improvement on low-light object detection benchmarks.",
            ),
            (
                "Junior AI Engineer",
                "Asisguard",
                "2020 – 2022",
                "Built real-time person re-identification pipeline using PyTorch and TensorRT. "
                "Deployed on Jetson Nano edge devices for security camera systems.",
            ),
        ],
        "projects": [
            ("StyleGAN Turkish Art Generator", "Fine-tuned StyleGAN3 on 50K Turkish miniature paintings dataset. HuggingFace Space with 5K+ monthly users."),
            ("Sign Language Translator", "Real-time Turkish sign language recognition using MediaPipe + LSTM. 94.2% accuracy. Open-sourced on GitHub (180 stars)."),
            ("Satellite Image Segmentation", "U-Net based segmentation model for agricultural land classification. Kaggle top 8%."),
        ],
        "internships": [
            ("AI Research Intern", "ASELSAN AI Lab", "Summer 2019", "Implemented attention mechanisms for radar waveform classification."),
            ("CV Intern", "Meteksan Defense", "Winter 2019", "Object detection pipeline for UAV imagery using YOLOv4."),
        ],
        "skills": "Python, PyTorch, TensorFlow, OpenCV, TensorRT, ONNX, Docker, CUDA, FastAPI, NumPy, scikit-learn, HuggingFace",
        "ai_section": (
            "Deep AI expertise: Published 1 workshop paper at ECCV 2023. Kaggle Expert badge. "
            "Experience with GANs, Transformers, diffusion models, LLMs, and edge AI deployment. "
            "Active contributor to PyTorch Vision repository."
        ),
    },
    {
        "filename": "cv_elif_sahin.pdf",
        "name": "Elif Şahin",
        "email": "elif.sahin@outlook.com",
        "phone": "+90 532 444 5566",
        "linkedin": "linkedin.com/in/elifsahin",
        "github": "github.com/elifsahin",
        "summary": (
            "Backend-focused Software Engineer with 5 years of experience in high-traffic "
            "API design, database optimization, and microservices architecture."
        ),
        "education": [
            ("Hacettepe University", "B.Sc. Computer Engineering", "2013 – 2017", "GPA: 3.44 / 4.00"),
        ],
        "languages": [
            ("English", "B2 — Upper Intermediate (Cambridge FCE)"),
        ],
        "experience": [
            (
                "Senior Backend Engineer",
                "Hepsiburada — Istanbul",
                "2020 – Present",
                "Designed inventory management service processing 2M+ SKUs. "
                "Optimized PostgreSQL query performance by 60% using query planning and indexing strategies.",
            ),
            (
                "Backend Developer",
                "Yemeksepeti (Delivery Hero)",
                "2017 – 2020",
                "Built restaurant onboarding APIs in Python/Django serving 25K+ vendors. "
                "Migrated monolith to microservices architecture (Docker, Kubernetes).",
            ),
        ],
        "projects": [
            ("API Gateway Boilerplate", "Production-grade FastAPI gateway with JWT auth, rate limiting, and distributed tracing. 400+ GitHub stars."),
            ("DB Migration CLI Tool", "Python CLI for zero-downtime PostgreSQL migrations. Used internally at Hacettepe University labs."),
        ],
        "internships": [
            ("Backend Intern", "STM Defense Technologies", "Summer 2016", "Developed RESTful APIs for satellite telemetry data visualization."),
            ("Database Intern", "HAVELSAN", "Summer 2015", "Database optimization and stored procedure development in Oracle SQL."),
        ],
        "skills": "Python, Django, FastAPI, PostgreSQL, MySQL, Redis, Docker, Kubernetes, RabbitMQ, Nginx, Linux, CI/CD",
        "ai_section": (
            "AI: Integrated OpenAI API for automated product categorization. "
            "Familiar with vector databases (pgvector) for semantic search. "
            "Completed DeepLearning.AI Practical MLOps course."
        ),
    },
    {
        "filename": "cv_deniz_arslan.pdf",
        "name": "Deniz Arslan",
        "email": "deniz.arslan@hotmail.com",
        "phone": "+90 543 555 6677",
        "linkedin": "linkedin.com/in/denizarslan",
        "github": "github.com/denizarslan",
        "summary": (
            "Self-taught full-stack developer who transitioned from mechanical engineering. "
            "Completed Ankara Coding Bootcamp (2020). Strong project portfolio and startup experience."
        ),
        "education": [
            ("Ankara University", "B.Sc. Mechanical Engineering", "2013 – 2017", "GPA: 2.98 / 4.00"),
            ("Ankara Coding Bootcamp", "Full-Stack Web Development", "2019 – 2020", "Certificate — Top of cohort"),
        ],
        "languages": [
            ("English", "B1 — Intermediate"),
        ],
        "experience": [
            (
                "Full-Stack Developer",
                "Craftbase (startup)",
                "2021 – Present",
                "Built entire SaaS platform from scratch (React, Node.js, MongoDB). "
                "Product reached 2K paying subscribers within 18 months.",
            ),
            (
                "Junior Web Developer",
                "Dijital Ajans",
                "2020 – 2021",
                "Developed e-commerce sites for 15+ clients using WordPress and React.",
            ),
        ],
        "projects": [
            ("Freelance Marketplace Platform", "Full-stack marketplace with real-time messaging (Socket.io), payment integration (Stripe). 500+ registered users."),
            ("CLI Budget Tracker", "Python terminal app for personal finance tracking. 120 GitHub stars."),
            ("3D Printing STL Validator", "Web tool using Three.js to visualize and validate 3D printer STL files."),
        ],
        "internships": [
            ("Mechanical Engineering Intern", "Ford Otosan", "Summer 2016", "CAD modeling and manufacturing process documentation."),
        ],
        "skills": "JavaScript, React, Node.js, Express, MongoDB, PostgreSQL, HTML/CSS, Socket.io, Docker, Stripe API, Git",
        "ai_section": (
            "AI: Used OpenAI API for chatbot integration in marketplace product. "
            "Completed fast.ai Practical Deep Learning for Coders (Part 1)."
        ),
    },
    {
        "filename": "cv_selin_celik.pdf",
        "name": "Selin Çelik",
        "email": "selin.celik@gmail.com",
        "phone": "+90 505 666 7788",
        "linkedin": "linkedin.com/in/selincelik",
        "github": "github.com/selincelik",
        "summary": (
            "Recent Boğaziçi University CS graduate with excellent academic record. "
            "Research experience in NLP and strong competitive programming background."
        ),
        "education": [
            ("Boğaziçi University", "B.Sc. Computer Engineering", "2019 – 2023", "GPA: 3.78 / 4.00 — Dean's List 6 semesters"),
        ],
        "languages": [
            ("English", "C1 — Advanced (IELTS 8.0)"),
            ("French", "A2 — Elementary"),
        ],
        "experience": [
            (
                "Junior Software Engineer",
                "Innova IT — Istanbul",
                "2023 – Present",
                "Developing billing microservices in Java Spring Boot. "
                "Introduced automated contract testing, reducing integration bugs by 35%.",
            ),
        ],
        "projects": [
            ("Turkish Sentiment Analysis Model", "Fine-tuned BERTurk on 100K reviews. F1-score 91.3%. Published on HuggingFace Hub."),
            ("Competitive Programming Judge", "Online judge platform (Django + React) hosting university-level contests. 800+ registered participants."),
            ("Graph Algorithm Visualizer", "Interactive D3.js web app teaching BFS, DFS, Dijkstra. Used in 3 university courses."),
        ],
        "internships": [
            ("Software Research Intern", "TUBITAK — Ankara", "Summer 2022", "NLP pipeline for scientific paper classification. Co-authored internal technical report."),
            ("Backend Intern", "Softtech (İş Bankası)", "Summer 2021", "Developed API endpoints for mobile banking backend in Spring Boot."),
        ],
        "skills": "Java, Python, Spring Boot, Django, React, D3.js, PostgreSQL, NLP, HuggingFace, Git, Linux",
        "ai_section": (
            "NLP research background: fine-tuned BERT-based models, experience with Hugging Face ecosystem, "
            "text classification, and information extraction. Attended EMNLP 2023 as a volunteer."
        ),
    },
    {
        "filename": "cv_furkan_dogan.pdf",
        "name": "Furkan Doğan",
        "email": "furkan.dogan@khas.edu.tr",
        "phone": "+90 532 777 8899",
        "linkedin": "linkedin.com/in/furkandogan",
        "github": "github.com/furkandogan",
        "summary": (
            "ML Engineer and AI researcher with M.Sc. from Koç University. "
            "3 years of experience building production ML systems. "
            "Focus on LLMs, recommendation systems, and MLOps."
        ),
        "education": [
            ("Koç University", "M.Sc. Computational Science & Engineering", "2019 – 2021", "GPA: 3.90 / 4.00 — Thesis: 'Efficient Transformer Pruning for Edge Deployment'"),
            ("Koç University", "B.Sc. Electrical & Electronics Engineering", "2015 – 2019", "GPA: 3.65 / 4.00 — Valedictorian"),
        ],
        "languages": [
            ("English", "C2 — Proficient (TOEFL iBT 115)"),
            ("German", "A2 — Elementary"),
        ],
        "experience": [
            (
                "ML Engineer",
                "Şirket.ai — Istanbul",
                "2022 – Present",
                "Built end-to-end recommendation engine (collaborative filtering + content-based) increasing CTR by 22%. "
                "Deployed LLaMA 2 fine-tuned model via vLLM for customer support automation. "
                "Managed ML platform on GCP Vertex AI.",
            ),
            (
                "AI Research Assistant",
                "Koç University — KUIS AI Lab",
                "2019 – 2022",
                "Research on neural network pruning and quantization. "
                "3 conference publications (ICML workshop, NeurIPS workshop, ECML).",
            ),
        ],
        "projects": [
            ("Transformer Pruning Library", "Open-source PyTorch library for structured pruning of BERT/GPT models. 600+ GitHub stars, used by 3 research groups."),
            ("Ollama Model Benchmark Suite", "Automated benchmarking framework for local LLMs. Compares Llama, Mistral, Phi on Turkish NLP tasks."),
            ("Real-time Fraud Detection", "Graph neural network (PyG) for transaction fraud detection. 99.1% precision on holdout set."),
        ],
        "internships": [
            ("AI Research Intern", "Microsoft — Redmond, WA (Remote)", "Summer 2020", "Contributed to Azure Cognitive Services NLP evaluation pipeline."),
            ("Data Science Intern", "Garanti BBVA Technology", "Summer 2018", "Churn prediction model for retail banking using LightGBM."),
        ],
        "skills": "Python, PyTorch, TensorFlow, HuggingFace, vLLM, Ollama, FastAPI, GCP, Docker, MLflow, DVC, Kafka, SQL",
        "ai_section": (
            "Expert-level AI: 3 ML research publications. Fine-tuned LLaMA 2 and Mistral for production. "
            "Deep expertise in transformer architecture, pruning, quantization (GGUF, GPTQ, AWQ). "
            "Built and deployed RAG pipelines. Familiar with LangChain, LlamaIndex, ChromaDB, Weaviate."
        ),
    },
    {
        "filename": "cv_ayse_kilic.pdf",
        "name": "Ayşe Kılıç",
        "email": "ayse.kilic@sabanciuniv.edu",
        "phone": "+90 543 888 9900",
        "linkedin": "linkedin.com/in/aysekilic",
        "github": "github.com/aysekilic",
        "summary": (
            "Frontend Engineer and UI/UX enthusiast. Sabancı University CS graduate with 3 industry internships. "
            "Expert in React ecosystem and accessibility-first design."
        ),
        "education": [
            ("Sabancı University", "B.Sc. Computer Science & Engineering", "2017 – 2021", "GPA: 3.55 / 4.00"),
        ],
        "languages": [
            ("English", "C1 — Advanced (Cambridge CAE grade B)"),
            ("Italian", "B1 — Intermediate"),
        ],
        "experience": [
            (
                "Frontend Engineer",
                "Figopara — Istanbul",
                "2021 – Present",
                "Led React component library development used across 4 product teams. "
                "Improved Lighthouse performance score from 61 to 94. "
                "Integrated AI-generated UX copy using OpenAI GPT-4 API.",
            ),
        ],
        "projects": [
            ("Design System Monorepo", "Storybook-driven React + TypeScript component library with 60+ components. 350 GitHub stars."),
            ("AI Writing Assistant Chrome Extension", "GPT-4 powered browser extension for grammar and tone suggestions. 2K active users."),
            ("Portfolio Builder SaaS", "No-code portfolio builder with Next.js and Supabase. 300+ created portfolios."),
        ],
        "internships": [
            ("Frontend Intern", "Turkish Airlines Digital", "Summer 2020", "Developed seat map component for online check-in flow using React."),
            ("UI Developer Intern", "Marti Technologies", "Summer 2019", "Built admin dashboard for scooter fleet management."),
            ("Web Intern", "Netaş", "Summer 2018", "HTML/CSS/JS development for internal tools portal."),
        ],
        "skills": "React, TypeScript, Next.js, Vue.js, Figma, Storybook, GraphQL, REST, Node.js, CSS, Jest, Cypress",
        "ai_section": (
            "AI integration experience: OpenAI GPT-4 API integration in production Chrome extension. "
            "Familiar with prompt engineering for UI copy generation. "
            "Completed fast.ai Practical Deep Learning (Part 1)."
        ),
    },
    {
        "filename": "cv_burak_ozturk.pdf",
        "name": "Burak Öztürk",
        "email": "burak.ozturk@gmail.com",
        "phone": "+90 532 999 0011",
        "linkedin": "linkedin.com/in/burakozturk",
        "github": "github.com/burakozturk",
        "summary": (
            "DevOps & Platform Engineer with strong software development background. "
            "Gazi University Computer Engineering graduate. Experienced in CI/CD, IaC, and AI model serving infrastructure."
        ),
        "education": [
            ("Gazi University", "B.Sc. Computer Engineering", "2014 – 2018", "GPA: 3.28 / 4.00"),
        ],
        "languages": [
            ("English", "B2 — Upper Intermediate"),
        ],
        "experience": [
            (
                "Senior DevOps Engineer",
                "Payinaş — Istanbul",
                "2021 – Present",
                "Designed GitOps platform on Kubernetes (ArgoCD, Helm) reducing release cycle from 2 weeks to daily. "
                "Set up GPU cluster for ML model training and Ollama-based inference serving.",
            ),
            (
                "Platform Engineer",
                "Ericsson Turkey",
                "2018 – 2021",
                "Managed on-premise OpenStack cloud for 5G core network functions. "
                "Automated infrastructure provisioning with Terraform and Ansible.",
            ),
        ],
        "projects": [
            ("GPU Cluster Autoscaler", "Kubernetes operator in Go that autoscales GPU nodes based on LLM inference queue depth. Used in production."),
            ("Ollama Deployment Charts", "Helm charts for multi-model Ollama deployments on Kubernetes. 250 GitHub stars."),
            ("CI/CD Pipeline Templates", "Reusable GitHub Actions and GitLab CI templates covering build, test, scan, and deploy stages."),
        ],
        "internships": [
            ("Systems Intern", "Türk Telekom", "Summer 2017", "Network automation scripts in Python for BGP route management."),
            ("Linux Admin Intern", "TÜBİTAK ULAKBİM", "Summer 2016", "Maintained HPC cluster and batch job scheduling with SLURM."),
        ],
        "skills": "Kubernetes, Docker, Terraform, Ansible, AWS, GCP, Azure, Go, Python, Prometheus, Grafana, ArgoCD, Helm, Linux",
        "ai_section": (
            "AI infrastructure: Deployed and managed Ollama multi-model serving on GPU Kubernetes cluster. "
            "Set up MLflow model registry and Seldon Core serving infrastructure. "
            "Experience with vLLM, TGI (Text Generation Inference), and NVIDIA Triton."
        ),
    },
    {
        "filename": "cv_merve_yildiz.pdf",
        "name": "Merve Yıldız",
        "email": "merve.yildiz@iyte.edu.tr",
        "phone": "+90 543 111 2200",
        "linkedin": "linkedin.com/in/merveyildiz",
        "github": "github.com/merveyildiz",
        "summary": (
            "Data Scientist and ML Engineer from Izmir Institute of Technology. "
            "2 years of industry experience with focus on NLP, time series forecasting, and MLOps."
        ),
        "education": [
            ("Izmir Institute of Technology (IYTE)", "B.Sc. Computer Engineering", "2017 – 2021", "GPA: 3.62 / 4.00 — Ranked 2nd in department"),
        ],
        "languages": [
            ("English", "C1 — Advanced (IELTS 7.0)"),
            ("Chinese", "A1 — Beginner (HSK 1)"),
        ],
        "experience": [
            (
                "Data Scientist",
                "Turkcell Technology — Istanbul",
                "2022 – Present",
                "Built churn prediction model reducing annual churn by 8% (saving ~€2M). "
                "Deployed NLP pipeline for customer complaint categorization (BERT, Turkish). "
                "Maintained MLflow-tracked experiment pipeline.",
            ),
            (
                "ML Research Intern → Junior ML Engineer",
                "Vestel Electronics R&D",
                "2021 – 2022",
                "Anomaly detection in TV manufacturing sensor data using LSTM autoencoders. "
                "Reduced defect escape rate by 12%.",
            ),
        ],
        "projects": [
            ("Turkish BERT Sentiment API", "Production-ready FastAPI service wrapping BERTurk for multi-class sentiment analysis. Docker + K8s. 190 GitHub stars."),
            ("Energy Demand Forecasting", "LSTM + Prophet hybrid model for 24h electricity demand forecast. Kaggle bronze medal."),
            ("AutoML Pipeline Framework", "Lightweight Python AutoML library comparing 10 classifiers with automated feature engineering. 95 GitHub stars."),
        ],
        "internships": [
            ("Data Science Intern", "Vestel Electronics", "Summer 2020", "Predictive maintenance model for production line machinery."),
            ("Research Intern", "IYTE AI Lab", "Summer 2019", "Medical image segmentation using U-Net for chest X-ray analysis."),
        ],
        "skills": "Python, PyTorch, scikit-learn, HuggingFace, MLflow, FastAPI, PostgreSQL, Docker, Kubernetes, PySpark, SQL, Tableau",
        "ai_section": (
            "Strong AI background: NLP (BERT, GPT fine-tuning), time series, anomaly detection, computer vision. "
            "Experience with LLM APIs (OpenAI, Cohere) and RAG architectures. "
            "Completed DeepLearning.AI NLP Specialization and MLOps Specialization."
        ),
    },
]


def build_styles():
    base = getSampleStyleSheet()

    styles = {}
    styles["title"] = ParagraphStyle(
        "CVTitle",
        parent=base["Normal"],
        fontSize=22,
        fontName=FONT_BOLD,
        textColor=colors.HexColor("#1a1a2e"),
        alignment=TA_CENTER,
        leading=28,
        spaceAfter=8,
    )
    styles["contact"] = ParagraphStyle(
        "Contact",
        parent=base["Normal"],
        fontSize=9,
        fontName=FONT_REGULAR,
        textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
        leading=12,
        spaceAfter=8,
    )
    styles["section_header"] = ParagraphStyle(
        "SectionHeader",
        parent=base["Normal"],
        fontSize=11,
        fontName=FONT_BOLD,
        textColor=colors.HexColor("#16213e"),
        spaceBefore=12,
        spaceAfter=4,
    )
    styles["body"] = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontSize=9.5,
        fontName=FONT_REGULAR,
        textColor=colors.HexColor("#333333"),
        spaceAfter=3,
        leading=14,
    )
    styles["body_bold"] = ParagraphStyle(
        "BodyBold",
        parent=base["Normal"],
        fontSize=9.5,
        fontName=FONT_BOLD,
        textColor=colors.HexColor("#222222"),
        spaceAfter=1,
    )
    styles["small"] = ParagraphStyle(
        "Small",
        parent=base["Normal"],
        fontSize=8.5,
        fontName=FONT_REGULAR,
        textColor=colors.HexColor("#666666"),
        spaceAfter=2,
    )
    return styles


def build_pdf(candidate: dict):
    filepath = os.path.join(OUTPUT_DIR, candidate["filename"])
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )
    s = build_styles()
    story = []

    story.append(Paragraph(candidate["name"], s["title"]))
    contact_line = (
        f"{candidate['email']}  |  {candidate['phone']}  |  "
        f"{candidate['linkedin']}  |  {candidate['github']}"
    )
    story.append(Paragraph(contact_line, s["contact"]))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#6c63ff")))
    story.append(Spacer(1, 6))

    story.append(Paragraph("PROFESSIONAL SUMMARY", s["section_header"]))
    story.append(Paragraph(candidate["summary"], s["body"]))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc")))

    story.append(Paragraph("EDUCATION", s["section_header"]))
    for edu in candidate["education"]:
        story.append(Paragraph(f"{edu[0]} — {edu[1]}", s["body_bold"]))
        story.append(Paragraph(f"{edu[2]}  |  {edu[3]}", s["small"]))
        story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc")))

    story.append(Paragraph("LANGUAGES", s["section_header"]))
    for lang, level in candidate["languages"]:
        story.append(Paragraph(f"• {lang}: {level}", s["body"]))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc")))

    story.append(Paragraph("WORK EXPERIENCE", s["section_header"]))
    for exp in candidate["experience"]:
        story.append(Paragraph(f"{exp[0]}  —  {exp[1]}  ({exp[2]})", s["body_bold"]))
        story.append(Paragraph(exp[3], s["body"]))
        story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc")))

    story.append(Paragraph("PROJECTS", s["section_header"]))
    for proj in candidate["projects"]:
        story.append(Paragraph(f"• <b>{proj[0]}</b>: {proj[1]}", s["body"]))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc")))

    story.append(Paragraph("INTERNSHIPS", s["section_header"]))
    for intern in candidate["internships"]:
        story.append(Paragraph(f"{intern[0]}  —  {intern[1]}  ({intern[2]})", s["body_bold"]))
        story.append(Paragraph(intern[3], s["small"]))
        story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc")))

    story.append(Paragraph("TECHNICAL SKILLS", s["section_header"]))
    story.append(Paragraph(candidate["skills"], s["body"]))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc")))

    story.append(Paragraph("AI & MACHINE LEARNING", s["section_header"]))
    story.append(Paragraph(candidate["ai_section"], s["body"]))

    doc.build(story)
    print(f"  [OK]  Generated: {candidate['filename']}")


def main():
    register_fonts()
    print(f"\nGenerating {len(CANDIDATES)} CV PDFs in: {OUTPUT_DIR}\n")
    for c in CANDIDATES:
        build_pdf(c)
    print(f"\nDone. {len(CANDIDATES)} PDF files created.\n")


if __name__ == "__main__":
    main()

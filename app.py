import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# Page configuration
st.set_page_config(
    page_title="شركة نجمة جدة للمقاولات",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS directly in the app.py file
css = """
/* Main styling */
body {
    font-family: 'Tajawal', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    background-color: #f9f9f9;
    direction: rtl;
    text-align: right;
}

/* Header styling */
h1, h2, h3 {
    font-family: 'Tajawal', sans-serif;
    color: #1a3c6e;
    font-weight: 700;
    text-align: right;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    flex-direction: row-reverse;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #f8f9fa;
    border-radius: 4px 4px 0 0;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
}

.stTabs [aria-selected="true"] {
    background-color: #e6eef8;
    border-bottom: 2px solid #f7a100;
}

/* Introduction text */
.intro-text {
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 30px;
    padding: 20px;
    background-color: #e6eef8;
    border-right: 4px solid #f7a100;
    border-radius: 8px 0 0 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    text-align: right;
}

/* Project cards */
.project-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 20px;
    direction: rtl;
}

.project-card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-top: 4px solid #f7a100;
    text-align: right;
}

.project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.project-card h3 {
    margin-top: 0;
    color: #1a3c6e;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    text-align: right;
}

/* Service cards */
.service-card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-right: 4px solid #1a3c6e;
    text-align: right;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.service-card h3 {
    margin-top: 0;
    color: #1a3c6e;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    text-align: right;
}

/* About section */
.about-section {
    background-color: #e6eef8;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    text-align: right;
}

.about-section h3 {
    color: #1a3c6e;
    margin-top: 20px;
    text-align: right;
}

/* Footer */
footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    border-top: 1px solid #eee;
    color: white;
    font-size: 14px;
    background-color: #1a3c6e;
    border-radius: 8px;
}

/* Metrics styling */
div[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: bold;
    color: #f7a100;
}

div[data-testid="stMetricLabel"] {
    font-weight: 500;
    color: #1a3c6e;
}

/* Project showcase container */
.project-showcase {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    padding: 15px;
    margin-bottom: 20px;
}

/* Service categories */
.service-residential { border-right-color: #4caf50; }
.service-commercial { border-right-color: #2196f3; }
.service-industrial { border-right-color: #f44336; }
.service-infrastructure { border-right-color: #9c27b0; }

/* Icon styling */
.icon {
    font-size: 24px;
    margin-left: 8px;
    vertical-align: middle;
}

.title-icon {
    font-size: 32px;
    margin-left: 10px;
    vertical-align: middle;
}

.card-icon {
    font-size: 20px;
    float: left;
    margin-top: -30px;
}

/* Hero section */
.hero-section {
    background: linear-gradient(135deg, #1a3c6e 0%, #2a5ca3 100%);
    color: white;
    padding: 40px;
    border-radius: 12px;
    margin-bottom: 30px;
    text-align: center;
}

.hero-section h1 {
    color: white;
    font-size: 2.5rem;
    margin-bottom: 20px;
}

.hero-section p {
    font-size: 1.2rem;
    margin-bottom: 30px;
}

.cta-button {
    background-color: #f7a100;
    color: white;
    padding: 12px 24px;
    border-radius: 30px;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
    transition: all 0.3s ease;
}

.cta-button:hover {
    background-color: #e69500;
    transform: scale(1.05);
}

/* Team member styling */
.team-member {
    text-align: center;
    padding: 20px;
}

.team-member img {
    border-radius: 50%;
    width: 150px;
    height: 150px;
    object-fit: cover;
    border: 4px solid #f7a100;
}

/* Testimonial styling */
.testimonial {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    position: relative;
    text-align: right;
}

.testimonial:before {
    content: '"';
    font-size: 60px;
    color: #f7a100;
    position: absolute;
    top: 10px;
    right: 10px;
    opacity: 0.2;
}

.testimonial-content {
    padding-right: 30px;
    font-style: italic;
}

.testimonial-author {
    text-align: left;
    font-weight: bold;
    color: #1a3c6e;
}

/* Add Tajawal font for Arabic text */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
"""

# Apply CSS
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <span class="title-icon">🏗️</span>
    <h1>شركة نجمة جدة للمقاولات</h1>
    <p>التميز في قطاع الإنشاءات العامة - شركة سعودية متخصصة في مجال التشييد والبناء والمقاولات العامة</p>
    <a href="#contact" class="cta-button">تواصل معنا</a>
</div>
""", unsafe_allow_html=True)

# Create tabs with icons
tab1, tab2, tab3, tab4 = st.tabs(["📞 تواصل معنا", "🏗️ مشاريعنا", "🛠️ خدماتنا", "🏢 من نحن"])

# Define company data
services = {
    "أعمال التشطيبات": {
        "icon": "🏠",
        "description": "لياسة ودهانات وجيبسون بورد وسيراميك ورخام وزجاج والمنيوم والأعمال الخشبية وكل ما يجب تنفيذه لإتمام الأعمال حسب أصول الصنعة",
        "category": "service-residential"
    },
    "أعمال الخرسانات": {
        "icon": "🏢",
        "description": "نجارة وحدادة وشدة معدنية ومباني وعزل مع التنفيذ حسب المواصفات المطلوبة للحديد والخرسانات، والبلوك، وكل ما يجب تنفيذه لإتمام الأعمال حسب أصول الصنعة",
        "category": "service-commercial"
    },
    "أعمال الإلكتروميكانيك": {
        "icon": "🏭",
        "description": "الكهرباء وتمديداتها وأنظمة التكييف والتبريد وأنظمة الإطفاء والحريق",
        "category": "service-industrial"
    },
    "تطوير البنية التحتية": {
        "icon": "🌉",
        "description": "الطرق والجسور ومشاريع الأشغال العامة التي تربط المجتمعات",
        "category": "service-infrastructure"
    },
    "التجديد وإعادة التشكيل": {
        "icon": "🔨",
        "description": "تحويل المساحات الموجودة بخدمات التجديد وإعادة التشكيل الخبيرة لدينا",
        "category": "service-residential"
    },
    "إدارة المشاريع": {
        "icon": "📋",
        "description": "إدارة المشاريع من البداية إلى النهاية لضمان التسليم في الوقت المحدد وضمن الميزانية",
        "category": "service-commercial"
    },
    "التصميم المعماري": {
        "icon": "✏️",
        "description": "تصاميم معمارية إبداعية وعملية تحول رؤيتك إلى واقع",
        "category": "service-commercial"
    },
    "البناء الأخضر": {
        "icon": "🌱",
        "description": "ممارسات البناء المستدامة وخيارات البناء المعتمدة من LEED",
        "category": "service-residential"
    }
}
}

projects = {
    "أبراج المدينة": {
        "icon": "🏢",
        "location": "المدينة المنورة، المملكة العربية السعودية",
        "description": "أبراج سكنية فاخرة تضم أكثر من 200 شقة متميزة ومرافق حديثة",
        "year": "2023",
        "category": "سكني"
    },
    "مركز جدة للأعمال": {
        "icon": "🏙️",
        "location": "جدة، المملكة العربية السعودية",
        "description": "مجمع مكاتب حديث مع تقنيات المباني الذكية وميزات التصميم المستدام",
        "year": "2022",
        "category": "تجاري"
    },
    "منتجع البحر الأحمر": {
        "icon": "🏖️",
        "location": "ساحل البحر الأحمر، المملكة العربية السعودية",
        "description": "منتجع فاخر على الشاطئ مع فلل خاصة ومرافق ضيافة عالمية المستوى",
        "year": "2021",
        "category": "ضيافة"
    },
    "مجمع الرياض الصناعي": {
        "icon": "🏭",
        "location": "الرياض، المملكة العربية السعودية",
        "description": "تطوير صناعي واسع النطاق مع مرافق للتخزين والتصنيع",
        "year": "2023",
        "category": "صناعي"
    },
    "مدينة الملك عبدالله الطبية": {
        "icon": "🏥",
        "location": "مكة المكرمة، المملكة العربية السعودية",
        "description": "مرفق طبي متطور مع مراكز علاج متخصصة ومختبرات بحثية",
        "year": "2020",
        "category": "رعاية صحية"
    },
    "توسعة طريق الدمام": {
        "icon": "🛣️",
        "location": "الدمام، المملكة العربية السعودية",
        "description": "مشروع بنية تحتية رئيسي لتوسيع شبكة الطرق السريعة مع جسور وتقاطعات",
        "year": "2022",
        "category": "بنية تحتية"
    },
    "مجمع الخبر للتسوق": {
        "icon": "🛍️",
        "location": "الخبر، المملكة العربية السعودية",
        "description": "وجهة تسوق متميزة مع علامات تجارية عالمية وخيارات ترفيه ومطاعم",
        "year": "2021",
        "category": "تجاري"
    },
    "مجمع تبوك السكني": {
        "icon": "🏘️",
        "location": "تبوك، المملكة العربية السعودية",
        "description": "مجمع سكني متكامل مع مدارس وحدائق ومرافق مجتمعية",
        "year": "2023",
        "category": "سكني"
    }
}

team_members = {
    "عبدالله السعود": {
        "position": "الرئيس التنفيذي والمؤسس",
        "bio": "مع أكثر من 30 عامًا في مجال البناء، قاد عبدالله شركة نجمة جدة من مقاول صغير إلى شركة بناء رائدة في المملكة العربية السعودية."
    },
    "محمد القحطاني": {
        "position": "مدير العمليات",
        "bio": "يشرف محمد على جميع عمليات المشاريع، مما يضمن الجودة والسلامة والتسليم في الوقت المناسب عبر جميع مشاريع الشركة."
    },
    "سارة الغامدي": {
        "position": "المهندس المعماري الرئيسي",
        "bio": "مهندسة معمارية حائزة على جوائز مع خبرة في التصميم المستدام وحلول البناء المبتكرة."
    },
    "خالد العتيبي": {
        "position": "مدير المشاريع",
        "bio": "متخصص في المشاريع التجارية والبنية التحتية واسعة النطاق مع أكثر من 20 عامًا من الخبرة."
    },
    "فاطمة الحربي": {
        "position": "مدير الشؤون المالية",
        "bio": "تدير العمليات المالية والاستثمارات الاستراتيجية للشركة لضمان النمو المستدام."
    }
}

testimonials = [
    {
        "quote": "قامت شركة نجمة جدة بتسليم مقر شركتنا الرئيسي قبل الموعد المحدد وضمن الميزانية. لقد تجاوز اهتمامهم بالتفاصيل وجودة العمل توقعاتنا.",
        "author": "أحمد الدوسري، الرئيس التنفيذي لشركة الابتكارات التقنية السعودية"
    },
    {
        "quote": "كان العمل مع شركة نجمة جدة في مشروع التطوير السكني الخاص بنا تجربة سلسة. احترافية فريقهم والتزامهم بالتميز لا مثيل له في هذا المجال.",
        "author": "نورة الشمري، مديرة شركة المنار للتطوير"
    },
    {
        "quote": "تعامل فريق شركة نجمة جدة مع التحديات المعقدة في منشأتنا الصناعية بحلول مبتكرة. خبرتهم في البناء الصناعي مثيرة للإعجاب حقًا.",
        "author": "سعد المطيري، مدير العمليات في المجموعة السعودية للتصنيع"
    }
]

# Create DataFrames for projects and services
projects_df = pd.DataFrame({
    "name": list(projects.keys()),
    "icon": [project["icon"] for project in projects.values()],
    "location": [project["location"] for project in projects.values()],
    "description": [project["description"] for project in projects.values()],
    "year": [project["year"] for project in projects.values()],
    "category": [project["category"] for project in projects.values()]
})

with tab4:
    st.markdown("<h2>🏢 من نحن</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        <span class='icon'>🏗️</span> مرحبًا بكم في شركة نجمة جدة للمقاولات، شركة رائدة في مجال البناء في المملكة العربية السعودية مع أكثر من 20 عامًا من الخبرة في تقديم التميز في البناء وتطوير البنية التحتية.
    </div>
    """, unsafe_allow_html=True)
    
    # About section
    st.markdown("""
    <div class="about-section">
        <h3>✨ قصتنا ✨</h3>
        <p>تأسست شركة نجمة جدة للمقاولات في عام 2003، ونمت من مقاول محلي صغير إلى واحدة من أكثر شركات البناء احترامًا في المملكة العربية السعودية. مع المقر الرئيسي في جدة ومكاتب في جميع أنحاء المملكة، أكملنا بنجاح أكثر من 200 مشروع تتراوح من التطورات السكنية الفاخرة إلى أعمال البنية التحتية واسعة النطاق.</p>
        
        <p>التزامنا بالجودة والابتكار ورضا العملاء جعل شركة نجمة جدة شريكًا موثوقًا به لعملاء القطاعين العام والخاص. نحن نجمع بين القيم التقليدية وتقنيات البناء المتطورة لتقديم مشاريع تصمد أمام اختبار الزمن.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Vision & Mission
    st.markdown('<div class="about-section" style="background-color: #f0f7ff;">', unsafe_allow_html=True)
    
    # Vision section
    st.write("### 🔭 رؤيتنا")
    st.write("أن نكون شركة البناء الرائدة في المملكة العربية السعودية، المعروفة بالتميز والابتكار وممارسات التنمية المستدامة التي تساهم في رؤية المملكة 2030.")
    
    # Mission section
    st.write("### 🎯 مهمتنا")
    st.write("تقديم مشاريع بناء عالية الجودة تتجاوز توقعات العملاء من خلال الحلول المبتكرة والحرفية الماهرة والالتزام الثابت بالسلامة والاستدامة وتنمية المجتمع.")
    
    # Values section
    st.write("### 💎 قيمنا")
    st.write("""
    - **التميز**: نسعى للتميز في كل جانب من جوانب عملنا
    - **النزاهة**: نمارس الأعمال التجارية بصدق وشفافية
    - **الابتكار**: نتبنى التقنيات الجديدة وأساليب البناء الحديثة
    - **السلامة**: نعطي الأولوية لسلامة فريقنا والمجتمعات
    - **الاستدامة**: نبني مع وضع الأجيال القادمة في الاعتبار
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Team section
    st.subheader("👥 فريق القيادة لدينا")
    
    cols = st.columns(3)
    for i, (name, info) in enumerate(team_members.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="team-member">
                <h3>{name}</h3>
                <p><strong>{info['position']}</strong></p>
                <p>{info['bio']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Company statistics
    st.subheader("📊 شركة نجمة جدة بالأرقام")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("سنوات الخبرة", "+20")
    with col2:
        st.metric("المشاريع المنجزة", "+200")
    with col3:
        st.metric("الفريق المهني", "+500")
    with col4:
        st.metric("رضا العملاء", "98%")

with tab3:
    st.markdown("<h2>🛠️ خدماتنا</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        <span class='icon'>🛠️</span> تقدم شركة نجمة جدة خدمات بناء شاملة عبر القطاعات السكنية والتجارية والصناعية والبنية التحتية. يضمن نهجنا المتكامل الجودة في كل مرحلة من مراحل مشروعك.
    </div>
    """, unsafe_allow_html=True)
    
    # Display services in cards
    st.markdown("<div class='project-grid'>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, (service_name, service_info) in enumerate(services.items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="service-card {service_info['category']}">
                <h3>{service_info['icon']} {service_name}</h3>
                <p>{service_info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Service process
    st.subheader("🔄 عملية الخدمة لدينا")
    
    process_steps = {
        "الاستشارة": "نبدأ باستشارة شاملة لفهم رؤيتك ومتطلباتك وقيود الميزانية.",
        "التخطيط والتصميم": "يقوم فريق الخبراء لدينا بتطوير خطط وتصاميم مفصلة مصممة خصيصًا لتلبية احتياجاتك وأهدافك المحددة.",
        "اختيار المواد": "نحن نوفر مواد عالية الجودة توازن بين الجماليات والمتانة والاستدامة.",
        "البناء": "ينفذ القوى العاملة الماهرة لدينا المشروع بدقة، متبعة بروتوكولات صارمة لمراقبة الجودة.",
        "ضمان الجودة": "تضمن عمليات التفتيش الدقيقة أن كل جانب من جوانب البناء يلبي معاييرنا الدقيقة.",
        "التسليم": "نقوم بتسليم مشروعك المكتمل في الوقت المحدد، مع وثائق شاملة ودعم."
    }
    
    for step, description in process_steps.items():
        st.markdown(f"""
        <div style="padding: 15px; margin-bottom: 10px; background-color: white; border-radius: 10px; border-right: 4px solid #1a3c6e;">
            <h4>{step}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Certifications
    st.subheader("🏅 شهاداتنا")
    
    certifications = [
        "ISO 9001:2015 - إدارة الجودة",
        "ISO 14001:2015 - الإدارة البيئية",
        "ISO 45001:2018 - الصحة والسلامة المهنية",
        "شهادة تصنيف المقاولين السعوديين - الدرجة الأولى",
        "محترفون معتمدون من LEED ضمن الفريق"
    ]
    
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
        <ul style="list-style-type: none; padding-right: 0;">
    """, unsafe_allow_html=True)
    
    for cert in certifications:
        st.markdown(f"<li style='margin-bottom: 10px;'>✅ {cert}</li>", unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<h2>🏗️ مشاريعنا</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        <span class='icon'>🏗️</span> استكشف محفظة مشاريعنا الناجحة في جميع أنحاء المملكة العربية السعودية. يعرض كل مشروع التزامنا بالجودة والابتكار ورضا العملاء.
    </div>
    """, unsafe_allow_html=True)
    
    # Project filter
    project_categories = ["الكل"] + list(set(project["category"] for project in projects.values()))
    selected_category = st.selectbox("تصفية حسب الفئة", project_categories)
    
    # Display projects in cards
    st.markdown("<div class='project-grid'>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    project_index = 0
    
    for project_name, project_info in projects.items():
        if selected_category == "الكل" or project_info["category"] == selected_category:
            with cols[project_index % 2]:
                st.markdown(f"""
                <div class="project-card">
                    <h3>{project_info['icon']} {project_name}</h3>
                    <p><strong>الموقع:</strong> {project_info['location']}</p>
                    <p><strong>الفئة:</strong> {project_info['category']}</p>
                    <p><strong>الإنجاز:</strong> {project_info['year']}</p>
                    <p>{project_info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                project_index += 1
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Project showcase
    st.subheader("🌟 أبرز المشاريع")
    
    # Create a network graph to showcase project relationships
    G = nx.Graph()
    
    # Add nodes for projects and categories
    for project_name, project_info in projects.items():
        G.add_node(project_name, 
                  title=f"{project_name}<br>{project_info['location']}<br>{project_info['description']}", 
                  group=1)
        G.add_node(project_info['category'], title=project_info['category'], group=0)
        G.add_edge(project_name, project_info['category'])
    
    # Create a pyvis network
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    
    # Set options
    net.set_options('''
    {
      "nodes": {
        "shape": "circle",
        "size": 30,
        "font": {
          "size": 16,
          "face": "Tajawal"
        },
        "borderWidth": 3,
        "shadow": true,
        "color": {
          "border": "#1a3c6e",
          "background": "#e6eef8"
        }
      },
      "edges": {
        "color": {
          "color": "#f7a100",
          "highlight": "#ff8c00"
        },
        "width": 2,
        "smooth": {
          "type": "continuous",
          "roundness": 0.5
        }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.08
        },
        "solver": "forceAtlas2Based"
      }
    }
    ''')
    
    # Add nodes and edges from networkx graph
    net.from_nx(G)
    
    # Generate the HTML file
    net.save_graph("family_tree.html")
    
    # Display the HTML file
    with open("family_tree.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    components.html(html, height=600)
    
    st.info("👆 استكشف شبكة مشاريعنا أعلاه. المشاريع متصلة بفئاتها. انقر على أي عقدة لرؤية التفاصيل!")
    
    # Client testimonials
    st.subheader("💬 شهادات العملاء")
    
    for testimonial in testimonials:
        st.markdown(f"""
        <div class="testimonial">
            <div class="testimonial-content">
                {testimonial['quote']}
            </div>
            <div class="testimonial-author">
                - {testimonial['author']}
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab1:
    st.markdown("<h2>📞 تواصل معنا</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        <span class='icon'>📞</span> هل أنت جاهز لبدء مشروعك؟ تواصل مع شركة نجمة جدة اليوم للحصول على استشارة. فريقنا جاهز لتحويل رؤيتك إلى واقع بخبرة وتميز.
    </div>
    """, unsafe_allow_html=True)
    
    # Contact form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>تواصل معنا</h3>
            <form>
                <div style="margin-bottom: 15px;">
                    <label for="name">الاسم</label>
                    <input type="text" id="name" placeholder="اسمك" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; text-align: right;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label for="email">البريد الإلكتروني</label>
                    <input type="email" id="email" placeholder="بريدك الإلكتروني" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; text-align: right;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label for="phone">رقم الهاتف</label>
                    <input type="tel" id="phone" placeholder="رقم هاتفك" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; text-align: right;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label for="message">الرسالة</label>
                    <textarea id="message" placeholder="أخبرنا عن مشروعك" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; height: 150px; text-align: right;"></textarea>
                </div>
                <button type="submit" style="background-color: #f7a100; color: white; border: none; padding: 12px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">إرسال الرسالة</button>
            </form>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>معلومات الاتصال</h3>
            <p><strong>العنوان:</strong> طريق الملك فهد، حي الحمراء، جدة، المملكة العربية السعودية</p>
            <p><strong>الهاتف:</strong> 6789 345 12 966+</p>
            <p><strong>البريد الإلكتروني:</strong> info@jeddahstarcompany.com</p>
            <p><strong>ساعات العمل:</strong> الأحد - الخميس: 8:00 صباحًا - 5:00 مساءً</p>
            
            <h4 style="margin-top: 20px;">مكاتبنا</h4>
            <ul style="list-style-type: none; padding-right: 0;">
                <li style="margin-bottom: 10px;">🏢 جدة (المقر الرئيسي)</li>
                <li style="margin-bottom: 10px;">🏢 الرياض</li>
                <li style="margin-bottom: 10px;">🏢 الدمام</li>
                <li style="margin-bottom: 10px;">🏢 مكة المكرمة</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Map placeholder
    st.markdown("""
    <div style="background-color: #e6eef8; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: center;">
        <h3>موقعنا</h3>
        <p>سيتم عرض الخريطة التفاعلية هنا في بيئة الإنتاج.</p>
        <div style="background-color: #ccc; height: 300px; display: flex; align-items: center; justify-content: center; border-radius: 5px;">
            <span style="font-size: 24px;">🗺️ مكان الخريطة</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer with company info
st.markdown("""
<footer>
    <p>© 2025 شركة نجمة جدة للمقاولات | التميز في البناء منذ 2003 | <a href="#" style="color: #f7a100;">سياسة الخصوصية</a> | <a href="#" style="color: #f7a100;">شروط الخدمة</a></p>
</footer>
""", unsafe_allow_html=True)

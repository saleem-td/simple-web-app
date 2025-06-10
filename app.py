import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# Page configuration
st.set_page_config(
    page_title="JSC - Jeddah Star Company",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS directly in the app.py file
css = """
/* Main styling */
body {
    font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    background-color: #f9f9f9;
}

/* Header styling */
h1, h2, h3 {
    font-family: 'Montserrat', sans-serif;
    color: #1a3c6e;
    font-weight: 700;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
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
    border-left: 4px solid #f7a100;
    border-radius: 0 8px 8px 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Project cards */
.project-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 20px;
}

.project-card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-top: 4px solid #f7a100;
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
}

/* Service cards */
.service-card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-left: 4px solid #1a3c6e;
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
}

/* About section */
.about-section {
    background-color: #e6eef8;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.about-section h3 {
    color: #1a3c6e;
    margin-top: 20px;
}

/* Footer */
footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    border-top: 1px solid #eee;
    color: #7f8c8d;
    font-size: 14px;
    background-color: #1a3c6e;
    color: white;
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
.service-residential { border-left-color: #4caf50; }
.service-commercial { border-left-color: #2196f3; }
.service-industrial { border-left-color: #f44336; }
.service-infrastructure { border-left-color: #9c27b0; }

/* Icon styling */
.icon {
    font-size: 24px;
    margin-right: 8px;
    vertical-align: middle;
}

.title-icon {
    font-size: 32px;
    margin-right: 10px;
    vertical-align: middle;
}

.card-icon {
    font-size: 20px;
    float: right;
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
}

.testimonial:before {
    content: '"';
    font-size: 60px;
    color: #f7a100;
    position: absolute;
    top: 10px;
    left: 10px;
    opacity: 0.2;
}

.testimonial-content {
    padding-left: 30px;
    font-style: italic;
}

.testimonial-author {
    text-align: right;
    font-weight: bold;
    color: #1a3c6e;
}
"""

# Apply CSS
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <span class="title-icon">🏗️</span>
    <h1>Jeddah Star Company</h1>
    <p>Building Excellence, Delivering Quality - Your Premier Construction Partner in Saudi Arabia</p>
    <a href="#contact" class="cta-button">Contact Us Today</a>
</div>
""", unsafe_allow_html=True)

# Create tabs with icons
tab1, tab2, tab3, tab4 = st.tabs(["🏢 About Us", "🛠️ Our Services", "🏗️ Projects", "📞 Contact"])

# Define company data
services = {
    "Residential Construction": {
        "icon": "🏠",
        "description": "Custom homes, apartment buildings, and residential complexes built to the highest standards.",
        "category": "service-residential"
    },
    "Commercial Construction": {
        "icon": "🏢",
        "description": "Office buildings, retail spaces, hotels, and other commercial properties designed for success.",
        "category": "service-commercial"
    },
    "Industrial Construction": {
        "icon": "🏭",
        "description": "Factories, warehouses, and industrial facilities built for efficiency and durability.",
        "category": "service-industrial"
    },
    "Infrastructure Development": {
        "icon": "🌉",
        "description": "Roads, bridges, and public works projects that connect communities.",
        "category": "service-infrastructure"
    },
    "Renovation & Remodeling": {
        "icon": "🔨",
        "description": "Transform existing spaces with our expert renovation and remodeling services.",
        "category": "service-residential"
    },
    "Project Management": {
        "icon": "📋",
        "description": "End-to-end project management ensuring on-time, on-budget delivery.",
        "category": "service-commercial"
    },
    "Architectural Design": {
        "icon": "✏️",
        "description": "Creative and functional architectural designs that bring your vision to life.",
        "category": "service-commercial"
    },
    "Green Building": {
        "icon": "🌱",
        "description": "Sustainable construction practices and LEED-certified building options.",
        "category": "service-residential"
    }
}

projects = {
    "Al Madinah Towers": {
        "icon": "🏢",
        "location": "Madinah, Saudi Arabia",
        "description": "Luxury residential towers with 200+ premium apartments and state-of-the-art amenities.",
        "year": "2023",
        "category": "Residential"
    },
    "Jeddah Business Center": {
        "icon": "🏙️",
        "location": "Jeddah, Saudi Arabia",
        "description": "Modern office complex with smart building technology and sustainable design features.",
        "year": "2022",
        "category": "Commercial"
    },
    "Red Sea Resort": {
        "icon": "🏖️",
        "location": "Red Sea Coast, Saudi Arabia",
        "description": "Luxury beachfront resort with private villas and world-class hospitality facilities.",
        "year": "2021",
        "category": "Hospitality"
    },
    "Riyadh Industrial Park": {
        "icon": "🏭",
        "location": "Riyadh, Saudi Arabia",
        "description": "Large-scale industrial development with warehousing and manufacturing facilities.",
        "year": "2023",
        "category": "Industrial"
    },
    "King Abdullah Medical City": {
        "icon": "🏥",
        "location": "Makkah, Saudi Arabia",
        "description": "State-of-the-art medical facility with specialized treatment centers and research labs.",
        "year": "2020",
        "category": "Healthcare"
    },
    "Dammam Highway Extension": {
        "icon": "🛣️",
        "location": "Dammam, Saudi Arabia",
        "description": "Major infrastructure project extending the highway network with bridges and interchanges.",
        "year": "2022",
        "category": "Infrastructure"
    },
    "Al Khobar Shopping Mall": {
        "icon": "🛍️",
        "location": "Al Khobar, Saudi Arabia",
        "description": "Premium retail destination with international brands, entertainment, and dining options.",
        "year": "2021",
        "category": "Commercial"
    },
    "Tabuk Residential Community": {
        "icon": "🏘️",
        "location": "Tabuk, Saudi Arabia",
        "description": "Integrated residential community with schools, parks, and community facilities.",
        "year": "2023",
        "category": "Residential"
    }
}

team_members = {
    "Abdullah Al-Saud": {
        "position": "CEO & Founder",
        "bio": "With over 30 years in construction, Abdullah has led JSC from a small contractor to a leading construction firm in Saudi Arabia."
    },
    "Mohammed Al-Qahtani": {
        "position": "Chief Operations Officer",
        "bio": "Mohammed oversees all project operations, ensuring quality, safety, and timely delivery across all JSC projects."
    },
    "Sara Al-Ghamdi": {
        "position": "Chief Architect",
        "bio": "Award-winning architect with expertise in sustainable design and innovative building solutions."
    },
    "Khalid Al-Otaibi": {
        "position": "Project Director",
        "bio": "Specializing in large-scale commercial and infrastructure projects with over 20 years of experience."
    },
    "Fatima Al-Harbi": {
        "position": "Finance Director",
        "bio": "Managing JSC's financial operations and strategic investments to ensure sustainable growth."
    }
}

testimonials = [
    {
        "quote": "JSC delivered our corporate headquarters ahead of schedule and under budget. Their attention to detail and quality workmanship exceeded our expectations.",
        "author": "Ahmed Al-Dosari, CEO of Saudi Tech Innovations"
    },
    {
        "quote": "Working with JSC on our residential development was a seamless experience. Their team's professionalism and commitment to excellence is unmatched in the industry.",
        "author": "Nora Al-Shammari, Director of Al Manar Development"
    },
    {
        "quote": "The JSC team tackled complex challenges on our industrial facility with innovative solutions. Their expertise in industrial construction is truly impressive.",
        "author": "Saad Al-Mutairi, Operations Manager at Saudi Manufacturing Group"
    }
]

# Create a DataFrame
family_df = pd.DataFrame(family_data)

with tab1:
    st.markdown("<h2>🏢 About Jeddah Star Company</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        <span class='icon'>🏗️</span> Welcome to Jeddah Star Company (JSC), a leading construction firm in Saudi Arabia with over 20 years of experience delivering excellence in construction and infrastructure development.
    </div>
    """, unsafe_allow_html=True)
    
    # About section
    st.markdown("""
    <div class="about-section">
        <h3>✨ Our Story ✨</h3>
        <p>Founded in 2003, Jeddah Star Company has grown from a small local contractor to one of Saudi Arabia's most respected construction firms. With headquarters in Jeddah and offices across the Kingdom, we've successfully completed over 200 projects ranging from luxury residential developments to large-scale infrastructure works.</p>
        
        <p>Our commitment to quality, innovation, and client satisfaction has established JSC as a trusted partner for both public and private sector clients. We combine traditional values with cutting-edge construction techniques to deliver projects that stand the test of time.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Vision & Mission
    st.markdown('<div class="about-section" style="background-color: #f0f7ff;">', unsafe_allow_html=True)
    
    # Vision section
    st.write("### 🔭 Our Vision")
    st.write("To be the leading construction company in Saudi Arabia, recognized for excellence, innovation, and sustainable development practices that contribute to the Kingdom's Vision 2030.")
    
    # Mission section
    st.write("### 🎯 Our Mission")
    st.write("To deliver high-quality construction projects that exceed client expectations through innovative solutions, skilled craftsmanship, and unwavering commitment to safety, sustainability, and community development.")
    
    # Values section
    st.write("### 💎 Our Values")
    st.write("""
    - **Excellence**: We strive for excellence in every aspect of our work
    - **Integrity**: We conduct business with honesty and transparency
    - **Innovation**: We embrace new technologies and construction methods
    - **Safety**: We prioritize the safety of our team and communities
    - **Sustainability**: We build with future generations in mind
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Team section
    st.subheader("👥 Our Leadership Team")
    
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
    st.subheader("📊 JSC by the Numbers")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Years of Experience", "20+")
    with col2:
        st.metric("Completed Projects", "200+")
    with col3:
        st.metric("Professional Team", "500+")
    with col4:
        st.metric("Client Satisfaction", "98%")

with tab2:
    st.markdown("<h2>🛠️ Our Services</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        <span class='icon'>🛠️</span> JSC offers comprehensive construction services across residential, commercial, industrial, and infrastructure sectors. Our integrated approach ensures quality at every stage of your project.
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
    st.subheader("🔄 Our Service Process")
    
    process_steps = {
        "Consultation": "We begin with a thorough consultation to understand your vision, requirements, and budget constraints.",
        "Planning & Design": "Our expert team develops detailed plans and designs tailored to your specific needs and objectives.",
        "Material Selection": "We source high-quality materials that balance aesthetics, durability, and sustainability.",
        "Construction": "Our skilled workforce executes the project with precision, following strict quality control protocols.",
        "Quality Assurance": "Rigorous inspections ensure every aspect of construction meets our exacting standards.",
        "Handover": "We deliver your completed project on time, with comprehensive documentation and support."
    }
    
    for step, description in process_steps.items():
        st.markdown(f"""
        <div style="padding: 15px; margin-bottom: 10px; background-color: white; border-radius: 10px; border-left: 4px solid #1a3c6e;">
            <h4>{step}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Certifications
    st.subheader("🏅 Our Certifications")
    
    certifications = [
        "ISO 9001:2015 - Quality Management",
        "ISO 14001:2015 - Environmental Management",
        "ISO 45001:2018 - Occupational Health and Safety",
        "Saudi Contractors Classification Certificate - Grade 1",
        "LEED Accredited Professionals on Staff"
    ]
    
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
        <ul style="list-style-type: none; padding-left: 0;">
    """, unsafe_allow_html=True)
    
    for cert in certifications:
        st.markdown(f"<li style='margin-bottom: 10px;'>✅ {cert}</li>", unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<h2>🏗️ Our Featured Projects</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        <span class='icon'>🏗️</span> Explore our portfolio of successful projects across Saudi Arabia. Each project showcases our commitment to quality, innovation, and client satisfaction.
    </div>
    """, unsafe_allow_html=True)
    
    # Project filter
    project_categories = ["All"] + list(set(project["category"] for project in projects.values()))
    selected_category = st.selectbox("Filter by Category", project_categories)
    
    # Display projects in cards
    st.markdown("<div class='project-grid'>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    project_index = 0
    
    for project_name, project_info in projects.items():
        if selected_category == "All" or project_info["category"] == selected_category:
            with cols[project_index % 2]:
                st.markdown(f"""
                <div class="project-card">
                    <h3>{project_info['icon']} {project_name}</h3>
                    <p><strong>Location:</strong> {project_info['location']}</p>
                    <p><strong>Category:</strong> {project_info['category']}</p>
                    <p><strong>Completed:</strong> {project_info['year']}</p>
                    <p>{project_info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                project_index += 1
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Project showcase
    st.subheader("🌟 Project Highlights")
    
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
          "face": "Montserrat"
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
    
    st.info("👆 Explore our project network above. Projects are connected to their categories. Click on any node to see details!")
    
    # Client testimonials
    st.subheader("💬 Client Testimonials")
    
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

with tab4:
    st.markdown("<h2>📞 Contact Us</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        <span class='icon'>📞</span> Ready to start your project? Contact JSC today for a consultation. Our team is ready to bring your vision to life with expertise and excellence.
    </div>
    """, unsafe_allow_html=True)
    
    # Contact form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>Get in Touch</h3>
            <form>
                <div style="margin-bottom: 15px;">
                    <label for="name">Name</label>
                    <input type="text" id="name" placeholder="Your Name" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label for="email">Email</label>
                    <input type="email" id="email" placeholder="Your Email" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label for="phone">Phone</label>
                    <input type="tel" id="phone" placeholder="Your Phone" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label for="message">Message</label>
                    <textarea id="message" placeholder="Tell us about your project" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; height: 150px;"></textarea>
                </div>
                <button type="submit" style="background-color: #f7a100; color: white; border: none; padding: 12px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">Send Message</button>
            </form>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>Contact Information</h3>
            <p><strong>Address:</strong> King Fahd Road, Al Hamra District, Jeddah, Saudi Arabia</p>
            <p><strong>Phone:</strong> +966 12 345 6789</p>
            <p><strong>Email:</strong> info@jeddahstarcompany.com</p>
            <p><strong>Working Hours:</strong> Sunday - Thursday: 8:00 AM - 5:00 PM</p>
            
            <h4 style="margin-top: 20px;">Our Offices</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 10px;">🏢 Jeddah (Headquarters)</li>
                <li style="margin-bottom: 10px;">🏢 Riyadh</li>
                <li style="margin-bottom: 10px;">🏢 Dammam</li>
                <li style="margin-bottom: 10px;">🏢 Makkah</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Map placeholder
    st.markdown("""
    <div style="background-color: #e6eef8; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: center;">
        <h3>Our Location</h3>
        <p>Interactive map would be displayed here in a production environment.</p>
        <div style="background-color: #ccc; height: 300px; display: flex; align-items: center; justify-content: center; border-radius: 5px;">
            <span style="font-size: 24px;">🗺️ Map Placeholder</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer with company info
st.markdown("""
<footer>
    <p>© 2025 Jeddah Star Company | Building Excellence Since 2003 | <a href="#" style="color: #f7a100;">Privacy Policy</a> | <a href="#" style="color: #f7a100;">Terms of Service</a></p>
</footer>
""", unsafe_allow_html=True)

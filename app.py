import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# Page configuration
st.set_page_config(
    page_title="Family Tree ✨",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS directly in the app.py file
css = """
/* Main styling */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    background-color: #fcfcfc;
}

/* Header styling */
h1, h2, h3 {
    font-family: 'Georgia', serif;
    color: #2c3e50;
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
    background-color: #e3f2fd;
    border-bottom: 2px solid #1976d2;
}

/* Introduction text */
.intro-text {
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 30px;
    padding: 20px;
    background-color: #fff8e1;
    border-left: 4px solid #ffb74d;
    border-radius: 0 8px 8px 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Member cards */
.member-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 20px;
}

.member-card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-top: 4px solid #4caf50;
}

.member-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.member-card h3 {
    margin-top: 0;
    color: #2c3e50;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

/* About section */
.about-section {
    background-color: #e8f5e9;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.about-section h3 {
    color: #2e7d32;
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
    background-color: #f5f5f5;
    border-radius: 8px;
}

/* Metrics styling */
div[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: bold;
    color: #ff7043;
}

div[data-testid="stMetricLabel"] {
    font-weight: 500;
    color: #455a64;
}

/* Network graph container */
.network-container {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    padding: 15px;
    margin-bottom: 20px;
}

/* Generation colors */
.generation-0 { background-color: #e3f2fd; }
.generation-1 { background-color: #e8f5e9; }
.generation-2 { background-color: #fff3e0; }
.generation-3 { background-color: #f3e5f5; }

/* Emoji styling */
.emoji {
    font-size: 24px;
    margin-right: 8px;
    vertical-align: middle;
}

.title-emoji {
    font-size: 32px;
    margin-right: 10px;
    vertical-align: middle;
}

.card-emoji {
    font-size: 20px;
    float: right;
    margin-top: -30px;
}
"""

# Apply CSS
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Title and introduction with emojis
st.markdown("<span class='title-emoji'>👨‍👩‍👧‍👦</span> <span class='title-emoji'>✨</span>", unsafe_allow_html=True)
st.title("Our Wonderful Family Tree")
st.markdown("""
<div class="intro-text">
    <span class='emoji'>🌳</span> Welcome to our interactive family tree! Explore the connections and learn more about each family member. 
    <span class='emoji'>💖</span> Discover the beautiful bonds that tie our family together across generations!
</div>
""", unsafe_allow_html=True)

# Create tabs with emojis
tab1, tab2, tab3 = st.tabs(["🌳 Family Tree", "👪 Family Members", "📜 About Us"])

# Define family data with emojis for professions
profession_emojis = {
    "Grandfather": "👴",
    "Grandmother": "👵",
    "Father": "👨",
    "Mother": "👩",
    "Obstetrics & Gynecology Consultant": "👩‍⚕️",
    "Human Resources Management": "👩‍💼",
    "Orthodontics Consultant": "🦷",
    "Finance": "💰",
    "Network Systems Engineering": "💻",
    "Management Information Systems": "📊",
    "Mechanical Engineering - Student": "🔧",
    "Middle School Student": "🎒",
    "Biochemistry & Nutrition": "🧪",
    "Chemical Engineering": "⚗️",
    "Accounting": "📝",
    "Mechanical Engineering": "⚙️",
    "Biochemistry": "🔬",
    "Economics": "📈",
    "Network Security": "🔒",
    "Science": "🔭",
    "Marine Biology": "🐠",
    "Network Technology": "🌐",
    "Child": "👶"
}

family_data = {
    "name": ["Saleem", "Samia", 
             "Talal", "Laila", "Maha", "Mona",
             "Ghada", "Dalia", "Dima", "Aya", "Saleem Jr", "Mohammed", "Faisal", "Omar",
             "Khloud", "Khaled",
             "Soha", "Lamia", "Basma", "Ruba", "Fawaz",
             "Mirna", "Mayar", "Miran", "Myrai", "Abdulaziz", "Abdulrahman", "Abdulwahab",
             "Layan", 
             "Rima", "Talia", 
             "Yazan", "Zeina", 
             "Yousef",
             "Abdulmalik", "Abdulilah", "Noah",
             "Salma",
             "Mohammed Jr", "Yara",
             "Malek"],
    "generation": [0, 0, 
                  1, 1, 1, 1,
                  2, 2, 2, 2, 2, 2, 2, 2,
                  2, 2,
                  2, 2, 2, 2, 2,
                  2, 2, 2, 2, 2, 2, 2,
                  3, 
                  3, 3, 
                  3, 3, 
                  3,
                  3, 3, 3,
                  3,
                  3, 3,
                  3],
    "parent": [None, None, 
              "Saleem", "Saleem", "Saleem", "Saleem",
              "Talal", "Talal", "Talal", "Talal", "Talal", "Talal", "Talal", "Talal",
              "Laila", "Laila",
              "Maha", "Maha", "Maha", "Maha", "Maha",
              "Mona", "Mona", "Mona", "Mona", "Mona", "Mona", "Mona",
              "Ghada", 
              "Dalia", "Dalia", 
              "Dima", "Dima", 
              "Aya",
              "Soha", "Soha", "Soha",
              "Lamia",
              "Ruba", "Ruba",
              "Fawaz"],
    "profession": ["Grandfather", "Grandmother", 
                  "Father", "Mother", "Mother", "Mother",
                  "Obstetrics & Gynecology Consultant", "Human Resources Management", "Orthodontics Consultant", 
                  "Finance", "Network Systems Engineering", "Management Information Systems", 
                  "Mechanical Engineering - Student", "Middle School Student",
                  "Biochemistry & Nutrition", "Management Information Systems",
                  "Human Resources Management", "Chemical Engineering", "Finance", "Accounting", "Mechanical Engineering",
                  "Biochemistry", "Economics", "Network Security", "Science", 
                  "Marine Biology", "Network Technology", "Accounting",
                  "Child", 
                  "Child", "Child", 
                  "Child", "Child", 
                  "Child",
                  "Child", "Child", "Child",
                  "Child",
                  "Child", "Child",
                  "Child"]
}

# Create a DataFrame
family_df = pd.DataFrame(family_data)

with tab1:
    st.markdown("<h2>🌳 Interactive Family Tree</h2>", unsafe_allow_html=True)
    
    # Create a network graph
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for i, row in family_df.iterrows():
        emoji = profession_emojis.get(row['profession'], "👤")
        G.add_node(row['name'], 
                  title=f"{row['name']} {emoji}<br>Profession: {row['profession']}", 
                  group=row['generation'])
    
    # Add edges (connections)
    for i, row in family_df.iterrows():
        if row['parent'] is not None:
            G.add_edge(row['parent'], row['name'])
    
    # Create a pyvis network
    net = Network(height="600px", width="100%", directed=True, bgcolor="#ffffff", font_color="black")
    
    # Set options
    net.set_options('''
    {
      "nodes": {
        "shape": "circle",
        "size": 30,
        "font": {
          "size": 16,
          "face": "Tahoma"
        },
        "borderWidth": 3,
        "shadow": true,
        "color": {
          "border": "#2c3e50",
          "background": "#ecf0f1"
        }
      },
      "edges": {
        "color": {
          "color": "#3498db",
          "highlight": "#e74c3c"
        },
        "width": 3,
        "smooth": {
          "type": "continuous",
          "roundness": 0.5
        }
      },
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0.5,
          "springLength": 150,
          "springConstant": 0.01,
          "nodeDistance": 120,
          "damping": 0.09
        },
        "solver": "hierarchicalRepulsion"
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "levelSeparation": 150,
          "nodeSpacing": 120,
          "treeSpacing": 200,
          "direction": "UD"
        }
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
    
    st.info("👆 You can interact with the family tree above. Drag nodes to rearrange, zoom in/out with the mouse wheel, and click on members to see details! ✨")

with tab2:
    st.markdown("<h2>👪 Our Amazing Family Members</h2>", unsafe_allow_html=True)
    
    # Create generation filter with emojis
    generations = {
        0: "👵👴 Grandparents",
        1: "👩👨 Children",
        2: "👱‍♀️👱‍♂️ Grandchildren",
        3: "👶 Great-grandchildren"
    }
    
    selected_gen = st.selectbox("Select Generation", list(generations.values()))
    gen_num = list(generations.keys())[list(generations.values()).index(selected_gen)]
    
    # Filter dataframe by generation
    filtered_df = family_df[family_df['generation'] == gen_num]
    
    # Display family members in cards
    st.markdown("<div class='member-grid'>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, (_, member) in enumerate(filtered_df.iterrows()):
        emoji = profession_emojis.get(member['profession'], "👤")
        
        # Get children information
        children = family_df[family_df['parent'] == member['name']]['name'].tolist()
        children_str = ', '.join(children) if children else ""
        children_emojis = '👶' * len(children) if children else ""
        
        with cols[i % 3]:
            card_html = f"""
            <div class="member-card">
                <h3>{member['name']} <span class="card-emoji">{emoji}</span></h3>
                <p><strong>Profession:</strong> {member['profession']}</p>
            """
            
            # Add parent info if exists
            if member['parent']:
                card_html += f"<p><strong>Parent:</strong> {member['parent']} 👪</p>"
            
            # Add children info if exists
            if children:
                card_html += f"<p><strong>Children:</strong> {children_str} {children_emojis}</p>"
                
            card_html += "</div>"
            
            st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<h2>📜 About Our Wonderful Family</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-section">
        <h3>✨ Our Family History ✨</h3>
        <p>This interactive family tree showcases our family's generations, from grandparents to great-grandchildren. Each member brings their unique talents and personality to our amazing family!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create separate sections with explicit HTML rendering
    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    
    # Family Structure section
    st.write("### 👨‍👩‍👧‍👦 Family Structure")
    st.write("Our family begins with Saleem and his wife Samia. They had four wonderful children: Talal, Laila, Maha, and Mona, who have gone on to have their own children and grandchildren, creating a beautiful extended family filled with love and support.")
    
    # Professional Achievements section
    st.write("### 🏆 Professional Achievements")
    st.write("Our family members have diverse professional backgrounds, including medical professionals, engineers, finance experts, and students pursuing their education. We're proud of everyone's accomplishments and the passion they bring to their fields!")
    
    # Family Traditions section
    st.write("### 💖 Family Traditions")
    st.write("Our family loves to gather for special occasions, sharing stories, delicious food, and creating memories that will last a lifetime. From holiday celebrations to summer vacations, we cherish the time we spend together!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Family statistics with emojis
    st.subheader("✨ Family Statistics ✨")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👨‍👩‍👧‍👦 Total Family Members", len(family_df))
    with col2:
        st.metric("🔄 Generations", len(family_df['generation'].unique()))
    with col3:
        st.metric("👱‍♀️👱‍♂️ Grandchildren", len(family_df[family_df['generation'] == 2]))
    with col4:
        st.metric("👶 Great-grandchildren", len(family_df[family_df['generation'] == 3]))
        
    # Additional statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👨 Male Members", len([name for name in family_df['name'] if name.startswith(('Mohammed', 'Saleem', 'Talal', 'Khaled', 'Fawaz', 'Yazan', 'Yousef', 'Abdulmalik', 'Abdulilah', 'Noah', 'Abdulaziz', 'Abdulrahman', 'Abdulwahab', 'Malek', 'Omar', 'Faisal'))]))
    with col2:
        st.metric("👩 Female Members", len([name for name in family_df['name'] if not name.startswith(('Mohammed', 'Saleem', 'Talal', 'Khaled', 'Fawaz', 'Yazan', 'Yousef', 'Abdulmalik', 'Abdulilah', 'Noah', 'Abdulaziz', 'Abdulrahman', 'Abdulwahab', 'Malek', 'Omar', 'Faisal'))]))
    with col3:
        st.metric("🎓 Professionals", len(family_df[family_df['profession'] != "Child"]))
    with col4:
        st.metric("👨‍👩‍👧‍👦 Family Units", len(family_df[family_df['parent'].isnull() == False]['parent'].unique()))
    
    # Fun facts section
    st.markdown("""
    <div class="about-section" style="background-color: #fff3e0; margin-top: 30px;">
        <h3>🎉 Fun Family Facts 🎉</h3>
        <ul>
            <li>Our family spans 4 generations! 👵👴👩👨👱‍♀️👱‍♂️👶</li>
            <li>We have professionals in medicine 👩‍⚕️, engineering 🔧, finance 💰, and many other fields!</li>
            <li>The family includes 13 great-grandchildren and counting! 👶</li>
            <li>Our family tree continues to grow and flourish with each passing year! 🌱</li>
            <li>If we had a family reunion, we'd need to reserve at least 5 tables at a restaurant! 🍽️</li>
            <li>The most common profession in our family is related to finance and business! 💼</li>
            <li>Our family has enough members to form two full basketball teams! 🏀</li>
            <li>If we lined up all family members by height, we'd span the length of a tennis court! 📏</li>
            <li>The combined age of all family members is over 1,000 years of life experience! 🎂</li>
            <li>Our family's favorite holiday celebration requires at least 40 chairs! 🪑</li>
            <li>We have family members born in every season of the year! 🌞❄️🍂🌷</li>
            <li>If everyone in the family stood on each other's shoulders, we could reach the top of a 5-story building! 🏢</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer with emojis
st.markdown("""
<footer>
    <p>✨ Our Family Tree 2025 ✨ | Created with ❤️ using Streamlit | 👨‍👩‍👧‍👦</p>
</footer>
""", unsafe_allow_html=True)

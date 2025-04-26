# ======================================================
# Global AI Content Impact Dashboard (Preswald Project)
# ======================================================

# ----------------- Imports -----------------
from preswald import text, plotly, connect, get_df
import pandas as pd
import plotly.express as px

# ----------------- Logging Setup (Optional for Local Preview) -----------------
import logging
logging.basicConfig(level=logging.INFO)

# ======================================================
# Section 1: Title
# ======================================================

text("# 🌍 Global AI Content Impact Dashboard")
text("Welcome! This dashboard analyzes how AI is transforming industries and countries based on real-world data.")

# ======================================================
# Section 2: Load Dataset
# ======================================================

try:
    connect()
    df = get_df('ai_impact')
    logging.info("Dataset loaded successfully!")
except Exception as e:
    text(f"🚨 Error loading dataset: {str(e)}")

# ======================================================
# Section 3: AI Adoption Trends Over Years (Multi-Line Chart)
# ======================================================

try:
    text("## 📈 AI Adoption Trends Over Years")
    text("This line plot shows AI adoption rate trends over time for the top 5 industries.")

    adoption_df = df[['Year', 'Industry', 'AI Adoption Rate (%)']].dropna()
    top_industries = adoption_df.groupby('Industry')['AI Adoption Rate (%)'].mean().nlargest(5).index.tolist()
    top_df = adoption_df[adoption_df['Industry'].isin(top_industries)]
    pivot_df = top_df.pivot_table(index="Year", columns="Industry", values="AI Adoption Rate (%)").reset_index()
    pivot_df.fillna(method='ffill', inplace=True)

    fig = px.line(
        pivot_df,
        x="Year",
        y=pivot_df.columns[1:],
        markers=True,
        title="Top 5 Industries: AI Adoption Rate Trends",
        template="simple_white",
        color_discrete_sequence=px.colors.qualitative.Safe,
        height=500
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="AI Adoption Rate (%)",
        legend_title="Industry",
        title_x=0.5,
    )

    plotly(fig)
except Exception as e:
    text(f"🚨 Error creating AI Adoption Trends: {str(e)}")

# ======================================================
# Section 4: Revenue Growth vs Job Loss (Grouped Bar Chart)
# ======================================================

try:
    text("## 📊 Revenue Growth vs Job Loss Across Industries")
    text("This grouped bar chart compares revenue gains and job losses across industries.")

    rev_job_df = df[['Industry', 'Revenue Increase Due to AI (%)', 'Job Loss Due to AI (%)']].dropna()
    rev_job_grouped = rev_job_df.groupby('Industry').mean().reset_index()
    top_rev_industries = rev_job_grouped.sort_values(by='Revenue Increase Due to AI (%)', ascending=False).head(10)
    top_rev_melted = top_rev_industries.melt(id_vars="Industry", value_vars=["Revenue Increase Due to AI (%)", "Job Loss Due to AI (%)"],
                                             var_name="Metric", value_name="Percentage")

    fig = px.bar(
        top_rev_melted,
        x="Industry",
        y="Percentage",
        color="Metric",
        barmode="group",
        title="Revenue Growth vs Job Loss by Industry",
        template="simple_white",
        height=600
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        title_x=0.5,
    )

    plotly(fig)
except Exception as e:
    text(f"🚨 Error creating Revenue vs Job Loss chart: {str(e)}")

# ======================================================
# Section 5: Trust vs Adoption vs Market Share (Bubble Chart)
# ======================================================

try:
    text("## 🌐 Trust vs AI Adoption vs Market Share")
    text("This bubble chart explores the relationship between AI adoption, consumer trust, and market share.")

    bubble_df = df[['Industry', 'AI Adoption Rate (%)', 'Consumer Trust in AI (%)', 'Market Share of AI Companies (%)']].dropna()
    bubble_grouped = bubble_df.groupby('Industry').mean().reset_index()

    fig = px.scatter(
        bubble_grouped,
        x="AI Adoption Rate (%)",
        y="Consumer Trust in AI (%)",
        size="Market Share of AI Companies (%)",
        color="Industry",
        hover_name="Industry",
        size_max=40,
        title="Trust vs Adoption vs Market Share (Bubble Size = Market Share)",
        template="plotly_white",
        height=600
    )
    fig.update_layout(title_x=0.5)

    plotly(fig)
except Exception as e:
    text(f"🚨 Error creating Trust vs Adoption chart: {str(e)}")

# ======================================================
# Section 6: AI Regulation by Country (Choropleth Map)
# ======================================================

try:
    text("## 🗺️ AI Regulation by Country (Choropleth Map)")
    text("This choropleth map shows regulation strictness across different countries.")

    regulation_df = df[['Country', 'Regulation Status']].dropna()
    regulation_map = {'Strict': 3, 'Moderate': 2, 'Lenient': 1}
    regulation_df['Regulation_Level'] = regulation_df['Regulation Status'].map(regulation_map)
    regulation_grouped = regulation_df.groupby('Country')['Regulation_Level'].mean().reset_index()

    fig = px.choropleth(
        regulation_grouped,
        locations="Country",
        locationmode="country names",
        color="Regulation_Level",
        color_continuous_scale="Bluered_r",
        range_color=(1, 3),
        title="AI Regulation Strictness by Country",
        template="plotly_white"
    )
    fig.update_layout(title_x=0.5)

    plotly(fig)
except Exception as e:
    text(f"🚨 Error creating AI Regulation Map: {str(e)}")

# ======================================================
# Section 7: AI Tools Adoption Across Industries (Pie Chart)
# ======================================================

try:
    text("## 🥧 AI Tools Adoption Across Industries")
    text("This pie chart highlights the most popular AI tools used across industries.")

    tools_df = df[['Industry', 'Top AI Tools Used']].dropna()
    tools_grouped = tools_df.groupby('Top AI Tools Used').size().reset_index(name='Count')
    top_tools = tools_grouped.sort_values(by='Count', ascending=False).head(10)

    fig = px.pie(
        top_tools,
        names='Top AI Tools Used',
        values='Count',
        title="Top 10 AI Tools Adoption",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="plotly_white"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)

    plotly(fig)
except Exception as e:
    text(f"🚨 Error creating AI Tools Pie Chart: {str(e)}")

# ======================================================
# Section 8: Revenue Growth Binned by AI Adoption (Bar Chart)
# ======================================================

try:
    text("## 📊 Revenue Growth by AI Adoption Level (Binned)")
    text("This chart shows how average revenue growth changes with AI adoption levels.")

    bins = [0, 25, 50, 75, 100]
    labels = ['Low (0-25%)', 'Moderate (25-50%)', 'High (50-75%)', 'Very High (75-100%)']
    df['AI_Adoption_Bin'] = pd.cut(df['AI Adoption Rate (%)'], bins=bins, labels=labels, include_lowest=True)
    bin_summary = df.groupby('AI_Adoption_Bin', observed=True)['Revenue Increase Due to AI (%)'].mean().reset_index()

    fig = px.bar(
        bin_summary,
        x='AI_Adoption_Bin',
        y='Revenue Increase Due to AI (%)',
        color='AI_Adoption_Bin',
        text_auto=True,
        title="Average Revenue Growth by AI Adoption Bin",
        template="plotly_white"
    )
    fig.update_layout(title_x=0.5)

    plotly(fig)
except Exception as e:
    text(f"🚨 Error creating Binned Revenue Chart: {str(e)}")

# ======================================================
# Section 9: Top 5 Industries Radar Charts
# ======================================================

try:
    text("## 🧠 Balancing Trust, Collaboration, and AI Adoption (Radar Chart)")
    text("These radar charts compare key metrics separately for top 5 industries.")

    radar_raw = df.groupby('Industry', observed=True)[
        ['Human-AI Collaboration Rate (%)', 'Consumer Trust in AI (%)', 'AI Adoption Rate (%)']
    ].mean().reset_index()

    top5_industries = radar_raw.sort_values('AI Adoption Rate (%)', ascending=False).head(5)
    radar_data = top5_industries.melt(id_vars='Industry', var_name='Metric', value_name='Value')

    for industry in radar_data['Industry'].unique():
        industry_data = radar_data[radar_data['Industry'] == industry]

        fig = px.line_polar(
            industry_data,
            r='Value',
            theta='Metric',
            line_close=True,
            title=f"{industry} - Excellence in Trust, Collaboration, Adoption"
        )
        fig.update_traces(fill='toself')
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            template='plotly_white',
            title_x=0.5
        )
        plotly(fig)

except Exception as e:
    text(f"🚨 Error creating Industry Excellence Radars: {str(e)}")

# ======================================================
# Section 10: Simulated PCA Clustering (No sklearn)
# ======================================================

try:
    text("📈 **PCA Analysis: Clustering Industries by AI Behavior**")
    text("This chart shows clustering of industries based on AI adoption, trust, and collaboration metrics.")

    # Assume df is already loaded
    connect()
    df = get_df('ai_impact')

    # Aggregate
    cluster_df = df.groupby('Industry').agg({
        'AI Adoption Rate (%)': 'mean',
        'Human-AI Collaboration Rate (%)': 'mean',
        'Consumer Trust in AI (%)': 'mean'
    }).reset_index()

    # Simulate PCA axes
    cluster_df['PCA1'] = (cluster_df['AI Adoption Rate (%)'] + cluster_df['Human-AI Collaboration Rate (%)']) / 2
    cluster_df['PCA2'] = (cluster_df['Consumer Trust in AI (%)'] + cluster_df['Human-AI Collaboration Rate (%)']) / 2

    # Define Clusters manually
    cluster_df['Cluster'] = pd.cut(
        cluster_df['PCA1'],
        bins=[-float('inf'), 50, 70, float('inf')],
        labels=["Laggard", "Moderate", "Leader"]
    )

    # Color mapping
    color_map = {
        "Leader": "blue",
        "Moderate": "green",
        "Laggard": "red"
    }

    # Mean values
    pca1_mean = cluster_df['PCA1'].mean()
    pca2_mean = cluster_df['PCA2'].mean()

    # Build plot
    fig = px.scatter(
        cluster_df,
        x="PCA1",
        y="PCA2",
        color="Cluster",
        color_discrete_map=color_map,
        hover_data=["Industry", "AI Adoption Rate (%)", "Human-AI Collaboration Rate (%)", "Consumer Trust in AI (%)"],
        size_max=12,
        template="plotly_white",
        text="Industry"  # <-- Add labels here!
    )

    fig.update_traces(marker=dict(size=12))

    # Add mean lines
    fig.add_shape(type="line",
                  x0=pca1_mean, y0=cluster_df['PCA2'].min(), x1=pca1_mean, y1=cluster_df['PCA2'].max(),
                  line=dict(color="gray", width=1, dash="dot"))
    fig.add_shape(type="line",
                  x0=cluster_df['PCA1'].min(), y0=pca2_mean, x1=cluster_df['PCA1'].max(), y1=pca2_mean,
                  line=dict(color="gray", width=1, dash="dot"))

    # Update label positioning (little offset)
    fig.update_traces(textposition='top center', textfont_size=10)

    # Update layout
    fig.update_layout(
        title="Industry Clustering by AI Behavior (Simulated PCA)",
        xaxis_title="AI Behavior Axis 1 (Adoption + Collaboration)",
        yaxis_title="AI Behavior Axis 2 (Trust + Collaboration)",
        legend_title="Cluster",
        height=650
    )

    # Quadrant labels
    fig.add_annotation(text="High Collaboration & Trust", xref="paper", yref="paper",
                       x=0.95, y=0.95, showarrow=False, font=dict(size=12))
    fig.add_annotation(text="Low Collaboration, High Trust", xref="paper", yref="paper",
                       x=0.05, y=0.95, showarrow=False, font=dict(size=12))
    fig.add_annotation(text="Low Trust & Collaboration", xref="paper", yref="paper",
                       x=0.05, y=0.05, showarrow=False, font=dict(size=12))
    fig.add_annotation(text="High Collaboration, Low Trust", xref="paper", yref="paper",
                       x=0.95, y=0.05, showarrow=False, font=dict(size=12))

    # Show the figure
    plotly(fig)


except Exception as e:
    text(f"🚨 Error creating PCA Clustering Chart: {str(e)}")

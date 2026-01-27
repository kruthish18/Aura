# import gradio as gr

# def analyze_brand(brand_name, content):
#     # Your Madison logic would go here
#     return f"Analysis results for {brand_name}"

# demo = gr.Interface(
#     fn=analyze_brand,
#     inputs=[
#         gr.Textbox(label="Brand Name"),
#         gr.Textbox(label="Brand Content", lines=5)
#     ],
#     outputs=gr.Textbox(label="Analysis Results")
# )

# demo.launch()

# import gradio as gr
# import requests
# import pandas as pd

# # Use your tunnel URL for local testing, or the public HF URL later
# N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/dd898add-0a6e-42ed-b336-4763a6615ca0"

# def analyze_brand(brand_name):
#     try:
#         payload = {"query": brand_name}
#         response = requests.post(N8N_WEBHOOK_URL, json=payload)
        
#         if response.status_code == 200:
#             raw_data = response.json()
#             # Handle the 'Aggregate' node output from your JSON
#             posts = raw_data if isinstance(raw_data, list) else raw_data.get('data', [])
            
#             if not posts:
#                 return pd.DataFrame(), "No data found for this brand."

#             df = pd.DataFrame(posts)
#             # Ensure Upvotes is numeric for the chart
#             df['Upvotes'] = pd.to_numeric(df['Upvotes'], errors='coerce').fillna(0).astype(int)
            
#             # Formatting the table for the UI
#             display_df = df[['Post Title', 'Upvotes', 'User', 'URL']]
#             msg = f"✅ Madison found {len(df)} posts for '{brand_name}'!"
#             return display_df, msg
#         else:
#             return pd.DataFrame(), f"❌ Error: n8n returned status {response.status_code}"
#     except Exception as e:
#         return pd.DataFrame(), f"❌ Connection Failed: {e}"

# # --- Professional Gradio UI ---
# with gr.Blocks(theme=gr.themes.Soft(), title="Madison Brand Intelligence") as demo:
#     gr.Markdown("# 🎯 Madison Brand Intelligence")
#     gr.Markdown("Real-time Reddit analysis for your Madison Agent.")
    
#     with gr.Row():
#         with gr.Column(scale=2):
#             brand_input = gr.Textbox(label="Brand Name", placeholder="e.g., OpenAI", value="OpenAI")
#             analyze_btn = gr.Button("🚀 Run Analysis", variant="primary")
#         with gr.Column(scale=1):
#             status_output = gr.Label(label="Status")

#     with gr.Tabs():
#         with gr.TabItem("📊 Analysis Table"):
#             data_table = gr.DataFrame(label="Latest Mentions", interactive=False)
            
#         with gr.TabItem("📈 Popularity Chart"):
#             trend_plot = gr.BarPlot(
#                 x="User", 
#                 y="Upvotes", 
#                 title="Top Posts by Engagement",
#                 tooltip=["Post Title", "Upvotes"],
#                 label="Engagement Chart"
#             )

#     # Click Event
#     analyze_btn.click(
#         fn=analyze_brand,
#         inputs=brand_input,
#         outputs=[data_table, status_output]
#     )
    
#     # Sync the chart with the table automatically
#     data_table.change(
#         fn=lambda df: df,
#         inputs=data_table,
#         outputs=trend_plot
#     )

# if __name__ == "__main__":
#     demo.launch()





import gradio as gr
import requests
import pandas as pd

# Use your tunnel URL for local or the public URL for HuggingFace
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/dd898add-0a6e-42ed-b336-4763a6615ca0"

def analyze_brand(brand_name):
    try:
        payload = {"query": brand_name}
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        
        if response.status_code == 200:
            raw_data = response.json()
            posts = raw_data if isinstance(raw_data, list) else raw_data.get('data', [])
            
            if not posts:
                return pd.DataFrame(), "0", "0", "0", "No data found."

            df = pd.DataFrame(posts)
            df['Upvotes'] = pd.to_numeric(df['Upvotes'], errors='coerce').fillna(0).astype(int)
            
            # Calculating Metrics
            total_mentions = str(len(df))
            highest_ups = str(df['Upvotes'].max())
            avg_eng = str(int(df['Upvotes'].mean()))
            status = f"✅ Madison found {total_mentions} results!"
            
            return df[['Post Title', 'Upvotes', 'User', 'URL']], total_mentions, highest_ups, avg_eng, status
        else:
            return pd.DataFrame(), "0", "0", "0", f"Error: {response.status_code}"
    except Exception as e:
        return pd.DataFrame(), "0", "0", "0", f"Connection Failed: {e}"

# --- Custom CSS for Streamlit Look ---
css = """
.metric-card { text-align: center; padding: 20px; border-radius: 10px; background: #f0f2f6; border: 1px solid #e6e9ef; }
.metric-value { font-size: 24px; font-weight: bold; color: #ff4b4b; }
.metric-label { font-size: 14px; color: #555; }
"""

with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎯 Madison Brand Intelligence")
    
    with gr.Row():
        # Sidebar-style Column
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("### 🔍 Search Settings")
            brand_input = gr.Textbox(label="Brand/Topic", value="OpenAI")
            analyze_btn = gr.Button("Run Analysis", variant="primary")
            status_msg = gr.Markdown("Ready to analyze.")

        # Main Dashboard Column
        with gr.Column(scale=3):
            # Metric Cards Row (Mimicking st.metric)
            with gr.Row():
                with gr.Column(elem_classes="metric-card"):
                    gr.Markdown("<div class='metric-label'>Total Mentions</div>")
                    m_total = gr.Markdown("<div class='metric-value'>0</div>")
                with gr.Column(elem_classes="metric-card"):
                    gr.Markdown("<div class='metric-label'>Highest Upvotes</div>")
                    m_high = gr.Markdown("<div class='metric-value'>0</div>")
                with gr.Column(elem_classes="metric-card"):
                    gr.Markdown("<div class='metric-label'>Avg Engagement</div>")
                    m_avg = gr.Markdown("<div class='metric-value'>0</div>")
            
            gr.Markdown("### 📊 Brand Mentions")
            data_table = gr.DataFrame(interactive=False)
            
            with gr.Tab("📈 Popularity Chart"):
                trend_plot = gr.BarPlot(x="User", y="Upvotes", title="Engagement by User")

    # Mapping Events
    analyze_btn.click(
        fn=analyze_brand,
        inputs=brand_input,
        outputs=[data_table, m_total, m_high, m_avg, status_msg]
    )
    
    # Update chart when table data changes
    data_table.change(fn=lambda df: df, inputs=data_table, outputs=trend_plot)

demo.launch()
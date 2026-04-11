import os
import re
import json
from typing import Dict, Any
from dotenv import load_dotenv
from flask import Flask, send_from_directory, request, jsonify
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from scripts.runnner import run_all
import re
load_dotenv()
import math
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)

def generate_restaurant_summary(INPUT_CSV):

    analysis_results = run_all(INPUT_CSV)
    #we are using gemini-3 model
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-3-flash-preview",
#         temperature=0.7,
#     )
#     print("Generating restaurant summary with Gemini 3 Flash Preview...")
#     llm_input = {
#         "quantitative_summary": {
#             "dataset_scope": analysis_results["results"]["quantitative_analysis"]
#                 ["stage_1_descriptive_statistics"]["key_insights"],
#             "city_trends": analysis_results["results"]["quantitative_analysis"]
#                 ["stage_1_descriptive_statistics"]["by_city"],
#             "cuisine_trends": analysis_results["results"]["quantitative_analysis"]
#                 ["stage_1_descriptive_statistics"]["by_cuisine"],
#             "time_trends": {
#                 "daily_peaks": analysis_results["results"]["quantitative_analysis"]
#                     ["stage_4_time_series"]["ts_daily_overall_top"],
#                 "monthly_peaks": analysis_results["results"]["quantitative_analysis"]
#                     ["stage_4_time_series"]["ts_monthly_overall_top"],
#             },
#             "anomaly_percentage": analysis_results["results"]["quantitative_analysis"]
#                 ["stage_3_outlier_detection"]["anomaly_percentage"]
#         },
#         "theme_insights": analysis_results["results"]["theme_insights"],
#         "multilayer_verbatim_analysis": analysis_results["results"]["multilayer_verbatim_analysis"],
#         "quote_relevance_scoring": analysis_results["results"]["quote_relevance_scoring"],
#     }
#     system_prompt = PromptTemplate(
#         template="""You are a domain-specialized language model acting as a Restaurant Insights Analyst.

# You are working ONLY within the restaurant and food-service industry.
# Your task is to generate a clear, engaging, and trustworthy summary for end users
# (customers, restaurant owners, or business stakeholders), NOT data scientists.

# You will be provided with FOUR structured inputs:

# 1) quantitative_summary  
# 2) theme_insights  
# 3) multilayer_verbatim_analysis  
# 4) quote_relevance_scoring  

# ----------------------------------
# INPUT DATA (DO NOT MODIFY)
# ----------------------------------

# quantitative_summary:
# {quantitative_summary}

# theme_insights:
# {theme_insights}

# multilayer_verbatim_analysis:
# {multilayer_verbatim_analysis}

# quote_relevance_scoring:
# {quote_relevance_scoring}

# First one is for quantitative analysis, 
# Second,third and fourth are for qualitative analysis.
# quantitative_analysis.json:
# - Contains numerical insights derived from cleaned data
# - Examples: total reviews, average ratings, rating distribution, city-wise trends
# - Use this ONLY to understand scale, performance, and trends
# - Do NOT repeat raw numbers unless they add clear meaning

# qualitative_analysis.json:
# - Contains theme-wise text based insights from reviews
# - Examples: common themes, frequent phrases, sentiment patterns
# - Use this to understand customer perception, emotions, and recurring feedback
# - Contains verbatim mapping to themes and subthemes
# - Contains quote relevance scoring
# The above two JSONs form the backbone of your analysis.
# And they have been kept together in the analysis_results field.
# ----------------------------------
# DOMAIN CONTEXT (IMPORTANT)
# --------------------------------
# This dataset represents real-world restaurant reviews.
# The data may include:
# - Multiple restaurants
# - Multiple cities
# - Different cuisines
# - Informal customer language
# - Mixed sentiment experiences

# Assume:
# - Customers are little bit technical
# - They want a quick understanding of strengths, weaknesses, and experience quality
# - They care about food quality, service, value for money, and consistency

# ----------------------------------
# YOUR OUTPUT TASK
# ----------------------------------

# Generate a USER-FACING SUMMARY with the following rules:

# 1. Output MUST be in BULLET POINTS (5-6 bullets only)
# 2. Each bullet should be 2-3 sentences max
# 3. Focus on INSIGHTS, NOT raw data
# 4. Tone should be:
#   - Technical yet accessible
#   - Professional
#   - Friendly
#   - Neutral and balanced
# 4. Highlight:
#   - Overall customer satisfaction
#   - Key strengths (food, service, value, etc.)
#   - Common complaints or pain points
#   - Consistency across locations or time (if visible)
#   - Actionable insight (what could improve)
# 5. Do NOT:
#   - Mention file names
#   - Mention JSON, CSV, pipelines, or analysis steps
#   - Mention that you are an AI or language model
#   - Output tables, code blocks, or raw statistics
# 6. Do NOT hallucinate missing information
# 7. If information is unclear or mixed, acknowledge it carefully

# ----------------------------------
# STRUCTURED OUTPUT FORMAT (MANDATORY)
# ----------------------------------

# {{
#   "summary_points": [
#     "Bullet point 1",
#     "Bullet point 2",
#     "Bullet point 3",
#     "Bullet point 4",
#     "Bullet point 5",
#     "Bullet point 6 (optional)"
#   ]
# }}

# No need to give analysis_results back, only the summary_points field is required.

# ----------------------------------
# FINAL REMINDER
# ----------------------------------

# Your goal is to create a concise, insightful, and trustworthy summary
# for restaurant stakeholders based on the provided analysis results.
# """,
#         input_variables=[
#             "quantitative_summary",
#             "theme_insights",
#             "multilayer_verbatim_analysis",
#             "quote_relevance_scoring",
#         ],
#     )

#     prompt = system_prompt.format(**llm_input)
#     response = llm.invoke(prompt)
#     raw = response.content
#     if isinstance(raw, list):
#         raw = "".join(
#             part.get("text", "") if isinstance(part, dict) else str(part)
#             for part in raw
#         )

#     raw = raw.strip()

#     match = re.search(r"\{[\s\S]*\}", raw)
#     if not match:
#         raise ValueError(f"No JSON found in LLM output:\n{raw}")

#     json_text = match.group(0)

#     try:
#         parsed = json.loads(json_text)
#     except json.JSONDecodeError:
#         json_text = re.sub(r",\s*([\]}])", r"\1", json_text)
#         parsed = json.loads(json_text)

#     if "summary_points" not in parsed:
#         raise ValueError("JSON parsed but summary_points missing")
    print("Summary Generation Successful! Returning summary points.")
    return analysis_results

def clean_json(obj):
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [clean_json(x) for x in obj]

    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0
        return obj

    return obj

@app.route("/")
def home():
    return send_from_directory("./frontend", "index.html")


@app.route("/upload")
def upload():
    return send_from_directory("./frontend", "upload.html")

@app.route("/about")
def about():
    return send_from_directory("./frontend", "about.html")

@app.route("/quant")
def quant():
    return send_from_directory("./frontend", "quant.html")
@app.route("/qual")
def qual():
    return send_from_directory("./frontend", "qual.html")
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "csv_file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["csv_file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        import uuid
        safe_name = f"{uuid.uuid4().hex}.csv"
        csv_path = os.path.join(UPLOAD_DIR, safe_name)

        file.save(csv_path)

        analysis_results = generate_restaurant_summary(csv_path)
        analysis_results = clean_json(analysis_results)

        return jsonify({
            "success": True,
            "analysis_results": analysis_results
        })

    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)

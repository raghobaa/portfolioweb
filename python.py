from flask import Flask, render_template, request
import pdfplumber
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="AIzaSyDv3zVBjzVttDt1lx36M5KO9oopKhG6SDg")
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Hardcoded resume path
PDF_PATH = "/Users/raghav/Desktop/rajaprerak.github.io-master/myresumemain (1).pdf"

def extract_text_from_pdf(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text.append(content)
    return "\n".join(text)

pdf_text = extract_text_from_pdf(PDF_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        prompt = f"""Context from Resume:\n{pdf_text}\n\nQuestion: {question}\n\nAnswer:"""
        try:
            response = model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = f"Error: {str(e)}"
    return render_template("python.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AQ_TOKEN = "AQ.Ab8RN6J37By9Q1sisuJPiVyx42IWeo9W0iLIRpmCDvJZzsFQLg"

@app.route('/ask', methods=['POST'])
def ask_gemini():
    data = request.get_json()
    user_query = data.get('query', '')
    system_prompt = data.get('system_prompt', '')

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AQ_TOKEN}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    gemini_data = {
        "contents": [{
            "parts": [
                {"text": f"System Instruction: {system_prompt}\n\nUser: {user_query}"}
            ]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=gemini_data)
        print("Google API Status Code:", response.status_code)
        print("Google API Response Text:", response.text)
        
        if response.status_code == 200:
            res_json = response.json()
            ai_reply = res_json['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply})
        else:
            return jsonify({"reply": "ချိတ်ဆက်မှု အဆင်မပြေပါဘူး နော်..."}), 500
    except Exception as e:
        print("Exception Error:", str(e))
        return jsonify({"reply": "Error ဖြစ်သွားပါတယ်..."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# In-memory defect database for demonstration
defects = [
    {
        "id": 101,
        "title": "Payment gateway timeout on checkout",
        "description": "User gets stuck on spinner when clicking pay button.",
        "module": "Payments",
        "severity": "Critical",
        "priority": "High",
        "type": "Backend",
        "status": "In Progress",
        "reporter": "Alice (QA)",
        "assignee": "Bob (Dev)",
        "created_at": "2026-03-01",
        "prevention_note": "Implement retry mechanism and log network timeouts."
    },
    {
        "id": 102,
        "title": "Broken layout on mobile view",
        "description": "Navigation bar overlaps header on screen width < 600px.",
        "module": "UI/Frontend",
        "severity": "Minor",
        "priority": "Low",
        "type": "UI",
        "status": "New",
        "reporter": "Charlie (QA)",
        "assignee": "Unassigned",
        "created_at": "2026-03-03",
        "prevention_note": ""
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/defects', methods=['GET'])
def get_defects():
    return jsonify(defects)

@app.route('/api/defects', methods=['POST'])
def create_defect():
    data = request.json
    new_defect = {
        "id": len(defects) + 101,
        "title": data.get("title"),
        "description": data.get("description"),
        "module": data.get("module"),
        "severity": data.get("severity"),
        "priority": data.get("priority"),
        "type": data.get("type"),
        "status": "New",
        "reporter": data.get("reporter", "QA Tester"),
        "assignee": "Unassigned",
        "created_at": datetime.date.today().strftime("%Y-%m-%d"),
        "prevention_note": data.get("prevention_note", "")
    }
    defects.append(new_defect)
    return jsonify({"message": "Defect logged successfully!", "defect": new_defect}), 201

@app.route('/api/defects/<int:defect_id>', methods=['PATCH'])
def update_defect(defect_id):
    data = request.json
    for d in defects:
        if d['id'] == defect_id:
            d['status'] = data.get('status', d['status'])
            d['assignee'] = data.get('assignee', d['assignee'])
            d['prevention_note'] = data.get('prevention_note', d['prevention_note'])
            return jsonify({"message": "Defect updated successfully!", "defect": d})
    return jsonify({"error": "Defect not found"}), 404

@app.route('/api/analytics', methods=['GET'])
def analytics():
    # Prediction and reporting metrics
    total = len(defects)
    by_severity = {"Critical": 0, "Major": 0, "Minor": 0}
    by_status = {"New": 0, "In Progress": 0, "Fixed": 0, "Closed": 0}
    by_module = {}

    for d in defects:
        by_severity[d['severity']] = by_severity.get(d['severity'], 0) + 1
        by_status[d['status']] = by_status.get(d['status'], 0) + 1
        by_module[d['module']] = by_module.get(d['module'], 0) + 1

    # Simple Defect Prediction Risk Indicator: High defect count in a module = High Risk
    risky_module = max(by_module, key=by_module.get) if by_module else "None"

    return jsonify({
        "total": total,
        "by_severity": by_severity,
        "by_status": by_status,
        "by_module": by_module,
        "prediction_risk": f"Module '{risky_module}' has the highest defect concentration and requires extra regression testing."
    })

if __name__ == '__main__':
    app.run(debug=True)
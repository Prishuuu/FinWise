from flask import Flask, render_template, request


import math

app = Flask(__name__)

# ---------- Utility Function for Salary Breakdown ----------
def calculate_salary(ctc, mode='auto', data=None):
    # If automatic, calculate basic and other components as before
    if mode == 'auto' or not data:
        basic = 0.4 * ctc
        hra = 0.4 * basic
        travel = 19200
        special = ctc - (basic + hra + travel)
        pf = 0.12 * basic
        gratuity = 0.0481 * basic
        extra_name = None
        extra_value = 0.0
    else:
        # Manual mode: get values from form, convert to float, default 0 if missing
        def get_val(key):
            try:
                return float(data.get(key, 0))
            except:
                return 0

        basic = 0.4 * ctc  # keep basic as 40% of CTC (or optionally allow manual input if needed)
        hra = get_val('hra')
        special = get_val('special')
        travel = get_val('travel')
        pf = get_val('pf')
        gratuity = get_val('gratuity')
        extra_name = data.get('extra_component_name', '').strip()
        extra_value = get_val('extra_component_value')

    # Calculate total deductions and taxable income for tax calculation
    # Annual taxable income = CTC - PF - Gratuity - Extra component (if deductible)
    # Assuming extra component is taxable and part of CTC, so included in taxable income

    # Total salary components sum (basic + hra + special + travel + extra)
    total_components = basic + hra + special + travel + extra_value

    # To be safe, if total_components > ctc, adjust special allowance downward
    if total_components > ctc:
        special = max(0, ctc - (basic + hra + travel + extra_value))

    # Annual taxable income calculation
    annual_taxable = ctc - pf - gratuity

    # Income tax slabs FY 2025 (assumed)
    tax = 0
    slabs = [
        (0, 300000, 0),
        (300001, 600000, 0.05),
        (600001, 900000, 0.1),
        (900001, 1200000, 0.15),
        (1200001, 1500000, 0.2),
        (1500001, float('inf'), 0.3)
    ]

    for lower, upper, rate in slabs:
        if annual_taxable > lower:
            taxable_amount = min(annual_taxable, upper) - lower
            tax += taxable_amount * rate

    # Calculate annual and monthly in-hand salary
    in_hand_annual = ctc - (pf + gratuity + tax)
    in_hand_monthly = in_hand_annual / 12

    # Prepare result dictionary
    result = {
        "Basic Salary": round(basic, 2),
        "HRA": round(hra, 2),
        "Special Allowance": round(special, 2),
        "Travel Allowance": round(travel, 2),
        "Provident Fund (EPF)": round(pf, 2),
        "Gratuity": round(gratuity, 2),
        "Income Tax": round(tax, 2),
        "Monthly In-Hand Salary": round(in_hand_monthly, 2),
        "Annual In-Hand Salary": round(in_hand_annual, 2)
    }

    if extra_name and extra_value > 0:
        result[extra_name] = round(extra_value, 2)

    return result


# ---------- Routes ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    result = {}
    if request.method == 'POST':
        ctc = float(request.form['ctc'])
        mode = request.form.get('mode', 'auto')
        result = calculate_salary(ctc, mode, request.form)
    return render_template('calculate.html', result=result)

@app.route('/growth', methods=['GET', 'POST'])
def growth():
    result = {}
    color = ""
    message = ""
    if request.method == 'POST':
        old_ctc = float(request.form['old_ctc'])
        new_ctc = float(request.form['new_ctc'])
        difference = new_ctc - old_ctc
        growth_percent = ((difference) / old_ctc) * 100 if old_ctc else 0.0

        if difference > 0:
            color = "text-success"
            message = "🎉 Great! You're growing financially. Keep it up!"
        elif difference < 0:
            color = "text-danger"
            message = "🔻 A dip in CTC — but remember, comebacks are stronger than setbacks!"
        else:
            color = "text-primary"
            message = "➖ Stable CTC. Let’s aim for growth next year!"

        result = {
            'Old CTC': old_ctc,
            'New CTC': new_ctc,
            'Difference': difference,
            'Growth (%)': round(growth_percent, 2)
        }
    return render_template('growth.html', result=result, color=color, message=message)

@app.route('/savings', methods=['GET', 'POST'])
def savings():
    result = {}
    if request.method == 'POST':
        in_hand_salary = float(request.form['in_hand'])
        expenses = float(request.form['expenses'])
        monthly_savings = in_hand_salary - expenses
        annual_savings = monthly_savings * 12

        saving_ratio = monthly_savings / in_hand_salary if in_hand_salary > 0 else 0

        if saving_ratio >= 0.5:
            color = 'text-success'
            message = "Excellent saving habits! You're on the right path. 💰"
        elif saving_ratio >= 0.2:
            color = 'text-primary'
            message = "Good job, aim for more consistent saving. 📈"
        else:
            color = 'text-danger'
            message = "Consider reducing expenses to save more. ⚠️"

        result = {
            'Monthly Savings': round(monthly_savings, 2),
            'Annual Savings': round(annual_savings, 2),
            'Color': color,
            'Message': message
        }
    return render_template('savings.html', result=result)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/expense-tracker', methods=['GET', 'POST'])
def expense_tracker():
    data = {}
    chart_data = {}
    message = ""
    if request.method == 'POST':
        # Expecting expense categories and amounts from form
        categories = request.form.getlist('category[]')
        amounts = request.form.getlist('amount[]')
        
        # Prepare data dictionary filtering valid entries
        data = {cat: float(amt) if amt else 0 for cat, amt in zip(categories, amounts) if cat.strip()}

        if data:
            total_expense = sum(data.values())
            message = f"Total Monthly Expenses: ₹{total_expense:.2f}"
            chart_data = data

    return render_template('expense_tracker.html', data=data, chart_data=chart_data, message=message)



# ---------- Run the app ----------
if __name__ == '__main__':
    app.run(debug=True)

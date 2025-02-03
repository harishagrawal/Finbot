import pytest
from flask import Flask, request

app = Flask(__name__)

def financial_health():
    if request.method == 'POST':
        # Get form data
        monthly_income = float(request.form['monthly_income'])
        savings_percentage = float(request.form['savings_percentage'])
        emergency_fund = request.form['emergency_fund']
        funds_invested = request.form['funds_invested']
        investment_type = request.form.get('investment_type', 'None')
        expected_return = float(request.form['expected_return'])
        monthly_variance = float(request.form['monthly_variance'])
        has_loans = request.form['has_loans']
        if request.form['monthly_loan_payment']:
            monthly_loan_payment = float(request.form.get('monthly_loan_payment', 0))
        else:
            monthly_loan_payment = 0
        if request.form.get('outstanding_loan'):
            outstanding_loan = float(request.form.get('outstanding_loan', 0))
        else:
            outstanding_loan = 0

        # Calculate metrics
        monthly_savings = monthly_income * (savings_percentage / 100)
        monthly_expenditure = monthly_income - monthly_savings
        # Calculate loan-to-income ratio
        if monthly_loan_payment > 0:
            loan_to_income_ratio = (monthly_loan_payment / monthly_income) * 100
        else:
            loan_to_income_ratio = 0
        # Calculate loan-to-savings ratio
        if monthly_savings > 0:
            loan_to_savings_ratio = outstanding_loan / monthly_savings
        else:
            loan_to_savings_ratio = 0
        # Calculate variance percentage
        if monthly_expenditure > 0:
            variance_percentage = (monthly_variance / monthly_expenditure) * 100
        else:
            variance_percentage = 0

        # Calculate score (0-10)
        score = 10  # Start with perfect score and deduct based on factors

        # Emergency fund check
        if emergency_fund == 'no':
            score -= 2

        # Investment check
        if funds_invested == 'no':
            score -= 1.5

        # Loan burden check
        if loan_to_income_ratio > 40:
            score -= 2
        elif loan_to_income_ratio > 30:
            score -= 1

        if loan_to_savings_ratio > 60:
            score -= 2

        # Expenditure variance check
        if variance_percentage > 20:
            score -= 1.5

        # Savings check
        if savings_percentage < 20:
            score -= 1

        # Ensure score stays within 0-10 range
        score = max(0, min(10, score))

        # Prepare analysis results
        analysis = {
            'monthly_savings': monthly_savings,
            'monthly_expenditure': monthly_expenditure,
            'loan_to_income_ratio': loan_to_income_ratio,
            'variance_percentage': variance_percentage,
            'score': round(score, 1)
        }
        if monthly_loan_payment > 0:
            analysis['monthly_loan_payment'] = monthly_loan_payment

        return render_template('result-nochart.html', analysis=analysis)

    return render_template('form.html')

class Test_FinancialHealthFinancialHealth:
    @pytest.mark.valid
    @pytest.mark.smoke
    def test_financial_health_no_loans(self):
        with app.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '20',
            'emergency_fund': 'yes',
            'funds_invested': 'yes',
            'investment_type': 'stocks',
            'expected_return': '8',
            'monthly_variance': '500',
            'has_loans': 'no',
            'monthly_loan_payment': '0',
            'outstanding_loan': '0'
        }):
            response = financial_health()
            analysis = response[1]['analysis']
            assert analysis['monthly_savings'] == 1000
            assert analysis['monthly_expenditure'] == 4000
            assert analysis['loan_to_income_ratio'] == 0
            assert analysis['variance_percentage'] == 12.5
            assert analysis['score'] == 10

    @pytest.mark.valid
    @pytest.mark.regression
    def test_financial_health_high_loan_burden(self):
        with app.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '10',
            'emergency_fund': 'yes',
            'funds_invested': 'yes',
            'investment_type': 'bonds',
            'expected_return': '5',
            'monthly_variance': '300',
            'has_loans': 'yes',
            'monthly_loan_payment': '2500',
            'outstanding_loan': '50000'
        }):
            response = financial_health()
            analysis = response[1]['analysis']
            assert analysis['monthly_savings'] == 500
            assert analysis['monthly_expenditure'] == 4500
            assert analysis['loan_to_income_ratio'] == 50
            assert analysis['loan_to_savings_ratio'] == 100
            assert analysis['variance_percentage'] == 6.67
            assert analysis['score'] == 5.5

    @pytest.mark.valid
    @pytest.mark.regression
    def test_financial_health_no_emergency_fund(self):
        with app.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '6000',
            'savings_percentage': '25',
            'emergency_fund': 'no',
            'funds_invested': 'yes',
            'investment_type': 'real_estate',
            'expected_return': '10',
            'monthly_variance': '400',
            'has_loans': 'no',
            'monthly_loan_payment': '0',
            'outstanding_loan': '0'
        }):
            response = financial_health()
            analysis = response[1]['analysis']
            assert analysis['monthly_savings'] == 1500
            assert analysis['monthly_expenditure'] == 4500
            assert analysis['loan_to_income_ratio'] == 0
            assert analysis['variance_percentage'] == 8.89
            assert analysis['score'] == 8

    @pytest.mark.valid
    @pytest.mark.regression
    def test_financial_health_high_variance(self):
        with app.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '7000',
            'savings_percentage': '15',
            'emergency_fund': 'yes',
            'funds_invested': 'no',
            'investment_type': 'None',
            'expected_return': '0',
            'monthly_variance': '2000',
            'has_loans': 'no',
            'monthly_loan_payment': '0',
            'outstanding_loan': '0'
        }):
            response = financial_health()
            analysis = response[1]['analysis']
            assert analysis['monthly_savings'] == 1050
            assert analysis['monthly_expenditure'] == 5950
            assert analysis['loan_to_income_ratio'] == 0
            assert analysis['variance_percentage'] == 33.61
            assert analysis['score'] == 7.5

    @pytest.mark.valid
    @pytest.mark.regression
    def test_financial_health_no_investments(self):
        with app.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '8000',
            'savings_percentage': '30',
            'emergency_fund': 'yes',
            'funds_invested': 'no',
            'investment_type': 'None',
            'expected_return': '0',
            'monthly_variance': '600',
            'has_loans': 'no',
            'monthly_loan_payment': '0',
            'outstanding_loan': '0'
        }):
            response = financial_health()
            analysis = response[1]['analysis']
            assert analysis['monthly_savings'] == 2400
            assert analysis['monthly_expenditure'] == 5600
            assert analysis['loan_to_income_ratio'] == 0
            assert analysis['variance_percentage'] == 10.71
            assert analysis['score'] == 8.5

    @pytest.mark.valid
    @pytest.mark.regression
    def test_financial_health_minimal_savings(self):
        with app.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '9000',
            'savings_percentage': '5',
            'emergency_fund': 'yes',
            'funds_invested': 'yes',
            'investment_type': 'mutual_funds',
            'expected_return': '7',
            'monthly_variance': '700',
            'has_loans': 'no',
            'monthly_loan_payment': '0',
            'outstanding_loan': '0'
        }):
            response = financial_health()
            analysis = response[1]['analysis']
            assert analysis['monthly_savings'] == 450
            assert analysis['monthly_expenditure'] == 8550
            assert analysis['loan_to_income_ratio'] == 0
            assert analysis['variance_percentage'] == 8.19
            assert analysis['score'] == 8

    @pytest.mark.valid
    @pytest.mark.regression
    def test_financial_health_all_deductions(self):
        with app.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '4000',
            'savings_percentage': '10',
            'emergency_fund': 'no',
            'funds_invested': 'no',
            'investment_type': 'None',
            'expected_return': '0',
            'monthly_variance': '1000',
            'has_loans': 'yes',
            'monthly_loan_payment': '2000',
            'outstanding_loan': '40000'
        }):
            response = financial_health()
            analysis = response[1]['analysis']
            assert analysis['monthly_savings'] == 400
            assert analysis['monthly_expenditure'] == 3600
            assert analysis['loan_to_income_ratio'] == 50
            assert analysis['loan_to_savings_ratio'] == 100
            assert analysis['variance_percentage'] == 27.78
            assert analysis['score'] == 2

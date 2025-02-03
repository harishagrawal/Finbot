import pytest
from flask import Flask, request
from financial_health import financial_health

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestFinancialHealthFinancialHealth:

    def test_perfect_financial_health_score(self, client):
        with client.application.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '30',
            'emergency_fund': 'yes',
            'funds_invested': 'yes',
            'investment_type': 'stocks',
            'expected_return': '7',
            'monthly_variance': '100',
            'has_loans': 'no',
            'monthly_loan_payment': '',
            'outstanding_loan': ''
        }):
            response = financial_health()
            assert 'analysis' in response.get_data(as_text=True)
            assert '"score": 10.0' in response.get_data(as_text=True)

    def test_no_emergency_fund_impact(self, client):
        with client.application.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '30',
            'emergency_fund': 'no',
            'funds_invested': 'yes',
            'investment_type': 'stocks',
            'expected_return': '7',
            'monthly_variance': '100',
            'has_loans': 'no',
            'monthly_loan_payment': '',
            'outstanding_loan': ''
        }):
            response = financial_health()
            assert 'analysis' in response.get_data(as_text=True)
            assert '"score": 8.0' in response.get_data(as_text=True)

    def test_high_loan_to_income_ratio(self, client):
        with client.application.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '30',
            'emergency_fund': 'yes',
            'funds_invested': 'yes',
            'investment_type': 'stocks',
            'expected_return': '7',
            'monthly_variance': '100',
            'has_loans': 'yes',
            'monthly_loan_payment': '2100',
            'outstanding_loan': '100000'
        }):
            response = financial_health()
            assert 'analysis' in response.get_data(as_text=True)
            assert '"score": 8.0' in response.get_data(as_text=True)
            assert '"loan_to_income_ratio": 42.0' in response.get_data(as_text=True)

    def test_low_savings_percentage(self, client):
        with client.application.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '15',
            'emergency_fund': 'yes',
            'funds_invested': 'yes',
            'investment_type': 'stocks',
            'expected_return': '7',
            'monthly_variance': '100',
            'has_loans': 'no',
            'monthly_loan_payment': '',
            'outstanding_loan': ''
        }):
            response = financial_health()
            assert 'analysis' in response.get_data(as_text=True)
            assert '"score": 9.0' in response.get_data(as_text=True)
            assert '"monthly_savings": 750.0' in response.get_data(as_text=True)

    def test_high_expenditure_variance(self, client):
        with client.application.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '30',
            'emergency_fund': 'yes',
            'funds_invested': 'yes',
            'investment_type': 'stocks',
            'expected_return': '7',
            'monthly_variance': '800',
            'has_loans': 'no',
            'monthly_loan_payment': '',
            'outstanding_loan': ''
        }):
            response = financial_health()
            assert 'analysis' in response.get_data(as_text=True)
            assert '"score": 8.5' in response.get_data(as_text=True)
            assert '"variance_percentage": 22.86' in response.get_data(as_text=True)

    def test_multiple_factors_affecting_score(self, client):
        with client.application.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '15',
            'emergency_fund': 'no',
            'funds_invested': 'no',
            'investment_type': 'none',
            'expected_return': '0',
            'monthly_variance': '800',
            'has_loans': 'yes',
            'monthly_loan_payment': '2100',
            'outstanding_loan': '100000'
        }):
            response = financial_health()
            assert 'analysis' in response.get_data(as_text=True)
            assert '"score": 2.0' in response.get_data(as_text=True)

    def test_zero_income_edge_case(self, client):
        with client.application.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '0',
            'savings_percentage': '0',
            'emergency_fund': 'no',
            'funds_invested': 'no',
            'investment_type': 'none',
            'expected_return': '0',
            'monthly_variance': '0',
            'has_loans': 'no',
            'monthly_loan_payment': '',
            'outstanding_loan': ''
        }):
            response = financial_health()
            assert 'analysis' in response.get_data(as_text=True)
            assert '"score": 5.5' in response.get_data(as_text=True)

    def test_loan_to_savings_ratio_impact(self, client):
        with client.application.test_request_context('/financial_health', method='POST', data={
            'monthly_income': '5000',
            'savings_percentage': '20',
            'emergency_fund': 'yes',
            'funds_invested': 'yes',
            'investment_type': 'stocks',
            'expected_return': '7',
            'monthly_variance': '100',
            'has_loans': 'yes',
            'monthly_loan_payment': '1000',
            'outstanding_loan': '60000'
        }):
            response = financial_health()
            assert 'analysis' in response.get_data(as_text=True)
            assert '"score": 8.0' in response.get_data(as_text=True)

    # Additional test for GET request
    def test_get_request(self, client):
        with client.application.test_request_context('/financial_health', method='GET'):
            response = financial_health()
            assert 'form.html' in response.get_data(as_text=True)


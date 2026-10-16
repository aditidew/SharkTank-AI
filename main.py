from openai import OpenAI
import requests
import certifi
import ssl
import httpx
 
# ==========================
# YOUR API KEY
# ==========================
 
API_KEY = "wHzWj2P0vy3cCINHg1kDL3PaVRP0osAq5t6c2G1c"
 
# ==========================
# SSL / NETWORK DIAGNOSTICS
# ==========================
 
print("=" * 50)
print("SSL DIAGNOSTICS")
print("=" * 50)
 
print("OpenSSL Version:")
print(ssl.OPENSSL_VERSION)
 
print("\nCertifi Bundle:")
print(certifi.where())
 
print("\nTesting HTTPS connectivity...")
 
try:
    r = requests.get("https://openai.generative.engine.capgemini.com/v1", timeout=10)
    print("SUCCESS")
    print("Status Code:", r.status_code)
except Exception as e:
    print("FAILED")
    print(type(e))
    print(e)
 
# ==========================
# OPENAI CLIENT
# ==========================
 
ssl_context = ssl.create_default_context(
    cafile=certifi.where()
)
 
http_client = httpx.Client(
    verify=ssl_context,
    timeout=60.0
)
 
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openai.generative.engine.capgemini.com/v1",
    http_client=http_client
)
 
# ==========================
# TEST OPENAI CONNECTION
# ==========================
 
try:
    print("\nFetching available models...")
 
    models = client.models.list()
 
    # print("\nAVAILABLE MODELS:")
    # for model in models.data:
    #         print(model.id)
 
    print("Connected successfully!")
    print("Number of models returned:", len(models.data))
 
except Exception as e:
    print("\nFailed to connect to OpenAI")
    print(type(e))
    print(e)
    raise
 
# ==========================
# IMPORT AGENTS
# ==========================
 
from finance_agent import FinanceAgent
from market_agent import MarketAgent
from legal_agent import LegalAgent
from aggregator import SharkAggregator
 
# ==========================
# INPUT STARTUP IDEA
# ==========================
 
startup_idea = """
We are building an AI-powered hiring platform
that conducts voice interviews and automatically
screens candidates for recruiters.
 
Customers:
HR teams and recruitment agencies.
 
Business Model:
Monthly SaaS subscription.
"""
 
# ==========================
# CREATE AGENTS
# ==========================
 
finance_agent = FinanceAgent(client)
market_agent = MarketAgent(client)
legal_agent = LegalAgent(client)
 
# ==========================
# RUN ANALYSIS
# ==========================
 
print("\nRunning Finance Analysis...")
finance_result = finance_agent.evaluate(startup_idea)
 
print("\nRunning Market Analysis...")
market_result = market_agent.evaluate(startup_idea)
 
print("\nRunning Legal Analysis...")
legal_result = legal_agent.evaluate(startup_idea)
 
# ==========================
# AGGREGATE RESULTS
# ==========================
 
aggregator = SharkAggregator()
 
final_result = aggregator.aggregate(
    finance_result,
    market_result,
    legal_result
)
 
# ==========================
# OUTPUT
# ==========================
 
print("\n" + "=" * 50)
print("FINAL SHARK TANK VERDICT")
print("=" * 50)
 
print(final_result)
 
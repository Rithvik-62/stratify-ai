import os
import sys
import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from utils import print_banner, print_trace

# Reconfigure stdout/stderr for UTF-8 support on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Load Data
sales_df = pd.read_csv("Master_Sales.csv")
product_df = pd.read_csv("Product_master.csv")

# Merge Data
merged_df = sales_df.merge(
    product_df,
    on="Product_ID"
)

@tool
def total_sales() -> str:
    """Get the absolute total sales across all transactions.
    Use this when the user asks for total sales, overall revenue, or total income from sales.
    """
    return str(merged_df["Sales"].sum())

@tool
def total_profit() -> str:
    """Get the absolute total profit across all transactions.
    Use this when the user asks for total profit, net gain, or overall profitability.
    """
    return str(merged_df["Profit"].sum())

@tool
def sales_by_category() -> str:
    """Get a detailed breakdown of sales grouped by category.
    Use this when the user asks for sales by category, which category performs best in sales, or distribution of sales across categories.
    """
    result = (
        merged_df
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )
    return result.to_string()

@tool
def profit_by_category() -> str:
    """Get a detailed breakdown of profit grouped by category.
    Use this when the user asks for profit by category, which category is most profitable, or distribution of profits across categories.
    """
    result = (
        merged_df
        .groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )
    return result.to_string()

@tool
def sales_by_segment() -> str:
    """Get a detailed breakdown of sales grouped by segment (e.g., Consumer, Corporate, Home Office).
    Use this when the user asks for sales by segment, segment-wise revenue, or how sales are distributed across customer segments.
    """
    result = (
        merged_df
        .groupby("Segment")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )
    return result.to_string()

# Gather all tools
tools = [total_sales, total_profit, sales_by_category, profit_by_category, sales_by_segment]

SYSTEM_PROMPT = (
    "You are a premium Sales & Business Analytics AI Agent. "
    "Your goal is to answer complex business questions using the provided tools, "
    "perform detailed analytics, and offer strategic business recommendations.\n\n"
    "Guidelines:\n"
    "1. Never guess numbers. Always use the appropriate tool to retrieve data.\n"
    "2. Be concise but insightful. When presenting numbers, explain what they mean for the business.\n"
    "3. Always provide concrete, actionable business recommendations based on the tool results. "
    "For example, if a category shows high sales but low or negative profit, highlight this anomaly and suggest mitigation strategies."
)

def run_agent(query: str, agent):
    print(f"\nUser Query: {query}")
    print("-" * 50)
    try:
        result = agent.invoke({
            "messages": [HumanMessage(content=query)]
        })
        print("\n--- Execution Trace ---")
        print_trace(result)
    except Exception as e:
        print(f"Error during agent execution: {e}")

def main():
    print_banner("SALES & BUSINESS ANALYTICS AI AGENT")
    
    # Check for API key
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY is not set. Please check your .env file.")
        return

    # Create the agent
    print("Initializing LangChain ReAct agent using DeepSeek...")
    agent = create_agent(
        model="deepseek:deepseek-chat",
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )
    print("Agent initialized successfully.")

    # Run a default query to show off the agent capabilities
    demo_query = "Compare sales and profit by category. Identify categories performing poorly (low/negative profits) and provide recommendations."
    run_agent(demo_query, agent)

    # CLI Loop
    print("\n" + "="*72)
    print("Interactive Chat Loop (Type 'exit' or 'quit' to stop)")
    print("="*72)
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if not user_input:
                continue
            run_agent(user_input, agent)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
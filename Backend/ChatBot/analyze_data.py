import os
import pandas as pd
import numpy as np

def analyze_ner_rainfall():
    """
    Data Analysis Script for Northeast India (NER) Rainfall Data.
    Run this script in VS Code terminal: python analyze_data.py
    """
    dataset_path = os.path.join(os.path.dirname(__file__), "datasets", "ner_rainfall_data.csv")
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        return
        
    print("=" * 70)
    print("📊 NORTHEAST INDIA (NER) RAINFALL DATA ANALYSIS")
    print("=" * 70)
    
    # 1. Load Dataset
    df = pd.read_csv(dataset_path)
    print("\n--- 1. DATASET OVERVIEW ---")
    print(df.head(10))
    print(f"\nTotal Records: {len(df)}")
    
    # 2. Summary Statistics
    print("\n--- 2. SUMMARY STATISTICS ---")
    print(df.describe())
    
    # 3. Weekly Rainfall Analysis
    print("\n--- 3. WEEKLY RAINFALL (HIGHEST TO LOWEST DEPARTURE) ---")
    weekly_df = df[df['period'] == 'Weekly'].sort_values(by='departure_percent', ascending=False)
    print(weekly_df[['state_subdivision', 'actual_rainfall_mm', 'normal_rainfall_mm', 'departure_percent']])
    
    # 4. Seasonal Rainfall Analysis
    print("\n--- 4. SEASONAL RAINFALL (DEFICIT / EXCESS STATES) ---")
    seasonal_df = df[df['period'] == 'Seasonal'].sort_values(by='departure_percent', ascending=True)
    print(seasonal_df[['state_subdivision', 'actual_rainfall_mm', 'normal_rainfall_mm', 'departure_percent']])
    
    # 5. Risk Insights for Chatbot & Logistics
    print("\n--- 5. RISK INSIGHTS FOR CHATBOT & LOGISTICS ---")
    high_rain_states = weekly_df[weekly_df['departure_percent'] > 30]
    deficit_states = seasonal_df[seasonal_df['departure_percent'] < -20]
    
    print("\n⚠️ States with Excessive Weekly Rain (>30% above normal - Landslide Risk):")
    for _, row in high_rain_states.iterrows():
        print(f"  • {row['state_subdivision']}: Actual={row['actual_rainfall_mm']}mm (Departure: +{row['departure_percent']}%)")
        
    print("\n📉 States with Major Seasonal Deficit (<-20% below normal):")
    for _, row in deficit_states.iterrows():
        print(f"  • {row['state_subdivision']}: Actual={row['actual_rainfall_mm']}mm vs Normal={row['normal_rainfall_mm']}mm (Departure: {row['departure_percent']}%)")
        
    print("\n=" * 70)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    analyze_ner_rainfall()

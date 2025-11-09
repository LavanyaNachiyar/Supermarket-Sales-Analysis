#!/usr/bin/env python3
"""
Quick Analysis Runner
Simple script to run the supermarket analysis with minimal setup
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'plotly': 'plotly',
        'sklearn': 'scikit-learn'
    }
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   • {pkg}")
        print("\n💡 Install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def run_analysis():
    """Run the main analysis"""
    try:
        from supermarket_analysis import SupermarketAnalyzer
        
        print("🔍 Checking for data file...")
        data_file = 'data/SuperMarket Analysis.csv'
        
        if not os.path.exists(data_file):
            print(f"❌ Data file not found: {data_file}")
            print("Please ensure the CSV file is in the 'data' folder")
            return False
        
        print("✅ Data file found")
        
        # Run analysis
        analyzer = SupermarketAnalyzer(data_file)
        analyzer.run_complete_analysis()
        
        return True
        
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False

def main():
    """Main execution function"""
    print("🏪 Supermarket Sales Analysis")
    print("="*40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run analysis
    if run_analysis():
        print("\n🎉 Analysis completed successfully!")
        print("\nGenerated files:")
        print("• supermarket_analysis_dashboard.png - Main dashboard")
        print("• sales_sunburst.html - Interactive city/branch view")
        print("• sales_scatter.html - Interactive scatter plot")
        print("• analysis_report.txt - Detailed text report")
    else:
        print("\n❌ Analysis failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
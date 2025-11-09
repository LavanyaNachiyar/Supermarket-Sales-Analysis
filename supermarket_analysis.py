#!/usr/bin/env python3
"""
Supermarket Sales Analysis
A comprehensive data analytics project for supermarket sales data
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class SupermarketAnalyzer:
    def __init__(self, data_path):
        """Initialize the analyzer with data"""
        self.data_path = data_path
        self.df = None
        self.load_data()
        
    def load_data(self):
        """Load and preprocess the data"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            
            # Convert date column
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Month'] = self.df['Date'].dt.month_name()
            self.df['Day'] = self.df['Date'].dt.day_name()
            
            print("📊 Data preprocessing completed")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def basic_stats(self):
        """Display basic statistics"""
        print("\n" + "="*50)
        print("📈 BASIC STATISTICS")
        print("="*50)
        
        print(f"Total Sales: ${self.df['Sales'].sum():,.2f}")
        print(f"Average Sale: ${self.df['Sales'].mean():.2f}")
        print(f"Total Transactions: {len(self.df):,}")
        print(f"Date Range: {self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}")
        
        print("\n🏪 Branch Performance:")
        branch_stats = self.df.groupby('Branch')['Sales'].agg(['count', 'sum', 'mean']).round(2)
        print(branch_stats)
        
        print("\n🛍️ Product Line Performance:")
        product_stats = self.df.groupby('Product line')['Sales'].agg(['count', 'sum', 'mean']).round(2)
        print(product_stats.sort_values('sum', ascending=False))
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("\n🎨 Creating visualizations...")
        
        # Set style
        plt.style.use('default')
        sns.set_palette('husl')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Sales by Branch
        plt.subplot(3, 3, 1)
        branch_sales = self.df.groupby('Branch')['Sales'].sum()
        plt.bar(branch_sales.index, branch_sales.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        plt.title('Total Sales by Branch', fontsize=14, fontweight='bold')
        plt.ylabel('Sales ($)')
        
        # 2. Sales by Product Line
        plt.subplot(3, 3, 2)
        product_sales = self.df.groupby('Product line')['Sales'].sum().sort_values(ascending=False)
        plt.barh(product_sales.index, product_sales.values, color='skyblue')
        plt.title('Sales by Product Line', fontsize=14, fontweight='bold')
        plt.xlabel('Sales ($)')
        
        # 3. Customer Type Distribution
        plt.subplot(3, 3, 3)
        customer_counts = self.df['Customer type'].value_counts()
        plt.pie(customer_counts.values, labels=customer_counts.index, autopct='%1.1f%%', 
                colors=['#FF9999', '#66B2FF'])
        plt.title('Customer Type Distribution', fontsize=14, fontweight='bold')
        
        # 4. Gender Distribution
        plt.subplot(3, 3, 4)
        gender_counts = self.df['Gender'].value_counts()
        plt.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
                colors=['#FFB366', '#66FFB2'])
        plt.title('Gender Distribution', fontsize=14, fontweight='bold')
        
        # 5. Payment Method Distribution
        plt.subplot(3, 3, 5)
        payment_counts = self.df['Payment'].value_counts()
        plt.bar(payment_counts.index, payment_counts.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        plt.title('Payment Methods', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        
        # 6. Sales Distribution
        plt.subplot(3, 3, 6)
        plt.hist(self.df['Sales'], bins=30, color='lightcoral', alpha=0.7, edgecolor='black')
        plt.title('Sales Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Sales ($)')
        plt.ylabel('Frequency')
        
        # 7. Rating Distribution
        plt.subplot(3, 3, 7)
        plt.hist(self.df['Rating'], bins=20, color='lightgreen', alpha=0.7, edgecolor='black')
        plt.title('Customer Rating Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        
        # 8. Sales by Month
        plt.subplot(3, 3, 8)
        monthly_sales = self.df.groupby('Month')['Sales'].sum()
        month_order = ['January', 'February', 'March']
        monthly_sales = monthly_sales.reindex([m for m in month_order if m in monthly_sales.index])
        plt.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2, markersize=8)
        plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
        plt.ylabel('Sales ($)')
        plt.xticks(rotation=45)
        
        # 9. Correlation Heatmap
        plt.subplot(3, 3, 9)
        numeric_cols = ['Unit price', 'Quantity', 'Sales', 'Rating', 'gross income']
        corr_matrix = self.df[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, square=True)
        plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('supermarket_analysis_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Dashboard saved as 'supermarket_analysis_dashboard.png'")
    
    def advanced_analysis(self):
        """Perform advanced analytics"""
        print("\n🔬 Advanced Analysis")
        print("="*50)
        
        # Customer Segmentation using K-Means
        features = ['Sales', 'Quantity', 'Rating']
        X = self.df[features].copy()
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # K-Means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        self.df['Customer_Segment'] = kmeans.fit_predict(X_scaled)
        
        # Segment analysis
        segment_analysis = self.df.groupby('Customer_Segment').agg({
            'Sales': ['mean', 'count'],
            'Quantity': 'mean',
            'Rating': 'mean'
        }).round(2)
        
        print("👥 Customer Segmentation Results:")
        print(segment_analysis)
        
        # Business insights
        print("\n💡 Key Business Insights:")
        
        # Top performing branch
        top_branch = self.df.groupby('Branch')['Sales'].sum().idxmax()
        print(f"• Best performing branch: {top_branch}")
        
        # Most popular product
        top_product = self.df.groupby('Product line')['Sales'].sum().idxmax()
        print(f"• Most profitable product line: {top_product}")
        
        # Peak sales day
        peak_day = self.df.groupby('Day')['Sales'].sum().idxmax()
        print(f"• Peak sales day: {peak_day}")
        
        # Average basket size
        avg_basket = self.df['Sales'].mean()
        print(f"• Average transaction value: ${avg_basket:.2f}")
        
        # Customer satisfaction
        avg_rating = self.df['Rating'].mean()
        print(f"• Average customer rating: {avg_rating:.1f}/10")
    
    def create_interactive_plots(self):
        """Create interactive Plotly visualizations"""
        print("\n🌟 Creating interactive visualizations...")
        
        # Interactive sales by city and branch
        fig1 = px.sunburst(
            self.df, 
            path=['City', 'Branch'], 
            values='Sales',
            title='Sales Distribution by City and Branch'
        )
        fig1.write_html('sales_sunburst.html')
        
        # Interactive scatter plot
        fig2 = px.scatter(
            self.df, 
            x='Unit price', 
            y='Sales', 
            color='Product line',
            size='Quantity',
            hover_data=['Rating', 'Customer type'],
            title='Sales vs Unit Price by Product Line'
        )
        fig2.write_html('sales_scatter.html')
        
        print("✅ Interactive plots saved as HTML files")
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        print("\n📋 Generating Analysis Report...")
        
        report = f"""
SUPERMARKET SALES ANALYSIS REPORT
{'='*50}

EXECUTIVE SUMMARY:
• Total Revenue: ${self.df['Sales'].sum():,.2f}
• Total Transactions: {len(self.df):,}
• Average Transaction: ${self.df['Sales'].mean():.2f}
• Analysis Period: {self.df['Date'].min().strftime('%B %Y')} - {self.df['Date'].max().strftime('%B %Y')}

BRANCH PERFORMANCE:
{self.df.groupby('Branch')['Sales'].agg(['count', 'sum']).to_string()}

PRODUCT LINE ANALYSIS:
{self.df.groupby('Product line')['Sales'].sum().sort_values(ascending=False).to_string()}

CUSTOMER INSIGHTS:
• Member vs Normal: {self.df['Customer type'].value_counts().to_dict()}
• Gender Split: {self.df['Gender'].value_counts().to_dict()}
• Average Rating: {self.df['Rating'].mean():.1f}/10

RECOMMENDATIONS:
1. Focus marketing efforts on the top-performing product lines
2. Implement loyalty programs to convert normal customers to members
3. Optimize inventory based on branch-specific performance
4. Leverage peak sales days for promotional activities
        """
        
        with open('analysis_report.txt', 'w') as f:
            f.write(report)
        
        print("✅ Report saved as 'analysis_report.txt'")
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("🚀 Starting Supermarket Sales Analysis")
        print("="*50)
        
        self.basic_stats()
        self.create_visualizations()
        self.advanced_analysis()
        self.create_interactive_plots()
        self.generate_report()
        
        print("\n🎉 Analysis Complete!")
        print("Files generated:")
        print("• supermarket_analysis_dashboard.png")
        print("• sales_sunburst.html")
        print("• sales_scatter.html")
        print("• analysis_report.txt")

def main():
    """Main function to run the analysis"""
    # Initialize analyzer
    analyzer = SupermarketAnalyzer('data/SuperMarket Analysis.csv')
    
    # Run complete analysis
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
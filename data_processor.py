import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
import streamlit as st
import re
from datetime import datetime

class DataProcessor:
    """
    Comprehensive data processing utility for Market Basket Analysis
    Handles data cleaning, transformation, and preparation for analysis
    """
    
    def __init__(self):
        self.original_data = None
        self.processed_data = None
        self.column_mapping = {}
        self.preprocessing_steps = []
        self.transactions = None
        self.basket_encoded = None
        
    def detect_column_types(self, df):
        """Intelligently detect column types based on content and names"""
        potential_mappings = {
            'transaction_id': [],
            'product_item': [],
            'customer_id': [],
            'date': [],
            'price_sales': [],
            'quantity': [],
            'category': []
        }
        
        for col in df.columns:
            col_lower = col.lower().strip()
            
            # Transaction ID detection patterns
            if any(keyword in col_lower for keyword in [
                'transaction', 'order', 'invoice', 'receipt', 'bill', 'ticket', 'txn'
            ]):
                potential_mappings['transaction_id'].append(col)
            
            # Product/Item detection patterns
            if any(keyword in col_lower for keyword in [
                'product', 'item', 'goods', 'article', 'sku', 'material', 
                'description', 'name', 'title'
            ]):
                potential_mappings['product_item'].append(col)
            
            # Customer ID detection patterns
            if any(keyword in col_lower for keyword in [
                'customer', 'client', 'user', 'buyer', 'member', 'cust'
            ]):
                potential_mappings['customer_id'].append(col)
            
            # Date detection patterns
            if any(keyword in col_lower for keyword in [
                'date', 'time', 'timestamp', 'created', 'purchased', 'ordered'
            ]):
                potential_mappings['date'].append(col)
            elif df[col].dtype == 'datetime64[ns]':
                potential_mappings['date'].append(col)
            
            # Price/Sales detection patterns
            if any(keyword in col_lower for keyword in [
                'price', 'cost', 'amount', 'sales', 'revenue', 'value', 'total'
            ]):
                if pd.api.types.is_numeric_dtype(df[col]):
                    potential_mappings['price_sales'].append(col)
            
            # Quantity detection patterns
            if any(keyword in col_lower for keyword in [
                'quantity', 'qty', 'count', 'number', 'units'
            ]) and 'price' not in col_lower:
                if pd.api.types.is_numeric_dtype(df[col]):
                    potential_mappings['quantity'].append(col)
            
            # Category detection patterns
            if any(keyword in col_lower for keyword in [
                'category', 'type', 'class', 'group', 'department', 'section'
            ]):
                potential_mappings['category'].append(col)
        
        return potential_mappings
    
    def clean_text_data(self, series):
        """Clean and standardize text data"""
        # Convert to string and strip whitespace
        cleaned = series.astype(str).str.strip()
        
        # Remove special characters except spaces and hyphens
        cleaned = cleaned.str.replace(r'[^\w\s-]', '', regex=True)
        
        # Standardize case (title case)
        cleaned = cleaned.str.title()
        
        # Remove extra whitespaces
        cleaned = cleaned.str.replace(r'\s+', ' ', regex=True)
        
        # Remove empty strings
        cleaned = cleaned.replace('', np.nan)
        
        return cleaned
    
    def validate_data_quality(self, df, transaction_col, product_col):
        """Validate data quality and return quality metrics"""
        quality_report = {
            'total_rows': len(df),
            'missing_transactions': df[transaction_col].isnull().sum(),
            'missing_products': df[product_col].isnull().sum(),
            'unique_transactions': df[transaction_col].nunique(),
            'unique_products': df[product_col].nunique(),
            'avg_items_per_transaction': 0,
            'quality_score': 0
        }
        
        # Calculate average items per transaction
        if quality_report['unique_transactions'] > 0:
            items_per_txn = df.groupby(transaction_col).size()
            quality_report['avg_items_per_transaction'] = items_per_txn.mean()
        
        # Calculate quality score (0-100)
        completeness = (1 - (quality_report['missing_transactions'] + quality_report['missing_products']) / (2 * quality_report['total_rows'])) * 100
        uniqueness = min(quality_report['unique_products'] / quality_report['total_rows'], 1) * 100
        transaction_richness = min(quality_report['avg_items_per_transaction'] / 5, 1) * 100
        
        quality_report['quality_score'] = (completeness + uniqueness + transaction_richness) / 3
        
        return quality_report
    
    def process_data(self, df, column_mapping):
        """
        Main data processing pipeline
        """
        try:
            self.original_data = df.copy()
            self.column_mapping = column_mapping
            self.preprocessing_steps = []
            
            # Step 1: Extract required columns
            working_df = df[[column_mapping['transaction_id'], column_mapping['product_item']]].copy()
            working_df.columns = ['TransactionID', 'Product']
            
            # Add optional columns if available
            if column_mapping.get('customer_id'):
                working_df['Customer'] = df[column_mapping['customer_id']]
            
            if column_mapping.get('price_sales'):
                working_df['Price'] = pd.to_numeric(df[column_mapping['price_sales']], errors='coerce')
            
            if column_mapping.get('quantity'):
                working_df['Quantity'] = pd.to_numeric(df[column_mapping['quantity']], errors='coerce')
            
            if column_mapping.get('date'):
                working_df['Date'] = pd.to_datetime(df[column_mapping['date']], errors='coerce')
            
            self.preprocessing_steps.append(f"✅ Extracted {len(working_df.columns)} columns")
            
            # Step 2: Data quality validation
            initial_rows = len(working_df)
            quality_report = self.validate_data_quality(working_df, 'TransactionID', 'Product')
            
            # Step 3: Handle missing values
            working_df = working_df.dropna(subset=['TransactionID', 'Product'])
            rows_after_cleaning = len(working_df)
            
            if rows_after_cleaning == 0:
                raise ValueError("No valid transactions remain after cleaning")
            
            self.preprocessing_steps.append(f"⚠️ Removed {initial_rows - rows_after_cleaning} rows with missing data")
            
            # Step 4: Clean and standardize data
            working_df['TransactionID'] = working_df['TransactionID'].astype(str).str.strip()
            working_df['Product'] = self.clean_text_data(working_df['Product'])
            
            # Remove rows with empty products after cleaning
            working_df = working_df.dropna(subset=['Product'])
            
            self.preprocessing_steps.append("✅ Cleaned and standardized text data")
            
            # Step 5: Handle quantities (expand rows if needed)
            if 'Quantity' in working_df.columns:
                expanded_rows = []
                for _, row in working_df.iterrows():
                    qty = max(1, int(row['Quantity'])) if not pd.isna(row['Quantity']) else 1
                    qty = min(qty, 10)  # Cap at 10 to prevent explosion
                    
                    for _ in range(qty):
                        new_row = row.copy()
                        if 'Quantity' in new_row.index:
                            new_row = new_row.drop('Quantity')
                        expanded_rows.append(new_row)
                
                if len(expanded_rows) > len(working_df):
                    working_df = pd.DataFrame(expanded_rows).reset_index(drop=True)
                    self.preprocessing_steps.append("✅ Expanded rows based on quantities")
            
            # Step 6: Remove duplicates
            initial_count = len(working_df)
            working_df = working_df.drop_duplicates(subset=['TransactionID', 'Product'])
            final_count = len(working_df)
            
            if initial_count != final_count:
                self.preprocessing_steps.append(f"⚠️ Removed {initial_count - final_count} duplicate entries")
            
            # Step 7: Filter transactions with minimum items
            transaction_sizes = working_df.groupby('TransactionID').size()
            valid_transactions = transaction_sizes[transaction_sizes >= 1].index
            working_df = working_df[working_df['TransactionID'].isin(valid_transactions)]
            
            # Step 8: Create transactions for basket analysis
            self.transactions = working_df.groupby('TransactionID')['Product'].apply(list).tolist()
            
            if len(self.transactions) == 0:
                raise ValueError("No transactions could be created")
            
            # Step 9: One-hot encoding
            te = TransactionEncoder()
            te_array = te.fit(self.transactions).transform(self.transactions)
            self.basket_encoded = pd.DataFrame(te_array, columns=te.columns_)
            
            self.preprocessing_steps.append(f"✅ Created {len(self.transactions)} transactions with {len(te.columns_)} unique products")
            self.preprocessing_steps.append("✅ Applied one-hot encoding for analysis")
            
            # Store processed data
            self.processed_data = {
                'clean_df': working_df,
                'transactions': self.transactions,
                'basket_df': self.basket_encoded,
                'quality_report': quality_report,
                'preprocessing_steps': self.preprocessing_steps
            }
            
            return True
            
        except Exception as e:
            self.preprocessing_steps.append(f"❌ Error: {str(e)}")
            return False
    
    def get_processing_summary(self):
        """Get summary of processing steps and results"""
        if not self.processed_data:
            return None
        
        summary = {
            'total_transactions': len(self.transactions),
            'unique_products': len(self.basket_encoded.columns),
            'avg_items_per_transaction': np.mean([len(t) for t in self.transactions]),
            'sparsity': (self.basket_encoded.sum().sum() / (len(self.basket_encoded) * len(self.basket_encoded.columns))) * 100,
            'processing_steps': self.preprocessing_steps,
            'quality_report': self.processed_data.get('quality_report', {})
        }
        
        return summary
    
    def create_sample_data(self):
        """Create sample retail data for testing"""
        sample_data = pd.DataFrame({
            'OrderID': [
                'O001', 'O001', 'O001', 'O002', 'O002', 'O003', 'O003', 'O003',
                'O004', 'O004', 'O005', 'O005', 'O006', 'O006', 'O006', 'O007',
                'O008', 'O008', 'O009', 'O009', 'O010', 'O010', 'O010'
            ],
            'Product': [
                'Bread', 'Milk', 'Butter', 'Bread', 'Eggs', 'Milk', 'Cheese', 'Yogurt',
                'Bread', 'Milk', 'Coffee', 'Sugar', 'Tea', 'Cookies', 'Milk',
                'Bread', 'Apples', 'Bananas', 'Milk', 'Bread', 'Juice', 'Cereal', 'Milk'
            ],
            'Customer': [
                'John', 'John', 'John', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob',
                'Carol', 'Carol', 'David', 'David', 'Eve', 'Eve', 'Eve', 'Frank',
                'Grace', 'Grace', 'Henry', 'Henry', 'Ivy', 'Ivy', 'Ivy'
            ],
            'Price': [
                2.50, 3.00, 1.80, 2.50, 2.20, 3.00, 4.50, 1.50,
                2.50, 3.00, 5.00, 2.00, 3.50, 4.00, 3.00, 2.50,
                4.00, 3.00, 3.00, 2.50, 2.50, 5.50, 3.00
            ],
            'Quantity': [
                1, 1, 2, 1, 3, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 2, 1, 1, 1
            ],
            'Date': pd.date_range('2024-01-01', periods=23, freq='H')
        })
        
        return sample_data

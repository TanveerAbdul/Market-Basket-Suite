import streamlit as st
import pandas as pd
import json
import zipfile
import io
import base64
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

class ExportManager:
    """Comprehensive export management system for multiple file formats"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def create_csv_export(self, dataframe, filename_prefix="data"):
        """Create CSV export"""
        csv_buffer = io.StringIO()
        dataframe.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        csv_buffer.close()
        
        return csv_data, f"{filename_prefix}_{self.timestamp}.csv"
    
    def create_excel_export(self, data_dict, filename_prefix="analysis"):
        """Create multi-sheet Excel export"""
        excel_buffer = io.BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            for sheet_name, dataframe in data_dict.items():
                if isinstance(dataframe, pd.DataFrame) and not dataframe.empty:
                    # Clean sheet name
                    clean_sheet_name = sheet_name.replace('/', '_').replace('\\', '_')[:31]
                    dataframe.to_excel(writer, sheet_name=clean_sheet_name, index=False)
        
        excel_buffer.seek(0)
        return excel_buffer.getvalue(), f"{filename_prefix}_{self.timestamp}.xlsx"
    
    def create_json_export(self, data_dict, filename_prefix="analysis"):
        """Create JSON export"""
        json_data = {}
        
        for key, value in data_dict.items():
            if isinstance(value, pd.DataFrame):
                json_data[key] = value.to_dict(orient='records')
            elif hasattr(value, 'tolist'):  # numpy arrays
                json_data[key] = value.tolist()
            else:
                json_data[key] = value
        
        # Add metadata
        json_data['metadata'] = {
            'export_timestamp': datetime.now().isoformat(),
            'format_version': '1.0',
            'tool': 'Market Basket Analysis Suite'
        }
        
        json_string = json.dumps(json_data, indent=2, default=str)
        return json_string, f"{filename_prefix}_{self.timestamp}.json"
    
    def create_pdf_report(self, analysis_results, processed_data, filename_prefix="report"):
        """Create comprehensive PDF report"""
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2563eb'),
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#1f2937')
        )
        
        # Title
        story.append(Paragraph("Market Basket Analysis Report", title_style))
        story.append(Spacer(1, 12))
        
        # Summary section
        story.append(Paragraph("Executive Summary", heading_style))
        
        if 'frequent_itemsets' in analysis_results and not analysis_results['frequent_itemsets'].empty:
            itemsets_count = len(analysis_results['frequent_itemsets'])
            rules_count = len(analysis_results.get('rules', pd.DataFrame()))
            
            summary_text = f"""
            This analysis identified {itemsets_count} frequent itemsets and {rules_count} association rules 
            from the provided retail transaction data. The analysis provides insights into customer 
            purchasing patterns and identifies opportunities for cross-selling and product bundling.
            """
            story.append(Paragraph(summary_text, styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Dataset overview
        story.append(Paragraph("Dataset Overview", heading_style))
        
        if processed_data and 'transactions' in processed_data:
            transactions_count = len(processed_data['transactions'])
            unique_products = len(processed_data['basket_df'].columns) if 'basket_df' in processed_data else 0
            avg_items = sum(len(t) for t in processed_data['transactions']) / len(processed_data['transactions'])
            
            overview_data = [
                ['Metric', 'Value'],
                ['Total Transactions', f"{transactions_count:,}"],
                ['Unique Products', f"{unique_products:,}"],
                ['Average Items per Transaction', f"{avg_items:.2f}"]
            ]
            
            overview_table = Table(overview_data)
            overview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            
            story.append(overview_table)
            story.append(Spacer(1, 20))
        
        # Top frequent itemsets
        if 'frequent_itemsets' in analysis_results and not analysis_results['frequent_itemsets'].empty:
            story.append(Paragraph("Top Frequent Itemsets", heading_style))
            
            top_itemsets = analysis_results['frequent_itemsets'].head(10)
            itemsets_data = [['Itemset', 'Support']]
            
            for _, row in top_itemsets.iterrows():
                itemset_str = ', '.join(list(row['itemsets']))
                itemsets_data.append([itemset_str, f"{row['support']:.4f}"])
            
            itemsets_table = Table(itemsets_data, colWidths=[4*inch, 1.5*inch])
            itemsets_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            
            story.append(itemsets_table)
            story.append(PageBreak())
        
        # Top association rules
        if 'rules' in analysis_results and not analysis_results['rules'].empty:
            story.append(Paragraph("Top Association Rules", heading_style))
            
            top_rules = analysis_results['rules'].head(10)
            rules_data = [['Antecedents', 'Consequents', 'Support', 'Confidence', 'Lift']]
            
            for _, row in top_rules.iterrows():
                antecedents = ', '.join(list(row['antecedents']))
                consequents = ', '.join(list(row['consequents']))
                rules_data.append([
                    antecedents,
                    consequents,
                    f"{row['support']:.4f}",
                    f"{row['confidence']:.4f}",
                    f"{row['lift']:.4f}"
                ])
            
            rules_table = Table(rules_data, colWidths=[1.8*inch, 1.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            rules_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            
            story.append(rules_table)
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue(), f"{filename_prefix}_{self.timestamp}.pdf"
    
    def create_comprehensive_zip(self, analysis_results, processed_data, visualizations=None):
        """Create comprehensive ZIP package with all export formats"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            
            # 1. CSV Files
            if 'frequent_itemsets' in analysis_results:
                csv_data, csv_filename = self.create_csv_export(
                    analysis_results['frequent_itemsets'], 
                    "frequent_itemsets"
                )
                zip_file.writestr(f"csv/{csv_filename}", csv_data)
            
            if 'rules' in analysis_results and not analysis_results['rules'].empty:
                # Clean rules for CSV export
                rules_export = analysis_results['rules'].copy()
                rules_export['antecedents'] = rules_export['antecedents'].apply(lambda x: ', '.join(list(x)))
                rules_export['consequents'] = rules_export['consequents'].apply(lambda x: ', '.join(list(x)))
                
                csv_data, csv_filename = self.create_csv_export(
                    rules_export[['antecedents', 'consequents', 'support', 'confidence', 'lift']], 
                    "association_rules"
                )
                zip_file.writestr(f"csv/{csv_filename}", csv_data)
            
            if processed_data and 'clean_df' in processed_data:
                csv_data, csv_filename = self.create_csv_export(
                    processed_data['clean_df'], 
                    "processed_data"
                )
                zip_file.writestr(f"csv/{csv_filename}", csv_data)
            
            # 2. Excel File
            excel_data_dict = {}
            if 'frequent_itemsets' in analysis_results:
                itemsets_export = analysis_results['frequent_itemsets'].copy()
                itemsets_export['itemsets'] = itemsets_export['itemsets'].apply(lambda x: ', '.join(list(x)))
                excel_data_dict['Frequent_Itemsets'] = itemsets_export
            
            if 'rules' in analysis_results and not analysis_results['rules'].empty:
                rules_export = analysis_results['rules'].copy()
                rules_export['antecedents'] = rules_export['antecedents'].apply(lambda x: ', '.join(list(x)))
                rules_export['consequents'] = rules_export['consequents'].apply(lambda x: ', '.join(list(x)))
                excel_data_dict['Association_Rules'] = rules_export[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
            
            if processed_data and 'clean_df' in processed_data:
                excel_data_dict['Processed_Data'] = processed_data['clean_df']
            
            if excel_data_dict:
                excel_data, excel_filename = self.create_excel_export(excel_data_dict)
                zip_file.writestr(f"excel/{excel_filename}", excel_data)
            
            # 3. JSON File
            json_export_data = {
                'analysis_parameters': analysis_results.get('parameters', {}),
                'analysis_algorithm': analysis_results.get('algorithm', 'Unknown'),
                'export_timestamp': datetime.now().isoformat()
            }
            
            if 'frequent_itemsets' in analysis_results:
                itemsets_json = analysis_results['frequent_itemsets'].copy()
                itemsets_json['itemsets'] = itemsets_json['itemsets'].apply(lambda x: list(x))
                json_export_data['frequent_itemsets'] = itemsets_json.to_dict(orient='records')
            
            if 'rules' in analysis_results and not analysis_results['rules'].empty:
                rules_json = analysis_results['rules'].copy()
                rules_json['antecedents'] = rules_json['antecedents'].apply(lambda x: list(x))
                rules_json['consequents'] = rules_json['consequents'].apply(lambda x: list(x))
                json_export_data['association_rules'] = rules_json[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_dict(orient='records')
            
            json_data, json_filename = self.create_json_export(json_export_data)
            zip_file.writestr(f"json/{json_filename}", json_data)
            
            # 4. PDF Report
            pdf_data, pdf_filename = self.create_pdf_report(analysis_results, processed_data)
            zip_file.writestr(f"reports/{pdf_filename}", pdf_data)
            
            # 5. README file
            readme_content = f"""
Market Basket Analysis Export Package
=====================================

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Algorithm Used: {analysis_results.get('algorithm', 'Unknown')}

Directory Structure:
-------------------
📁 csv/                    - Individual CSV files
📁 excel/                  - Multi-sheet Excel workbook
📁 json/                   - JSON format data
📁 reports/                - PDF summary report

File Descriptions:
-----------------
• frequent_itemsets_*.csv  - Frequent itemsets with support values
• association_rules_*.csv  - Association rules with metrics
• processed_data_*.csv     - Cleaned transaction data
• analysis_*.xlsx          - Complete analysis in Excel format
• analysis_*.json          - Machine-readable JSON export
• report_*.pdf             - Executive summary report

Analysis Parameters:
-------------------
{json.dumps(analysis_results.get('parameters', {}), indent=2)}

Usage Notes:
-----------
- CSV files can be opened in Excel, Google Sheets, or any text editor
- JSON files are suitable for programmatic analysis
- PDF report provides executive summary and key findings
- Excel file contains all data in organized sheets

For questions or support, please refer to the application documentation.
            """
            zip_file.writestr("README.txt", readme_content)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue(), f"market_basket_analysis_complete_{self.timestamp}.zip"
    
    def create_download_button(self, data, filename, label, mime_type, help_text=None, key=None):
        """Create a styled download button"""
        return st.download_button(
            label=label,
            data=data,
            file_name=filename,
            mime=mime_type,
            help=help_text,
            key=key,
            use_container_width=True
        )
    
    def get_file_size_mb(self, data):
        """Get file size in MB"""
        if isinstance(data, str):
            return len(data.encode('utf-8')) / (1024 * 1024)
        else:
            return len(data) / (1024 * 1024)

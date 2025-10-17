"""
HTML/PDF formatter using Jinja2 templates.
"""
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template
from reports.base_formatter import BaseFormatter
from core.report_data import ReportData


class HTMLFormatter(BaseFormatter):
    """Formats reports as HTML documents using Jinja2 templates."""
    
    def __init__(self):
        # Get the directory where this file is located (reports directory)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Set up Jinja2 environment to load templates from reports directory
        self.env = Environment(loader=FileSystemLoader(current_dir))
    
    def format(self, data: ReportData) -> str:
        """Generate HTML content using Jinja2 template."""
        # Load template
        template = self.env.get_template('report.html')
        
        # Add current timestamp to data
        data.current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Render template
        html_content = template.render(report_data=data)
        
        return html_content
    
    def get_extension(self) -> str:
        return ".html"
    
    def get_mime_type(self) -> str:
        return "text/html"


class PDFFormatter(HTMLFormatter):
    """Formats reports as PDF documents using HTML template and xhtml2pdf."""
    
    def format(self, data: ReportData) -> str:
        """Generate HTML content that will be converted to PDF."""
        return super().format(data)
    
    def get_extension(self) -> str:
        return ".pdf"
    
    def get_mime_type(self) -> str:
        return "application/pdf"
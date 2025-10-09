"""
Main report generator that coordinates formatters.
"""
from datetime import datetime
from typing import Optional, Dict, Type
from xhtml2pdf import pisa
from reports.base_formatter import BaseFormatter
from reports.markdown_formatter import MarkdownFormatter
from reports.html_formatter import HTMLFormatter, PDFFormatter
from core.report_data import ReportData


# Format type constants
class ReportFormats:
    MARKDOWN = 'markdown'
    HTML = 'html'
    PDF = 'pdf'


class ReportGenerator:
    """Main class for generating audit reports in various formats."""
    
    def __init__(self):
        # Register available formatters
        self.formatters: Dict[str, Type[BaseFormatter]] = {
            ReportFormats.MARKDOWN: MarkdownFormatter,
            ReportFormats.HTML: HTMLFormatter,
            ReportFormats.PDF: PDFFormatter
        }
    
    def get_available_formats(self) -> list:
        """Get list of available report formats."""
        return list(self.formatters.keys())
    
    def generate(self, data: ReportData, format_type: str = ReportFormats.MARKDOWN, 
                 output_file: Optional[str] = None) -> str:
        """
        Generate a report in the specified format.
        
        Args:
            data: ReportData object containing all audit information
            format_type: Type of report format (use ReportFormats constants)
            output_file: Optional path to save the report to
        
        Returns:
            Path to the generated report file
        
        Raises:
            ValueError: If unsupported format is requested
            ImportError: If required dependencies are missing
        """
        if format_type not in self.formatters:
            raise ValueError(
                f"Unsupported format: {format_type}. "
                f"Supported formats: {list(self.formatters.keys())}"
            )
        
        # Create formatter instance
        formatter_class = self.formatters[format_type]
        formatter = formatter_class()
        
        # Generate the report content
        content = formatter.format(data)
        
        # Determine output file path
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"whistleblower_report_{timestamp}"
        
        # Add extension if not present
        extension = formatter.get_extension()
        if not output_file.endswith(extension):
            output_file += extension
        
        # Handle different output types
        if format_type == ReportFormats.PDF:
            return self._generate_pdf(content, output_file)
        else:
            # For markdown and HTML, write directly to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return output_file
    
    def _generate_pdf(self, html_content: str, output_file: str) -> str:
        """
        Convert HTML content to PDF using xhtml2pdf.
        
        Args:
            html_content: HTML content to convert
            output_file: Path to save PDF file
            
        Returns:
            Path to the generated PDF file
            
        Raises:
            RuntimeError: If PDF generation fails
        """
        with open(output_file, 'wb') as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
            if pisa_status.err:
                raise RuntimeError(f"PDF generation failed with {pisa_status.err} errors")
        
        return output_file
    
    def generate_multiple(self, data: ReportData, formats: list, 
                         output_prefix: Optional[str] = None) -> Dict[str, str]:
        """
        Generate reports in multiple formats.
        
        Args:
            data: ReportData object containing all audit information
            formats: List of format types to generate
            output_prefix: Optional prefix for output files
            
        Returns:
            Dictionary mapping format to file path
        """
        results = {}
        
        for format_type in formats:
            try:
                output_file = None
                if output_prefix:
                    formatter = self.formatters[format_type]()
                    extension = formatter.get_extension()
                    output_file = f"{output_prefix}{extension}"
                
                file_path = self.generate(data, format_type, output_file)
                results[format_type] = file_path
                
            except Exception as e:
                results[format_type] = f"Error: {e}"
        
        return results
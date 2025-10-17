"""
Abstract base formatter class for report generation.
"""
from abc import ABC, abstractmethod
from core.report_data import ReportData


class BaseFormatter(ABC):
    """Abstract base class for report formatters."""
    
    @abstractmethod
    def format(self, data: ReportData) -> str:
        """
        Format the report data into the desired output format.
        
        Args:
            data: ReportData object containing all audit information
            
        Returns:
            Formatted report content as string
        """
        pass
    
    @abstractmethod
    def get_extension(self) -> str:
        """
        Get the file extension for this format.
        
        Returns:
            File extension (e.g., '.md', '.pdf')
        """
        pass
    
    @abstractmethod
    def get_mime_type(self) -> str:
        """
        Get the MIME type for this format.
        
        Returns:
            MIME type (e.g., 'text/markdown', 'application/pdf')
        """
        pass
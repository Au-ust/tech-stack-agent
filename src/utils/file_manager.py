"""
File Management Utilities
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class FileManager:
    """
    Manages file operations for the tech stack agent.
    """
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize FileManager.
        
        Args:
            output_dir: Directory for saving generated documents
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_document(
        self,
        content: str,
        project_name: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> str:
        """
        Save a document to the output directory.
        
        Args:
            content: Document content
            project_name: Optional project name for filename
            filename: Optional custom filename (overrides project_name)
            
        Returns:
            Full path to saved file
        """
        if filename:
            file_path = self.output_dir / filename
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if project_name:
                # Sanitize project name for filename
                safe_name = "".join(
                    c for c in project_name if c.isalnum() or c in (' ', '-', '_')
                ).strip().replace(' ', '_')
                filename = f"tech_stack_{safe_name}_{timestamp}.md"
            else:
                filename = f"tech_stack_{timestamp}.md"
            
            file_path = self.output_dir / filename
        
        # Save file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(file_path.absolute())
    
    def load_template(self, template_name: str) -> str:
        """
        Load a template file.
        
        Args:
            template_name: Name of the template file
            
        Returns:
            Template content
        """
        template_path = Path("src/templates") / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def list_outputs(self) -> list[str]:
        """
        List all generated documents.
        
        Returns:
            List of document filenames
        """
        if not self.output_dir.exists():
            return []
        
        return [f.name for f in self.output_dir.glob("*.md")]


# Global file manager instance
_global_file_manager: Optional[FileManager] = None


def get_file_manager() -> FileManager:
    """
    Get or create a global FileManager instance.
    
    Returns:
        Shared FileManager instance
    """
    global _global_file_manager
    if _global_file_manager is None:
        _global_file_manager = FileManager()
    return _global_file_manager

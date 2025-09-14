import json
import csv
import re
import html
from typing import List, Dict, Any
import pandas as pd

class DataCleaner:
    def __init__(self):
        self.cleaned_data = []

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text or not isinstance(text, str):
            return ""
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\(\)\/]', '', text)
        
        # Strip and title case for consistency
        text = text.strip()
        
        return text

    def normalize_company_name(self, company: str) -> str:
        """Normalize company names"""
        if not company or not isinstance(company, str):
            return "Unknown Company"
        
        company = self.clean_text(company)
        
        # Remove common prefixes/suffixes
        company = re.sub(r'\b(Inc|Ltd|LLC|Corp|Corporation|Company|Co)\b\.?', '', company, flags=re.IGNORECASE)
        
        # Title case
        company = company.title().strip()
        
        return company if company else "Unknown Company"

    def normalize_job_title(self, title: str) -> str:
        """Normalize job titles"""
        if not title or not isinstance(title, str):
            return "Unknown Position"
        
        title = self.clean_text(title)
        
        # Title case
        title = title.title()
        
        # Common abbreviations
        title = re.sub(r'\bSr\b', 'Senior', title)
        title = re.sub(r'\bJr\b', 'Junior', title)
        title = re.sub(r'\bMgr\b', 'Manager', title)
        
        return title.strip() if title.strip() else "Unknown Position"

    def remove_duplicates(self, data: List[Dict]) -> List[Dict]:
        """Remove duplicate entries based on title and company"""
        seen = set()
        unique_data = []
        
        for item in data:
            # Create a key based on title and company
            key = f"{item.get('title', '').lower().strip()}_{item.get('company', '').lower().strip()}"
            
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        return unique_data

    def validate_entry(self, entry: Dict) -> bool:
        """Validate if an entry has minimum required data"""
        title = entry.get('title', '').strip()
        company = entry.get('company', '').strip()
        description = entry.get('description', '').strip()
        
        # Must have at least title and some content
        if not title:
            return False
        
        # Description should have some meaningful content
        if len(description) < 10:
            return False
        
        return True

    def clean_data(self, input_file: str, output_file: str) -> int:
        """Main cleaning function"""
        print(f"🧹 Cleaning data from {input_file}...")
        
        try:
            # Load raw data
            with open(input_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            print(f"📥 Loaded {len(raw_data)} raw entries")
            
            # Clean each entry
            for entry in raw_data:
                # Clean individual fields with safe defaults
                cleaned_entry = {
                    'source': entry.get('source', 'Unknown').strip(),
                    'title': self.normalize_job_title(entry.get('title', '')),
                    'company': self.normalize_company_name(entry.get('company', '')),
                    'description': self.clean_text(entry.get('description', '')),
                    'type': entry.get('type', 'job').strip(),
                    'score': entry.get('score', 0) if entry.get('score') is not None else 0
                }
                
                # Validate entry
                if self.validate_entry(cleaned_entry):
                    self.cleaned_data.append(cleaned_entry)
            
            print(f"🔍 After validation: {len(self.cleaned_data)} entries")
            
            # Remove duplicates
            self.cleaned_data = self.remove_duplicates(self.cleaned_data)
            print(f"After deduplication: {len(self.cleaned_data)} entries")
            
            # Save cleaned data
            self.save_cleaned_data(output_file)
            
            return len(self.cleaned_data)
            
        except Exception as e:
            print(f"Error in cleaning: {e}")
            raise

    def save_cleaned_data(self, filename: str):
        """Save cleaned data to JSON and CSV"""
        import os
        os.makedirs("data", exist_ok=True)
        
        # Save as JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.cleaned_data, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        csv_filename = filename.replace('.json', '.csv')
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            if self.cleaned_data:
                writer = csv.DictWriter(f, fieldnames=self.cleaned_data[0].keys())
                writer.writeheader()
                writer.writerows(self.cleaned_data)
        
        print(f"Saved cleaned data to {filename} and {csv_filename}")

    def get_data_statistics(self) -> Dict[str, Any]:
        """Get statistics about the cleaned data"""
        if not self.cleaned_data:
            return {}
        
        stats = {
            'total_entries': len(self.cleaned_data),
            'sources': {},
            'avg_description_length': 0,
            'companies': set(),
            'job_types': {}
        }
        
        total_desc_length = 0
        
        for entry in self.cleaned_data:
            # Source distribution
            source = entry.get('source', 'Unknown')
            stats['sources'][source] = stats['sources'].get(source, 0) + 1
            
            # Description length
            desc_len = len(entry.get('description', ''))
            total_desc_length += desc_len
            
            # Unique companies
            stats['companies'].add(entry.get('company', 'Unknown'))
            
            # Job types
            job_type = entry.get('type', 'Unknown')
            stats['job_types'][job_type] = stats['job_types'].get(job_type, 0) + 1
        
        stats['avg_description_length'] = total_desc_length / len(self.cleaned_data)
        stats['unique_companies'] = len(stats['companies'])
        
        return stats

if __name__ == "__main__":
    cleaner = DataCleaner()
    count = cleaner.clean_data("data/raw_jobs.json", "data/cleaned_jobs.json")
    
    stats = cleaner.get_data_statistics()
    print("\nCLEANING STATISTICS:")
    print(f"Total entries: {stats.get('total_entries', 0)}")
    print(f"Unique companies: {stats.get('unique_companies', 0)}")
    print(f"Average description length: {stats.get('avg_description_length', 0):.1f} characters")
    print(f"Sources: {stats.get('sources', {})}")
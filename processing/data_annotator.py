import json
import csv
import re
from typing import List, Dict, Any
import random

class DataAnnotator:
    def __init__(self):
        self.annotated_data = []
        
        # Define annotation categories for Software Engineering domain
        self.skill_keywords = {
            'Python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy'],
            'JavaScript': ['javascript', 'js', 'node', 'react', 'vue', 'angular', 'express'],
            'Java': ['java', 'spring', 'hibernate', 'maven', 'gradle'],
            'DevOps': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform', 'jenkins'],
            'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
            'Machine Learning': ['ml', 'ai', 'tensorflow', 'pytorch', 'sklearn', 'data science'],
            'Cloud': ['aws', 'azure', 'gcp', 'cloud', 'serverless', 'lambda'],
            'Frontend': ['html', 'css', 'react', 'vue', 'angular', 'typescript'],
            'Backend': ['api', 'rest', 'graphql', 'microservices', 'database'],
            'Mobile': ['ios', 'android', 'react native', 'flutter', 'swift', 'kotlin']
        }
        
        self.experience_keywords = {
            'Entry Level': ['entry', 'junior', 'graduate', 'intern', '0-2 years', 'beginner', 'new grad'],
            'Mid Level': ['mid', 'intermediate', '2-5 years', '3-5 years', 'experienced'],
            'Senior Level': ['senior', 'sr', 'lead', '5+ years', '6+ years', 'expert', 'principal'],
            'Management': ['manager', 'mgr', 'director', 'vp', 'head of', 'team lead', 'tech lead']
        }
        
        self.content_types = {
            'Job Description': ['hiring', 'position', 'role', 'opportunity', 'apply', 'requirements'],
            'Interview Question': ['interview', 'question', 'how to', 'explain', 'what is', 'why'],
            'Career Advice': ['career', 'advice', 'tips', 'how to become', 'path', 'guidance'],
            'Technical Discussion': ['discussion', 'best practices', 'comparison', 'vs', 'opinion'],
            'Company Info': ['company', 'culture', 'benefits', 'team', 'about us', 'mission']
        }

    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        for skill, keywords in self.skill_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_skills.append(skill)
                    break  # Don't add the same skill multiple times
        
        return list(set(found_skills))  # Remove duplicates

    def classify_experience_level(self, text: str) -> str:
        """Classify experience level based on text content"""
        if not text:
            return "Not Specified"
        
        text_lower = text.lower()
        
        # Check for specific patterns
        for level, keywords in self.experience_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        # Look for year patterns
        year_pattern = r'(\d+)[\+\-\s]*years?'
        matches = re.findall(year_pattern, text_lower)
        
        if matches:
            years = max([int(match) for match in matches])
            if years <= 2:
                return "Entry Level"
            elif years <= 5:
                return "Mid Level"
            else:
                return "Senior Level"
        
        return "Not Specified"

    def classify_content_type(self, title: str, description: str, source: str) -> str:
        """Classify the type of content"""
        combined_text = f"{title} {description}".lower()
        
        # Source-based classification
        if source == "StackOverflow":
            return "Interview Question"
        elif source == "Reddit" and any(word in combined_text for word in ['advice', 'help', 'career']):
            return "Career Advice"
        
        # Content-based classification
        for content_type, keywords in self.content_types.items():
            for keyword in keywords:
                if keyword in combined_text:
                    return content_type
        
        # Default based on common patterns
        if any(word in combined_text for word in ['apply', 'position', 'hiring']):
            return "Job Description"
        elif '?' in title:
            return "Interview Question"
        
        return "Technical Discussion"

    def calculate_relevance_score(self, text: str) -> float:
        """Calculate relevance score for software engineering (0-1)"""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        tech_keywords = [
            'software', 'developer', 'engineer', 'programming', 'code', 'development',
            'python', 'java', 'javascript', 'react', 'node', 'api', 'database',
            'cloud', 'aws', 'docker', 'git', 'algorithm', 'data structure'
        ]
        
        found_keywords = sum(1 for keyword in tech_keywords if keyword in text_lower)
        max_possible = len(tech_keywords)
        
        # Base score from keyword density
        base_score = min(found_keywords / 10, 1.0)  # Normalize to max 1.0
        
        # Bonus for longer, more detailed content
        length_bonus = min(len(text) / 1000, 0.2)  # Up to 0.2 bonus for length
        
        return min(base_score + length_bonus, 1.0)

    def annotate_entry(self, entry: Dict) -> Dict:
        """Annotate a single entry with all labels"""
        title = entry.get('title', '')
        description = entry.get('description', '')
        company = entry.get('company', '')
        source = entry.get('source', '')
        
        # Combine text for analysis
        full_text = f"{title} {description}"
        
        # Generate annotations
        annotations = {
            'skill_tags': self.extract_skills(full_text),
            'experience_level': self.classify_experience_level(full_text),
            'content_type': self.classify_content_type(title, description, source),
            'relevance_score': round(self.calculate_relevance_score(full_text), 2),
            'text_length': len(description),
            'has_requirements': 'requirements' in full_text.lower() or 'required' in full_text.lower(),
            'remote_work': any(word in full_text.lower() for word in ['remote', 'work from home', 'distributed', 'telecommute']),
            'company_size': self.estimate_company_size(company, full_text)
        }
        
        # Create annotated entry
        annotated_entry = entry.copy()
        annotated_entry.update(annotations)
        
        return annotated_entry

    def estimate_company_size(self, company: str, text: str) -> str:
        """Estimate company size based on context clues"""
        text_lower = f"{company} {text}".lower()
        
        startup_indicators = ['startup', 'seed', 'series a', 'early stage', 'fast-growing']
        large_corp_indicators = ['fortune', 'enterprise', 'global', 'multinational', 'thousands']
        
        if any(indicator in text_lower for indicator in startup_indicators):
            return "Startup"
        elif any(indicator in text_lower for indicator in large_corp_indicators):
            return "Large Corporation"
        else:
            return "Medium Company"

    def annotate_data(self, input_file: str, output_file: str) -> int:
        """Main annotation function"""
        print(f" Annotating data from {input_file}...")
        
        try:
            # Load cleaned data
            with open(input_file, 'r', encoding='utf-8') as f:
                cleaned_data = json.load(f)
            
            print(f"Loaded {len(cleaned_data)} cleaned entries")
            
            # Annotate each entry
            for entry in cleaned_data:
                annotated_entry = self.annotate_entry(entry)
                self.annotated_data.append(annotated_entry)
            
            # Sort by relevance score (highest first) and take top entries
            self.annotated_data.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            print(f"Annotated {len(self.annotated_data)} entries")
            
            # Save annotated data
            self.save_annotated_data(output_file)
            
            return len(self.annotated_data)
            
        except Exception as e:
            print(f"Error in annotation: {e}")
            raise

    def save_annotated_data(self, filename: str):
        """Save annotated data to JSON and CSV"""
        import os
        os.makedirs("data", exist_ok=True)
        
        # Save as JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.annotated_data, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        csv_filename = filename.replace('.json', '.csv')
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            if self.annotated_data:
                # Convert skill_tags list to string for CSV
                csv_data = []
                for entry in self.annotated_data:
                    csv_entry = entry.copy()
                    csv_entry['skill_tags'] = ', '.join(csv_entry.get('skill_tags', []))
                    csv_data.append(csv_entry)
                
                writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                writer.writeheader()
                writer.writerows(csv_data)
        
        print(f"Saved annotated data to {filename} and {csv_filename}")

    def get_annotation_statistics(self) -> Dict[str, Any]:
        """Get statistics about the annotations"""
        if not self.annotated_data:
            return {}
        
        stats = {
            'total_entries': len(self.annotated_data),
            'experience_levels': {},
            'content_types': {},
            'top_skills': {},
            'avg_relevance_score': 0,
            'remote_work_percentage': 0,
            'company_sizes': {}
        }
        
        total_relevance = 0
        remote_count = 0
        all_skills = []
        
        for entry in self.annotated_data:
            # Experience levels
            exp_level = entry.get('experience_level', 'Unknown')
            stats['experience_levels'][exp_level] = stats['experience_levels'].get(exp_level, 0) + 1
            
            # Content types
            content_type = entry.get('content_type', 'Unknown')
            stats['content_types'][content_type] = stats['content_types'].get(content_type, 0) + 1
            
            # Skills
            skills = entry.get('skill_tags', [])
            all_skills.extend(skills)
            
            # Relevance score
            total_relevance += entry.get('relevance_score', 0)
            
            # Remote work
            if entry.get('remote_work', False):
                remote_count += 1
            
            # Company sizes
            company_size = entry.get('company_size', 'Unknown')
            stats['company_sizes'][company_size] = stats['company_sizes'].get(company_size, 0) + 1
        
        # Calculate averages and percentages
        stats['avg_relevance_score'] = total_relevance / len(self.annotated_data)
        stats['remote_work_percentage'] = (remote_count / len(self.annotated_data)) * 100
        
        # Top skills
        from collections import Counter
        skill_counts = Counter(all_skills)
        stats['top_skills'] = dict(skill_counts.most_common(10))
        
        return stats

    def export_sample_annotations(self, sample_size: int = 20, filename: str = "data/sample_annotations.json"):
        """Export a sample of annotated data for review"""
        if not self.annotated_data:
            print("No annotated data available")
            return
        
        # Take top entries by relevance score
        sample_data = self.annotated_data[:min(sample_size, len(self.annotated_data))]
        
        # Create a simplified view for easy review
        simplified_sample = []
        for i, entry in enumerate(sample_data, 1):
            simplified_entry = {
                'id': i,
                'title': entry.get('title', ''),
                'company': entry.get('company', ''),
                'description_preview': entry.get('description', '')[:200] + "..." if len(entry.get('description', '')) > 200 else entry.get('description', ''),
                'annotations': {
                    'skill_tags': entry.get('skill_tags', []),
                    'experience_level': entry.get('experience_level', ''),
                    'content_type': entry.get('content_type', ''),
                    'relevance_score': entry.get('relevance_score', 0),
                    'remote_work': entry.get('remote_work', False),
                    'company_size': entry.get('company_size', '')
                }
            }
            simplified_sample.append(simplified_entry)
        
        # Save sample
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(simplified_sample, f, indent=2, ensure_ascii=False)
        
        print(f"Exported {len(simplified_sample)} sample annotations to {filename}")

if __name__ == "__main__":
    annotator = DataAnnotator()
    count = annotator.annotate_data("data/cleaned_jobs.json", "data/annotated_jobs.json")
    
    # Export sample for review
    annotator.export_sample_annotations(sample_size=20)
    
    # Print statistics
    stats = annotator.get_annotation_statistics()
    print("\nANNOTATION STATISTICS:")
    print(f"Total entries: {stats.get('total_entries', 0)}")
    print(f"Average relevance score: {stats.get('avg_relevance_score', 0):.2f}")
    print(f"Remote work opportunities: {stats.get('remote_work_percentage', 0):.1f}%")
    print(f"Experience levels: {stats.get('experience_levels', {})}")
    print(f"Content types: {stats.get('content_types', {})}")
    print(f"Top skills: {list(stats.get('top_skills', {}).keys())[:5]}")
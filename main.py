#!/usr/bin/env python3
"""
Data Engineering Pipeline for Job Data Processing
"""

import os
import sys
from scraper.job_scraper import JobScraper
from processing.data_cleaner import DataCleaner
from processing.data_annotator import DataAnnotator

def main():
    """Main pipeline execution"""
    print(" Starting Data Engineering Pipeline for Job Data")
    print("=" * 60)
    
    # Step 1: Data Scraping
    print("\n STEP 1: DATA SCRAPING")
    print("-" * 30)
    
    scraper = JobScraper()
    try:
        scraper.scrape_all(total_count=60)  # Get 60+ entries
        count = scraper.save_raw_data("data/raw_jobs.json")
        print(f" Successfully scraped {count} job entries")
    except Exception as e:
        print(f" Error in scraping: {e}")
        return False
    
    # Step 2: Data Cleaning  
    print("\n🧹 STEP 2: DATA CLEANING")
    print("-" * 30)
    
    cleaner = DataCleaner()
    try:
        cleaned_count = cleaner.clean_data("data/raw_jobs.json", "data/cleaned_jobs.json")
        print(f"Successfully cleaned data: {cleaned_count} entries")
    except Exception as e:
        print(f"Error in cleaning: {e}")
        return False
    
    # Step 3: Data Annotation
    print("\n  STEP 3: DATA ANNOTATION")
    print("-" * 30)
    
    annotator = DataAnnotator()
    try:
        annotated_count = annotator.annotate_data("data/cleaned_jobs.json", "data/annotated_jobs.json")
        print(f"Successfully annotated data: {annotated_count} entries")
    except Exception as e:
        print(f" Error in annotation: {e}")
        return False
    
    # Summary
    print("\n PIPELINE SUMMARY")
    print("=" * 60)
    print(f"Raw data: data/raw_jobs.json & data/raw_jobs.csv")
    print(f"Cleaned data: data/cleaned_jobs.json & data/cleaned_jobs.csv") 
    print(f" Annotated data: data/annotated_jobs.json & data/annotated_jobs.csv")
    print("\n Pipeline completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
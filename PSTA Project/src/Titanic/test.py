#!/usr/bin/env python3
"""
Test script for PDF generation from markdown.
Run this script after implementing the fixes to verify that PDF generation works correctly.
"""

import os
import sys
import argparse
from utils import markdown_to_pdf  # Import from your utils.py file

def main():
    parser = argparse.ArgumentParser(description='Generate PDF from markdown file')
    parser.add_argument('--input', '-i', required=True, help='Input markdown file')
    parser.add_argument('--output', '-o', required=False, help='Output PDF file (default: same name as input with .pdf extension)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        return 1
    
    # Determine output file
    if args.output:
        output_file = args.output
    else:
        output_file = os.path.splitext(args.input)[0] + '.pdf'
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    
    print(f"Generating PDF from {args.input} to {output_file}...")
    
    # Extract program name from filename for documentation title
    program_name = os.path.basename(os.path.splitext(args.input)[0])
    
    # Generate PDF
    success = markdown_to_pdf(
        output_file=output_file,
        file_path=args.input
    )
    
    if success:
        print(f"PDF successfully generated: {output_file}")
        return 0
    else:
        print("PDF generation failed. Check for alternative output formats.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
import csv
import os
import re
import shutil
import glob
import base64
import markdown
import tempfile
import datetime
import sys
import subprocess
from typing import Text, Optional
import concurrent.futures


def escape_invalid_chars(s):
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', lambda m: '\\u{:04x}'.format(ord(m.group(0))), s)


def create_csv(name, column_names, result):
    # Open csv file for writing
    with open(f'./input/{name}.csv', mode='w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(result)


def read_first_lines_from_file(name):
    file_path = "./input/" + name
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        lines = [next(reader) for _ in range(2)]
    return lines


def delete_all_files_in_directory(directory_path):
    if os.path.exists(directory_path):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)


def save_uploaded_file(uploaded_file, directory_path):
    delete_all_files_in_directory(directory_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    file_path = os.path.join(directory_path, uploaded_file.name)
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(uploaded_file, f)
    return file_path


def read_files(directory_path):
    file_contents = {}
    for file_path in glob.glob(os.path.join(directory_path, '*')):
        with open(file_path, 'r') as file:
            content = file.read()
            file_name = os.path.basename(file_path)
            file_contents[file_name] = content
    return file_contents


def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def find_file(file_name):
    """
    Enhanced file finder that attempts to locate a file by name in the input directory
    using multiple search strategies.
    
    Args:
        file_name: Name of the file to find
        
    Returns:
        str or None: Path to the found file or None if not found
    """
    # Search in the standard path first
    for root, dirs, files in os.walk('./input/BF4000M1/'):
        if file_name in files:
            return os.path.join(root, file_name)
            
    # Try alternative locations if not found
    alternative_paths = [
        './input/',  # Root input directory
        './input/uploaded/',  # Uploaded files directory
        './',  # Current directory
    ]
    
    for base_path in alternative_paths:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                # Try exact match
                if file_name in files:
                    return os.path.join(root, file_name)
                
                # Try case-insensitive match
                for f in files:
                    if f.upper() == file_name.upper():
                        return os.path.join(root, f)
    
    # Not found            
    return None


def save_as_markdown(input_text, file_path):
    """Save text as a markdown file, ensuring the directory exists"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(input_text)


# Function to convert image to base64 string
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def node_exists(node_id, st):
    for node in st.session_state['nodes']:
        if node.id == node_id:
            return True
    return False


def detect_language(file_path):
    """
    Detects whether a file contains COBOL or PL/1 code based on content analysis.
    
    Args:
        file_path: Path to the program file
        
    Returns:
        str: 'COBOL' or 'PL1' based on detected language
    """
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            content = file.read(4000)  # Read first 4000 chars for detection
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        with open(file_path, "r", encoding='latin-1', errors='replace') as file:
            content = file.read(4000)
    
    # Define distinctive patterns for each language
    cobol_patterns = [
        r'(?i)\bIDENTIFICATION\s+DIVISION\b',
        r'(?i)\bPROCEDURE\s+DIVISION\b',
        r'(?i)\bDATA\s+DIVISION\b',
        r'(?i)\bWORKING-STORAGE\s+SECTION\b',
        r'(?i)\bFILE\s+SECTION\b',
        r'(?i)\bPROGRAM-ID\b',
        r'(?i)\bLINKAGE\s+SECTION\b',
        r'(?i)\bCONFIGURATION\s+SECTION\b'
    ]
    
    pl1_patterns = [
        r'(?i)\bPROC\s+OPTIONS\b',
        r'(?i)\bDCL\b',
        r'(?i)\bBEGIN\b',
        r'(?i)\bEND\b',
        r'(?i)\bPROCEDURE\b',
        r'(?i)\bDECLARE\b',
        r'(?i)\bBUILTIN\b',
        r'(?i)\bDO\s+WHILE\b',
        r'(?i)\bIF\s+THEN\s+ELSE\b'
    ]
    
    # Count matches for each language
    cobol_score = sum(1 for pattern in cobol_patterns if re.search(pattern, content))
    pl1_score = sum(1 for pattern in pl1_patterns if re.search(pattern, content))
    
    # Determine language based on scores
    if cobol_score > pl1_score:
        return 'COBOL'
    elif pl1_score > cobol_score:
        return 'PL1'
    else:
        # If scores are equal, check for more definitive markers
        if re.search(r'(?i)\bPROGRAM-ID\b', content):
            return 'COBOL'
        if re.search(r'(?i)\bPROC\s+OPTIONS\b', content):
            return 'PL1'
        
        # Default to COBOL if we can't determine
        return 'COBOL'


def get_code_complexity(code_chunk):
    """
    Estimates code complexity based on various factors.
    
    Args:
        code_chunk: A string containing code
        
    Returns:
        float: Complexity score (higher = more complex)
    """
    # Count control structures
    if_count = len(re.findall(r'\bIF\b', code_chunk, re.IGNORECASE))
    loop_count = len(re.findall(r'\b(PERFORM|DO|UNTIL|VARYING)\b', code_chunk, re.IGNORECASE))
    case_count = len(re.findall(r'\b(EVALUATE|SELECT|WHEN|CASE)\b', code_chunk, re.IGNORECASE))
    
    # Count unique variables (approximate)
    words = re.findall(r'\b[A-Z0-9][A-Z0-9\-\_]+\b', code_chunk, re.IGNORECASE)
    unique_vars = len(set(words))
    
    # Count SQL or database operations
    sql_ops = len(re.findall(r'\b(SELECT|INSERT|UPDATE|DELETE|EXEC\s+SQL)\b', code_chunk, re.IGNORECASE))
    
    # Calculate complexity
    complexity = (if_count * 1.0) + (loop_count * 1.5) + (case_count * 1.2) + (unique_vars * 0.1) + (sql_ops * 2.0)
    
    return complexity


def adaptive_chunk_size(code_chunk, default_size=10000):
    """
    Determines appropriate chunk size based on code complexity.
    
    Args:
        code_chunk: A string containing code
        default_size: The default maximum chunk size
        
    Returns:
        int: Recommended chunk size
    """
    complexity = get_code_complexity(code_chunk)
    
    # Adjust size based on complexity
    if complexity > 50:  # Very complex
        return default_size // 2  # Smaller chunks for complex code
    elif complexity < 10:  # Very simple
        return default_size * 2  # Larger chunks for simple code
    else:
        return default_size  # Default size for moderate complexity


def optimized_file_splitter(file_path, language=None, max_chunks=5):
    """
    Optimized file splitter that intelligently divides code for analysis.
    It adaptively adjusts chunk size based on complexity and limits total chunks.
    
    Args:
        file_path: Path to the program file
        language: 'COBOL' or 'PL1', detected automatically if None
        max_chunks: Maximum number of chunks to create
        
    Returns:
        list: List of text chunks that follow appropriate structural boundaries
    """
    # Detect language if not provided
    if language is None:
        language = detect_language(file_path)
    
    # Read the file with error handling
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            file_content = file.read()
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        with open(file_path, "r", encoding='latin-1', errors='replace') as file:
            file_content = file.read()
    
    # If file is small, return it as a single chunk
    if len(file_content) < 15000:
        return [file_content]
    
    # Define language-specific structural markers
    if language == 'COBOL':
        primary_markers = [
            r'(?i)(\s+|^)(IDENTIFICATION\s+DIVISION|ID\s+DIVISION)(\s+|\.)',
            r'(?i)(\s+|^)(ENVIRONMENT\s+DIVISION)(\s+|\.)',
            r'(?i)(\s+|^)(DATA\s+DIVISION)(\s+|\.)',
            r'(?i)(\s+|^)(PROCEDURE\s+DIVISION)(\s+|\.)'
        ]
        secondary_markers = [
            r'(?i)(\s+|^)(CONFIGURATION\s+SECTION)(\s+|\.)',
            r'(?i)(\s+|^)(INPUT-OUTPUT\s+SECTION)(\s+|\.)',
            r'(?i)(\s+|^)(FILE\s+SECTION)(\s+|\.)',
            r'(?i)(\s+|^)(WORKING-STORAGE\s+SECTION)(\s+|\.)',
            r'(?i)(\s+|^)(LINKAGE\s+SECTION)(\s+|\.)'
        ]
    else:  # PL1
        primary_markers = [
            r'(?i)(\s+|^)([A-Z0-9_]+\s*:\s*PROC\b)',
            r'(?i)(\s+|^)(PROCEDURE\s+OPTIONS)',
            r'(?i)(\s+|^)(END\s+[A-Z0-9_]+\s*;)'
        ]
        secondary_markers = [
            r'(?i)(\s+|^)(BEGIN\s*;)',
            r'(?i)(\s+|^)(END\s*;)',
            r'(?i)(\s+|^)(DCL\s+)',
            r'(?i)(\s+|^)(DECLARE\s+)'
        ]
    
    # First, try to split by primary markers (divisions or procedures)
    primary_split_points = []
    for pattern in primary_markers:
        for match in re.finditer(pattern, file_content):
            primary_split_points.append(match.start())
    
    primary_split_points.sort()
    
    # If we have enough primary split points, use them
    if len(primary_split_points) >= 2:
        chunks = []
        start_pos = 0
        
        # Add the program header as context to each chunk
        header_size = min(1000, primary_split_points[0]) if primary_split_points else 1000
        header = file_content[:header_size]
        
        # Create chunks from primary split points
        for i, pos in enumerate(primary_split_points):
            # Determine if this is a good split point (not too small)
            if i > 0 and pos - primary_split_points[i-1] < 2000:
                continue  # Skip this split point if resulting chunk would be too small
                
            if pos > start_pos:
                chunk = header + "\n\n" + file_content[start_pos:pos]
                chunks.append(chunk)
                start_pos = pos
        
        # Add the final chunk
        if start_pos < len(file_content):
            chunks.append(header + "\n\n" + file_content[start_pos:])
        
        # If we have a reasonable number of chunks, return them
        if 2 <= len(chunks) <= max_chunks:
            return chunks
    
    # If primary splitting didn't work well, try secondary markers
    secondary_split_points = []
    for pattern in secondary_markers:
        for match in re.finditer(pattern, file_content):
            secondary_split_points.append(match.start())
    
    # Combine with primary split points
    all_split_points = list(set(primary_split_points + secondary_split_points))
    all_split_points.sort()
    
    if len(all_split_points) >= 2:
        chunks = []
        start_pos = 0
        
        # Add the program header as context to each chunk
        header_size = min(1000, all_split_points[0]) if all_split_points else 1000
        header = file_content[:header_size]
        
        # Target chunk size to get desired number of chunks
        target_chunk_size = len(file_content) // max_chunks
        
        current_pos = 0
        for pos in all_split_points:
            if pos - current_pos >= target_chunk_size:
                chunk = header + "\n\n" + file_content[current_pos:pos]
                chunks.append(chunk)
                current_pos = pos
        
        # Add the final chunk
        if current_pos < len(file_content):
            chunks.append(header + "\n\n" + file_content[current_pos:])
        
        # If we have a reasonable number of chunks, return them
        if len(chunks) <= max_chunks:
            return chunks
    
    # If structured splitting doesn't give good results, fall back to simple size-based splitting
    chunks = []
    total_size = len(file_content)
    chunk_size = total_size // max_chunks
    
    # Add the program header as context to each chunk
    header_size = min(1000, len(file_content) // 10)
    header = file_content[:header_size]
    
    for i in range(0, max_chunks - 1):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        
        # Include header with each chunk
        chunks.append(header + "\n\n" + file_content[start:end])
    
    # Add the final chunk
    chunks.append(header + "\n\n" + file_content[(max_chunks - 1) * chunk_size:])
    
    return chunks


def generate_enhanced_pdf(markdown_content, output_file, program_name, language='COBOL'):
    """
    Enhanced PDF generation with professional styling, table of contents, and metadata.
    
    Args:
        markdown_content: Markdown content to convert to PDF
        output_file: Path where the PDF will be saved
        program_name: Name of the program (for metadata)
        language: Programming language ('COBOL' or 'PL1')
        
    Returns:
        bool: Success or failure of PDF generation
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        # Step 1: Install required dependencies if not already installed
        try:
            import weasyprint
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint", "markdown", "pyyaml"])
        
        # Step 2: Process markdown content to ensure proper structure
        # Extract TOC items for reference
        toc_items = re.findall(r'^(#{1,3})\s+(.*?)$', markdown_content, re.MULTILINE)
        
        # Step 3: Create a custom CSS for better formatting
        css = """
        @page {
            size: letter;
            margin: 2cm;
            @top-center {
                content: string(title);
                font-size: 9pt;
                font-family: "Helvetica", sans-serif;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                font-family: "Helvetica", sans-serif;
            }
        }
        
        body {
            font-family: "Helvetica", sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            counter-reset: h1 h2 h3;
        }
        
        h1 {
            string-set: title content();
            color: #003366;
            font-size: 18pt;
            border-bottom: 1pt solid #003366;
            padding-bottom: 5pt;
            margin-top: 24pt;
            page-break-before: always;
        }
        
        h1:first-of-type {
            page-break-before: avoid;
        }
        
        h2 {
            color: #003366;
            font-size: 16pt;
            border-bottom: 0.5pt solid #666666;
            padding-bottom: 3pt;
            margin-top: 18pt;
        }
        
        h3 {
            color: #004d99;
            font-size: 14pt;
            margin-top: 14pt;
        }
        
        h4 {
            color: #004d99;
            font-size: 12pt;
            margin-top: 12pt;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15pt 0;
        }
        
        th, td {
            border: 1pt solid #cccccc;
            padding: 8pt;
            text-align: left;
        }
        
        th {
            background-color: #edf2f7;
            font-weight: bold;
        }
        
        code {
            font-family: "Courier New", monospace;
            background-color: #f5f5f5;
            padding: 2pt 4pt;
            border-radius: 3pt;
        }
        
        pre {
            background-color: #f5f5f5;
            padding: 10pt;
            border-radius: 5pt;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        
        ul, ol {
            margin-top: 5pt;
            margin-bottom: 10pt;
        }
        
        li {
            margin-bottom: 3pt;
        }
        
        .cover-page {
            text-align: center;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .cover-title {
            font-size: 24pt;
            color: #003366;
            margin-bottom: 10pt;
        }
        
        .cover-subtitle {
            font-size: 18pt;
            color: #666666;
            margin-bottom: 30pt;
        }
        
        .cover-language {
            font-size: 14pt;
            color: #666666;
            margin-bottom: 20pt;
        }
        
        .cover-date {
            font-size: 12pt;
            color: #666666;
        }
        
        .toc-heading {
            font-size: 18pt;
            color: #003366;
            margin-top: 30pt;
            margin-bottom: 20pt;
        }
        
        .toc-entry {
            margin-bottom: 5pt;
        }
        
        .toc-entry a {
            text-decoration: none;
            color: #000000;
        }
        
        .toc-entry .page-number {
            float: right;
        }
        
        .toc-level-1 {
            font-weight: bold;
            margin-left: 0;
        }
        
        .toc-level-2 {
            margin-left: 20pt;
        }
        
        .toc-level-3 {
            margin-left: 40pt;
        }
        """
        
        # Step 4: Create a cover page and TOC
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        cover_page = f"""
        <div class="cover-page">
            <div class="cover-title">{program_name}</div>
            <div class="cover-subtitle">Program Documentation</div>
            <div class="cover-language">{language} Program</div>
            <div class="cover-date">Generated on: {current_date}</div>
        </div>
        """
        
        # Create TOC
        toc_content = '<div class="toc-heading">Table of Contents</div>\n'
        
        for heading_level, heading_text in toc_items:
            level = len(heading_level)  # Number of # characters
            heading_text = heading_text.strip()
            toc_content += f'<div class="toc-entry toc-level-{level}"><a href="#{heading_text.lower().replace(" ", "-")}">{heading_text}</a></div>\n'
        
        # Step 5: Convert markdown to HTML with improved formatting
        import markdown
        
        # Add IDs to headings for TOC links
        def add_header_ids(match):
            heading_marker = match.group(1)
            heading_text = match.group(2)
            header_id = heading_text.lower().replace(" ", "-")
            return f'{heading_marker} {heading_text} {{#{header_id}}}'
        
        markdown_content = re.sub(r'^(#{1,3})\s+(.*?)$', add_header_ids, markdown_content, flags=re.MULTILINE)
        
        html_content = markdown.markdown(
            markdown_content, 
            extensions=['tables', 'fenced_code', 'codehilite', 'toc']
        )
        
        # Combine everything
        complete_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{program_name} - Documentation</title>
            <style>{css}</style>
        </head>
        <body>
            {cover_page}
            
            <div style="page-break-before: always;"></div>
            {toc_content}
            
            <div style="page-break-before: always;"></div>
            {html_content}
        </body>
        </html>
        """
        
        # Step 6: Generate PDF using WeasyPrint
        import weasyprint
        
        weasyprint.HTML(string=complete_html).write_pdf(output_file)
        
        return True
        
    except Exception as e:
        print(f"Error with enhanced PDF generation: {e}")
        
        # Fall back to basic HTML generation if PDF fails
        try:
            html_output = output_file.replace('.pdf', '.html')
            with open(html_output, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>{program_name} Documentation</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
                        h1, h2, h3 {{ color: #2c3e50; }}
                        pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
                    </style>
                </head>
                <body>
                    <h1>{program_name} Documentation ({language})</h1>
                    {markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])}
                </body>
                </html>""")
            
            print(f"Saved HTML version instead at: {html_output}")
            
            # Try simpler PDF conversion as last resort
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                return True
            except:
                # Just save plain markdown if all else fails
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                return False
                
        except Exception as e2:
            print(f"Error with fallback HTML generation: {e2}")
            # Last resort: save as plain text
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            return False


def markdown_to_pdf(output_file: Text, markdown_content: Optional[Text] = None, file_path: Optional[Text] = None):
    """
    Basic markdown to PDF conversion using the markdown_pdf library.
    
    Args:
        output_file: Path to save the PDF file
        markdown_content: Markdown content to convert (optional)
        file_path: Path to a markdown file to convert (optional)
    """
    if markdown_content is None and file_path is None:
        raise ValueError("Either markdown_content or file_path must be provided.")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        # Try to install required packages if not present
        try:
            import weasyprint
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint", "markdown"])
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content if markdown_content is not None else open(file_path, 'r').read(),
            extensions=['tables', 'fenced_code']
        )
        
        # Add basic styling
        html_with_css = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>PDF Document</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Save HTML to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as temp_file:
            temp_file.write(html_with_css)
            temp_html = temp_file.name
        
        # Convert HTML to PDF
        import weasyprint
        weasyprint.HTML(filename=temp_html).write_pdf(output_file)
        
        # Clean up temp file
        os.unlink(temp_html)
            
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        
        # Fallback: save as plain text with .pdf extension
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content or '')
            
        return False
import re
import os

def parse_pl1_structures(file_name, output_dir):
    """
    Parses a PL/1 file, extracts structural elements (excluding single-line patterns and END statements),
    and stores them in separate files based on detected patterns.
    Everything before the first recognized pattern is also saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    with open(file_name, 'r') as file:
        lines = file.readlines()
    code_chunks = []
    current_chunk = []
    start_line = 1
    current_structure = 'GENERAL'
    # Regex patterns for PL/I structures
    proc_pattern = re.compile(r'^\s*([\w-]+):\s*PROC\s*.*;')
    percent_dcl_pattern = re.compile(r'^\s*%DCL\b\s+.*')
    dcl_start_pattern = re.compile(r'^\s*DCL\b\s+.*')
    do_while_pattern = re.compile(r'^\s*DO\s+WHILE\b.*')
    def save_current_chunk():
        """Saves the current chunk into the code_chunks list and resets it."""
        if current_chunk:
            code_chunks.append({
                'type': current_structure,
                'file_name': file_name,
                'start_line': start_line,
                'end_line': i,
                'content': '\n'.join(current_chunk)
            })
    for i, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        # Match PROC definitions
        if proc_pattern.match(stripped_line):
            save_current_chunk()
            current_structure = 'PROCEDURE'
            start_line = i
            current_chunk = [line.rstrip()]
        # Match %DCL statements
        elif percent_dcl_pattern.match(stripped_line):
            save_current_chunk()
            current_structure = '%DCL'
            start_line = i
            current_chunk = [line.rstrip()]
        # Match DCL statements
        elif dcl_start_pattern.match(stripped_line):
            save_current_chunk()
            current_structure = 'DCL'
            start_line = i
            current_chunk = [line.rstrip()]
        # Match DO WHILE loops
        elif do_while_pattern.match(stripped_line):
            save_current_chunk()
            current_structure = 'DO_WHILE'
            start_line = i
            current_chunk = [line.rstrip()]
        else:
            current_chunk.append(line.rstrip())
    # Save the last remaining chunk
    save_current_chunk()
    # Write each extracted code chunk to a separate file
    for chunk in code_chunks:
        output_file_name = os.path.join(output_dir, f"{os.path.basename(file_name)}_{chunk['type']}_{chunk['start_line']}.txt")
        with open(output_file_name, 'w') as output_file:
            output_file.write(f"Type: {chunk['type']}\n")
            output_file.write(f"File: {chunk['file_name']}\n")
            output_file.write(f"Start Line: {chunk['start_line']}, End Line: {chunk['end_line']}\n")
            output_file.write(chunk['content'])
            output_file.write("\n")
    print(f"Code chunks have been saved in {output_dir}")


import re
import os
import shutil
from typing import Dict, List
from datetime import datetime


class PL1FileParser:
    def __init__(self):
        # Define patterns with descriptions for better documentation
        self.patterns: Dict[str, tuple] = {
            'PROCEDURE': (
                r'^\s*([\w-]+):\s*PROC\s*.*;',
                'Procedure declarations'
            ),
            'PCT_DCL': (
                r'^\s*%DCL\b\s+.*',
                'Preprocessor declarations'
            ),
            'DCL': (
                r'^\s*DCL\b\s+.*',
                'Variable declarations'
            ),
            'DO_WHILE': (
                r'^\s*DO\s+WHILE\b.*',
                'DO WHILE loops'
            ),
            'DO_UNTIL': (
                r'^\s*DO\s+UNTIL\b.*',
                'DO UNTIL loops'
            ),
            'DO_FOR': (
                r'^\s*DO\s+FOR\b.*',
                'DO FOR loops'
            ),
            'IF_THEN': (
                r'^\s*IF\b.*\bTHEN\b.*',
                'IF-THEN statements'
            ),
            'SELECT': (
                r'^\s*SELECT\s*;?$',
                'SELECT statements'
            ),
            'BEGIN': (
                r'^\s*BEGIN\s*;?$',
                'BEGIN blocks'
            ),
            'PACKAGE': (
                r'^\s*PACKAGE\s+.*',
                'Package definitions'
            ),
            'INCLUDE': (
                r'^\s*%INCLUDE\b.*',
                'Include statements'
            )
        }

        # Compile patterns
        self.compiled_patterns = {
            name: re.compile(pattern)
            for name, (pattern, _) in self.patterns.items()
        }

    def cleanup_output_directory(self, output_dir: str) -> None:
        """Remove all files in the output directory."""
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    def parse_pl1_file(self, file_path: str, output_dir: str) -> None:
        """Parse PL/1 file and save structured chunks to separate files."""
        # Create main output directory
        self.cleanup_output_directory(output_dir)

        # Create subdirectories for different chunk types including GENERAL
        chunk_types = list(self.patterns.keys()) + ['GENERAL']
        for chunk_type in chunk_types:
            chunk_dir = os.path.join(output_dir, chunk_type)
            os.makedirs(chunk_dir, exist_ok=True)

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Initialize parsing variables
        chunks = []
        dcl_chunks = []
        current_chunk = []
        start_line = 1
        current_type = 'GENERAL'
        nesting_level = 0

        def save_chunk(end_line: int) -> None:
            """Save current chunk with metadata."""
            if current_chunk:
                chunk_data = {
                    'type': current_type,
                    'file_name': os.path.basename(file_path),
                    'start_line': start_line,
                    'end_line': end_line,
                    'nesting_level': nesting_level,
                    'content': '\n'.join(current_chunk),
                    'timestamp': datetime.now().isoformat()
                }

                # Collect DCL statements separately
                if current_type == 'DCL':
                    dcl_chunks.append(chunk_data)
                else:
                    chunks.append(chunk_data)

        # Parse file
        for i, line in enumerate(lines, 1):
            stripped_line = line.strip()

            # Skip empty lines and comments
            if not stripped_line or stripped_line.startswith('/*'):
                current_chunk.append(line.rstrip())
                continue

            # Check for END statements
            if re.match(r'^\s*END\s*;?$', stripped_line):
                save_chunk(i)
                nesting_level = max(0, nesting_level - 1)
                current_type = 'GENERAL'
                start_line = i
                current_chunk = [line.rstrip()]
                continue

            # Check for new chunk patterns
            new_type = None
            for pattern_name, pattern in self.compiled_patterns.items():
                if pattern.match(stripped_line):
                    new_type = pattern_name
                    break

            if new_type:
                save_chunk(i - 1)
                current_type = new_type
                start_line = i
                current_chunk = [line.rstrip()]
                if new_type in ['PROCEDURE', 'DO_WHILE', 'DO_UNTIL', 'DO_FOR', 'BEGIN']:
                    nesting_level += 1
            else:
                current_chunk.append(line.rstrip())

        # Save final chunk
        save_chunk(len(lines))

        # Write regular chunks to files
        for chunk in chunks:
            try:
                base_name = os.path.splitext(os.path.basename(chunk['file_name']))[0]
                chunk_filename = f"{base_name}_{chunk['type']}_{chunk['start_line']:04d}.txt"
                chunk_dir = os.path.join(output_dir, chunk['type'])
                chunk_path = os.path.join(chunk_dir, chunk_filename)

                os.makedirs(os.path.dirname(chunk_path), exist_ok=True)

                with open(chunk_path, 'w', encoding='utf-8') as f:
                    f.write(f"{'=' * 80}\n")
                    f.write(f"Type: {chunk['type']}\n")
                    f.write(f"Description: {self.patterns.get(chunk['type'], ('', 'General code'))[1]}\n")
                    f.write(f"File: {chunk['file_name']}\n")
                    f.write(f"Lines: {chunk['start_line']}-{chunk['end_line']}\n")
                    f.write(f"Nesting Level: {chunk['nesting_level']}\n")
                    f.write(f"Extracted: {chunk['timestamp']}\n")
                    f.write(f"{'=' * 80}\n\n")
                    f.write(chunk['content'])
                    f.write("\n")

            except Exception as e:
                print(f"Error writing chunk {chunk_filename}: {e}")

        # Write all DCL chunks to a single file
        if dcl_chunks:
            dcl_file_path = os.path.join(output_dir, 'DCL', 'all_DCLs.txt')
            try:
                with open(dcl_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"{'=' * 80}\n")
                    f.write(f"Combined DCL Statements from {os.path.basename(file_path)}\n")
                    f.write(f"Extracted: {datetime.now().isoformat()}\n")
                    f.write(f"{'=' * 80}\n\n")

                    for chunk in dcl_chunks:
                        f.write(f"\n{'=' * 40}\n")
                        f.write(f"Lines: {chunk['start_line']}-{chunk['end_line']}\n")
                        f.write(f"{'=' * 40}\n")
                        f.write(chunk['content'])
                        f.write("\n")

                # print(f"DCL statements written to: {dcl_file_path}")
            except Exception as e:
                print(f"Error writing DCL file: {e}")


def main():
    parser = PL1FileParser()
    input_file = "../src/input/P3BF625.PGM"
    output_dir = "output"

    parser.parse_pl1_file(input_file, output_dir)
    print(f"Parsing completed. Results saved in: {output_dir}")


if __name__ == "__main__":
    main()
    # file_path = "../src/input/P3BF625.PGM"
    # output_path = "output"
    #
    # parse_pl1_structures(file_path, output_path)


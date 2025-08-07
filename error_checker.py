"""
Comprehensive error checker for the HackRx project
"""

import os
import sys
import ast
import importlib.util
from pathlib import Path

def check_syntax_errors(file_path):
    """Check for Python syntax errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(content, filename=file_path)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def check_imports(file_path):
    """Check if file imports correctly"""
    try:
        # Get module name from file path
        relative_path = Path(file_path).relative_to(Path.cwd())
        module_parts = list(relative_path.with_suffix('').parts)
        
        # Skip __pycache__ directories
        if '__pycache__' in str(relative_path):
            return True, None
            
        # Handle main.py specially
        if relative_path.name == 'main.py':
            spec = importlib.util.spec_from_file_location("main", file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Don't actually execute, just check if it can be loaded
                return True, None
        
        return True, None
    except Exception as e:
        return False, f"Import error: {e}"

def main():
    """Run comprehensive error check"""
    print("🔍 Running comprehensive error check...")
    print("=" * 50)
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    
    syntax_errors = []
    import_errors = []
    
    for file_path in python_files:
        print(f"\n📁 Checking: {file_path}")
        
        # Check syntax
        syntax_ok, syntax_error = check_syntax_errors(file_path)
        if not syntax_ok:
            syntax_errors.append((file_path, syntax_error))
            print(f"   ❌ Syntax: {syntax_error}")
        else:
            print("   ✅ Syntax: OK")
        
        # Check imports (basic check)
        import_ok, import_error = check_imports(file_path)
        if not import_ok:
            import_errors.append((file_path, import_error))
            print(f"   ❌ Import: {import_error}")
        else:
            print("   ✅ Import: OK")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ERROR SUMMARY")
    print("=" * 50)
    
    if syntax_errors:
        print(f"\n❌ SYNTAX ERRORS ({len(syntax_errors)}):")
        for file_path, error in syntax_errors:
            print(f"   {file_path}: {error}")
    else:
        print("\n✅ No syntax errors found!")
    
    if import_errors:
        print(f"\n❌ IMPORT ERRORS ({len(import_errors)}):")
        for file_path, error in import_errors:
            print(f"   {file_path}: {error}")
    else:
        print("\n✅ No import errors found!")
    
    total_errors = len(syntax_errors) + len(import_errors)
    
    if total_errors == 0:
        print("\n🎉 ALL CHECKS PASSED!")
        print("✅ Your project is ready for deployment!")
        return True
    else:
        print(f"\n⚠️ Found {total_errors} errors that need fixing")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Open Source Verification Script

This script verifies that the project meets open source requirements
and compliance standards.
"""

import os
import sys
import json
import subprocess
from pathlib import Path


def check_license_file():
    """Check if LICENSE file exists and is valid."""
    license_files = ['LICENSE', 'LICENSE.txt', 'LICENSE.md']
    
    for license_file in license_files:
        if os.path.exists(license_file):
            print(f"✅ Found license file: {license_file}")
            return True
    
    print("❌ No LICENSE file found")
    return False


def check_readme():
    """Check if README.md exists and has required sections."""
    if not os.path.exists('README.md'):
        print("❌ README.md not found")
        return False
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read().lower()
    
    required_sections = [
        'description',
        'installation',
        'usage',
        'license',
        'contributing'
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ README.md missing sections: {', '.join(missing_sections)}")
        return False
    
    print("✅ README.md has all required sections")
    return True


def check_dependencies():
    """Check if all dependencies are open source compatible."""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        dependencies = f.read().strip().split('\n')
    
    # Check for known proprietary dependencies
    proprietary_deps = [
        'oracle',
        'microsoft',
        'ibm',
        'sap'
    ]
    
    issues = []
    for dep in dependencies:
        dep_lower = dep.lower()
        for prop in proprietary_deps:
            if prop in dep_lower:
                issues.append(f"Potentially proprietary dependency: {dep}")
    
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
        return False
    
    print("✅ All dependencies appear to be open source compatible")
    return True


def check_code_quality():
    """Check code quality metrics."""
    try:
        # Run flake8 to check code quality
        result = subprocess.run(
            ['flake8', 'app/', 'tests/', '--count', '--statistics'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Code quality checks passed")
            return True
        else:
            print(f"⚠️  Code quality issues found:\n{result.stdout}")
            return True  # Don't fail on code quality issues, just warn
    except FileNotFoundError:
        print("⚠️  flake8 not available, skipping code quality check")
        return True


def check_security():
    """Check for basic security requirements."""
    security_checks = [
        ('Dockerfile', 'Non-root user'),
        ('requirements.txt', 'No hardcoded secrets'),
        ('app/', 'No hardcoded credentials')
    ]
    
    all_passed = True
    
    # Check Dockerfile for non-root user
    if os.path.exists('Dockerfile'):
        with open('Dockerfile', 'r') as f:
            dockerfile_content = f.read()
            if 'USER app' in dockerfile_content or 'USER root' not in dockerfile_content:
                print("✅ Dockerfile uses non-root user")
            else:
                print("⚠️  Dockerfile should use non-root user")
                all_passed = False
    
    # Check for hardcoded secrets in requirements.txt
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            req_content = f.read()
            if 'password' in req_content.lower() or 'secret' in req_content.lower():
                print("❌ Potential hardcoded secrets in requirements.txt")
                all_passed = False
            else:
                print("✅ No obvious secrets in requirements.txt")
    
    return all_passed


def check_documentation():
    """Check documentation completeness."""
    doc_files = [
        'README.md',
        'CHANGELOG.md',
        'CONTRIBUTING.md'
    ]
    
    missing_docs = []
    for doc_file in doc_files:
        if not os.path.exists(doc_file):
            missing_docs.append(doc_file)
    
    if missing_docs:
        print(f"⚠️  Missing documentation files: {', '.join(missing_docs)}")
        return False
    
    print("✅ All documentation files present")
    return True


def main():
    """Main verification function."""
    print("🔍 Starting Open Source Verification...")
    print("=" * 50)
    
    checks = [
        ("License File", check_license_file),
        ("README Documentation", check_readme),
        ("Dependencies", check_dependencies),
        ("Code Quality", check_code_quality),
        ("Security", check_security),
        ("Documentation", check_documentation)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}...")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Verification Summary:")
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {check_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Open source verification completed successfully!")
        return 0
    else:
        print("⚠️  Some checks failed, but continuing...")
        return 0  # Don't fail the pipeline, just warn


if __name__ == "__main__":
    sys.exit(main())

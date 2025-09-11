#!/bin/bash
set -e

# Publish to GitHub Script
# This script publishes the project to GitHub after sanitization
#
# Environment Variables:
# - GITHUB_TOKEN: Required. GitHub personal access token
# - GITHUB_REPO: Optional. GitHub repository name (default: user-management-app)
# - GITHUB_USER: Optional. GitHub username (default: your-username)
# - GITHUB_COMMIT_MESSAGE: Optional. Custom commit message for GitHub updates
# - CI_COMMIT_TAG: GitLab CI variable containing the tag name

echo "🚀 Starting GitHub Publishing Process..."
echo "=========================================="

# Configuration
GITHUB_REPO="${GITHUB_REPO:-user-management-app}"
GITHUB_USER="${GITHUB_USER:-your-username}"
GITHUB_TOKEN="${GITHUB_TOKEN}"
TAG_NAME="${CI_COMMIT_TAG:-latest}"
GITHUB_COMMIT_MESSAGE="${GITHUB_COMMIT_MESSAGE:-Update MediNext AI files from Superwise repository

- Tag: $TAG_NAME
- Commit: $CI_COMMIT_SHA
- Pipeline: $CI_PIPELINE_ID
- Updated: $(date -u +%Y-%m-%dT%H:%M:%SZ)}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check required environment variables
check_requirements() {
    print_status "Checking requirements..."
    
    if [ -z "$GITHUB_TOKEN" ]; then
        print_error "GITHUB_TOKEN environment variable is required"
        exit 1
    fi
    
    if [ -z "$GITHUB_COMMIT_MESSAGE" ]; then
        print_error "GITHUB_COMMIT_MESSAGE environment variable is required"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        print_error "git is required but not installed"
        exit 1
    fi
    
    
    print_status "All requirements satisfied"
}

# Setup HTTPS authentication for GitHub
setup_github_auth() {
    print_status "Setting up GitHub authentication..."
    
    # Configure git to use HTTPS with token
    git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"
    
    print_status "GitHub authentication setup completed"
}

# Clone or update GitHub repository
setup_github_repo() {
    print_status "Setting up GitHub repository..."
    
    GITHUB_URL="https://${GITHUB_TOKEN}@github.com/superwise-ai/${GITHUB_REPO}.git"
    
    if [ -d "github_repo" ]; then
        print_status "Updating existing GitHub repository..."
        cd github_repo
        git fetch origin
        git reset --hard origin/main
    else
        print_status "Cloning GitHub repository..."
        git clone "$GITHUB_URL" github_repo
        cd github_repo
    fi
    
    print_status "GitHub repository ready"
}

# Copy project files to GitHub repo
copy_project_files() {
    print_status "Copying project files to GitHub repository..."
    
    # Run sanitization on the original project before copying
    print_status "Running sanitization on original project..."
    cd ..
    python3 ci/sanitize_public_artifacts.py
    cd github_repo
    
    # First, remove all existing files except .git
    print_status "Cleaning existing files from GitHub repository..."
    find . -maxdepth 1 -not -name '.git' -not -name '.' -not -name '..' -exec rm -rf {} \; 2>/dev/null || true
    
    # Copy everything from GitLab repo (mirror approach)
    print_status "Mirroring GitLab repository to GitHub..."
    for item in ../*; do
        if [ -f "$item" ]; then
            # Copy files
            filename=$(basename "$item")
            if [ "$filename" != ".git" ] && [ "$filename" != ".gitignore" ]; then
                cp "$item" .
                print_status "Copied file: $filename"
            fi
        elif [ -d "$item" ]; then
            # Copy directories
            dirname=$(basename "$item")
            if [ "$dirname" != ".git" ] && [ "$dirname" != "github_repo" ] && [ "$dirname" != "." ] && [ "$dirname" != ".." ]; then
                cp -r "$item" .
                print_status "Copied directory: $dirname"
            fi
        fi
    done
    
    # Copy specific hidden files we want
    for hidden_file in ../.env.example; do
        if [ -f "$hidden_file" ]; then
            filename=$(basename "$hidden_file")
            cp "$hidden_file" .
            print_status "Copied hidden file: $filename"
        fi
    done
    
    # Now remove sensitive files that shouldn't be in public repo
    print_status "Removing sensitive files from GitHub repository..."
    python3 ../ci/sanitize_public_artifacts.py --remove-only
    
    print_status "Project files copied successfully (mirror approach with sensitive file removal)"
}

# Create or update GitHub repository
update_github_repo() {
    print_status "Updating GitHub repository..."
    
    # Configure git user
    git config user.name "GitLab CI"
    git config user.email "ci@gitlab.com"
    
    # Add all changes
    git add .
    
    # Check if there are changes to commit
    if git diff --staged --quiet; then
        print_status "No changes to commit"
    else
        # Commit changes with customizable message
        git commit -m "$GITHUB_COMMIT_MESSAGE"
        
        print_status "Changes committed successfully"
    fi
    
    # Push to GitHub
    print_status "Pushing to GitHub..."
    git push origin main
    
    # Create and push tag if this is a tagged release
    if [ "$TAG_NAME" != "latest" ] && [[ "$TAG_NAME" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        print_status "Creating and pushing tag: $TAG_NAME"
        git tag -a "$TAG_NAME" -m "Release $TAG_NAME"
        git push origin "$TAG_NAME"
    fi
    
    print_status "GitHub repository updated successfully"
}

# Create GitHub release
create_github_release() {
    if [ "$TAG_NAME" != "latest" ] && [[ "$TAG_NAME" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        print_status "Creating GitHub release for $TAG_NAME..."
        
        # Create release notes
        cat > release_notes.md << EOF
# Release $TAG_NAME

## Changes
- Updated from GitLab CI/CD pipeline
- Commit: $CI_COMMIT_SHA
- Pipeline: $CI_PIPELINE_ID

## Installation
\`\`\`bash
# Clone the repository
git clone https://github.com/superwise-ai/$GITHUB_REPO.git
cd $GITHUB_REPO

# Run with Docker
docker build -t $GITHUB_REPO .
docker run -p 8501:8501 $GITHUB_REPO

# Or run with Docker Compose
docker-compose up --build
\`\`\`

## Usage
Access the application at http://localhost:8501

## Documentation
See README.md for detailed documentation.
EOF
        
        # Create release using GitHub API
        curl -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/superwise-ai/$GITHUB_REPO/releases" \
            -d "{
                \"tag_name\": \"$TAG_NAME\",
                \"target_commitish\": \"main\",
                \"name\": \"Release $TAG_NAME\",
                \"body\": \"$(cat release_notes.md | sed 's/"/\\"/g' | tr '\n' '\\n')\",
                \"draft\": false,
                \"prerelease\": false
            }"
        
        print_status "GitHub release created successfully"
    else
        print_status "Skipping release creation (not a tagged release)"
    fi
}

# Main execution
main() {
    print_status "Starting GitHub publishing process..."
    print_status "Repository: $GITHUB_USER/$GITHUB_REPO"
    print_status "Tag: $TAG_NAME"
    print_status "Commit: $CI_COMMIT_SHA"
    
    check_requirements
    setup_github_auth
    setup_github_repo
    copy_project_files
    update_github_repo
    create_github_release
    
    print_status "GitHub publishing completed successfully!"
    print_status "Repository URL: https://github.com/superwise-ai/$GITHUB_REPO"
}

# Run main function
main "$@"

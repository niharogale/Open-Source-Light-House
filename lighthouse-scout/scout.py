from mcp.server.fastmcp import FastMCP
import os
import git

mcp = FastMCP("Lighthouse-Scout")

@mcp.tool()
def map_repository(path: str) -> str:
    """Recursively maps the file structure and identifies the tech stack."""
    if not os.path.exists(path):
        return "Error: Path does not exist."
    
    structure = []
    tech_stack = set()
    
    for root, dirs, files in os.walk(path):
        # Ignore heavy/irrelevant folders
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'dist']]
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}{os.path.basename(root)}/")
        
        for f in files:
            structure.append(f"{indent}    {f}")
            if f.endswith('.py'): tech_stack.add("Python")
            if f.endswith(('.ts', '.tsx')): tech_stack.add("TypeScript/React")
            if f.endswith('.cu'): tech_stack.add("CUDA (NVIDIA)")

    return f"Tech Stack: {', '.join(tech_stack)}\n\nStructure:\n" + "\n".join(structure[:50])

@mcp.tool()
def analyze_developer_dna(repo_path: str) -> str:
    """Analyzes recent commits to identify coding patterns and architectural style."""
    try:
        repo = git.Repo(repo_path)
        commits = list(repo.iter_commits(max_count=10))
        
        summary = []
        for c in commits:
            summary.append(f"- {c.summary} (by {c.author})")
            
        return "Recent Patterns found in commits:\n" + "\n".join(summary)
    except Exception as e:
        return f"Could not analyze Git history: {str(e)}"

if __name__ == "__main__":
    mcp.run()
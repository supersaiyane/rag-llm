import os

ENABLE_GITHUB = os.getenv("ENABLE_GITHUB", "true") == "true"
ENABLE_FILESYSTEM = os.getenv("ENABLE_FILESYSTEM", "false") == "true"

FILESYSTEM_DOC_PATH = os.getenv("FILESYSTEM_DOC_PATH", "/docs-source")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_REPOS = [
    "https://github.com/supersaiyane/Cheatsheet-Kubernetes.git",
    "https://github.com/supersaiyane/Cheatsheet-Docker.git",
    "https://github.com/hashicorp/terraform.git",
]
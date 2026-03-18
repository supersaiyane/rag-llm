import os
import shutil
import subprocess
import tempfile

from storage.git_registry import GitRegistry
from config.settings import GITHUB_TOKEN


IGNORE_DIRS = {
    ".github",
    "internal",
    "test",
    "tests",
    "testdata",
    "examples",
    "scripts",
    "vendor",
    "node_modules",
    ".vscode",
    ".idea"
}

IGNORE_FILES = {
    "changelog.md",
    "license.md",
    "contributing.md",
    "code_of_conduct.md"
}


class GithubConnector:

    def __init__(self, repos, target_path):

        self.repos = repos
        self.target_path = target_path
        self.registry = GitRegistry()

    def get_latest_commit(self, repo):

        repo_url = self._build_repo_url(repo)

        result = subprocess.check_output(
            ["git", "ls-remote", repo_url, "HEAD"]
        ).decode()

        return result.split()[0]

    def _build_repo_url(self, repo):

        if not GITHUB_TOKEN:
            return repo

        return repo.replace(
            "https://",
            f"https://{GITHUB_TOKEN}@"
        )

    def prepare(self):

        print("🐙 Preparing GitHub repositories")

        docs_empty = not any(os.scandir(self.target_path))

        for repo in self.repos:

            repo_name = repo.split("/")[-1].replace(".git", "")
            repo_url = self._build_repo_url(repo)

            latest_commit = self.get_latest_commit(repo)
            stored_commit = self.registry.get_commit(repo)

            # FORCE CLONE IF DOCS EMPTY
            if docs_empty:
                print(f"📦 Docs folder empty → forcing clone: {repo_name}")

            elif stored_commit == latest_commit:
                print(f"⏭ Repo unchanged, skipping: {repo_name}")
                continue

            else:
                print(f"⬇️ Repo changed, indexing: {repo_name}")

            tmp_dir = tempfile.mkdtemp()

            try:

                subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, tmp_dir],
                    check=True
                )

                for root, dirs, files in os.walk(tmp_dir):

                    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

                    for file in files:

                        if not file.endswith(".md"):
                            continue

                        src = os.path.join(root, file)

                        relative_path = os.path.relpath(src, tmp_dir)

                        safe_name = relative_path.replace("/", "__")

                        dst_file = f"{repo_name}__{safe_name}"

                        dst = os.path.join(self.target_path, dst_file)

                        shutil.copy(src, dst)

                        print(f"📄 Indexed: {dst_file}")

                self.registry.update_commit(repo, latest_commit)

            finally:

                shutil.rmtree(tmp_dir)

            print("✅ GitHub repositories prepared")

            print("🐙 Preparing GitHub repositories")

            for repo in self.repos:

                repo_name = repo.split("/")[-1].replace(".git", "")

                repo_url = self._build_repo_url(repo)

                # --------------------------------
                # Check commit state
                # --------------------------------

                latest_commit = self.get_latest_commit(repo)

                stored_commit = self.registry.get_commit(repo)

                if stored_commit == latest_commit:

                    print(f"⏭ Repo unchanged, skipping: {repo_name}")

                    continue

                print(f"⬇️ Repo changed, indexing: {repo_name}")

                tmp_dir = tempfile.mkdtemp()

                try:

                    subprocess.run(
                        ["git", "clone", "--depth", "1", repo_url, tmp_dir],
                        check=True
                    )

                    for root, dirs, files in os.walk(tmp_dir):

                        # Filter ignored directories
                        dirs[:] = [
                            d for d in dirs
                            if d not in IGNORE_DIRS and not d.startswith(".")
                        ]

                        for file in files:

                            if not file.endswith(".md"):
                                continue

                            if file.lower() in IGNORE_FILES:
                                continue

                            src = os.path.join(root, file)

                            relative_path = os.path.relpath(src, tmp_dir)

                            safe_name = relative_path.replace("/", "__")

                            dst_file = f"{repo_name}__{safe_name}"

                            dst = os.path.join(self.target_path, dst_file)

                            shutil.copy(src, dst)

                            print(f"📄 Indexed: {dst_file}")

                    # --------------------------------
                    # Update registry commit
                    # --------------------------------

                    self.registry.update_commit(repo, latest_commit)

                finally:

                    shutil.rmtree(tmp_dir)

            print("✅ GitHub repositories prepared")
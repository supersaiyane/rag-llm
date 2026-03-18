import os
import shutil


class FilesystemConnector:

    def __init__(self, source_path, target_path):

        self.source_path = source_path
        self.target_path = target_path

    def prepare(self):

        if not os.path.exists(self.source_path):
            print(f"⚠️ Source path not found: {self.source_path}")
            return

        print(f"📂 Copying documents from {self.source_path}")

        for root, _, files in os.walk(self.source_path):

            for file in files:

                if not file.endswith(".md"):
                    continue

                src = os.path.join(root, file)
                dst = os.path.join(self.target_path, file)

                shutil.copy(src, dst)
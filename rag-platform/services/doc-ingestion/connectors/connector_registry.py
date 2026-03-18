from app.config.settings import INGESTION_SOURCES
from app.connectors.filesystem_connector import FilesystemConnector
from app.connectors.gitlab_connector import GitlabConnector
from app.connectors.github_connector import GithubConnector
from app.connectors.confluence_connector import ConfluenceConnector


def get_active_connectors():

    connectors = []

    if INGESTION_SOURCES.get("filesystem"):
        connectors.append(FilesystemConnector())

    if INGESTION_SOURCES.get("gitlab"):
        connectors.append(GitlabConnector())

    if INGESTION_SOURCES.get("github"):
        connectors.append(GithubConnector())

    if INGESTION_SOURCES.get("confluence"):
        connectors.append(ConfluenceConnector())

    return connectors
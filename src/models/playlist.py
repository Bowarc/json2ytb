from typing import Dict, Any

class Thumbnail:
    def __init__(self, url: str, width: int, height: int):
        self.url: str = url
        self.width: int = width
        self.height: int = height

    def __repr__(self):
        return f"Thumbnail(url={self.url}, width={self.width}, height={self.height})"

class Snippet:
    def __init__(self, published_at: str, channel_id: str, title: str, description: str, 
                 thumbnails: Dict[str, Thumbnail], channel_title: str, localized: Dict[str, str]):
        self.published_at: str = published_at
        self.channel_id: str = channel_id
        self.title: str = title
        self.description: str = description
        self.thumbnails: Dict[str, Thumbnail] = thumbnails
        self.channel_title: str = channel_title
        self.localized: Dict[str, str] = localized

    def __repr__(self):
        return (f"Snippet(published_at={self.published_at}, channel_id={self.channel_id}, "
                f"title={self.title}, description={self.description}, "
                f"thumbnails={self.thumbnails}, channel_title={self.channel_title}, "
                f"localized={self.localized})")

class Playlist:
    def __init__(self, kind: str, etag: str, id: str, snippet: Snippet):
        self.kind: str = kind
        self.etag: str = etag
        self.id: str = id
        self.snippet: Snippet = snippet

    def __repr__(self):
        return (f"Playlist(kind={self.kind}, etag={self.etag}, id={self.id}, "
                f"snippet={self.snippet})")


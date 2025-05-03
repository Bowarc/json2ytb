
from typing import List

class YtVideo:
    def __init__(self,
            id: str,
            thumbnails: List[str],
            title: str,
            long_desc: str,
            channel: str,
            duration: str,
            views: str,
            publish_time: str,
            url_suffix: str
        ):
        self.id: str = id
        self.thumbnails: List[str]= thumbnails
        self.title: str = title
        self.long_desc: str = long_desc
        self.channel: str = channel
        self.duration: str = duration
        self.views: str = views
        self.publish_time: str = publish_time
        self.url_suffix: str = url_suffix

    def __repr__(self):
        return (f"YtVideo(id={self.id!r}, "
        f"thumbnails={self.thumbnails!r}, "
        f"title={self.title!r}, "
        f"long_desc={self.long_desc!r}, "
        f"channel={self.channel!r}, "
        f"duration={self.duration!r}, "
        f"views={self.views!r}, "
        f"publish_time={self.publish_time!r}, "
        f"url_suffix={self.url_suffix!r})")

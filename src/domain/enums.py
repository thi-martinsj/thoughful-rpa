from enum import Enum

class Selector(Enum):
  ID = "#"
  CLASS = "."
  INPUT_VALUE = "input_value"
  TAG = "tag"

class APNewsCategory(Enum):
  LIVE_BLOGS = "live blogs"
  PHOTO_GALLERIES = "photo galleries"
  SECTIONS = "sections"
  STORIES = "stories"
  SUBSECTIONS = "subsections"
  VIDEOS = "videos"

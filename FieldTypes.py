class ComFields:
    def __init__(self):
        self.ARCHIVED = 'archived'
        self.AUTHOR = 'author'
        self.AUTHOR_FLAIR_CSS_CLASS = 'author_flair_css_class'
        self.AUTHOR_FLAIR_TEXT = 'author_flair_text'
        self.BODY = 'body'
        self.CONTROVERSIALITY = 'controversiality'
        self.CREATED_UTC = 'created_utc'
        self.DISTINGUISHED = 'distinguished'
        self.DOWNS = 'downs'
        self.EDITED = 'edited'
        self.GILDED = 'gilded'
        self.ID = 'id'
        self.LINK_ID = 'link_id'
        self.NAME = 'name'
        self.PARENT_ID = 'parent_id'
        self.RETRIEVED_ON = 'retrieved_on'
        self.SCORE = 'score'
        self.SCORE_HIDDEN = 'score_hidden'
        self.SUBREDDIT = 'subreddit'
        self.SUBREDDIT_ID = 'subreddit_id'
        self.UPS = 'ups'

    def all_fields(self):
        ALL_FIELDS = [
            self.ARCHIVED,
            self.AUTHOR,
            self.AUTHOR_FLAIR_CSS_CLASS,
            self.AUTHOR_FLAIR_TEXT,
            self.BODY,
            self.CONTROVERSIALITY,
            self.CREATED_UTC,
            self.DISTINGUISHED,
            self.DOWNS,
            self.EDITED,
            self.GILDED,
            self.ID,
            self.LINK_ID,
            self.NAME,
            self.PARENT_ID,
            self.RETRIEVED_ON,
            self.SCORE,
            self.SCORE_HIDDEN,
            self.SUBREDDIT,
            self.SUBREDDIT_ID,
            self.UPS
        ]
        return ALL_FIELDS

class SubFields:
    def __init__(self):
        self.ARCHIVED = 'archived'
        self.AUTHOR = 'author'
        self.AUTHOR_CAKEDAY = 'author_cakeday'
        self.AUTHOR_FLAIR_BACKGROUND_COLOR = 'author_flair_background_color'
        self.AUTHOR_FLAIR_CSS_CLASS = 'author_flair_css_class'
        self.AUTHOR_FLAIR_RICHTEXT = 'author_flair_richtext'
        self.AUTHOR_FLAIR_TEXT = 'author_flair_text'
        self.AUTHOR_FLAIR_TEXT_COLOR = 'author_flair_text_color'
        self.AUTHOR_FLAIR_TYPE = 'author_flair_type'
        self.BRAND_SAFE = 'brand_safe'
        self.CAN_GILD = 'can_gild'
        self.CONTEST_MODE = 'contest_mode'
        self.CREATED_UTC = 'created_utc'
        self.DISTINGUISHED = 'distinguished'
        self.DOMAIN = 'domain'
        self.EDITED = 'edited'
        self.GILDED = 'gilded'
        self.HIDDEN = 'hidden'
        self.HIDE_SCORE = 'hide_score'
        self.ID = 'id'
        self.IS_CROSSPOSTABLE = 'is_crosspostable'
        self.IS_REDDIT_MEDIA_DOMAIN = 'is_reddit_media_domain'
        self.IS_SELF = 'is_self'
        self.IS_VIDEO = 'is_video'
        self.LINK_FLAIR_CSS_CLASS = 'link_flair_css_class'
        self.LINK_FLAIR_RICHTEXT = 'link_flair_richtext'
        self.LINK_FLAIR_TEXT = 'link_flair_text'
        self.LINK_FLAIR_TEXT_COLOR = 'link_flair_text_color'
        self.LINK_FLAIR_TYPE = 'link_flair_type'
        self.LOCKED = 'locked'
        self.MEDIA = 'media'
        self.MEDIA_EMBED = 'media_embed'
        self.NO_FOLLOW = 'no_follow'
        self.NUM_COMMENTS = 'num_comments'
        self.NUM_CROSSPOSTS = 'num_crossposts'
        self.OVER_18 = 'over_18'
        self.PARENT_WHITELIST_STATUS = 'parent_whitelist_status'
        self.PERMALINK = 'permalink'
        self.POST_HINT = 'post_hint'
        self.PREVIEW = 'preview'
        self.RETRIEVED_ON = 'retrieved_on'
        self.RTE_MODE = 'rte_mode'
        self.SCORE = 'score'
        self.SECURE_MEDIA = 'secure_media'
        self.SECURE_MEDIA_EMBED = 'secure_media_embed'
        self.SELFTEXT = 'selftext'
        self.SEND_REPLIES = 'send_replies'
        self.SPOILER = 'spoiler'
        self.STICKIED = 'stickied'
        self.SUBREDDIT = 'subreddit'
        self.SUBREDDIT_ID = 'subreddit_id'
        self.SUBREDDIT_NAME_PREFIXED = 'subreddit_name_prefixed'
        self.SUBREDDIT_TYPE = 'subreddit_type'
        self.SUGGESTED_SORT = 'suggested_sort'
        self.THUMBNAIL = 'thumbnail'
        self.THUMBNAIL_HEIGHT = 'thumbnail_height'
        self.THUMBNAIL_WIDTH = 'thumbnail_width'
        self.TITLE = 'title'
        self.URL = 'url'
        self.WHITELIST_STATUS = 'whitelist_status'

    def all_fields(self):
        ALL_FIELDS = [
            self.ARCHIVED,
            self.AUTHOR,
            self.AUTHOR_CAKEDAY,
            self.AUTHOR_FLAIR_BACKGROUND_COLOR,
            self.AUTHOR_FLAIR_CSS_CLASS,
            self.AUTHOR_FLAIR_RICHTEXT,
            self.AUTHOR_FLAIR_TEXT,
            self.AUTHOR_FLAIR_TEXT_COLOR,
            self.AUTHOR_FLAIR_TYPE,
            self.BRAND_SAFE,
            self.CAN_GILD,
            self.CONTEST_MODE,
            self.CREATED_UTC,
            self.DISTINGUISHED,
            self.DOMAIN,
            self.EDITED,
            self.GILDED,
            self.HIDDEN,
            self.HIDE_SCORE,
            self.ID,
            self.IS_CROSSPOSTABLE,
            self.IS_REDDIT_MEDIA_DOMAIN,
            self.IS_SELF,
            self.IS_VIDEO,
            self.LINK_FLAIR_CSS_CLASS,
            self.LINK_FLAIR_RICHTEXT,
            self.LINK_FLAIR_TEXT,
            self.LINK_FLAIR_TEXT_COLOR,
            self.LINK_FLAIR_TYPE,
            self.LOCKED,
            self.MEDIA,
            self.MEDIA_EMBED,
            self.NO_FOLLOW,
            self.NUM_COMMENTS,
            self.NUM_CROSSPOSTS,
            self.OVER_18,
            self.PARENT_WHITELIST_STATUS,
            self.PERMALINK,
            self.POST_HINT,
            self.PREVIEW,
            self.RETRIEVED_ON,
            self.RTE_MODE,
            self.SCORE,
            self.SECURE_MEDIA,
            self.SECURE_MEDIA_EMBED,
            self.SELFTEXT,
            self.SEND_REPLIES,
            self.SPOILER,
            self.STICKIED,
            self.SUBREDDIT,
            self.SUBREDDIT_ID,
            self.SUBREDDIT_NAME_PREFIXED,
            self.SUBREDDIT_TYPE,
            self.SUGGESTED_SORT,
            self.THUMBNAIL,
            self.THUMBNAIL_HEIGHT,
            self.THUMBNAIL_WIDTH,
            self.TITLE,
            self.URL,
            self.WHITELIST_STATUS
        ]
        return ALL_FIELDS
    

if __name__ == "__main__":
    obj = ComFields()
    print(obj.all_fields())

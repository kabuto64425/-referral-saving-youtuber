import datetime
from django.db import models
from users.models import User
from django.utils.timezone import make_naive

class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # チャンネルID
    channel_id = models.CharField(
        verbose_name='channel_id',
        max_length=200,
        blank=True,
        null=True,
    )

    # サンプル項目1 文字列
    channel_title = models.CharField(
        verbose_name='チャンネル名',
        max_length=200,
        blank=True,
        null=True,
    )

    # url
    channel_url = models.CharField(
        verbose_name='channel_url',
        max_length=1000,
        blank=True,
        null=True,
    )

    # 動画本数
    video_count = models.PositiveIntegerField(
        verbose_name='video_count',
        blank=True,
        null=True,
        default=0,
    )

    # アップロード動画のプレイリストID
    uploads_playlist_id = models.CharField(
        verbose_name='uploads_playlist_id',
        max_length=200,
        blank=True,
        null=True,
    )

    # 最新のvideoid
    recently_upload_video_id = models.CharField(
        verbose_name='recently_upload_video_id',
        max_length=200,
        blank=True,
        null=True,
    )

    # 最新動画のタイトル
    recently_upload_video_title = models.CharField(
        verbose_name='recently_upload_video_title',
        max_length=500,
        blank=True,
        null=True,
    )

    # 最新動画公開日時
    recently_upload_video_published_at = models.DateTimeField(
        verbose_name='recently_upload_video_published_at',
        blank=True,
        null=True
    )

    # 最新動画のサムネイルURL(medium)
    recently_upload_video_tumbnail_url = models.CharField(
        verbose_name='recently_upload_video_tumbnail_url',
        max_length=1000,
        blank=True,
        null=True,
    )

    # 最新動画のサムネイルの幅
    recently_upload_video_tumbnail_width = models.PositiveIntegerField(
        verbose_name='recently_upload_video_tumbnail_width',
        blank=True,
        null=True,
    )

    # 最新動画のサムネイルの高さ
    recently_upload_video_tumbnail_height = models.PositiveIntegerField(
        verbose_name='recently_upload_video_tumbnail_height',
        blank=True,
        null=True,
    )

    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.channel_title
     
    def daysAgoFromUploadVideo(self):
        """
        リストボックスや管理画面での表示
        """
        td = datetime.datetime.now() - make_naive(self.recently_upload_video_published_at)
        return td.days
        #return datetime.datetime.now()

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'サンプル'
        verbose_name_plural = 'サンプル'

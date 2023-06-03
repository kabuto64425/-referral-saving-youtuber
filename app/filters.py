import django_filters
from django.db import models

from .models import Item


class OrderingFilter(django_filters.filters.OrderingFilter):
    """日本語対応"""
    descending_fmt = '%s （降順）'


class ItemFilterSet(django_filters.FilterSet):
    """
     django-filter 構成クラス
    https://django-filter.readthedocs.io/en/latest/ref/filterset.html
    """

    # 検索フォームの「並び順」の設定
    order_by = OrderingFilter(
        initial='channel_title',
        fields=(
            ('channel_title', 'channel_title'),
        ),
        field_labels={
            'channel_title': 'チャンネル名',
        },
        label='並び順'
    )

    class Meta:
        model = Item
        # 一部フィールドを除きモデルクラスの定義を全て引用する
        exclude = [
            'created_at',
            'updated_by',
            'updated_at',
            'created_by',
            'channel_id',
            'channel_url',
            'video_count',
            'uploads_playlist_id',
            'recently_upload_video_id',
            'recently_upload_video_title',
            'recently_upload_video_published_at',
            'recently_upload_video_tumbnail_url',
            'recently_upload_video_tumbnail_width',
            'recently_upload_video_tumbnail_height'
        ]
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

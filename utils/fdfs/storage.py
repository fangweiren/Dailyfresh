# -*- coding: utf-8 -*-
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    """FastDFS文件存储类"""

    def _open(self, name, mode='rb'):
        """打开文件时使用"""
        pass

    def _save(self, name, content):
        """保存文件时使用"""
        # name：你选择上传文件的名字
        # content：包含你上传文件内容的File对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client('/etc/fdfs/client.conf')

        # 上传文件到FastDFS系统中
        res = client.upload_appender_by_buffer(content.read())

        # dict {
        #     'Group name'      : group_name,
        #     'Remote file_id'  : remote_file_id,
        #     'Status'          : 'Upload successed.',
        #     'Local file name' : '',
        #     'Uploaded size'   : upload_size,
        #     'Storage IP'      : storage_ip
        # }
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到FastDFS失败')

        # 获取返回的文件id
        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        """Django判断文件名是否可用"""
        return False

    def url(self, name):
        """返回访问文件的url的地址"""
        return 'http://192.168.37.133:8888/' + name

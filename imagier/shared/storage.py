from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    """
    This storage engine for Django deletes a previous file when Django tries
    to write to a specific path that maps to an existing file.
    http://www.djangosnippets.org/snippets/976/
    """

    def get_available_name(self, name, max_length=None):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        if self.exists(name):
            self.delete(name)
        return name

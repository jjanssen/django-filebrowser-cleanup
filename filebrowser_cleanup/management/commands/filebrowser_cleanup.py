import os, sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.db import models

from filebrowser.base import FileObject
from filebrowser.fields import FileBrowseField
from filebrowser.functions import get_version_path, url_to_path
from filebrowser import settings as fb_settings

try:
    import filebrowser
except ImportError:
    raise ImproperlyConfigured("Why would you want to use filebrowser-cleanup if you don't have filebrowser?")


class Command(BaseCommand):
    help = 'Cleanup all unused files on disk which are no longer used by the Filebrowse field.'

    def handle(self, **options):
        self.verbosity = int(options.get('verbosity', 1))        
        
        print
        print "WARNING: This will irreparably remove EVERYTHING from your uploads."
        print "This works with Filebrowser 3.0, but it does not have versions declaration."
        print "Your choices after this are to restore from backups."
        
        yes_or_no = raw_input("Are you sure you wish to continue? [y/N] ")
        
        if not yes_or_no.lower().startswith('y'):
            print "No action taken."
            sys.exit()
        
        self.remove_files()
         
        
    def remove_files(self):
        files_in_db     = self.get_all_filebrowse_values()
        files_on_disk   = self.get_files_on_disk()
        
        obsolete_files  = set(files_on_disk) - set(files_in_db)
        
        self.stdout.write("There are %d files and thumbnails in the database.\n" % len(files_in_db))
        self.stdout.write("There are %d files and thumbnails on the disk.\n" % len(files_on_disk))
        
        counter = 0
        for del_file in obsolete_files:
            counter += 1
            if self.verbosity > 1:
                self.stdout.write("Deleting %s\n" % del_file)
            
            try:
                os.remove(del_file)
            except OSError:
                self.stdout.write("Unable to remove %s\n" % del_file)
            
        if counter:
            self.stdout.write("Deleted %d files on the disk.\n" % counter)
        else:
            self.stdout.write("There are no files available to delete.\n")
        
        
    def get_all_models(self):
        collection = {}        
        for model in models.get_models():
            filebrowse_fields = [field.name for field in model._meta.fields if isinstance(field, FileBrowseField)]

            if len(filebrowse_fields) > 0:
                collection[model] = filebrowse_fields
                
        return collection
        
        
    def get_all_filebrowse_values(self):
        versions = getattr(settings, 'FILEBROWSER_VERSIONS', fb_settings.VERSIONS)
        files    = []
        
        for model, fields in self.get_all_models().items():
            for record in model.objects.values(*fields):
                for field, value in record.items():
                    if value:
                        file_obj = FileObject(value.replace(settings.MEDIA_URL, ''))
                        files.append(file_obj.path_full)

                        for version in versions:
                            version_path = get_version_path(url_to_path(file_obj.url_save), version)
                            version_file = os.path.join(settings.MEDIA_ROOT, version_path)
                            if os.path.isfile(version_file):                                
                                files.append(version_file)
                                  
        return files
    
        
    def get_files_on_disk(self):
        filelisting = []
        upload_dir  = getattr(settings, 'FILEBROWSER_DIRECTORY', fb_settings.DIRECTORY)
        rootpath    = os.path.join(settings.MEDIA_ROOT, upload_dir)

        for root, dirs, files in os.walk(rootpath):
            if '.svn' in dirs:
                dirs.remove('.svn')

            for name in files:
                filelisting.append(u'%s' % os.path.join(root, name))
        
        return filelisting
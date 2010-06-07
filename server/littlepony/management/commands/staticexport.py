from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.conf import settings

class Command(BaseCommand):
    args = ''
    help = 'Exports urlexamples to static files'
    option_list = BaseCommand.option_list + (
            make_option('--output-path', '-o',
                type="string",
                action='store',
                dest='output_path',
                default=settings.STATIC_EXPORT_PATH,
                help='write files in destination directory'),
            make_option('--no-package',
                action='store_false',
                dest='package',
                default="True",
                help='Do not copy media and rewrite URLs'),
            make_option('--validate-html',
                action='store_true',
                dest='validate_html',
                default="False",
                help='Validate HTML files (uses validation middleware)'),
        )

    def handle(self, *args, **options):
        import os, re
        from django.template.defaultfilters import slugify
        from datetime import datetime
        from littlepony.util.urlexamples import export_static, render_index
        
        date = slugify(datetime.now())[:-5]
        fullpath = os.path.join(options['output_path'], date)
        
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
            
        #dir_exists = os.path.isdir(options['output_path'])
        #if not dir_exists:
        #    raise CommandError('Directory "%s" does not exist. Please create it for me, or specify a different output directory.' % options['output_path'])
        
        statics = [e for e in export_static()]
        for e in statics:
            f = open(os.path.join(fullpath, e['filename']), "w+")
            response = e['response']
            
            if options['package'] and 'html' in e['content_type']:
                # replace media url with static packaged path
                response = unicode(response).replace(settings.MEDIA_URL, 'media/')
                # replace urls with paths to static files
                for s in statics:
                    r = re.compile('(\'|")(' + s['url'] + ')(\'|")', re.DOTALL)
                    response = r.sub('\g<1>' + s['filename'] + '\g<3>', response)
                    
            if options['validate_html'] == True and 'html' in e['content_type']:
                from littlepony.middleware import validate_html
                print "Validating %s for valid HTML." % e['url']
                valid, message = validate_html(response)
                if not valid: raise Exception("The url %s did not contain valid HTML." % e['url'])
                
            f.writelines(response)
            f.close()
            print "Wrote %s" % e['filename']
        
        if options['package']:
            from shutil import copytree, rmtree
            dest = os.path.join(fullpath, 'media')
            if os.path.exists(dest):
                rmtree(dest)
            copytree(settings.MEDIA_ROOT, dest)
            print "Copied media files"
            
        index = render_index(statics)
        f = open(os.path.join(fullpath, 'index.html'), 'w+')
        f.writelines(index)
        f.close()
        print "Wrote index.html"
        print "Done."

        
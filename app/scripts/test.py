# Server path
current_path = '/home/tylerkershner/app/templates/pi_display/logs/'

def remove_dupes(path, filename):
    with open('%s/%s' % (path, filename), 'r') as f:
        urls = [url.rstrip('\r\n') for url in f]
        unique_urls = []
        duplicate_urls = []

        for url in urls:
            if url + '\n' in unique_urls:
                duplicate_urls.append(url + '\n')
            else:
                unique_urls.append(url + '\n')

        # Open/close file in write mode to erase it
        open('%s/%s' % (path, filename), 'w').close()

        # Write contents of clean_urls list to file
        with open('%s/%s' % (path, filename), 'a+') as clean_file:
            for url in unique_urls:
                clean_file.write(url)

        print '%d duplicate URLs in %s' % (len(duplicate_urls), filename)
        print '%d total unique URLs now in %s' % (len(unique_urls), filename)


remove_dupes(current_path, 'test.txt')
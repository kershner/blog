def make_toplay_file(path, filename):

    with open('%s/%s_urls.txt' % (path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    # Opening and closing the urls.txt file.  Side effect to erase contents of file.
    print '\n\n\n\nErasing contents of %s_urls.txt...' % filename
    open('%s/%s_urls_to_play.txt' % (path, filename), 'w').close()

    toplay_file = open('%s/%s_urls_to_play.txt' % (path, filename), 'a+')
    for entry in urls_list:
        toplay_file.write(entry)
    toplay_file.close()

    with open('%s/%s_urls_to_play.txt' % (path, filename), 'r') as temp:
        temp_list = list(temp)
        print '\n\nLines from %s_urls.txt written to %s_urls_to_play.txt' % (filename, filename)
        print '%s_urls_to_play.txt now contains %d URLs' % (filename, len(temp_list))

if __name__ == '__main__':
    current_path = '/home/tylerkershner/app/templates/pi_display/logs'
    categories = ['all', 'animals', 'gaming', 'strange', 'educational']
    for category in categories:
        make_toplay_file(current_path, category)
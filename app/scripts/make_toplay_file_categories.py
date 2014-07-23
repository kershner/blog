def make_toplay_file(path, filename):
    urls_file = open('%s/%s_urls.txt' % (path, filename), 'r')
    urls_list = list(urls_file)
    toplay_file = open('%s/%s_urls_to_play.txt' % (path, filename), 'a+')
    toplay_list = list(toplay_file)

    if len(toplay_list) > 1:
        print '\n\nStill %d URLs in %s_urls_to_play.txt, making no changes...' % (len(toplay_list), filename)
        toplay_file.close()
    else:
        for entry in urls_list:
            toplay_file.write(entry)
        toplay_file.close()
        with open('%s/%s_urls_to_play.txt' % (path, filename), 'r') as temp:
            temp_list = list(temp)
            print '\n\nLines from %s_urls.txt written to %s_urls_to_play.txt' % (filename, filename)
            print '%s_urls_to_play.txt now contains %d URLs' % (filename, len(temp_list))

    urls_file.close()

if __name__ == '__main__':
    prompt = raw_input('Are you running this script from home or work? > ').lower()
    if prompt == 'work':
        current_path = 'E:/programming/projects/blog/app/templates/pi_display/logs/'
    elif prompt == 'home':
        current_path = 'H:/programming/projects/blog/app/templates/pi_display/logs/'

    categories = ['animals', 'gaming', 'strange', 'educational']
    for category in categories:
        make_toplay_file(current_path, category)

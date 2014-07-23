def make_toplay_file(path):
    urls_file = open('%s/urls.txt' % path, 'r')
    urls_list = list(urls_file)
    toplay_file = open('%s/urls_to_play.txt' % path, 'a+')
    toplay_list = list(toplay_file)

    if len(toplay_list) > 1:
        print '\n\nStill %d URLs in urls_to_play.txt, making no changes...' % len(toplay_list)
        toplay_file.close()
    else:
        for entry in urls_list:
            toplay_file.write(entry)
        toplay_file.close()
        with open('%s/urls_to_play.txt' % path, 'r') as temp:
            temp_list = list(temp)
            print '\n\nLines from urls.txt written to urls_to_play.txt'
            print 'urls_to_play.txt now contains %d URLs' % len(temp_list)

    urls_file.close()

if __name__ == '__main__':
    prompt = raw_input('Are you running this script from home or work? > ').lower()
    if prompt == 'work':
        current_path = 'E:/programming/projects/blog/app/templates/pi_display/logs/'
    elif prompt == 'home':
        current_path = 'H:/programming/projects/blog/app/templates/pi_display/logs/'

    make_toplay_file(current_path)
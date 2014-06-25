###########################
# Temporary script to output image sizes to KB (more human readable)
# Will use this information later to find out exactly what size of GIF causes
# the Raspberry Pi to choke, then will use that information to update the scraper.
###########################

image_sizes = open('E:/programming/projects/blog/app/templates/pi_display/image_sizes.txt', 'r')
kb_sizes = open('E:/programming/projects/blog/app/templates/pi_display/kb_sizes.txt', 'a')
large_urls = open('E:/programming/projects/blog/app/templates/pi_display/large_urls.txt', 'a')

list_image_sizes = list(image_sizes)

count = 0

for entry in list_image_sizes:
    url = entry[:entry.find(' - ')]
    start_point = entry.find(' - ') + 2
    end_point = entry.find('bytes') - 1
    image_bytes = entry[start_point:end_point + 1]
    kilobytes = '%s - %.2f KBs' % (url, (int(image_bytes) / 1024.0))
    if (int(image_bytes) / 1024.0) > 8000:
        count += 1
        large_urls.write(str(kilobytes) + '\n')
    #kb_sizes.write(str(kilobytes) + '\n')

print '%d GIFs larger than 8MBs' % count


image_sizes.close()
kb_sizes.close()
large_urls.close()
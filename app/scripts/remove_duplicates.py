large_urls_file = open('E:/programming/projects/blog/app/templates/pi_display/bad_urls.txt', 'a+')
large_urls_list = list(large_urls_file)

clean_urls = open('E:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'a+')

urls_list = []
duplicates = 0

for entry in large_urls_list:
    if entry in urls_list:
        print '%s already found, skipping...' % entry
        duplicates += 1
        continue
    else:
        urls_list.append(entry)
        clean_urls.write(entry)

print '%d duplicates removed' % duplicates

clean_urls.close()
large_urls_file.close()

open('E:/programming/projects/blog/app/templates/pi_display/bad_urls.txt', 'w').close()
large_urls_file = open('E:/programming/projects/blog/app/templates/pi_display/bad_urls.txt', 'a+')
updated_clean_urls = open('E:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'a+')
updated_clean_urls_list = list(updated_clean_urls)
for entry in updated_clean_urls_list:
    large_urls_file.write(entry)

updated_clean_urls.close()
large_urls_file.close()

# Opening and closing the clean_urls.txt file.  Side effect to erase contents of file.
print '\n\n\n\nErasing contents of clean_urls.txt...'
open('E:/programming/projects/blog/app/templates/pi_display/clean_urls.txt', 'w').close()
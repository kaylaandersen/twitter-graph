from datacollect import oauth, tgdb
import time

source_sn = 'BernieSanders'

tweepy_cursor = tweepy.Cursor(self.api.followers_ids, screen_name=handle).pages()
save_obj = {}
while True:
    try:
         page = tweepy_cursor.next()
         cursor = tweepy_cursor.next_cursor
         for follower in page:
               writer.writerow([follower])
     except StopIteration:
         break

     # update and write save file in case we need to resume later
     save_obj['cursor'] = cursor
     self.write_save_file(save_obj=save_obj)

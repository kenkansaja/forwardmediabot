from telegram.ext import MessageFilter

class Album(MessageFilter):
	def filter(self, message):
	    if (
			message.photo or message.video or message.audio or message.document
		) and message.media_group_id is not None:
	        return True


album = Album()

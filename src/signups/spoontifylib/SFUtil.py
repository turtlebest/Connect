import Singleton
import SFDBManager
import datetime
import time

class SFUtil(object):
	@staticmethod
	def isSignUpValid(username,password,repassword):
		if len(username) < 4:
			return False
		if password != repassword or len(password) < 6:
			return False
		return True

	@staticmethod
	def isLoginValid(username,password):
		if len(username) < 4:
			return False
		if len(password) < 6:
			return False
		return True

	@staticmethod
	def isArtist(username):
		sf_db = SFDBManager.SFDBManager()
		check_artist_sentence = """SELECT * FROM artist WHERE artist_name = %s"""
		sets = [username]
		check_back_data = sf_db.query_data(check_artist_sentence,sets)
		if not check_back_data:
			return False
		return True

	@staticmethod
	def updateAccessTime(username,is_artist):
		sf_db = SFDBManager.SFDBManager()
		update_sentence =''
		if is_artist:
			update_sentence = """UPDATE artist SET last_access_time = NOW() WHERE artist_name = %s"""
		else:
			update_sentence = """UPDATE user SET last_access_time = NOW() WHERE user_name = %s"""
		sets = [username]
		sf_db.execute_sql(update_sentence, sets)
		return

	@staticmethod
	def isUserExist(username):
		sf_db = SFDBManager.SFDBManager()
		check_userexist_sentence = """SELECT * FROM user WHERE user_name = %s"""
		sets = [username]
		check_back_data = sf_db.query_data(check_userexist_sentence, sets)
		if not check_back_data:
			if SFUtil.isArtist(username):
				return True
			else:
				return False
		return True

	@staticmethod
	def checkUserType(username):
		sf_db = SFDBManager.SFDBManager()
		check_user_set = [username]
		check_is_user_sentence = """SELECT * FROM user WHERE user_name = %s"""
		check_is_user_back_data = sf_db.query_data(check_is_user_sentence, check_user_set)
		if check_is_user_back_data:
			return 2
		check_is_artist_sentence = """SELECT * FROM artist WHERE artist_name = %s"""
		check_is_artist_back_data = sf_db.query_data(check_is_artist_sentence, check_user_set)
		if check_is_artist_back_data:
			return 1
		return 0


	@staticmethod
	def isUAlogin(request):
		if "username" in request.session:
			return True

	@staticmethod
	def getGenreList():
		sf_db = SFDBManager.SFDBManager()
		genre_option_query_sentence = """SELECT DISTINCT genre FROM type_category"""
		genre_list = sf_db.query_data(genre_option_query_sentence)
		return genre_list


	@staticmethod
	def getTypeList():
		sf_db = SFDBManager.SFDBManager()
		type_option_query_sentence = """SELECT type_name FROM type_category"""
		type_list = sf_db.query_data(type_option_query_sentence)
		return type_list

	@staticmethod
	def getVenueList():
		sf_db = SFDBManager.SFDBManager()
		venue_query_sentence = """SELECT venue_name FROM venue"""
		venue_list = sf_db.query_data(venue_query_sentence)
		return venue_list

	@staticmethod
	def getArtistList():
		sf_db = SFDBManager.SFDBManager()
		artist_query_sentence = """SELECT artist_name FROM artist"""
		artist_list = sf_db.query_data(artist_query_sentence)
		return artist_list

	@staticmethod
	def getAllConcertList():
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""SELECT * FROM concert""",[])


	@staticmethod
	def getAllComingConcertList():
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""SELECT * FROM concert WHERE concert.hold_time > NOW()""",[])

	@staticmethod
	def getAllPastConcertList():
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""SELECT * FROM concert WHERE concert.hold_time < NOW()""",[])


	@staticmethod
	def getConcertList(artist_name):
		sf_db = SFDBManager.SFDBManager()
		concert_query_sentence = """SELECT concert_id, title FROM concert WHERE artist_name = %s"""
		concert_artist_set = [artist_name]
		concert_list = sf_db.query_data(concert_query_sentence, concert_artist_set)
		return concert_list


	@staticmethod
	def getNewConcertList(user_name):
		sf_db = SFDBManager.SFDBManager()
		concert_query_sentence = """SELECT DISTINCT concert_id, title FROM concert
		WHERE create_time > (SELECT last_access_time FROM user WHERE user_name = %s)"""
		concert_user_set = [user_name]
		concert_list = sf_db.query_data(concert_query_sentence, concert_user_set)
		return concert_list

# ====================================================
# 
# 	Like and Follow
# 
# ====================================================	

	@staticmethod
	def checkIsLiked(username,artistname):
		sf_db = SFDBManager.SFDBManager()
		check_ulikea_query_sentence = """SELECT * FROM like_artist WHERE from_user =%s AND to_artist = %s"""
		check_ulikea_set = [username,artistname]
		check_ulikea_list = sf_db.query_data(check_ulikea_query_sentence, check_ulikea_set)
		if check_ulikea_list:
			return True
		else:
			return False



	@staticmethod
	def changeLikedState(username,artistname):
		sf_db = SFDBManager.SFDBManager()
		change_likes_exe_set = [username, artistname]
		if not SFUtil.checkIsLiked(username=username, artistname=artistname):
			change_likes_exe_sentence = """INSERT INTO like_artist VALUES(%s,%s,NOW())"""
		else:
			change_likes_exe_sentence = """DELETE FROM like_artist WHERE from_user =%s AND to_artist = %s"""
		sf_db.execute_sql(change_likes_exe_sentence,change_likes_exe_set)
		return


	@staticmethod
	def checkIsFollowed(from_user,to_user):
		sf_db = SFDBManager.SFDBManager()
		check_ufollowu_query_sentence = """SELECT * FROM follow_user WHERE from_user =%s AND to_user = %s"""
		check_ufollowu_set = [from_user,to_user]
		check_ufollowu_list = sf_db.query_data(check_ufollowu_query_sentence, check_ufollowu_set)
		if check_ufollowu_list:
			return True
		else:
			return False

			
	@staticmethod
	def changeFollowState(from_user, to_user):
		sf_db = SFDBManager.SFDBManager()
		change_follow_exe_set = [from_user, to_user]
		if not SFUtil.checkIsFollowed(from_user=from_user, to_user=to_user):
			change_follow_exe_sentence = """INSERT INTO follow_user VALUES(%s,%s,NOW())"""
		else:
			change_follow_exe_sentence = """DELETE FROM follow_user WHERE from_user =%s AND to_user = %s"""
		sf_db.execute_sql(change_follow_exe_sentence,change_follow_exe_set)
		return

	@staticmethod
	def getLikedArtist(username):
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""SELECT to_artist FROM like_artist WHERE from_user = %s""", [username])

	@staticmethod
	def getFollowedUser(username):
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""SELECT to_user FROM follow_user WHERE from_user = %s""", [username])



# ====================================================
# 
# 	Post List stuffs
# 
# ====================================================
	@staticmethod
	def getPostListForConcert(concert_id):
		sf_db = SFDBManager.SFDBManager()
		about_this_concert_query_sentence = """SELECT post.post_id, post.user_name, post.artist_name, post.concert_id, concert.title, post.information, post.create_date, post.recommend_list_id, post.post_type
			FROM post LEFT JOIN concert ON post.concert_id = concert.concert_id WHERE post.concert_id = %s ORDER BY post.create_date DESC"""
		about_this_concert_set = [concert_id]
		return sf_db.query_data(about_this_concert_query_sentence, about_this_concert_set)


	@staticmethod
	def getPostListForArtist(artistname):
		sf_db = SFDBManager.SFDBManager()
		artistprofile_post_list_query_sentence = """SELECT post.post_id, post.user_name, post.artist_name, post.concert_id, concert.title, post.information, post.create_date, post.recommend_list_id, post.post_type FROM post LEFT JOIN concert ON post.concert_id = concert.concert_id WHERE post.artist_name = %s ORDER BY post.create_date DESC"""
		artistprofile_post_list_set = [artistname]
		return sf_db.query_data(artistprofile_post_list_query_sentence, artistprofile_post_list_set)
		

	@staticmethod
	def getPostListForUserProfile(username):
		sf_db = SFDBManager.SFDBManager()
		userprofile_post_list_query_sentence = """SELECT post.post_id, post.user_name, post.artist_name, post.concert_id, concert.title, post.information, post.create_date, post.recommend_list_id, post.post_type FROM post LEFT JOIN concert ON post.concert_id = concert.concert_id WHERE post.user_name = %s ORDER BY post.create_date DESC"""
		userprofile_post_list_set = [username]
		return sf_db.query_data(userprofile_post_list_query_sentence, userprofile_post_list_set)


	@staticmethod
	def getPostListForUserFeed(username):
		sf_db = SFDBManager.SFDBManager()
		post_list_query_sentence = """SELECT post.post_id, post.user_name, post.artist_name, post.concert_id, concert.title, post.information, post.create_date, post.recommend_list_id, post.post_type
		FROM post LEFT JOIN concert ON post.concert_id = concert.concert_id 
		WHERE post.user_name = %s OR post.artist_name IN (SELECT to_artist FROM like_artist WHERE from_user=%s) 
		OR post.user_name IN (SELECT to_user FROM follow_user WHERE from_user=%s)
		ORDER BY post.create_date DESC"""
		post_list_set = [username, username,username]
		return sf_db.query_data(post_list_query_sentence, post_list_set)


	@staticmethod
	def createPost(username=None, artistname=None, concert_id=None, information="", recommend_list_id=None, post_type="basic"):
		sf_db = SFDBManager.SFDBManager()
		insert_post_sentence = """INSERT INTO post VALUES (0, %s, %s, %s, %s, %s, %s, NOW())"""	
		insert_post_set = [username, artistname, concert_id, recommend_list_id, information, post_type]
		sf_db.execute_sql(insert_post_sentence, insert_post_set)
		return


# ===============================================================
# 
# 	Reputation stuffs
# 
# ===============================================================
	
	@staticmethod
	def checkReputation(username):
		return SFUtil.getReputation(username) > 100


	@staticmethod
	def getReputation(username):
		sf_db = SFDBManager.SFDBManager()
		get_reputation = sf_db.query_data("""SELECT reputation FROM user WHERE user_name = %s""", [username])
		return get_reputation[0][0]



# ===============================================================
# 
# 	Concert Discuss Post stuffs
# 
# ===============================================================

	@staticmethod
	def createConcertandPost(request):
		sf_db = SFDBManager.SFDBManager()
		concert_data_query_sentence = """SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'spoontifyDB' AND TABLE_NAME = 'concert'"""
		check_concert_back_data = sf_db.query_data(concert_data_query_sentence)
		concertID = int(check_concert_back_data[0][0])
		# convert data time format to normal time format
		concert_datetime = datetime.datetime.strptime(request.POST.get('concert_time_input'), "%Y-%m-%d %H:%M")
		if request.session['is_artist']:
			# if creator is artist
			concert_time_insert_sentence = """INSERT INTO concert VALUES(0, %s,%s, NULL, %s, %s, %s, NOW(), NOW(), %s)"""
			ctsets = [request.POST.get('concert_title_input'), request.session['username'],request.POST.get('descript_input') ,request.POST.get('venueselection'),concert_datetime.strftime('%Y-%m-%d %H:%M:%S'), request.POST.get('hyperlink_input')]
		else:
			# if creator is user, not artist
			# user create concert
			concert_time_insert_sentence = """INSERT INTO concert VALUES(0, %s,%s, %s, %s, %s, %s, NOW(), NOW(), %s)"""
			ctsets = [request.POST.get('concert_title_input'), request.POST.get('uartistselection'),request.session['username'],request.POST.get('descript_input') ,request.POST.get('venueselection'),concert_datetime.strftime('%Y-%m-%d %H:%M:%S'), request.POST.get('hyperlink_input')]
		sf_db.execute_sql(concert_time_insert_sentence, ctsets)
		checked_concerttype_list = request.POST.getlist('checks')
		for eachtype in checked_concerttype_list:
			insert_concerttype_sentence = """INSERT INTO concert_type VALUES(%s,%s)"""
			ctchecksets = [concertID, eachtype]
			sf_db.execute_sql(insert_concerttype_sentence, ctchecksets)
		if request.session['is_artist']:
			SFUtil.createPost(username=None, artistname=request.session['username'], concert_id=concertID, information='I will have a upcoming concert', recommend_list_id=None, post_type="concert")
		else:
			SFUtil.createPost(username=request.session['username'], artistname=request.POST.get('uartistselection'), concert_id=concertID, information='I just add a concert', recommend_list_id=None, post_type="ucon")
		return concertID

	@staticmethod
	def getvAddress(venuename):
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""SELECT * FROM venue WHERE venue_name = %s""", [venuename])
# ===============================================================
# 
# 	recommend list stuffs
# 
# ===============================================================

	@staticmethod
	def createRecommendList(username, rltitle, genre):
		sf_db = SFDBManager.SFDBManager()
		get_rlID_query_sentence = """SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'spoontifyDB' AND TABLE_NAME = 'recommend_list'"""
		rlID = int(sf_db.query_data(get_rlID_query_sentence)[0][0])
		insert_rl_sentence = """INSERT INTO recommend_list VALUES (0, %s, %s, %s, NOW(), NOW())"""	
		insert_rl_set = [rltitle, username, genre]
		sf_db.execute_sql(insert_rl_sentence, insert_rl_set)
		SFUtil.createPost(username=username, artistname=None, concert_id=None, information=rltitle, recommend_list_id=rlID, post_type="mkrl")
		return


	@staticmethod
	def getRecommendListForUserself(username):
		sf_db = SFDBManager.SFDBManager()
		rl_query_sentence = """SELECT recommend_list_id, recommend_list_title FROM recommend_list WHERE user_name = %s"""
		rl_query_set = [username]
		return sf_db.query_data(rl_query_sentence, rl_query_set)


	@staticmethod
	def createRecommendCell(recommend_list_id, concert_id):
		sf_db = SFDBManager.SFDBManager()
		create_rc_sentence = """INSERT INTO recommend_cell VALUES (%s, %s, NOW())"""
		create_rc_set = [recommend_list_id, concert_id]
		sf_db.execute_sql(create_rc_sentence, create_rc_set)
		rlcreator = sf_db.query_data("""SELECT user_name, recommend_list_title FROM recommend_list WHERE recommend_list_id = %s""",[recommend_list_id])
		concertholder = sf_db.query_data("""SELECT artist_name FROM concert WHERE concert_id = %s""",[concert_id])
		concert_title = sf_db.query_data("""SELECT title FROM concert WHERE concert_id = %s""",[concert_id])
		SFUtil.createPost(username=rlcreator[0][0], artistname=concertholder[0][0], concert_id=concert_id, information=rlcreator[0][1], recommend_list_id=recommend_list_id, post_type="modrl")
		
		sf_db.execute_sql("""UPDATE recommend_list SET last_modify = NOW() WHERE recommend_list_id = %s""", [recommend_list_id])
		return		


	@staticmethod
	def	getRecommendListData(recommend_list_id):
		sf_db = SFDBManager.SFDBManager()
		rld_query_sentence = """SELECT recommend_list_title, user_name, genre FROM recommend_list WHERE recommend_list_id = %s"""
		rld_query_set = [recommend_list_id]
		return sf_db.query_data(rld_query_sentence, rld_query_set)


	@staticmethod
	def getRecommendCellsForList(recommend_list_id):
		sf_db = SFDBManager.SFDBManager()
		rlc_query_sentence = """SELECT recommend_cell.concert_id, concert.title, concert.artist_name, concert.hold_time FROM recommend_cell LEFT JOIN concert ON concert.concert_id = recommend_cell.concert_id WHERE recommend_cell.recommend_list_id = %s"""
		rlc_query_set = [recommend_list_id]
		return sf_db.query_data(rlc_query_sentence, rlc_query_set)


	@staticmethod
	def getSavedRecommendList(username, concert_id):
		sf_db = SFDBManager.SFDBManager()
		savedrl_query_sentence = """SELECT recommend_list.recommend_list_id, recommend_list.recommend_list_title FROM recommend_list RIGHT JOIN recommend_cell ON recommend_list.recommend_list_id = recommend_cell.recommend_list_id WHERE recommend_list.user_name = %s AND recommend_cell.concert_id = %s"""
		savedrl_query_set = [username, concert_id]
		return  sf_db.query_data(savedrl_query_sentence, savedrl_query_set)


# ===============================================================
# 
# 	Attending, Rating, Review
# 
# ===============================================================

	@staticmethod
	def getAttendingStatus(username, concert_id):
		sf_db = SFDBManager.SFDBManager()
		gas_query_sentence = """SELECT a_status, rating, review FROM attending WHERE user_name = %s AND concert_id = %s"""
		gas_query_set = [username, concert_id]
		if sf_db.query_data(gas_query_sentence,gas_query_set):
			return sf_db.query_data(gas_query_sentence,gas_query_set)[0]
		else:
			return sf_db.query_data(gas_query_sentence,gas_query_set)

	@staticmethod
	def getRatingReviewStatus(username, concert_id):
		sf_db = SFDBManager.SFDBManager()
		gas_query_sentence = """SELECT rating, review FROM attending WHERE user_name = %s AND concert_id = %s"""
		gas_query_set = [username, concert_id]
		return sf_db.query_data(gas_query_sentence,gas_query_set)[0]
		

	@staticmethod
	def changeAttendingStatus(username, status, concert_id):
		sf_db = SFDBManager.SFDBManager()
		if status == "not going":
			modify_attending_sentence = """DELETE FROM attending WHERE user_name=%s AND concert_id = %s"""
			ma_exe_set = [username, concert_id]
		elif SFUtil.getAttendingStatus(username, concert_id):
			modify_attending_sentence = """UPDATE attending SET a_status=%s WHERE user_name = %s AND concert_id = %s"""
			ma_exe_set = [status, username, concert_id]
		else:
			modify_attending_sentence = """INSERT attending VALUES(%s,%s,%s,Null, Null, Null,Null)"""
			ma_exe_set = [username, concert_id, status]
		sf_db.execute_sql(modify_attending_sentence, ma_exe_set)
		return


	@staticmethod
	def updateAttendingRR(username, concert_id, rating, review):
		sf_db = SFDBManager.SFDBManager()
		if rating == "-1":
			if review == "":
				modify_attending_RR_sentence = """UPDATE attending SET rating=%s, review=%s, rating_time=%s, review_time=%s WHERE user_name = %s AND concert_id = %s"""
				maRR_exe_set = [None, None, None, None, username, concert_id]
			else:
				modify_attending_RR_sentence = """UPDATE attending SET rating=%s, review=%s, rating_time=%s, review_time=NOW() WHERE user_name = %s AND concert_id = %s"""
				maRR_exe_set = [None, review, None, username, concert_id]
		else:
			if review == "":
				modify_attending_RR_sentence = """UPDATE attending SET rating=%s, review=%s, rating_time=NOW(), review_time=%s WHERE user_name = %s AND concert_id = %s"""
				maRR_exe_set = [rating, None, None, username, concert_id]
			else:
				modify_attending_RR_sentence = """UPDATE attending SET rating=%s, review=%s, rating_time=NOW(), review_time=NOW() WHERE user_name = %s AND concert_id = %s"""
				maRR_exe_set = [rating, review, username, concert_id]
		sf_db.execute_sql(modify_attending_RR_sentence, maRR_exe_set)
		return


	@staticmethod
	def getAVGRating(concert_id):
		sf_db = SFDBManager.SFDBManager()
		avgr_query_sentence = """SELECT AVG(rating) FROM attending WHERE concert_id=%s GROUP BY concert_id"""
		avgr_query_set = [concert_id]
		avgrating_back_data = sf_db.query_data(avgr_query_sentence,avgr_query_set)
		if avgrating_back_data:
			return avgrating_back_data[0][0]
		else:
			return None
		

	@staticmethod
	def getReviewList(concert_id):
		sf_db = SFDBManager.SFDBManager()
		grl_query_sentence = """SELECT user_name, review, review_time FROM attending WHERE concert_id=%s AND review is not NULL"""
		grl_query_set = [concert_id]
		return sf_db.query_data(grl_query_sentence,grl_query_set)



# ===============================================================
# 
# 	Ticket stuff
# 
# ===============================================================

	@staticmethod
	def addTicketType(concert_id, ticket_type):
		sf_db = SFDBManager.SFDBManager()
		return sf_db.execute_sql("""INSERT INTO ticket VALUES (%s, %s, 0, 0)""", [concert_id, ticket_type])


	@staticmethod
	def getTicketTypeList(concert_id):
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""SELECT ticket_type, price, availability FROM ticket WHERE concert_id = %s""", [concert_id])


	@staticmethod
	def updateTicketInfo(concert_id, ticket_type, price, availability):
		sf_db = SFDBManager.SFDBManager()
		sf_db.execute_sql("""UPDATE ticket SET price = %s, availability = %s WHERE concert_id = %s AND ticket_type = %s""", [price, availability, concert_id, ticket_type])
		return


# ===============================================================
# 
# 	Search stuffs
# 
# ===============================================================

	@staticmethod
	def searchUsernameByUsernameNickname(searched_text):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT user_name, nick_name FROM user WHERE user_name LIKE (%s) OR nick_name LIKE (%s)""", [searched_text, searched_text])

	@staticmethod
	def searchArtistnameByArtistname(searched_text):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT artist_name FROM artist WHERE artist_name LIKE (%s)""", [searched_text])

	@staticmethod
	def searchConcertByTitle(searched_text):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT concert_id, title, artist_name, hold_time FROM concert WHERE title LIKE (%s)""", [searched_text])

	@staticmethod
	def searchConcertByTitleHoldTime(searched_text, searched_time):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT concert_id, title, artist_name, hold_time FROM concert 
			WHERE title LIKE (%s) AND %s < hold_time""", [searched_text, searched_time])



	@staticmethod
	def searchConcertByGenre(searched_text):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT concert.concert_id, concert.title, concert.artist_name, concert.hold_time 
			FROM concert INNER JOIN concert_type ON concert.concert_id = concert_type.concert_id
			WHERE concert_type.type_name LIKE (%s)""", [searched_text])

	@staticmethod
	def searchConcertByGenreHoldtime(searched_text,searched_time):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT concert.concert_id, concert.title, concert.artist_name, concert.hold_time 
			FROM concert INNER JOIN concert_type ON concert.concert_id = concert_type.concert_id
			WHERE concert_type.type_name LIKE (%s) AND %s < hold_time""", [searched_text, searched_time])	

	
	@staticmethod
	def searchRLByGenre(searched_text):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT recommend_list_id, recommend_list_title, user_name 
			FROM recommend_list WHERE genre LIKE (%s)""", [searched_text])


	@staticmethod
	def searchUsernameByGenre(searched_text):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT user.user_name, user.nick_name
			FROM user INNER JOIN user_type ON user.user_name = user_type.user_name
			WHERE user_type.type_name LIKE (%s)""", [searched_text])

	@staticmethod
	def searchArtistnameByGenre(searched_text):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT artist.artist_name
			FROM artist INNER JOIN artist_type ON artist.artist_name = artist_type.artist_name
			WHERE artist_type.type_name LIKE (%s)""", [searched_text])		


	@staticmethod
	def searchConcertByLocation(searched_text):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT concert.concert_id, concert.title, concert.artist_name, concert.hold_time 
			FROM concert INNER JOIN venue ON venue.venue_name = concert.venue_name
			WHERE venue.venue_name LIKE (%s) OR venue.vstate LIKE (%s) OR venue.vcity LIKE (%s) """, [searched_text, searched_text, searched_text])

	@staticmethod
	def searchConcertByLocationHoldtime(searched_text, searched_time):
		sf_db = SFDBManager.SFDBManager()
		searched_text = '%'+searched_text+'%'
		return sf_db.query_data("""SELECT DISTINCT concert.concert_id, concert.title, concert.artist_name, concert.hold_time 
			FROM concert INNER JOIN venue ON venue.venue_name = concert.venue_name
			WHERE venue.venue_name LIKE (%s) OR venue.vstate LIKE (%s) OR venue.vcity LIKE (%s) AND %s < hold_time""", [searched_text, searched_text, searched_time])


	@staticmethod
	def searchConcertByHoldtime(searched_text):
		sf_db = SFDBManager.SFDBManager()
		print searched_text+" 00:00:01"
		searched_text_convert = datetime.datetime.strptime(searched_text, "%Y-%m-%d")
		return sf_db.query_data("""SELECT DISTINCT concert_id, title, artist_name, hold_time 
			FROM concert WHERE %s < hold_time""", [searched_text_convert.strftime('%Y-%m-%d %H:%M:%S')])


	@staticmethod
	def searchConcertWOConcertTime(artist_name,concert_title,genre,location):
		sf_db = SFDBManager.SFDBManager()
		artist_name = '%'+artist_name+'%'
		concert_title = '%'+concert_title+'%'
		genre = '%'+genre+'%'
		location = '%'+location+'%'

		return sf_db.query_data(""" SELECT DISTINCT concert.concert_id, concert.title, concert.artist_name, concert.hold_time 
			FROM concert INNER JOIN concert_type ON concert.concert_id = concert_type.concert_id
			INNER JOIN venue ON venue.venue_name = concert.venue_name
			WHERE concert_type.type_name LIKE (%s) AND concert.artist_name LIKE (%s) AND
			concert.title LIKE (%s) AND (venue.venue_name LIKE (%s) OR venue.vstate LIKE (%s) OR venue.vcity LIKE (%s))""",
			[genre, artist_name, concert_title,location,location,location])


	@staticmethod
	def searchConcertWithConcertFromTime(artist_name,concert_title,genre,location,concert_from_time):
		sf_db = SFDBManager.SFDBManager()
		artist_name = '%'+artist_name+'%'
		concert_title = '%'+concert_title+'%'
		genre = '%'+genre+'%'
		location = '%'+location+'%'
		concert_from_time = datetime.datetime.strptime(concert_from_time, "%Y-%m-%d %H:%M")

		return sf_db.query_data(""" SELECT DISTINCT concert.concert_id, concert.title, concert.artist_name, concert.hold_time 
			FROM concert INNER JOIN concert_type ON concert.concert_id = concert_type.concert_id
			INNER JOIN venue ON venue.venue_name = concert.venue_name
			WHERE concert_type.type_name LIKE (%s) AND concert.artist_name LIKE (%s) AND
			concert.title LIKE (%s) AND (venue.venue_name LIKE (%s) OR venue.vstate LIKE (%s) OR venue.vcity LIKE (%s))
			AND %s < concert.hold_time""",
			[genre, artist_name, concert_title,location,location,location, concert_from_time.strftime('%Y-%m-%d %H:%M')])


	@staticmethod
	def searchConcertWithConcertToTime(artist_name,concert_title,genre,location,concert_to_time):
		sf_db = SFDBManager.SFDBManager()
		artist_name = '%'+artist_name+'%'
		concert_title = '%'+concert_title+'%'
		genre = '%'+genre+'%'
		location = '%'+location+'%'
		concert_to_time = datetime.datetime.strptime(concert_to_time, "%Y-%m-%d %H:%M")

		return sf_db.query_data(""" SELECT DISTINCT concert.concert_id, concert.title, concert.artist_name, concert.hold_time 
			FROM concert INNER JOIN concert_type ON concert.concert_id = concert_type.concert_id
			INNER JOIN venue ON venue.venue_name = concert.venue_name
			WHERE concert_type.type_name LIKE (%s) AND concert.artist_name LIKE (%s) AND
			concert.title LIKE (%s) AND (venue.venue_name LIKE (%s) OR venue.vstate LIKE (%s) OR venue.vcity LIKE (%s))
			AND %s > concert.hold_time""",
			[genre, artist_name, concert_title,location,location,location, concert_to_time.strftime('%Y-%m-%d %H:%M')])


	@staticmethod
	def searchConcertWithConcertFromToTime(artist_name,concert_title,genre,location,concert_from_time,concert_to_time):
		sf_db = SFDBManager.SFDBManager()
		artist_name = '%'+artist_name+'%'
		concert_title = '%'+concert_title+'%'
		genre = '%'+genre+'%'
		location = '%'+location+'%'
		concert_from_time = datetime.datetime.strptime(concert_from_time, "%Y-%m-%d %H:%M")
		concert_to_time = datetime.datetime.strptime(concert_to_time, "%Y-%m-%d %H:%M")

		return sf_db.query_data(""" SELECT DISTINCT concert.concert_id, concert.title, concert.artist_name, concert.hold_time 
			FROM concert INNER JOIN concert_type ON concert.concert_id = concert_type.concert_id
			INNER JOIN venue ON venue.venue_name = concert.venue_name
			WHERE concert_type.type_name LIKE (%s) AND concert.artist_name LIKE (%s) AND
			concert.title LIKE (%s) AND (venue.venue_name LIKE (%s) OR venue.vstate LIKE (%s) OR venue.vcity LIKE (%s))
			AND %s < concert.hold_time AND %s > concert.hold_time""",
			[genre, artist_name, concert_title,location,location,location, concert_from_time.strftime('%Y-%m-%d %H:%M'),concert_to_time.strftime('%Y-%m-%d %H:%M')])



# ===============================================================
# 
# 	Stored procedure
# 
# ===============================================================

	@staticmethod
	def getRecommendArtistbysumReputation(user_name):
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""CALL recommendArtistbysumReputation(%s)""",[user_name])
	

	@staticmethod
	def getRecommendConcertbysumRecommended(user_name):
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""CALL recommendConcertbysumRecommended(%s)""",[user_name])
	
	@staticmethod
	def getRecommendArtistbySimilarFlavor(user_name):
		sf_db = SFDBManager.SFDBManager()
		return sf_db.query_data("""CALL recommendArtistbySimilarFlavor(%s)""",[user_name])






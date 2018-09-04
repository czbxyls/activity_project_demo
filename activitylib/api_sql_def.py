

API_ACTIVITY_QUERY_COMMENTS_SQL = "SELECT c.id,c.user_id, content comment,refer_id " \
							"FROM comment_tab c WHERE c.activity_id=%s ORDER BY c.id DESC"

API_ACTIVITY_QUERY_PARTICIPATORS_SQL = "SELECT p.id, p.user_id FROM participate_tab p " \
									   " WHERE p.activity_id=%s ORDER BY p.id ASC"

API_ACTIVITY_QUERY_MINE_SQL = "SELECT p.user_id, p.activity_id " \
									   "FROM participate_tab p WHERE 1=1 AND p.user_id=%s ORDER BY p.activity_id DESC"

API_ACTIVITY_QUERY_SQL = "SELECT a.id activity_id, a.`name` activity_name, a.`desc` activity_desc, location, begin_time, " \
						 "end_time, a.`channel_id` channel_id, a.admin_id post_admin_id FROM activity_tab a " \
						 " WHERE 1=1 "

API_ACTIVITY_DETAIL_SQL = "SELECT a.id activity_id, a.`name` activity_name, a.`detail` activity_detail, a.`desc` activity_desc, " \
						  "location, begin_time, end_time, a.`channel_id` channel_id, a.admin_id post_admin_id " \
						  "FROM activity_tab a WHERE 1=1 and a.id=%s"
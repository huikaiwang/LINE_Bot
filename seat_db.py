import os
import configparser
import psycopg2
from mysql.connector import Error

root = "Root's access token"

def check_reg(user_id,text):
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL,sslmode='require')
	cursor = conn.cursor()
	search_query = """ select Access_Token from Students where Access_Token = %s """
	cursor.execute(search_query,(text,))
	conn.commit()
	res = cursor.fetchone()
	if res:
		ID=""
		if res[0] == root:
			ID="Root"
		else:
			ID="Member"
		search_query = """ update Students set User_ID = %s , state = %s  where Access_Token=%s """
		cursor.execute(search_query,(user_id,ID,text,))
		conn.commit()
		cursor.close()
		conn.close()
		return True
	cursor.close()
	conn.close()
	return res	

def check_user(user_id):
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL,sslmode='require')
	cursor = conn.cursor()
	search_query = """ select SID from Students where User_ID=%s """
	cursor.execute(search_query,(user_id,))
	conn.commit()
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	if res:
		return res[0]
	return res

def check_state(user_id):
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL,sslmode='require')
	cursor = conn.cursor()
	search_query = """ select state from Students where User_ID = %s """
	cursor.execute(search_query,(user_id,))
	conn.commit()
	res = cursor.fetchone()
	cursor.close()
	conn.close()
	if res:
		return res[0]
	return res

def search_user():
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL,sslmode='require')
	cursor = conn.cursor()
	search_query = """ select User_ID from Students where User_ID !=%s"""
	cursor.execute(search_query,("NULL",))
	conn.commit()
	res = cursor.fetchall()
	cursor.close()
	conn.close()
	return list(res)

def err_test():
        
        print(1)
        print(2)
        print(3)

if __name__ == "__main__":
	search_user(code)
	check_reg(user_id,text)
	check_state(sid)
	check_user(user_id)
	err_test()

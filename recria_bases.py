def main():
	from webapp_social_media import db
	from webapp_social_media.models import User, Post
	db.drop_all()
	db.create_all()

if __name__ == '__main__':
	main()
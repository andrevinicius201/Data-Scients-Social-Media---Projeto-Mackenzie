def main():
    from webapp_social_media import db
    from webapp_social_media.models import User, Post, InterestTopic, InterestTopicUser

    topics = ["Sql", "Java", "Python", "C#", "C++"]

    db.drop_all()
    db.create_all()

    for x in range(5):
        topic = InterestTopic(label=topics[x])
        db.session.add(topic)
    db.session.commit()


if __name__ == '__main__':
    main()
